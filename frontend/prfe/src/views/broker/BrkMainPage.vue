<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <h1 class="text-start display-5 fw-bolder text-capitalize pb-6">{{ brokerName }}</h1>
        <p class="text-start display-7 fw-bolder">@{{ brokerUsername }}</p>
        <div class="dashboard-and-pie">
          <!-- Left side: Dashboard Boxes -->
          <div class="dashboard-boxes">
            <div class="box">
              <div class = "box-header">
                <div class = "icon-container">
                  <i class="fa fa-shopping-cart" style="font-size: 13px"></i>
                </div>
                <p>Total Sales</p>
              </div>
              <h2>{{ totalSales }}</h2>
            </div>
            <div class="box">
              <div class = "box-header">
                <div class = "icon-container">
                  <i class="fa fa-money-bill" style="font-size: 13px"></i>
                </div>
                <p>Total Commissions</p>
              </div>
              <h2>{{ totalCommissions }}</h2>
            </div>
            <div class="box">
              <div class = "box-header">
                <div class = "icon-container">
                  <i class="fa fa-users" style="font-size: 13px"></i>
                </div>
                <p>Total Customers</p>
              </div>
              <h2>{{ totalCustomers }} </h2>
            </div>
          </div>
          
          <!-- Right side: Pie Chart -->
          <div class="piechart-container">
            <div v-if="salesStatus.sold === 0 && salesStatus.pending === 0 && salesStatus.reserved === 0">
              <p>No sales data available.</p>
            </div>
            <div v-else>
              <canvas id="salesPieChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Bottom: Bar Chart -->
        <div v-if="salesStatus.sold > 0">
          <div class="bar-chart-header">
            <label for="year-select">Select Year for Sales Data</label>

            <select id="year-select" v-model="selectedYear" @change="fetchSalesByMonth" :disabled="loading">
              <option v-if="loading" value="" disabled>Loading years...</option>
              <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
            </select>
          </div>
          <canvas id="salesBarChart"></canvas>
        </div>
        <div v-else>
          <p>No sales data available for the selected year.</p>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { mapState } from "vuex";
import axios from "axios";
import { BarElement,Chart, ArcElement, Tooltip, Legend, PieController, CategoryScale, LinearScale, Title,BarController } from "chart.js"; // Import necessary components from Chart.js
Chart.register(BarElement, CategoryScale, LinearScale,PieController, ArcElement, Title, Tooltip, Legend,BarController);

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
      loading: true, // Initially set to true while fetching
    brokerName: "",
    brokerUsername: "",
    totalSales: 0,
    totalCommissions: 0,
    totalCustomers: 0,
    salesStatus: {
      sold: 0,
      pending: 0,
      reserved: 0,
    },
    salefilter: {
      months: [],
      salesCount: [],
      availableYears: [],  
      },
      selectedYear: new Date().getFullYear(), // Default to current year

    };
  },
  mounted() {
    if (!this.loggedIn || this.userType !== "broker" || !this.companyId) {
      this.redirectToLogin();
    }
    this.fetchBrokerInfo(); // Fetch data when component is mounted
    this.fetchSalesByMonth();
  },
  watch: {
    // Re-render the pie chart when sales data changes
    salesStatus: "renderPieChart",
    salefilter:"renderBarChart",
  },
  updated() {
  if (this.salesStatus.sold > 0) {
    this.renderBarChart();
  }
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
          this.brokerUsername = data.username;
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
async fetchSalesByMonth() {
  const brokerId = this.userId;
  const year = this.selectedYear || new Date().getFullYear(); // Default to current year if no selection
  
  try {
    const response = await axios.get(`http://localhost:8000/sales/by-month/?broker_id=${brokerId}&year=${year}`);
    
    if (response.data.success) {
      const monthSales = response.data.month_sales;
      const availableYears = response.data.years;

      this.availableYears = availableYears; // Set available years

      // List of all months in order
      const allMonths = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      this.months = allMonths;
      this.salesCount = allMonths.map((month) => monthSales[month] || 0); // Fill missing months with 0

      // Re-render the bar chart after updating the data
      this.renderBarChart();
    }
  } catch (error) {
    console.error("Error fetching sales data by month:", error);
  } finally {
    this.loading = false; // Set loading to false after fetching
  }
},
renderBarChart() {
  // Check if a chart already exists and destroy it before creating a new one
  if (this.barChart) {
    this.barChart.destroy();  // Destroy the previous chart instance
    this.barChart = null;     // Ensure the chart is set to null after destruction
  }

  // Clear the canvas if needed (sometimes helps with persistent issues)
  const canvas = document.getElementById("salesBarChart");
  if (canvas) {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
  }

  this.$nextTick(() => {
    const ctx = document.getElementById("salesBarChart");

    if (!ctx) {
      console.error("Canvas element not found.");
      return;
    }

    // Create a new chart instance
    this.barChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: this.months,
        datasets: [
          {
            label: "Sold Sales",
            data: this.salesCount,
            backgroundColor: "#36A2EB",
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "top" },
          tooltip: {
            callbacks: {
              label: function (context) {
                const value = context.raw || 0;
                return `${context.label}: ${value}`;
              },
            },
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "Month",
            },
          },
          y: {
            title: {
              display: true,
              text: "Number of Sales",
            },
          },
        },
      },
    });
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
html,
body {
  height: 100%;
  margin: 0;
  /* Removes default margin */
  padding: 0;
  /* Removes default padding */
}

/* Ensure .main-page fills the available space */
.main-page {
  display: flex;
  min-height: 100vh;
  /* Ensures it spans the full viewport height */
  background-color: #e8f0fa;
  /* Gray background */
}



.content {
  flex: 1;
  padding: 20px;
  text-align: center;
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



.box {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.box p {
  font-size: 14px;
  color: #666;
}

.box h2 {
  font-size: 24px;
  margin: 10px 0 0;
}
#salesBarChart {
  max-width: 100%;
  width: 100%; /* Adjust the width to 100% of its container */
  height: 500px; /* Increase the height of the chart */
  margin: 20px auto;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: #fff;
}

.main-content {
  display: flex;
  flex-direction: column; /* Stacks content vertically */
  margin-top: 80px;
  margin-left: 250px;
  flex: 1;
  padding: 20px;
}

.dashboard-and-pie {
  display: flex;
  justify-content: space-between;
  gap: 20px; /* Space between the boxes and pie chart */
  margin-bottom: 30px; /* Space between the pie chart and the bar chart */
}

.dashboard-boxes {
  display: flex;
  flex-direction: column; /* Stacks the boxes vertically */
  gap: 20px; /* Space between the boxes */
  flex: 1;
  margin-top: 50px; /* Adds more space at the top */
  margin-bottom: 20px; /* Keeps bottom margin as is */
}

.box {
  position: relative;
  /* Make the box a positioning context */
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.box-header {
  display: flex;
  align-items: center;
  justify-content: start;
  gap: 15px;
  margin: 0;
}

.icon-container {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  /* Make the icon circular */
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #343a40;
  color: #ffffff;
}

.box-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  /* Space between icon and title */
}

.box h2 {
  margin: 10px 0 0;
  font-size: 30px;
  font-weight: bold;
  color: #000;
  padding-bottom: 10px;
}

.box-header p {
  margin: 0;
  padding: 0;
  font-size: 13px;
  color: #000000;
}


.piechart-container {
  flex: 1;
  display: flex;
  justify-content: center; /* Centers the pie chart */
  align-items: center;
  margin-top: 30px;
}

#salesPieChart {
  max-width: 500px;
  width: 100%;
  padding: 20px;
  text-align: center;
  border: 2px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: #fff;
}

.bar-chart-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  justify-content: center;
}

.bar-chart-header label {
  margin-right: 10px;
  font-weight: bold;
}

.bar-chart-header select {
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

#salesBarChart {
  max-width: 100%;
  width: 100%;
  height: 500px;
  margin-top: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: #fff;
}

.box {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.box p {
  font-size: 14px;
  color: #666;
}

.box h2 {
  font-size: 24px;
  margin: 10px 0 0;
}

@media (max-width: 768px) {
  .dashboard-and-pie {
    flex-direction: column; /* Stacks everything vertically on small screens */
    align-items: center;
  }

  .piechart-container {
    width: 100%; /* Makes the pie chart responsive */
  }

  .dashboard-boxes {
    width: 100%; /* Makes the boxes responsive */
  }
}

</style>
