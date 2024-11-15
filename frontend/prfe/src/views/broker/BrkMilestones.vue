<template>
  <HeaderLivwell/>
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
          <div
            v-for="site in siteSales"
            :key="site.id"
            class="site"
            @click="openModal(site)"
          >
            <img :src="site.picture" alt="Site Image" />
            <h4>{{ site.name }}</h4>
            <p>Total Sales: {{ site.total_sales }}</p>
          </div>
        </div>
      </div>

      <div v-else class="no-progress">
        <p>No progress yet.</p>
      </div>

      <!-- Modal for displaying site information -->
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
          <button class="close-button" @click="closeModal">X</button>
          <p v-if="selectedSite">{{ selectedSite.name }}</p>
          <div v-if="selectedSite && selectedSite.sales && selectedSite.sales.length > 0">
            <h4>Sales Details:</h4>
            <ul>
              <li v-for="sale in selectedSite.sales" :key="sale.date_sold">
                <strong>Unit Name:</strong> {{ sale.unit_name }} <br />
                <strong>Customer Name:</strong> {{ sale.customer_name }} <br />
                <strong>Date Sold:</strong> {{ sale.date_sold }}
              </li>
            </ul>
          </div>
          <div v-else-if="selectedSite">
            <p>No sales found for this site.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import HeaderLivwell from "@/components/HeaderLivwell.vue";
import SideNav from "@/components/SideNav.vue"; // Importing the SideNav component

export default {
  name: "BrkMilestones",
  components: {
    SideNav, HeaderLivwell 
  },
  data() {
    return {
      totalSales: 0,
      totalCommissions: 0,
      totalMilestones: 0,
      siteSales: [], // To store site sales information
      showModal: false, // Controls the modal visibility
      selectedSite: null, // Stores the currently selected site information
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
    
    async fetchSalesDetails(site) {
      const brokerId = localStorage.getItem("broker_id"); // Get broker ID from local storage
      try {
        const response = await fetch(`http://localhost:8000/sales/details/?site_id=${site.id}&broker_id=${brokerId}`);
        if (response.ok) {
          const salesData = await response.json();
          this.selectedSite = {
            ...site,
            sales: salesData.sales, // Store sales data in the selected site
          };
        } else {
          console.error("Failed to fetch sales details");
        }
      } catch (error) {
        console.error("An error occurred while fetching sales details:", error);
      }
    },

    async openModal(site) {
      await this.fetchSalesDetails(site); // Fetch sales details when opening the modal
      this.showModal = true; // Show the modal after data is fetched
    },
    
    closeModal() {
      this.showModal = false;
      this.selectedSite = null; // Reset selected site when closing the modal
    },
  },
  mounted() {
    this.fetchMilestonesData(); // Fetch total sales and commissions when the component is mounted
  },
};
</script>

<style scoped>
.milestones-page {
  display: flex;
  height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}

.milestones-summary {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.milestone-item {
  flex: 1;
  text-align: center;
}

.site-sales {
  margin-top: 20px;
}

.site-container {
  display: flex;
  justify-content: space-evenly;
  flex-wrap: nowrap;
}

.site {
  margin: 0 10px;
  text-align: center;
  cursor: pointer;
}

.site img {
  max-width: 100px;
  height: auto;
}

.no-progress {
  margin-top: 20px;
  font-weight: bold;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
  text-align: center;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 1.2em;
  cursor: pointer;
}
</style>
