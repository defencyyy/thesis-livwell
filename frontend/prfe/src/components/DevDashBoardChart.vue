<template>
  <div class="chart-container">
    <div class="chart-header">
      <h2 class="chart-title">Top 5 Sites by Customer Count</h2>
    </div>
    <div class="chart-wrapper">
      <canvas id="site-customer-chart"></canvas>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";

export default {
  name: "CustomerDistributionChart",
  props: {
    customerData: {
      // Expecting customerData to be passed as a prop
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      chart: null,
    };
  },
  mounted() {
    Chart.register(...registerables);
    this.renderChart(); // Render the chart once the data is ready
  },
  watch: {
    customerData: "renderChart", // Re-render the chart if customerData changes
  },
  methods: {
    renderChart() {
      const ctx = document
        .getElementById("site-customer-chart")
        .getContext("2d");

      if (!ctx) {
        console.error("Canvas context not found!");
        return;
      }

      console.log("Rendering chart with data:", this.customerData);

      this.chart = new Chart(ctx, {
        type: "pie", // Pie chart for site distribution
        data: {
          labels: this.customerData.map((site) => site.name),
          datasets: [
            {
              label: "Customer Count",
              data: this.customerData.map((site) => site.count),
              backgroundColor: [
                "#A78BFA",
                "#F0A500",
                "#3A8DFF",
                "#D1C4E9",
                "#FF4F58",
              ],
              borderColor: "#fff",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: true },
            tooltip: {
              callbacks: {
                label: (tooltipItem) => {
                  const site = tooltipItem.label;
                  const count = tooltipItem.raw;
                  return `${site}: ${count} Customers`;
                },
              },
            },
          },
        },
      });
    },
  },
};
</script>

<style scoped>
.chart-container {
  background-color: #fff; /* Clean white background */
  border-radius: 4px; /* Rounded edges */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15); /* Subtle shadow */
  padding: 20px;
  width: 100%;
  max-width: 1100px;
  margin: auto;
}

.chart-header {
  display: flex;
  justify-content: space-between; /* Space out title and year selector */
  align-items: center; /* Center items vertically */
  margin-bottom: 10px;
}

.chart-title {
  font-size: 18px;
  padding: 10px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.chart-wrapper {
  position: relative;
}

canvas {
  max-width: 100%;
}
</style>
