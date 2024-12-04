<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <!-- Dashboard Boxes -->
        <div class="dashboard-boxes">
          <div class="box">
            <p>Brokers</p>
            <h2>{{ brokerCount }}</h2>
          </div>
          <div class="box">
            <p>Sites</p>
            <h2>{{ siteCount }}</h2>
          </div>
          <div class="box">
            <p>Available Units</p>
            <h2>{{ availableUnits }}</h2>
          </div>
          <div class="box">
            <p>Sold Sales</p>
            <h2>{{ salesCount }}</h2>
          </div>
          <div class="box">
            <p>Ongoing Sales</p>
            <h2>{{ ongoingSales }}</h2>
          </div>
        </div>

        <!-- Sales Table with Search and Filter -->
        <div class="sales-table">
          <h3>Pending Sales</h3>

          <!-- Search and Filter -->
          <div class="search-filter-controls">
            <input
              type="text"
              v-model="searchQuery"
              @input="filterSales"
              placeholder="Search by Names or Site"
              class="search-input"
            />
            <select
              v-model="selectedStatus"
              @change="filterSales"
              class="filter-dropdown"
            >
              <option value="">All Pending Status</option>
              <option value="Pending Reservation">Pending Reservation</option>
              <option value="Pending Sold">Pending Sold</option>
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
        </div>
      </div>
    </div>
  </div>
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
      } catch (error) {
        console.error("Error fetching sites:", error);
      }
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
        console.log("Pending sales:", this.pendingSales);
        this.filteredSales = this.pendingSales;
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
              .includes(this.searchQuery.toLowerCase()) ||
            (sale.site &&
              sale.site.name
                .toLowerCase()
                .includes(this.searchQuery.toLowerCase()))
        );
      }

      if (this.selectedStatus) {
        filtered = filtered.filter(
          (sale) => sale.status === this.selectedStatus
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
  margin: 0; /* Removes default margin */
  padding: 0; /* Removes default padding */
}

/* Ensure .main-page fills the available space */
.main-page {
  display: flex;
  min-height: 100vh; /* Ensures it spans the full viewport height */
  background-color: #ebebeb; /* Gray background */
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
  color: #ffffff;
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

.dashboard-boxes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 20px 0;
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

.sales-table {
  margin: 20px 0;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.sales-table table {
  width: 100%;
  border-collapse: collapse;
}

.sales-table th,
.sales-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.sales-table th {
  background: #f6f6f6;
  font-weight: bold;
}

.sales-table td {
  background: #fff;
}
</style>
