<template>
  <div class="chart-container">
    <div class="chart-header">
      <h2 class="chart-title">Top 5 Brokers by Sales Sold</h2>
    </div>
    <div class="chart-wrapper">
      <canvas id="broker-sales-chart"></canvas>
    </div>
    <div class="broker-list">
      <ul v-if="brokers.length > 0"></ul>
      <p v-else>No brokers with sales yet.</p>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";

export default {
  name: "DevMilestoneChart",
  data() {
    return {
      chart: null,
      brokers: [], // To store the brokers data
      rankingColors: [], // Store the colors for each rank
    };
  },
  mounted() {
    Chart.register(...registerables);
    this.fetchTopBrokers();
  },
  methods: {
    async fetchTopBrokers() {
      try {
        const response = await fetch(
          "http://localhost:8000/developer/brokers/api/top-brokers/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Top Brokers Data:", data);

        // Filter brokers with total_sales > 0 and limit to top 5
        this.brokers = data
          .filter((broker) => broker.total_sales > 0)
          .slice(0, 5);

        // Generate ranking colors
        this.rankingColors = this.generateRankingColors(this.brokers.length);
        this.renderChart();
      } catch (error) {
        console.error("Error fetching top brokers:", error);
      }
    },
    generateRankingColors(count) {
      // Define a light purple gradient color range
      const colors = [
        "#D8A7D3", // Light Purple
        "#C692D6", // Slightly darker purple
        "#B17FD9", // Medium purple
        "#9E6CDB", // Darker purple
        "#8B59DE", // Even darker purple
      ];

      // Return a subset of the colors based on how many brokers there are
      return colors.slice(0, count);
    },
    renderChart() {
      if (!this.brokers.length) {
        console.error("No broker data available to render the chart.");
        document.getElementById("broker-sales-chart").innerHTML =
          "No brokers with sales.";
        return;
      }

      const ctx = document
        .getElementById("broker-sales-chart")
        .getContext("2d");

      const totalSales = this.brokers.map((broker) => broker.total_sales);
      const brokerNames = this.brokers.map((broker) => broker.full_name);

      this.chart = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: brokerNames,
          datasets: [
            {
              label: "Total Sales",
              data: totalSales,
              backgroundColor: this.rankingColors,
              borderWidth: 2,
              borderColor: "#fff",
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top", // Move the legend above the donut
              labels: {
                boxWidth: 15, // Adjust the size of the color box
                padding: 10, // Add padding between legend items
              },
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  const brokerName = context.label;
                  const sales = context.raw;
                  return `${brokerName}: ${sales} Sales`;
                },
              },
            },
          },
          layout: {
            padding: {
              top: 20, // Add space above the chart for the legend
              bottom: 20, // Add space below the chart
            },
          },
          cutout: "50%",
        },
      });
    },
  },
};
</script>

<style scoped>
.chart-container {
  background-color: #fff;
  border-radius: 4px;
  padding: 20px;
  width: 100%;
  max-width: 1100px;
  margin: auto;
}

.chart-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.chart-title {
  font-size: 18px;
  padding: 10px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

canvas {
  max-width: 100%;
}

.broker-list {
  margin-top: 20px;
  max-height: 200px; /* Limit the height of the broker list */
  overflow-y: auto; /* Make the list scrollable */
}

.broker-list ul {
  padding: 0;
  list-style: none;
}

.broker-list li {
  font-size: 16px;
  color: #333;
  padding: 5px 0;
}

.rank-indicator {
  display: inline-block;
  width: 15px;
  height: 15px;
  margin-right: 10px;
  border-radius: 50%;
}
</style>
