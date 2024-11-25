<template>
  <AppHeader />
  <div class="main-page">
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
  created() {
    this.fetchBrokerInfo();
  },
  methods: {
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

      // Using Vuex userId instead of brokerId
      const brokerId = this.userId; // You can use this.userId here

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
.contentpage {
  border: 1px solid black;
}
.content h1,
h5 {
  color: black;
  text-align: left;
  padding-left: 50px;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}

.content1,
.content2 {
  text-align: left;
  background-color: #d9d9d9;
  height: 30%;
  border-radius: 10px;
  padding-left: 10px;
  margin-bottom: 20px;
  margin-right: 20px;
  margin-left: 50px;
}
.content1 h2,
.content2 h2 {
  padding-right: 30px;
}
.content3 {
  text-align: center;
  background-color: #d9d9d9;
  border-radius: 10px;
  padding-left: 10px;
  margin-bottom: 20px;
  margin-right: 20px;
  margin-left: 20px;
  height: 60%;
  width: 500%;
}
.content3 h2 {
  text-align: center;
  padding-top: 20px;
}

.content4 {
  background-color: #d9d9d9;
  border-radius: 10px;
  height: 40%;
  width: 200%;
  margin-bottom: 20px;
  margin-right: 20px;
  margin-left: 50px;
  padding-left: 20px;
  text-align: start;
}
.content img {
  margin-left: 10px;
}
.contentpage {
  display: flex;
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
