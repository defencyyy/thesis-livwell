<template>
  <div>
    <!-- Main wrapper div -->
    <AppHeader />
    <div class="main-page">
      <SideNav />
      <div class="content">
        <p class="text-start display-7 fw-bolder">{{ brokerEmail }}</p>
        <h1 class="text-start display-5 fw-bolder text-capitalize pb-6">His, {{ brokerName }}</h1>
        <p class="text-start pt-5"><strong>Total Sales:</strong> {{ totalSales }}</p>
        <p class="text-start "><strong>Total Commissions:</strong> {{ totalCommissions }}</p>
        <p class="text-start "> <strong>Total Customers: </strong> {{ totalCustomers }}</p>
       
        <!-- Pie Chart Section -->
        <div
          v-if="
            salesStatus.sold === 0 &&
            salesStatus.pending === 0 &&
            salesStatus.reserved === 0
          "
        >
          <p>No sales data available.</p>
        </div>
        <div v-else>
          <canvas id="salesPieChart"></canvas>
        </div>

        <!-- <button @click="logout">Logout</button> -->
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { mapState } from "vuex";
import axios from "axios";
import { Chart, ArcElement, Tooltip, Legend, PieController } from "chart.js"; // Import necessary components from Chart.js
Chart.register(PieController, ArcElement, Tooltip, Legend);

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
  watch: {
    // Re-render the pie chart when sales data changes
    salesStatus: "renderPieChart",
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
            console.log("Sales Status:", this.salesStatus);
          }
        }
      } catch (error) {
        console.error("Error fetching broker info:", error);
      } finally {
        this.loading = false; // Hide the loading spinner once data is fetched
      }
    },

    // Function to render the pie chart
    renderPieChart() {
      this.$nextTick(() => {
        const ctx = document.getElementById("salesPieChart");

        if (ctx) {
          new Chart(ctx, {
            type: "pie",
            data: {
              labels: ["Sold", "Pending Reservation", "Reserved", "Pending Sold"], // Add "Pending Sold"
              datasets: [
                {
                  data: [
                    this.salesStatus.sold,
                    this.salesStatus.pending,
                    this.salesStatus.reserved,
                    this.salesStatus.Pending_sold,
                  ],
                  backgroundColor: ["#36A2EB", "#FFCE56", "#FF6384", "#FF9F40"], // You can adjust the colors
                },
              ],
            },
            options: {
              responsive: true,
              plugins: {
                legend: {
                  position: "top",
                },
                tooltip: {
                  callbacks: {
                    label: function (context) {
                      const label = context.label || "";
                      const value = context.raw || 0;
                      return `${label}: ${value}`;
                    },
                  },
                },
              },
            },
          });
        } else {
          console.error("Canvas element not found.");
        }
      });
    },

    async logout() {
      try {
        await axios.post(
          "http://localhost:8000/api/token/brklogout/",
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

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
  border: 2px solid #ccc;
  border-radius: 10px;
  margin: 20px 20px 20px 20px;
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.2);
  background-color: rgb(223, 255, 223);
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

canvas {
  max-width: 400px;
  max-height: 400px;
  margin: 20px auto;
}

#salesPieChart
{
  padding: 20px;
  text-align: center;
  border: 2px solid #ccc;
  border-radius: 10px;
  /* margin: 20px 20px 20px 20px;   */
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.2);
  background-color: rgb(244, 244, 244);
}

/* .content {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: auto;
}

.broker-info {
  margin-bottom: 20px;
}

.broker-info p,
.broker-info h1 {
  font-family: 'Arial', sans-serif;
  color: #333;
}

.broker-info strong {
  font-weight: bold;
  color: #0056b3;
}

h1 {
  font-size: 24px;
  color: #333;
  text-align: center;
}

#salesPieChart {
  width: 100%;
  max-width: 500px;
  margin: 20px auto;
}

.logout-container {
  text-align: center;
  margin-top: 20px;
}

.logout-btn {
  padding: 10px 20px;
  background-color: #ff4c4c; /* Red background 
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background-color: #e63946; 
} */

</style>
