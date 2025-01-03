<template>
  <div class="chart-container">
    <div class="chart-header-container">
      <p class="chart-title">Sales Data for</p>
      <select
        id="year"
        v-model="selectedYear"
        @change="updateChart"
        class="year-selector"
      >
        <option v-for="year in availableYears" :key="year" :value="year">
          {{ year }}
        </option>
      </select>
    </div>
    <div class="chart-wrapper">
      <canvas id="sales-chart"></canvas>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
export default {
  name: "SalesChart",
  props: ["salesData"], // Removed unnecessary salesData prop
  data() {
    return {
      chart: null,
      selectedYear: new Date().getFullYear(),
      availableYears: [], // Dynamically populated years
      localSalesData: [], // Local copy of sales data
    };
  },
  mounted() {
    Chart.register(...registerables);
    if (this.salesData && this.salesData.length > 0) {
      this.localSalesData = this.salesData;
      this.availableYears = this.getAvailableYears();
      this.selectedYear = Math.max(...this.availableYears); // Default to most recent year
      this.renderChart();
    } else {
      console.error("Sales data not available");
    }
  },
  methods: {
    updateChart() {
      if (!this.selectedYear) {
        console.error("Selected year is undefined");
        return;
      }
      const chartData = this.getChartData();
      this.chart.data = chartData;
      this.chart.update();
    },

    getChartData() {
      const salesByMonth = Array(12).fill(0);
      const filteredSales = this.localSalesData.filter((sale) => {
        const saleDate = new Date(sale.date_sold);
        return saleDate.getFullYear() === this.selectedYear;
      });
      filteredSales.forEach((sale) => {
        const month = new Date(sale.date_sold).getMonth();
        salesByMonth[month]++;
      });

      return {
        labels: [
          "Jan",
          "Feb",
          "Mar",
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug",
          "Sep",
          "Oct",
          "Nov",
          "Dec",
        ],
        datasets: [
          {
            label: "Sales",
            data: salesByMonth,
            backgroundColor: "#A78BFA", // Light purple for bars
            borderColor: "#A78BFA", // Matching border color
            borderWidth: 1,
          },
        ],
      };
    },

    getAvailableYears() {
      const years = this.localSalesData.map((sale) =>
        new Date(sale.date_sold).getFullYear()
      );
      return [...new Set(years)];
    },

    renderChart() {
      if (!this.localSalesData.length) {
        console.error("No sales data available to render the chart.");
        return;
      }

      const ctx = document.getElementById("sales-chart").getContext("2d");
      this.chart = new Chart(ctx, {
        type: "bar", // Bar chart
        data: this.getChartData(),
        options: {
          responsive: true,
          plugins: {
            legend: { display: false }, // Remove the legend
          },
          scales: {
            x: {
              grid: { display: false }, // No grid lines for X-axis
              ticks: { color: "#555" },
            },
            y: {
              beginAtZero: true,
              grid: { color: "#eaeaea" },
              ticks: { color: "#555" },
            },
          },
          layout: {
            padding: {
              top: 20, // Spacing above the chart
              bottom: 10,
              left: 10,
              right: 10,
            },
          },
        },
      });
    },
  },
};
</script>

<style scoped>
.chart-wrapper {
  position: relative;
  width: 100%;
  height:100%;
}

.chart-container {
  background-color: #fff; /* Clean white background */
  border-radius: 4px; /* Rounded edges */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15); /* Subtle shadow */
  padding: 20px;
  width: 100%;
  max-width: 1100px;
  margin: auto;
}

.chart-header-container {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  margin-bottom: 5px;
}

.chart-title {
  font-size: 18px;
  padding: 10px;
  font-weight: bold;
  color: #333;
  margin: 0;

}

.year-selector {
  border: none;
  padding: 0;
  /* padding: 12px 10px; */
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  color: #333;
  margin: 0;
}

canvas {
  max-width: 100%;
}
</style>
