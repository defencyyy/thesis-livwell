<template>
  <div>
    <pie :data="pieChartData" :options="pieChartOptions" />
  </div>
</template>

<script>
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

// Registering required Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend);

export default {
  name: "PieChart",
  components: {
    Pie,
  },
  props: {
    sold: {
      type: Number,
      required: true
    },
    pending: {
      type: Number,
      required: true
    },
    reserved: {
      type: Number,
      required: true
    },
  },
 computed: {
   pieChartData() {
    console.log(this.sold, this.pending);
    return {
      labels: ['Sold', 'Pending Reservation', 'Reserved'],
      datasets: [
        {
          // Avoid zero values by setting a small non-zero value (0.1) where necessary
          //data: [this.sold, this.pending, this.reserved], 
          data:[4,2,2],
          backgroundColor: ['#4caf50', '#ff9800', '#2196f3'],
          hoverBackgroundColor: ['#45a049', '#e6893b', '#1976d2'],
        },
      ],
    };
  },
    pieChartOptions() {
      return {
        responsive: true,
        plugins: {
          tooltip: {
            callbacks: {
              label: function (tooltipItem) {
                return tooltipItem.raw + ' units';
              },
            },
          },
          legend: {
            position: 'top',
          },
        },
      };
    },
  },
};
</script>

<style scoped>
.pie-chart-container {
  width: 50%;
  margin: 0 auto;
}

</style>
