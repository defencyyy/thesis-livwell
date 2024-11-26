<template>
  <div>
    <!-- Main wrapper div -->
    <AppHeader />
    <div class="main-page">
      <SideNav />
      <div class="content">
        <h1>His, {{ brokerName }}</h1>
        <p>{{ brokerEmail }}</p>
        <strong>Total Sales:</strong> {{ totalSales }}
        <strong>Total Commissions:</strong> {{ totalCommissions }}
        <p>Total Customers: {{ totalCustomers }}</p>

        <!-- Pie chart section -->
        <div class="pie-chart-container">
          <p class="chart-title">Sales Chart</p>

          <!-- Display loading or no data message if sales data is empty -->
          <div v-if="!salesStatus.sold && !salesStatus.pending && !salesStatus.reserved">
            <p class="no-data-message">No sales data available. Once you make some sales, your chart will be displayed here.</p>
          </div>          
          <div v-else>
            <PieChart :sold="salesStatus.sold" :pending="salesStatus.pending" :reserved="salesStatus.reserved" />
          </div>

          <!-- Optional: A loading spinner if the chart is still fetching data -->
          <div v-if="loading" class="loading-spinner">
            <span>Loading...</span>
          </div>
        </div>

        <button @click="logout">Logout</button>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { mapState } from "vuex";
import axios from "axios";
import PieChart from "@/components/PieChart.vue";

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
      loggedIn: (state) => state.loggedIn, 
    }),
  },
  data() {
    return {
      PieChart,
      loading: true, // Flag for loading state
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
  mounted() {
    if (!this.loggedIn || this.userType !== "broker" || !this.companyId) {
      this.redirectToLogin();
    }
    this.fetchBrokerInfo(); // Fetch data when component is mounted
  },
  methods: {
    async fetchBrokerInfo() {
      const brokerId = this.userId;

      if (!brokerId) {
        console.error("User ID is not available!");
        return;
      }

      this.loading = true; // Show loading spinner while fetching data

      try {
        const response = await fetch(`http://localhost:8000/brokers/${brokerId}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });

        const data = await response.json();
        if (data.success !== false) {
          this.brokerName = `${data.f_name} ${data.l_name}`;
          this.brokerEmail = data.email;
        }

        const salesResponse = await fetch(`http://localhost:8000/sales/total/?broker_id=${brokerId}`);
        if (salesResponse.ok) {
          const salesData = await salesResponse.json();
          this.totalSales = salesData.total_sales;
        }

        const commissionsResponse = await fetch(`http://localhost:8000/sales/commissions/?broker_id=${brokerId}`);
        if (commissionsResponse.ok) {
          const commissionsData = await commissionsResponse.json();
          this.totalCommissions = commissionsData.total_commissions;
        }

        const customersResponse = await fetch(`http://localhost:8000/customers/broker/${brokerId}/?include_sales=false`);
        if (customersResponse.ok) {
          const customersData = await customersResponse.json();
          this.totalCustomers = customersData.total_customers;
        }

        const salesStatusResponse = await fetch(`http://localhost:8000/sales/?broker_id=${brokerId}`);
        if (salesStatusResponse.ok) {
          const statusData = await salesStatusResponse.json();
          
          if (statusData.success) {
            this.salesStatus = statusData.sales_status_data;
            console.log('Sales Status:', this.salesStatus);

          }
        }
      } catch (error) {
        console.error("Error fetching broker info:", error);
      } finally {
        this.loading = false; // Hide the loading spinner once data is fetched
      }
    },

    async logout() {
      try {
        await axios.post("http://localhost:8000/api/token/brklogout/", {}, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });

        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("user_id");
        localStorage.removeItem("user_role");
        localStorage.removeItem("company_id");

        this.$store.commit("clearUser");
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

.pie-chart-container {
  width: 60%;
  margin: 20px auto;
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.chart-title {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #333;
}

.no-data-message {
  font-size: 1rem;
  color: #888;
  margin-top: 20px;
}

.loading-spinner {
  font-size: 1.2rem;
  color: #555;
  margin-top: 20px;
  font-weight: bold;
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
</style>
