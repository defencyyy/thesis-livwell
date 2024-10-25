<template>
  <div class="milestones-page">
    <SideNav />
    <div class="content">
      <h1>Milestones</h1>
      <p>Here you can track your project's milestones.</p>
      
      <div class="milestones-summary">
        <h2>Milestones Summary</h2>
        <p><strong>Total Sales:</strong> {{ totalSales }}</p>
        <p><strong>Total Commissions:</strong> {{ totalCommissions }}</p>
        <p><strong>Total Milestones:</strong> {{ totalMilestones }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue"; // Importing the SideNav component

export default {
  name: "BrkMilestones",
  components: {
    SideNav,
  },
  data() {
    return {
      totalSales: 0, // Default value for total sales
      totalCommissions: 0, // Default value for total commissions
      totalMilestones: 0, // Default value for total milestones
    };
  },
  methods: {
    async fetchTotalSales() {
      const brokerId = localStorage.getItem("broker_id"); // Get broker ID from local storage

      if (!brokerId) {
        console.error("Broker ID not found in local storage.");
        return; // Exit if broker ID is not available
      }

      try {
        const response = await fetch(`http://localhost:8000/sales/total/?broker_id=${brokerId}`);
        if (response.ok) {
          const data = await response.json();
          this.totalSales = data.total_sales; // Update total sales in the component state
        } else {
          console.error("Failed to fetch total sales");
        }
      } catch (error) {
        console.error("An error occurred while fetching total sales:", error);
      }
    },
  },
  mounted() {
    this.fetchTotalSales(); // Fetch total sales when the component is mounted
  },
};
</script>

<style scoped>
.milestones-page {
  display: flex; /* Aligns SideNav and content side by side */
  height: 100vh; /* Full height of the viewport */
}

.content {
  flex: 1; /* Fills remaining space */
  padding: 20px; /* Adds some padding */
  text-align: center; /* Center text in the content area */
}

.milestones-summary {
  margin-top: 20px; /* Adds margin to separate from title */
}
</style>
