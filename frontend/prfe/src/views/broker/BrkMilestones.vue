<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title"><strong>Milestones Summary</strong></div>
          </div>
        </div>

        <div v-if="loading" class="loading-message">Loading data...</div>

        <div v-if="error" class="error-message">{{ error }}</div>

        <div class="dashboard-boxes" v-else>
          <div class="box">
            <div class="box-header">
              <div class="icon-container">
                <i class="fa fa-shopping-cart" style="font-size: 13px"></i>
              </div>
              <p>Total Sales</p>
            </div>
            <h2>{{ totalSales }}</h2>
          </div>

          <div class="box">
            <div class="box-header">
              <div class="icon-container">
                <i class="fa fa-money-bill" style="font-size: 13px"></i>
              </div>
              <p>Total Commissions</p>
            </div>
            <h2>{{ formatCurrency(totalCommissions) }}</h2>
          </div>

          <div class="box">
            <div class="box-header">
              <div class="icon-container">
                <i class="fas fa-flag" style="font-size: 13px"></i>
              </div>
              <p>Total Milestones</p>
            </div>
            <h2>{{ totalMilestones }}</h2>
          </div>
        </div>

        <br /><br />
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">
              <strong>Site Sales Information</strong>
            </div>
          </div>
        </div>

        <div v-if="siteSales.length === 0">No progress yet.</div>

        <div v-else class="site-grid">
          <div
            v-for="site in siteSales"
            :key="site.id"
            class="site-card"
            @click="openModal(site)"
          >
            <img
              :src="site.picture || require('@/assets/home.png')"
              alt="Site Image"
              class="site-image"
            />
            <h2 class="site-name">
              {{ site.name }}
            </h2>
            <p class="site-totalsales">
              <strong>Total Sales</strong><br />{{ site.total_sales }}
            </p>
          </div>
        </div>

        <div class="milestones-section">
          <!-- Milestones Achieved Table -->
          <br /><br />
          <div class="title-wrapper">
            <div class="title-left">
              <div class="title-icon"></div>
              <div class="edit-title"><strong>Milestones Achieved</strong></div>
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
            <div class="card-body">
              <table class="next-milestone-table">
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
          <br /><br />
          <div class="title-wrapper">
            <div class="title-left">
              <div class="title-icon"></div>
              <div class="edit-title"><strong>Next Milestones</strong></div>
            </div>
          </div>

          <div class="outside-headers">
            <span class="header-item">Name</span>
            <span class="header-item">Reward</span>
            <span class="header-item">Description</span>
          </div>

          <div v-if="nextMilestones.length === 0">No pending milestones.</div>

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
            <div class="card-body">
              <table class="next-milestone-table">
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
        <b-modal
          v-model="showModal"
          :title="`Site ${selectedSite ? selectedSite.name : ''}`"
          centered
          hide-footer
        >
          <div>
            <div v-if="selectedSite && selectedSite.sales.length > 0">
              <center>
                <h5>Sales Details</h5>
                <br />
              </center>
              <table class="table">
                <thead>
                  <tr>
                    <th>Unit Name</th>
                    <th>Customer Name</th>
                    <th>Date Sold</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="sale in selectedSite.sales" :key="sale.date_sold">
                    <td>{{ sale.unit_name }}</td>
                    <td>{{ sale.customer_name }}</td>
                    <td>{{ sale.date_sold }}</td>
                  </tr>
                </tbody>
              </table>
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
import AppHeader from "@/components/Header.vue";
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
    formatCurrency(amount) {
      if (isNaN(amount)) return "₱0.00"; // Return '₱0.00' if the amount is not a number
      return new Intl.NumberFormat("en-PH", {
        style: "currency",
        currency: "PHP",
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }).format(amount);
    },
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
          `${process.env.vue_app_api_url}/sales/total/?broker_id=${brokerId}`
        );
        if (salesResponse.ok) {
          const salesData = await salesResponse.json();
          this.totalSales = salesData.total_sales;
        } else {
          this.error = "Failed to fetch total sales.";
        }

        // Fetch total commissions
        const commissionsResponse = await fetch(
          `${process.env.vue_app_api_url}/sales/commissions/?broker_id=${brokerId}`
        );
        if (commissionsResponse.ok) {
          const commissionsData = await commissionsResponse.json();
          this.totalCommissions = commissionsData.total_commissions;
        } else {
          this.error = "Failed to fetch total commissions.";
        }

        // Fetch milestones data
        const milestonesResponse = await fetch(
          `${process.env.vue_app_api_url}/milestones/?broker_id=${brokerId}`
        );
        if (milestonesResponse.ok) {
          const milestonesData = await milestonesResponse.json();
          this.achievedMilestones = milestonesData.achieved_milestones;
          this.nextMilestones = milestonesData.next_milestones;
          this.totalMilestones = milestonesData.total_milestones; // Get total milestones count
        } else {
          this.error = "Failed to fetch milestones.";
        }

        // Fetch site sales data
        const sitesResponse = await fetch(
          `${process.env.vue_app_api_url}/sales/sites/?broker_id=${brokerId}`
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
          `${process.env.vue_app_api_url}/sales/details/?site_id=${site.id}&broker_id=${brokerId}`
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
  padding: 0;
}

.main-page {
  display: flex;
  min-height: 100vh;
  background-color: #e8f0fa;
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
  max-width: 1100px;
  width: 100%;
  margin: 0 auto;
}

.box-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.box h2 {
  margin: 10px 0 0;
  font-size: 30px;
  font-weight: bold;
  color: #000;
  padding-bottom: 10px;
}

.box {
  position: relative;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.box-header {
  display: flex;
  align-items: center;
  justify-content: start;
  gap: 15px;
  margin: 0;
}

.icon-container {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #343a40;
  color: #ffffff;
}

.box-header p {
  margin: 0;
  padding: 0;
  font-size: 13px;
  color: #000000;
}

.outside-headers {
  display: grid;
  grid-template-columns: 25% 25% 50%;
  padding: 10px 18px;
  margin: 20px auto 10px;
  max-width: 1100px;
  font-weight: bold;
  text-align: left;
}

.outside-headers .header-item {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 5px 0;
  line-height: 1.2;
  word-wrap: break-word;
  font-size: 14px;
}

.next-milestone-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 14px;
}

.next-milestone-table td {
  padding: 10px 0;
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
  margin: 0 auto;
}

.site-card {
  background: #fff;
  padding: 16px;
  text-align: center;
  cursor: pointer;
}

.site-card:hover {
  transform: translateY(-2px);
}

.site-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
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

.site-sales {
  margin-top: 20px;
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

@media (max-width: 1440px) {
  .outside-headers .header-item {
    padding: 5px 0;
    font-size: 14px; /* Adjust font size for better fit on medium screens */
  }
}

@media (max-width: 1024px) {
  .outside-headers .header-item {
    font-size: 12px; /* Decrease font size on smaller screens */
    width: 30%; /* Reduce width to allow more space between items */
  }
}

@media (max-width: 720px) {
  .outside-headers {
    flex-direction: column;
    align-items: center; /* Stack items vertically */
    text-align: center;
  }

  .outside-headers .header-item {
    width: 100%; /* Each item takes up full width on smaller screens */
    padding: 10px 0; /* Increase padding for better touch targets */
  }
}
</style>
