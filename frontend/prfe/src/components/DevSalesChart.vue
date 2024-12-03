<template>
  <div>
    <h2>Sales Data for {{ selectedYear }}</h2>
    <div>
      <label for="year">Select Year:</label>
      <select id="year" v-model="selectedYear" @change="updateChart">
        <option v-for="year in availableYears" :key="year" :value="year">
          {{ year }}
        </option>
      </select>
    </div>
    <canvas id="sales-chart"></canvas>
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
    console.log("Initial sales data:", this.salesData); // Add this line
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
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December",
        ],
        datasets: [
          {
            label: "Sales",
            data: salesByMonth,
            fill: false,
            borderColor: "rgba(75, 192, 192, 1)",
            tension: 0.1,
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
        type: "line",
        data: this.getChartData(),
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Sales Per Month",
            },
          },
          scales: {
            x: {
              ticks: {
                autoSkip: false,
                maxRotation: 0,
                padding: 20,
              },
            },
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    },
  },
};
</script>

<style scoped>
canvas {
  max-width: 100%;
  height: 400px;
}
</style>
