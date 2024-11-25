<template>
  <div class="main-page">
    <AppHeader />
    <SideNav />
    <div class="content">
      <h1>Hi, {{ brokerName }}</h1>
      <p>{{ brokerEmail }}</p>
      <strong>Total Sales:</strong> {{ totalSales }}
      <strong>Total Commissions:</strong> {{ totalCommissions }}
      <p>Total Customers: {{ totalCustomers }}</p>

      <!-- Pie chart displaying sales status -->
      <div class="pie-chart-container">
        <PieChart
          :sold="salesStatus.sold"
          :pending="salesStatus.pending"
          :reserved="salesStatus.reserved"
        />
      </div>

      <h1>Hi, {{ brokerName }}</h1>

      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { mapState } from "vuex";
import axios from "axios";
import PieChart from "@/components/PieChart.vue"; // Import the PieChart component

export default {
  name: "BrkMainPage",
  components: {
    SideNav,
    AppHeader,
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId || null,
      userType: (state) => state.userType || null,
      companyId: (state) => state.companyId || null,
      loggedIn: (state) => state.loggedIn, // Use Vuex loggedIn state
    }),
    localStorageUserId() {
      return localStorage.getItem("user_id");
    },
    localStorageCompanyId() {
      return localStorage.getItem("company_id");
    },
  },
  mounted() {
    if (!this.loggedIn || this.userType !== "broker" || !this.companyId) {
      this.redirectToLogin();
    }
    console.log("User ID from Vuex:", this.userId);
    console.log("User Type from Vuex:", this.userType);
    this.fetchBrokerInfo(); // Make sure to call this here to fetch broker info on mount
  },
  watch: {
    loggedIn(newVal) {
      if (!newVal || this.userType !== "broker" || !this.companyId) {
        this.redirectToLogin();
      }
    },
    userType(newVal) {
      if (newVal !== "broker" || !this.companyId) {
        this.redirectToLogin();
      }
    },
    companyId(newVal) {
      if (!newVal || this.userType !== "broker") {
        this.redirectToLogin();
      }
    },
  },
  data() {
    return {
      PieChart,
      brokerName: "",
      brokerEmail: "",
      totalSales: 0,
      totalCommissions: 0,
      totalCustomers: 0,
      salesStatus: {
        sold: 0,
        pending: 0,
        reserved: 0,
      },
    };
  },
  methods: {
    async fetchBrokerInfo() {
      const brokerId = this.userId; // Use this.userId for broker ID

      if (!brokerId) {
        console.error("User ID is not available!");
        return; // Exit early if no userId
      }

      try {
        const response = await fetch(
          `http://localhost:8000/brokers/${brokerId}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        const data = await response.json();
        if (data.success !== false) {
          this.brokerName = `${data.f_name} ${data.l_name}`;
          this.brokerEmail = data.email;
        } else {
          console.error("Broker info not found or error:", data.message);
        }
      } catch (error) {
        console.error("Error fetching broker info:", error);
      }

      const salesResponse = await fetch(
        `http://localhost:8000/sales/total/?broker_id=${brokerId}`
      );
      if (salesResponse.ok) {
        const salesData = await salesResponse.json();
        this.totalSales = salesData.total_sales;
      }

      const commissionsResponse = await fetch(
        `http://localhost:8000/sales/commissions/?broker_id=${brokerId}`
      );
      if (commissionsResponse.ok) {
        const commissionsData = await commissionsResponse.json();
        this.totalCommissions = commissionsData.total_commissions;
      }

      const customersResponse = await fetch(
        `http://localhost:8000/customers/broker/${brokerId}/?include_sales=false`
      );
      if (customersResponse.ok) {
        const customersData = await customersResponse.json();
        this.totalCustomers = customersData.total_customers;
      }

      const salesStatusResponse = await fetch(
        `http://localhost:8000/sales/?broker_id=${brokerId}`
      );
      if (salesStatusResponse.ok) {
        const statusData = await salesStatusResponse.json();
        if (statusData.success) {
          this.salesStatus = statusData.sales_status_data;
        }
      }
    },

    async logout() {
      try {
        // Notify backend about logout
        await axios.post(
          "http://localhost:8000/api/token/brklogout/", // Update URL to match backend endpoint
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        // Clear localStorage and Vuex state
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("user_id");
        localStorage.removeItem("user_role");
        localStorage.removeItem("company_id");

        // Call Vuex mutation to reset user state
        this.$store.commit("clearUser");

        // Redirect to login page
        this.redirectToLogin();
      } catch (error) {
        console.error("Error during logout:", error);
        alert("Logout failed. Please try again.");
      }
    },

    redirectToLogin() {
      this.$router.push({ name: "BrkLogin" });
    },
  },
};
</script>

<style scoped>
.main-page {
  display: flex;
  height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}

.content h1,
h5 {
  color: black;
  text-align: left;
  padding-left: 50px;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #ff1a1a;
}

.pie-chart-container {
  width: 50%;
  margin: 20px auto;
}
</style>
