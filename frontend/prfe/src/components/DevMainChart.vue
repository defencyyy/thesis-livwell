<template>
  <div class="chart-container">
    <h5 class="chart-title">Sales Status Distribution for {{ year }}</h5>
    <canvas id="salesStatusChart"></canvas>
    <p v-if="noData">No data available for the selected year.</p>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default {
  name: "DevMainChart",
  data() {
    return {
      year: new Date().getFullYear(),
      chart: null,
      noData: false, // New state to track no data
      statusColorMapping: {
        "Pending Reservation": "#F39C12", // Yellow
        Reserved: "#2980B9", // Blue
        "Pending Sold": "#8E44AD", // Purple
        Sold: "#E91E63", // Pink
      },
    };
  },
  mounted() {
    this.fetchSalesStatusData();
  },
  methods: {
    async fetchSalesStatusData() {
      const token = localStorage.getItem("accessToken");
      console.log("Authorization Header:", `Bearer ${token}`);
      if (!token) {
        console.error("No token found, user is not authenticated.");
        return; // Don't proceed if no token is available.
      }

      try {
        const response = await fetch(
          `${process.env.vue_app_api_url}/developer/sales/status/${this.year}/`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (!response.ok) {
          if (response.status === 404) {
            this.noData = true; // Set the noData flag if no data is returned
          }
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Sales Status Data:", data);

        const salesData = data.data;
        if (salesData && salesData.length > 0) {
          this.renderChart(salesData);
          this.noData = false; // Reset no data flag
        } else {
          this.noData = true; // Set noData if there are no sales records
        }
      } catch (error) {
        console.error("Error fetching sales status data:", error);
      }
    },

    renderChart(salesData) {
      const ctx = document.getElementById("salesStatusChart").getContext("2d");

      // Extract labels and counts
      const labels = salesData.map((item) => item.status);
      const counts = salesData.map((item) => item.count);

      // Map the sales status to the predefined color palette
      const backgroundColors = salesData.map(
        (item) => this.statusColorMapping[item.status]
      );

      // If chart exists, destroy it before creating a new one
      if (this.chart) {
        this.chart.destroy();
      }

      // Create new chart
      this.chart = new Chart(ctx, {
        type: "pie",
        data: {
          labels: labels,
          datasets: [
            {
              data: counts,
              backgroundColor: backgroundColors,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
          },
        },
      });
    },
  },
};
</script>

<style>
.chart-title {
  padding: 7px;
}

.chart-container {
  display: flex;
  flex-direction: column; /* Ensures the heading stays above the chart */
  align-items: center; /* Horizontally centers the chart */
  justify-content: center; /* Vertically centers the chart */
  width: 100%; /* Adjust as needed */
  text-align: center; /* Centers the heading */
}
#salesStatusChart {
  max-width: 300px; /* Set a max-width for responsiveness */
  height: auto; /* Maintain aspect ratio */
}
</style>
