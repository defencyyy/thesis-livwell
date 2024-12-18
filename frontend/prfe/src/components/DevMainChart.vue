<template>
  <div class="chart-container">
    <h5 class="chart-title">Sales Status Distribution for {{ year }}</h5>
    <canvas id="salesStatusChart"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
import axios from "axios";

Chart.register(...registerables);

export default {
  name: "DevMainChart",
  data() {
    return {
      year: new Date().getFullYear(),
      chart: null,
    };
  },
  mounted() {
    this.fetchSalesStatusData();
  },
  methods: {
    async fetchSalesStatusData() {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/sales/status/${this.year}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        const salesData = response.data.data;
        this.renderChart(salesData);
      } catch (error) {
        console.error("Error fetching sales status data:", error);
      }
    },
    renderChart(salesData) {
      const ctx = document.getElementById("salesStatusChart").getContext("2d");

      // Extract labels and counts
      const labels = salesData.map((item) => item.status);
      const counts = salesData.map((item) => item.count);

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
              backgroundColor: ["#F39C12", "#2980B9", "#8E44AD", "#E91E63"],
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

.chart-title{
  padding: 7px;
}

.chart-container {
  display: flex;
  flex-direction: column; /* Ensures the heading stays above the chart */
  align-items: center;   /* Horizontally centers the chart */
  justify-content: center; /* Vertically centers the chart */
  width: 100%;           /* Adjust as needed */
  text-align: center;    /* Centers the heading */
}
  #salesStatusChart {
    max-width: 300px; /* Set a max-width for responsiveness */
    height: auto;     /* Maintain aspect ratio */
  }
</style>

