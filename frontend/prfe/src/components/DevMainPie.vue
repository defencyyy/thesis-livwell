<template>
  <div class="pie-chart">
    <canvas ref="DevMainPie"></canvas>
  </div>
</template>

<script>
import { Pie } from "chart.js";

export default {
  props: {
    salesData: {
      type: Array,
      required: true,
    },
  },
  mounted() {
    this.renderPieChart();
  },
  methods: {
    renderPieChart() {
      const ctx = this.$refs.pieChart.getContext("2d");
      const data = {
        labels: this.salesData.map((item) => item.site),
        datasets: [
          {
            data: this.salesData.map((item) => item.sales),
            backgroundColor: [
              "#FF5733",
              "#33FF57",
              "#3357FF",
              "#F0F033",
              "#FF33F6",
            ],
          },
        ],
      };
      new Pie(ctx, {
        data: data,
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
            tooltip: {
              callbacks: {
                label: function (tooltipItem) {
                  return tooltipItem.label + ": " + tooltipItem.raw + " sales";
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
.pie-chart {
  width: 100%;
  max-width: 600px;
  margin: auto;
}
</style>
