<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">

        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">Milestones Summary</div>
          </div>
        </div>


        <div v-if="loading" class="loading-message">Loading data...</div>

        <div v-if="error" class="error-message">{{ error }}</div>

        <div class = "dashboard-boxes" v-else>
          <div class = "box">
            <p>Total Sales</p>
            <h2>{{ totalSales }}</h2>
          </div>
          <div class = "box">
            <p>Total Commissions</p>
            <h2>{{ totalCommissions }}</h2>
          </div>
          <div class = "box">
            <p>Total Milestones</p>
            <h2>{{ totalMilestones }}</h2>
          </div>
        </div>

        <br><br>
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">Site Sales Information</div>
          </div>
        </div>
        <div v-if="siteSales.length === 0">
            No progress yet.
        </div>
        <div v-else class = "site-grid">
          <div
                v-for="site in siteSales"
                :key="site.id"
                class="site-card"
                @click="openModal(site)"
              >
              <img
                  :src="site.picture || 'https://via.placeholder.com/100'"
                  alt="Site Image"
                  class = "site-image"
                />
              <h2 class="site-name">
                {{ site.name }}
              </h2>
              <p class="site-totalsales">
                <strong>Total Sales</strong><br>{{ site.total_sales }}
              </p>
            </div>
        </div>

        <div class="milestones-section">

          <!-- Milestones Achieved Table -->
          <br><br>
          <div class="title-wrapper">
            <div class="title-left">
              <div class="title-icon"></div>
              <div class="edit-title">Milestones Achieved</div>
            </div>
          </div>

          <div class="outside-headers">
            <span class="header-item">Name</span>
            <span class="header-item">Reward</span>
            <span class="header-item">Description</span>
          </div>

          <div v-if="achievedMilestones.length === 0">
            No milestones achieved yet.
          </div>
          <div
            v-else
            v-for="milestone in achievedMilestones"
            :key="milestone.id"
            class="card border-0 rounded-1 mx-auto my-2"
            style="
              max-width: 1100px;
              box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <div class = "card-body">
              <table class = "next-milestone-table">
                <tbody>
                  <tr>
                    <td>
                      <span>{{ milestone.name }}</span>
                    </td>
                    <td>
                      <span>{{ milestone.reward }}</span>
                    </td>
                    <td>
                      <span>{{ milestone.description }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
      
          <!-- Next Milestones Table -->
           <br><br>
          <div class="title-wrapper">
            <div class="title-left">
              <div class="title-icon"></div>
              <div class="edit-title">Next Milestones</div>
            </div>
          </div>
          <div class="outside-headers">
            <span class="header-item">Name</span>
            <span class="header-item">Reward</span>
            <span class="header-item">Description</span>
          </div>

          <div v-if="nextMilestones.length === 0">
            No pending milestones.
          </div>

          <div
            v-else
            v-for="milestone in nextMilestones"
            :key="milestone.id"
            class="card border-0 rounded-1 mx-auto my-2"
            style="
              max-width: 1100px;
              box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <div class = "card-body">
              <table class = "next-milestone-table">
                <tbody>
                  <tr>
                    <td>
                      <span>{{ milestone.name }}</span>
                    </td>
                    <td>
                      <span>{{ milestone.reward }}</span>
                    </td>
                    <td>
                      <span>{{ milestone.description }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Modal -->
        <b-modal v-model ="showModal" :title="`Site ${selectedSite ? selectedSite.name : ''}`" centered hide-footer>
          <div>
            <div v-if="selectedSite && selectedSite.sales.length > 0">
              <h5>Sales Details</h5><br>
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
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from "@/components/Header.vue"
import SideNav from "@/components/SideNav.vue";
import { mapGetters } from "vuex";
import { BModal } from "bootstrap-vue-3";

export default {
  name: "BrkMilestones",
  components: {
    SideNav,
    BModal,
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
  margin-left: 250px;
  flex-direction: column;
  flex: 1;
  margin-top: 60px;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}

.title-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1100px;
  margin: 20px auto;
  /* Center the wrapper */
}

.title-left {
  display: flex;
  align-items: center;
}

.title-icon {
  width: 15px;
  height: 5px;
  background-color: #343a40;
  border-radius: 5px;
  margin-right: 10px;
}

.edit-title {
  color: #000000;
  text-align: left;
}

.dashboard-boxes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px; /* Adds more space at the top */
  margin-bottom: 20px; /* Keeps bottom margin as is */
}

.box {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.box p {
  font-size: 14px;
  color: #666;
}

.box h2 {
  font-size: 24px;
  margin: 10px 0 0;
}

.outside-headers {
  display: grid;
  grid-template-columns: 25% 25% 50%; /* Match column widths */
  padding: 10px 18px;
  margin: 20px auto 10px;
  max-width: 1100px;
  font-weight: bold;
  text-align: left; /* Left-align for consistency with table */
}

.outside-headers .header-item {
  display: flex;
  justify-content: flex-start; /* Align text horizontally to the left */
  align-items: center; /* Center vertically */
  padding: 5px 0; /* Consistent with table cell padding */
  line-height: 1.2;
  word-wrap: break-word;
}

.next-milestone-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left; /* Consistent with headers */
}

.next-milestone-table td {
  padding: 10px 0; /* Matches outside-headers padding */
}

.next-milestone-table td:nth-child(1),
.outside-headers .header-item:nth-child(1) {
  width: 25%;
}

.next-milestone-table td:nth-child(2),
.outside-headers .header-item:nth-child(2) {
  width: 25%;
}

.next-milestone-table td:nth-child(3),
.outside-headers .header-item:nth-child(3) {
  width: 50%;
}

.site-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  max-width: 1100px;
  /* Matches the max-width of the card */
  margin: 0 auto;
  /* Centers the grid within the parent */
}

.site-card {
  background: #fff;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  /* transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; */
}

.site-card:hover {
  transform: translateY(-2px);
}

.site-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  /* Ensures the image is cropped to fit the area */
  border-radius: 12px;
  margin-bottom: 10px;
}

.site-name {
  font-size: 15px;
  font-weight: bold;
}

.site-totalsales {
  font-size: 14px;
  color: #777;
}

/* juju end */

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
