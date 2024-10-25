<template>
  <div class="milestones-page">
    <SideNav />
    <div class="content">
      <h2>Milestones Summary</h2>
      <div class="milestones-summary">
        <div class="milestone-item">
          <strong>Total Sales:</strong> {{ totalSales }}
        </div>
        <div class="milestone-item">
          <strong>Total Commissions:</strong> {{ totalCommissions }}
        </div>
        <div class="milestone-item">
          <strong>Total Milestones:</strong> {{ totalMilestones }}
        </div>
      </div>
      
      <div v-if="siteSales.length > 0" class="site-sales">
        <h3>Site Sales Information</h3>
        <div class="site-container">
          <div v-for="site in siteSales" :key="site.id" class="site">
            <img :src="site.picture" alt="Site Image" />
            <h4>{{ site.name }}</h4>
            <p>Total Sales: {{ site.total_sales }}</p>
          </div>
        </div>
      </div>

      <div v-else class="no-progress">
        <p>No progress yet.</p>
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
      totalSales: 0,
      totalCommissions: 0,
      totalMilestones: 0,
      siteSales: [], // To store site sales information
    };
  },
  methods: {
    async fetchMilestonesData() {
      const brokerId = localStorage.getItem("broker_id"); // Get broker ID from local storage

      if (!brokerId) {
        console.error("Broker ID not found in local storage.");
        return; // Exit if broker ID is not available
      }

      try {
        // Fetch total sales
        const salesResponse = await fetch(`http://localhost:8000/sales/total/?broker_id=${brokerId}`);
        if (salesResponse.ok) {
          const salesData = await salesResponse.json();
          this.totalSales = salesData.total_sales; // Update total sales in the component state
        } else {
          console.error("Failed to fetch total sales");
        }

        // Fetch total commissions
        const commissionsResponse = await fetch(`http://localhost:8000/sales/commissions/?broker_id=${brokerId}`);
        if (commissionsResponse.ok) {
          const commissionsData = await commissionsResponse.json();
          this.totalCommissions = commissionsData.total_commissions; // Update total commissions in the component state
        } else {
          console.error("Failed to fetch total commissions");
        }

        // Fetch site sales data
        const sitesResponse = await fetch(`http://localhost:8000/sales/sites/?broker_id=${brokerId}`);
        if (sitesResponse.ok) {
          const sitesData = await sitesResponse.json();
          // Filter sites to include only those where sales exist
          this.siteSales = sitesData.sites.filter(site => site.total_sales > 0);
        } else {
          console.error("Failed to fetch site sales data");
        }
      } catch (error) {
        console.error("An error occurred while fetching milestones data:", error);
      }
    },
  },
  mounted() {
    this.fetchMilestonesData(); // Fetch total sales and commissions when the component is mounted
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
  display: flex; /* Use flexbox to align items horizontally */
  justify-content: space-around; /* Space items evenly */
  margin-top: 20px; /* Adds margin to separate from title */
}

.milestone-item {
  flex: 1; /* Allow items to take equal space */
  text-align: center; /* Center text within each item */
}

.site-sales {
  margin-top: 20px; /* Adds margin to separate from milestones */
}

.site-container {
  display: flex; /* Aligns site items in a row */
  justify-content: space-evenly; /* Space items evenly */
  flex-wrap: nowrap; /* Prevents wrapping to a new line */
}

.site {
  margin: 0 10px; /* Adds margin for individual site info */
  text-align: center; /* Center text in each site */
  flex: 0 1 auto; /* Allows the site items to take their natural size */
}

.site img {
  max-width: 100px; /* Set a fixed width for images */
  height: auto; /* Maintains aspect ratio */
}

.no-progress {
  margin-top: 20px; /* Adds margin for no progress message */
  font-weight: bold; /* Makes the message stand out */
}
</style>
