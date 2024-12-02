<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <h2>Milestones Summary</h2>

        <div v-if="loading" class="loading-message">Loading data...</div>

        <div v-if="error" class="error-message">{{ error }}</div>

        <div class="milestones-summary" v-else>
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
              <img
                :src="site.picture || 'https://via.placeholder.com/100'"
                alt="Site Image"
              />
              <h4>{{ site.name }}</h4>
              <p>Total Sales: {{ site.total_sales }}</p>
            </div>
          </div>
        </div>

        <div v-else-if="!loading" class="no-progress">
          <p>No progress yet.</p>
        </div>

        <div class="milestones-section">
          <!-- Milestones Achieved Table -->
          <h3>Milestones Achieved</h3>
          <table v-if="achievedMilestones.length > 0">
  <thead>
    <tr>
      <th>Name</th>
      <th>Reward</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="milestone in achievedMilestones" :key="milestone.id">
      <td>{{ milestone.name }}</td>
      <td>{{ milestone.reward }}</td>
      <td>{{ milestone.description }}</td>
    </tr>
  </tbody>
</table>

          <p v-else>No milestones achieved yet.</p>

          <!-- Next Milestones Table -->
          <h3>Next Milestones</h3>
          <table v-if="nextMilestones.length > 0">
  <thead>
    <tr>
      <th>Name</th>
      <th>Reward</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="milestone in nextMilestones" :key="milestone.id">
      <td>{{ milestone.name }}</td>
      <td>{{ milestone.reward }}</td>
      <td>{{ milestone.description }}</td>
    </tr>
  </tbody>
</table>

          <p v-else>No Pending Milestones</p>
        </div>

        <!-- Modal -->
        <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
          <div class="modal-content">
            <button class="close-button" @click="closeModal">X</button>

            <p v-if="selectedSite">{{ selectedSite.name }}</p>

            <div v-if="selectedSite && selectedSite.sales.length > 0">
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
  </div>
</template>

<script>
import AppHeader from "@/components/Header.vue"
import SideNav from "@/components/SideNav.vue";
import { mapGetters } from "vuex";

export default {
  name: "BrkMilestones",
  components: {
    SideNav,
    AppHeader,
  },
  data() {
    return {
      totalSales: 0,
      totalCommissions: 0,
      totalMilestones: 0,
      siteSales: [],
      achievedMilestones: [],
      nextMilestones: [],
      showModal: false,
      selectedSite: null,
      error: null,
      loading: false,
    };
  },
  computed: {
    ...mapGetters(["getUserId", "isLoggedIn"]),
  },
  methods: {
    async fetchMilestonesData() {
      const brokerId = this.getUserId;

      if (!brokerId) {
        this.error = "Broker ID not found. Please log in again.";
        return;
      }

      this.loading = true;
      try {
        // Fetch total sales
        const salesResponse = await fetch(
          `http://localhost:8000/sales/total/?broker_id=${brokerId}`
        );
        if (salesResponse.ok) {
          const salesData = await salesResponse.json();
          this.totalSales = salesData.total_sales;
        } else {
          this.error = "Failed to fetch total sales.";
        }

        // Fetch total commissions
        const commissionsResponse = await fetch(
          `http://localhost:8000/sales/commissions/?broker_id=${brokerId}`
        );
        if (commissionsResponse.ok) {
          const commissionsData = await commissionsResponse.json();
          this.totalCommissions = commissionsData.total_commissions;
        } else {
          this.error = "Failed to fetch total commissions.";
        }

        // Fetch milestones data
        const milestonesResponse = await fetch(`http://localhost:8000/milestones/?broker_id=${brokerId}`);
        if (milestonesResponse.ok) {
          const milestonesData = await milestonesResponse.json();
          this.achievedMilestones = milestonesData.achieved_milestones;
          this.nextMilestones = milestonesData.next_milestones;
        } else {
          this.error = "Failed to fetch milestones.";
        }

        // Fetch site sales data
        const sitesResponse = await fetch(
          `http://localhost:8000/sales/sites/?broker_id=${brokerId}`
        );
        if (sitesResponse.ok) {
          const sitesData = await sitesResponse.json();
          this.siteSales = sitesData.sites.filter(
            (site) => site.total_sales > 0
          );
        } else {
          this.error = "Failed to fetch site sales data.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching milestones data.";
      } finally {
        this.loading = false;
      }
    },

    async fetchSalesDetails(site) {
      const brokerId = this.getUserId;

      if (!brokerId) {
        this.error = "Broker ID not found. Please log in again.";
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:8000/sales/details/?site_id=${site.id}&broker_id=${brokerId}`
        );
        if (response.ok) {
          const salesData = await response.json();
          this.selectedSite = {
            ...site,
            sales: salesData.sales,
          };
        } else {
          this.error = "Failed to fetch sales details.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching sales details.";
      }
    },

    async openModal(site) {
      await this.fetchSalesDetails(site);
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.selectedSite = null;
    },
  },
  mounted() {
    this.fetchMilestonesData();
  },
};
</script>


<style scoped>
html,
body {
  height: 100%;
  margin: 0;
  /* Removes default margin */
  padding: 0;
  /* Removes default padding */
}

/* Ensure .main-page fills the available space */
.main-page {
  display: flex;
  min-height: 100vh;
  /* Ensures it spans the full viewport height */
  background-color: #ebebeb; /* Gray background */
  /* Gray background */
}

.main-content {
  display: flex;
  flex-direction: column;
  margin-top: 80px;
  margin-left: 250px;
  /* Offset for header height */
  flex: 1;
  /* margin-left: 250px; */
  /* Set margin equal to sidebar width */
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

.loading-message {
  margin: 20px 0;
  color: #007bff;
  font-size: 1.2em;
}

.error-message {
  margin: 20px 0;
  color: red;
  font-size: 1.2em;
}
</style>
