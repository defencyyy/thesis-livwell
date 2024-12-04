<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <!-- Dashboard Boxes -->
        <div class="dashboard-boxes">
          <div class="box">
            <div class="box-header">
              <div class="icon-container">
                <i class="fa fa-user" style="font-size: 13px;"></i> <!-- Replace with your desired icon -->
              </div>
              <p>Brokers</p>
            </div>
            <h2>{{ brokerCount }}</h2>
          </div>
          <div class="box">
            <div class="box-header">
              <div class="icon-container">
                <i class="fa fa-building" style="font-size: 13px;"></i> <!-- Replace with your desired icon -->
              </div>
              <p>Sites</p>
            </div>
            <h2>{{ siteCount }}</h2>
          </div>
          <div class="box">
            <div class="box-header">
              <div class="icon-container">
                <i class="fa fa-home" style="font-size: 13px;"></i> <!-- Replace with your desired icon -->
              </div>
              <p>Available Units</p>
            </div>
            <h2>{{ availableUnits }}</h2>
          </div>
          <div class="box">
            <div class="box-header">
              <div class="icon-container">
                <i class="fa fa-shopping-cart" style="font-size: 13px;"></i> <!-- Replace with your desired icon -->
              </div>
              <p>Sold Sales</p>
            </div>
            <h2>{{ salesCount }}</h2>
          </div>
          <div class="box">
            <div class="box-header">
              <div class="icon-container">
                <i class="fa fa-spinner" style="font-size: 13px;"></i> <!-- Replace with your desired icon -->
              </div>
              <p>Ongoing Sales</p>
            </div>
            <h2>{{ ongoingSales }}</h2>
          </div>
        </div>


        <div class="grid-layout">
          <!-- Left Section -->
          <div class="left-content">
            <div class="title-wrapper">
              <div class="title-left">
                <div class="title-icon"></div>
                <div class="edit-title">Pending Sales</div>
              </div>
            </div>
            <div class="card border-0 rounded-1 mx-auto" style="box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)">
              <div class="card-body">
                <div class="row">
                  <div class="toolbar">
                    <div class="left-section">
                      <div class="search-bar-container">
                        <input type="text" v-model="searchQuery" @input="filterSales"
                          placeholder="Search Broker/Customer" class="search-bar" />
                        <i class="fa fa-search search-icon"></i>
                      </div>
                      <select v-model="selectedStatus" @change="filterSales" class="dropdown">
                        <option value="">All Status</option>
                        <option value="Pending Reservation">Pending Reservation</option>
                        <option value="Pending Sold">Pending Sold</option>
                      </select>
                      <select v-model="selectedSite" @change="filterSales" class="dropdown">
                        <option value="">All Sites</option>
                        <option v-for="site in filteredSites" :key="site.id" :value="site.id">
                          {{ site.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="outside-headers">
              <span class="header-item">ID</span>
              <span class="header-item">Broker</span>
              <span class="header-item">Customer</span>
              <span class="header-item">Site</span>
              <span class="header-item">Status</span>
            </div>

            <div v-if="filteredSales.length > 0">
              <div v-for="sale in filteredSales" :key="sale.id" class="card border-0 rounded-1 mx-auto" style="
              max-width: 1100px;
              box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            ">
                <div class="card-body">
                  <table class="sale-table">
                    <tbody>
                      <tr>
                        <td>{{ sale.relativeID }}</td>
                        <td>{{ sale.brokerName }}</td>
                        <td>{{ sale.customerName }}</td>
                        <td>{{ sale.site ? sale.site.name : "No Site" }}</td>
                        <td>{{ sale.status }}</td>
                      </tr>
                    </tbody>
                  </table>

                </div>

              </div>
            </div>
            <p v-else>No pending sales found with the selected filters.</p>

          </div>

          <!-- Right Section -->
          <div class="right-content">
            <div class="card border-0 rounded-1 mx-auto"
              style="box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); height: 60vh;">
              <div class="card-body">
                <div class="row">
                  <div class="toolbar">
                    <div class="left-section">
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- <div class="sales-table">
          <h3>Pending Sales</h3>

          <div class="search-filter-controls">
            <input type="text" v-model="searchQuery" @input="filterSales" placeholder="Search by Names"
              class="search-input" />
            <select v-model="selectedStatus" @change="filterSales" class="filter-dropdown">
              <option value="">All Statuses</option>
              <option value="Pending Reservation">Pending Reservation</option>
              <option value="Pending Sold">Pending Sold</option>
            </select>
            <select v-model="selectedSite" @change="filterSales" class="filter-dropdown">
              <option value="">All Sites</option>
              <option v-for="site in filteredSites" :key="site.id" :value="site.id">
                {{ site.name }}
              </option>
            </select>
          </div>

          <table v-if="filteredSales.length">
            <thead>
              <tr>
                <th>Sale ID</th>
                <th>Broker</th>
                <th>Customer</th>
                <th>Site</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="sale in filteredSales" :key="sale.id">
                <td>{{ sale.relativeID }}</td>
                <td>{{ sale.brokerName }}</td>
                <td>{{ sale.customerName }}</td>
                <td>{{ sale.site ? sale.site.name : "No Site" }}</td>
                <td>{{ sale.status }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else>No pending sales found with the selected filters.</p>
        </div> -->
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";
import { mapState } from "vuex";

export default {
  name: "DevMainPage",
  components: {
    SideNav,
    AppHeader,
  },
  data() {
    return {
      brokerCount: 0,
      siteCount: 0,
      availableUnits: 0,
      salesCount: 0,
      ongoingSales: 0,
      pendingSales: [],
      filteredSales: [],
      searchQuery: "",
      selectedStatus: "",
      selectedSite: "",
      sites: [],
      filteredSites: [],
      loading: true,
      error: null,
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId,
      companyId: (state) => state.companyId,
    }),
  },
  mounted() {
    this.fetchDashboardData();
    this.fetchSites();
    this.fetchPendingSales();
    this.setupAxiosInterceptors(); // Add Axios Interceptor setup
  },
  methods: {
    async fetchDashboardData() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/dashboard/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        console.log("Fetched dashboard data:", response.data);
        this.brokerCount = response.data.brokers;
        this.siteCount = response.data.sites;
        this.availableUnits = response.data.availableUnits;
        this.salesCount = response.data.salesCount;
        this.ongoingSales = response.data.ongoingSales;
      } catch (error) {
        this.error = "Error fetching dashboard data";
        console.error("Error fetching dashboard data:", error);
      } finally {
        this.loading = false;
      }
    },

    async fetchSites() {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/sites/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.sites = Array.isArray(response.data) ? response.data : [];
        this.filterSitesWithPendingSales();
      } catch (error) {
        console.error("Error fetching sites:", error);
      }
    },

    filterSitesWithPendingSales() {
      const siteIdsWithPendingSales = new Set(
        this.pendingSales
          .filter(
            (sale) =>
              sale.status === "Pending Reservation" ||
              sale.status === "Pending Sold"
          )
          .map((sale) => sale.site.id)
      );

      const filteredSites = this.sites.filter((site) =>
        siteIdsWithPendingSales.has(site.id)
      );

      this.filteredSites = [...filteredSites];
    },

    async fetchPendingSales() {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/sales/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        const sales = response.data.data || [];
        this.pendingSales = sales
          .filter(
            (sale) =>
              sale.status === "Pending Reservation" ||
              sale.status === "Pending Sold"
          )
          .map((sale, index) => ({
            ...sale,
            relativeID: index + 1,
            brokerName: `${sale.broker.first_name} ${sale.broker.last_name}`,
            customerName: `${sale.customer.first_name} ${sale.customer.last_name}`,
          }));
        this.filteredSales = this.pendingSales;
        this.filterSitesWithPendingSales();
      } catch (error) {
        console.error("Error fetching pending sales:", error);
      }
    },

    filterSales() {
      let filtered = this.pendingSales;

      if (this.searchQuery) {
        filtered = filtered.filter(
          (sale) =>
            `${sale.customerName}`
              .toLowerCase()
              .includes(this.searchQuery.toLowerCase()) ||
            `${sale.brokerName}`
              .toLowerCase()
              .includes(this.searchQuery.toLowerCase())
        );
      }

      if (this.selectedStatus) {
        filtered = filtered.filter(
          (sale) => sale.status === this.selectedStatus
        );
      }

      if (this.selectedSite) {
        filtered = filtered.filter(
          (sale) => sale.site.id === parseInt(this.selectedSite)
        );
      }

      this.filteredSales = filtered;
    },

    async refreshAccessToken() {
      try {
        const refreshToken = localStorage.getItem("refreshToken");
        const response = await axios.post(
          "http://localhost:8000/api/token/refresh/",
          {
            refresh: refreshToken,
          }
        );
        if (response.status === 200) {
          const { access } = response.data;
          localStorage.setItem("accessToken", access);
          return access;
        }
      } catch (error) {
        console.error("Error refreshing token:", error);
        this.handleTokenRefreshFailure();
      }
    },

    handleTokenRefreshFailure() {
      alert("Session expired. Redirecting to home.");
      localStorage.clear();
      this.$store.dispatch("logout");
      this.$router.push({ name: "Home" });
    },

    setupAxiosInterceptors() {
      axios.interceptors.response.use(
        (response) => response,
        async (error) => {
          if (error.response?.status === 401) {
            const refreshedToken = await this.refreshAccessToken();
            if (refreshedToken) {
              error.config.headers[
                "Authorization"
              ] = `Bearer ${refreshedToken}`;
              return axios(error.config);
            }
          }
          return Promise.reject(error);
        }
      );
    },
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
  background-color: #e8f0fa;
  /* Gray background */
}

.SideNav {
  width: 250px;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #343a40;
  z-index: 1;
}

.AppHeader {
  width: 100%;
  height: 60px;
  background-color: #343a40;
  display: flex;
  align-items: center;
  padding-left: 10px;
}

.main-content {
  display: flex;
  margin-left: 250px;
  flex-direction: column;
  flex: 1;
  margin-top: 90px;
}

.content {
  flex: 1;
  padding: 20px;
  display: flex;
  /* Use flexbox to center the content */
  align-items: center;
  /* Center vertically */
  flex-direction: column;
  /* Stack the dashboard boxes and sales table vertically */
}

.title-left {
  display: flex;
  align-items: center;
}

.title-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1100px;
  width: 100%;
  margin: 20px auto;
  /* Center the wrapper */
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

.grid-layout {
  display: grid;
  grid-template-columns: 3fr 2fr;
  /* Equal width for both columns */

  gap: 20px;
  /* Match the spacing of the dashboard boxes */
  width: 100%;
  max-width: 1100px;
  /* Match the max-width of the dashboard-boxes */
  margin-left: 5px;
  /* Center grid-layout horizontally */

}

.left-content {
  display: flex;
  flex-direction: column;

}


.right-content {
  display: flex;
  flex-direction: column;
  margin-top: 20px;

}

.card {
  width: 100%;
  margin-bottom: 5px;
  margin-top: 0;
  max-width: 1100px;
  /* Ensures the card and grid align */
  margin-left: auto;
  /* Centers the card */
  margin-right: auto;

}

.toolbar {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
  padding-left: 20px;
  /* Space on the left side */
  padding-right: 20px;
  /* Space on the right side */
}

.toggle-button {
  margin-left: 10px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  color: #333;
  padding: 5px 10px;
  cursor: pointer;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 10px;
  /* Space between search bar and dropdown */
}

.search-bar-container {
  position: relative;
  width: 100%;
  max-width: 400px;
  /* Adjust the width as needed */
}

.search-bar {
  width: 250px;
  padding: 8px 12px 8px 40px;
  /* Add left padding to make space for the icon */
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 12px;
}

.search-icon {
  position: absolute;
  top: 50%;
  left: 10px;
  /* Position the icon inside the input */
  transform: translateY(-50%);
  color: #777;
  font-size: 16px;
  pointer-events: none;
  /* Prevent the icon from blocking clicks in the input */
}

.dropdown-container {
  position: relative;
}

.dropdown {
  appearance: none;
  padding: 8px 12px;
  height: 38px;
  /* Explicitly set height */
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 12px;
  width: 80%;
  max-width: 150px;
  background-color: white;
  color: #333;
  padding-right: 30px;
  background-image: url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"%3E%3Cpath d="M7 10l5 5 5-5z"/%3E%3C/svg%3E');
  background-position: right 10px center;
  background-repeat: no-repeat;
  background-size: 14px;
}

.dashboard-boxes {
  display: grid;
  /* Use grid for responsive layout */
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  /* Responsive grid */
  gap: 20px;
  /* Add spacing between boxes */
  max-width: 1100px;
  width: 100%;
  /* Set a max width */
  margin: 0 auto;
  /* Center the container horizontally */
}

.box-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  /* Space between icon and title */
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
  /* Make the box a positioning context */
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
  /* Make the icon circular */
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

/* Ensure that the sale table's headers and columns align */
.sale-table {
  width: 100%;
  border-collapse: collapse;
  /* Ensures there is no space between cells */
  table-layout: fixed;
  /* Forces equal width for columns */
}

.sale-table th,
.sale-table td {
  text-align: left;
}

.sale-table th {
  background-color: #f7f7f7;
  font-weight: bold;
}

.sale-table td {
  word-wrap: break-word;
  /* Ensures long text breaks properly */
}

/* Align the outside headers with the table */
.outside-headers {
  display: grid;
  grid-template-columns: 5% 30% 25% 20% 20%;
  /* Adjust widths for better layout */
  width: 100%;
  padding: 0 15px;
  margin: 12px auto 10px;
}

.header-item {
  text-align: left;
  font-size: 12px;
  color: #333;
  font-weight: bold;

}

.sale-table th:nth-child(2),
.sale-table td:nth-child(2) {
  /* Location column */
  width: 30%;
}

.sale-table th:nth-child(3),
.sale-table td:nth-child(3) {
  /* Status column */
  width: 25%;
}

.sale-table th:nth-child(4),
.sale-table td:nth-child(4) {
  /* Actions column */
  width: 20%;
}

.sale-table th:nth-child(5),
.sale-table td:nth-child(5) {
  /* Actions column */
  width: 20%;
}

td {
  font-size: 12px;
}
</style>
