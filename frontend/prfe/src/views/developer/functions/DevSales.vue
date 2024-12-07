<template>
  <div class="developer-sales-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">Sales Management</div>
          </div>
        </div>
        <div class="sales-dashboard-container">
          <div class="box">
            <div class="box-header">
              <div class="icon-container">
                <i class="fa fa-chart-line" style="font-size: 13px"></i>
              </div>
              <p>Sales</p>
              <select v-model="salesPeriod" @change="calculateSalesStatistics" class="sales-dropdown">
                <option value="monthly">Monthly</option>
                <option value="yearly">Yearly</option>
                <option value="all">All-Time</option>
              </select>
            </div>
            <h2>{{ displayedSales }}</h2>
          </div>
          <div class="box">
            <div class="box-header">
              <div class="icon-container">
                <i class="fa fa-shopping-cart" style="font-size: 13px"></i>
              </div>
              <p>Sold Units</p>
            </div>
            <h2>{{ soldUnits }}</h2>
          </div>
          <div class="box">
            <div class="box-header">
              <div class="icon-container">
                <i class="fa fa-spinner" style="font-size: 13px"></i>
              </div>
              <p>Ongoing Sales</p>
            </div>
            <h2>{{ ongoingSales }}</h2>
          </div>
        </div>
        <div class="dashboard-container">
          <div class="left-dashboard">
            <div class="unit-box">
              <div class="box-header">
                <div class="icon-container">
                  <i class="fa fa-home" style="font-size: 13px"></i>
                </div>
                <p>Total Units</p>
              </div>
              <h2>{{ totalUnits }}</h2>
            </div>
            <div class="unit-box">
              <div class="box-header">
                <div class="icon-container">
                  <i class="fa fa-home" style="font-size: 13px"></i>
                </div>
                <p>Available Units</p>
              </div>
              <h2>{{ availableUnits }}</h2>
            </div>
          </div>
          <div class="right-dashboard">
            
            <SalesChart v-if="sales.length" :salesData="sales" />
          </div>
        </div>

        <div class="card border-0 rounded-1 mx-auto" style="box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)">
          <div class="card-body">
            <div class="row">
              <div class="toolbar">
                <div class="left-section">
                  <div class="search-bar-container">
                    <input type="text" v-model="searchQuery" @input="filterSales"
                      placeholder="Search Customer/Broker/Unit/Site " class="search-bar" />
                    <i class="fa fa-search search-icon"></i>
                  </div>
                  <select v-model="selectedBroker" @change="filterSales" class="dropdown">
                    <option value="">All Brokers</option>
                    <option v-for="broker in brokers" :key="broker.id" :value="broker.id">
                      {{ broker.first_name }} {{ broker.last_name }}
                    </option>
                  </select>
                  <select v-model="selectedStatus" @change="filterSales" class="dropdown">
                    <option value="">All Status</option>
                    <option value="Pending Reservation">
                      Pending Reservation
                    </option>
                    <option value="Reserved">Reserved</option>
                    <option value="Pending Sold">Pending Sold</option>
                    <option value="Sold">Sold</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Search and Filter Controls -->
        <!-- <div class="search-filter-controls">
          <input
            type="text"
            v-model="searchQuery"
            @input="filterSales"
            placeholder="Search by Customer Name or Broker Name"
            class="search-input"
          />
          <select
            v-model="selectedBroker"
            @change="filterSales"
            class="filter-dropdown"
          >
            <option value="">Select Broker</option>
            <option
              v-for="broker in brokers"
              :key="broker.id"
              :value="broker.id"
            >
              {{ broker.first_name }} {{ broker.last_name }}
            </option>
          </select>
          <select
            v-model="selectedCustomer"
            @change="filterSales"
            class="filter-dropdown"
          >
            <option value="">Select Customer</option>
            <option
              v-for="customer in customers"
              :key="customer.id"
              :value="customer.id"
            >
              {{ customer.first_name }} {{ customer.last_name }}
            </option>
          </select>
          <select
            v-model="selectedSite"
            @change="filterSales"
            class="filter-dropdown"
          >
            <option value="">Select Site</option>
            <option v-for="site in sites" :key="site.id" :value="site.id">
              {{ site.name }}
            </option>
          </select>
          <select
            v-model="selectedStatus"
            @change="filterSales"
            class="filter-dropdown"
          >
            <option value="">All Statuses</option>
            <option value="Pending Reservation">Pending Reservation</option>
            <option value="Reserved">Reserved</option>
            <option value="Pending Sold">Pending Sold</option>
            <option value="Sold">Sold</option>
          </select>
          <button @click="filterSales" class="search-button">Search</button>
        </div> -->

        <div class="outside-headers">
          <span class="header-item">Customer Name</span>
          <span class="header-item">Broker Name</span>
          <span class="header-item">Site Name</span>
          <span class="header-item">Unit #</span>
          <span class="header-item">Status</span>
          <span class="header-item">Action</span>
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
                    <td>
                      {{ sale.customer.first_name }}
                      {{ sale.customer.last_name }}
                    </td>
                    <td>
                      {{ sale.broker.first_name }} {{ sale.broker.last_name }}
                    </td>
                    <td>{{ sale.site.name || "N/A" }}</td>
                    <td>{{ sale.unit.unit_title }}</td>
                    <td :class="getStatusClass(sale.status)">
                      {{ sale.status }}
                    </td>
                    <td>
                      <button @click="openSalesDetailModal(sale)" class="btn btn-primary">
                        Manage
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <p v-else>No sales match the selected criteria.</p>

        <!-- Sales Detail Modal -->
        <div v-if="showModal" class="modal">
          <div class="modal-content">
            <h2>Manage Sale</h2>
            <p>
              <strong>Customer:</strong> {{ selectedSale.customer.first_name }}
              {{ selectedSale.customer.last_name }}
            </p>
            <p><strong>Unit:</strong> {{ selectedSale.unit.unit_title }}</p>
            <p><strong>Site:</strong> {{ selectedSale.site.name || "N/A" }}</p>
            <p>
              <strong>Reservation Fee:</strong>
              {{ formatCurrency(selectedSale.reservation_fee) }}
            </p>
            <p>
              <strong>Payment Method:</strong> {{ selectedSale.payment_method }}
            </p>
            <p v-if="selectedSale.reservation_file">
              <strong>Reservation File:</strong>
              <a :href="getFileUrl(selectedSale.reservation_file)" target="_blank">View File</a>
            </p>
            <!-- Update Status -->
            <div class="update-status">
              <label for="status">Update Status:</label>
              <select v-model="selectedSale.status" id="status" class="filter-dropdown">
                <option value="Pending Reservation">Pending Reservation</option>
                <option value="Reserved">Reserved</option>
                <option value="Pending Sold">Pending Sold</option>
                <option value="Sold">Sold</option>
              </select>
            </div>
            <div class="modal-buttons">
              <button @click="confirmUpdate" class="btn btn-primary">
                Save Changes
              </button>
              <button @click="closeModal" class="btn btn-secondary">
                Close
              </button>
            </div>
          </div>
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
import SalesChart from "@/components/DevSalesChart.vue";

export default {
  name: "DevSales",
  components: { SideNav, AppHeader, SalesChart },
  data() {
    return {
      sales: [],
      filteredSales: [],
      showModal: false,
      selectedSale: null,
      searchQuery: "",
      selectedBroker: "",
      selectedCustomer: "",
      selectedSite: "",
      selectedStatus: "",
      brokers: [],
      customers: [],
      sites: [],
      statuses: ["Pending Reservation", "Reserved", "Pending Sold", "Sold"],
      salesPeriod: "monthly",
      displayedSales: 0,
      ongoingSales: 0,
      totalUnits: 0,
      availableUnits: 0,
      soldUnits: 0,
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId,
      companyId: (state) => state.companyId,
      loggedIn: (state) => state.loggedIn,
    }),
  },
  mounted() {
    if (!this.loggedIn || !this.companyId) {
      this.redirectToLogin();
    } else {
      this.fetchSales();
      this.fetchUnits();
    }
  },
  methods: {
    async fetchSales() {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/sales/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.sales = response.data.data || [];
        this.filteredSales = this.sales;

        // Calculate initial statistics
        this.calculateSalesStatistics();
        this.extractEntities();
      } catch (error) {
        console.error("Error fetching sales data:", error);
      }
    },
    async fetchUnits() {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/units/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        const units = response.data.data || [];
        this.availableUnits = units.filter(
          (unit) => unit.status === "Available"
        ).length;
      } catch (error) {
        console.error("Error fetching units data:", error);
      }
    },
    calculateSalesStatistics() {
      const currentDate = new Date();
      let filteredSales = this.sales;

      if (this.salesPeriod === "monthly") {
        filteredSales = this.sales.filter((sale) => {
          if (!sale.date_sold) return false; // Skip if `date_sold` is missing
          const saleDate = new Date(sale.date_sold);
          return (
            saleDate.getMonth() === currentDate.getMonth() &&
            saleDate.getFullYear() === currentDate.getFullYear()
          );
        });
      } else if (this.salesPeriod === "yearly") {
        filteredSales = this.sales.filter((sale) => {
          if (!sale.date_sold) return false; // Skip if `date_sold` is missing
          const saleDate = new Date(sale.date_sold);
          return saleDate.getFullYear() === currentDate.getFullYear();
        });
      }

      this.displayedSales = filteredSales.length;

      // Recalculate ongoing sales, total units, and sold units
      this.ongoingSales = this.sales.filter(
        (sale) => sale.status !== "Sold"
      ).length;
      this.totalUnits = this.sales.length;
      this.soldUnits = this.sales.filter(
        (sale) => sale.status === "Sold"
      ).length;
    },
    extractEntities() {
      this.brokers = [...new Set(this.sales.map((sale) => sale.broker))];
      this.customers = [...new Set(this.sales.map((sale) => sale.customer))];
      this.sites = [...new Set(this.sales.map((sale) => sale.site))];
    },
    filterSales() {
      let filtered = this.sales;

      if (this.selectedBroker) {
        filtered = filtered.filter(
          (sale) => sale.broker.id === this.selectedBroker
        );
      }

      if (this.selectedCustomer) {
        filtered = filtered.filter(
          (sale) => sale.customer.id === this.selectedCustomer
        );
      }

      if (this.selectedSite) {
        filtered = filtered.filter(
          (sale) => sale.site.id === this.selectedSite
        );
      }

      // Apply search filtering
      if (this.searchQuery) {
        filtered = filtered.filter(
          (sale) =>
            `${sale.customer.first_name} ${sale.customer.last_name}`
              .toLowerCase()
              .includes(this.searchQuery.toLowerCase()) ||
            `${sale.broker.first_name} ${sale.broker.last_name}`
              .toLowerCase()
              .includes(this.searchQuery.toLowerCase())
        );
      }

      // Filter by status
      if (this.selectedStatus) {
        filtered = filtered.filter(
          (sale) => sale.status === this.selectedStatus
        );
      }

      this.filteredSales = filtered;
    },
    async updateSaleStatus() {
      try {
        console.log("Sending PUT request with data:", {
          status: this.selectedSale.status,
        });

        const response = await axios.put(
          `http://localhost:8000/developer/sales/${this.selectedSale.id}/`,
          { status: this.selectedSale.status },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        console.log("Response from API:", response.data);

        if (response.status === 200) {
          alert("Sale status updated successfully!");
          this.fetchSales(); // Refresh data
          this.closeModal();
        } else {
          alert("Error updating sale status.");
        }
      } catch (error) {
        console.error("Error updating sale status:", error);
        alert("Failed to update sale status.");
      }
    },
    openSalesDetailModal(sale) {
      console.log("Opening modal for sale:", sale);
      this.selectedSale = { ...sale }; // Create a copy to avoid direct binding
      this.showModal = true;
      console.log("Modal state:", this.showModal);
    },
    closeModal() {
      this.showModal = false;
      this.selectedSale = null;
    },
    getFileUrl(filePath) {
      return `http://localhost:8000${filePath}`;
    },
    redirectToLogin() {
      this.$router.push({ name: "DevLogin" });
    },
    getStatusClass(status) {
      return {
        "status-pending-reservation": status === "Pending Reservation",
        "status-reserved": status === "Reserved",
        "status-pending-sold": status === "Pending Sold",
        "status-sold": status === "Sold",
      };
    },
    confirmUpdate() {
      if (
        confirm(
          `Are you sure you want to update the status to ${this.selectedSale.status}?`
        )
      ) {
        this.updateSaleStatus();
      }
    },
    formatCurrency(amount) {
      return new Intl.NumberFormat().format(amount);
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
.developer-sales-page {
  display: flex;
  min-height: 100vh;
  /* Ensures it spans the full viewport height */
  background-color: #e8f0fa;
  /* Gray background */
}

.SideNav {
  width: 100%;
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

.title-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  /* Push items to opposite sides */
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
  width: 400px;
  padding: 8px 12px 8px 40px;
  /* Add left padding to make space for the icon */
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 14px;
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
  border-radius: 3px;
  font-size: 14px;
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

.sales-dashboard-container {
  display: grid;
  /* Use grid for responsive layout */
  grid-template-columns: 1fr 1fr 1fr;
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
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex-grow: 1; /* Allow boxes to grow in height if needed */
}

.unit-box {
  position: relative;
  /* Make the box a positioning context */
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex-grow: 1; /* Allow boxes to grow in height if needed */
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

.dashboard-container {
  margin-left: 63px;
  margin-bottom: 30px;
  display: grid;
  grid-template-columns: 1fr 3fr;
  /* Equal width for both columns */
  gap: 20px;
  /* Match the spacing of the dashboard boxes */
  width: 100%;
  max-width: 1100px;
  /* Match the max-width of the dashboard-boxes */
}

.left-dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.right-dashboard {
  display: flex;
  flex-direction: column;
}

.card {
  background-color: #fff;
  margin-bottom: 10px;
  margin-top: 0;
  max-width: 1100px;
  /* Ensures the card and grid align */
  margin-left: auto;
  /* Centers the card */
  margin-right: auto;
}

.outside-headers {
  display: grid;
  grid-template-columns: 20% 20% 20% 15% 15% 10%;
  /* Adjust widths for better layout */
  max-width: 1100px;
  width: 100%;
  padding: 0 15px;
  margin: 12px auto 10px;
}

.header-item {
  text-align: left;
  font-size: 14px;
  color: #333;
  font-weight: bold;
}

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

.sale-table th:nth-child(2),
.sale-table td:nth-child(2) {
  /* Location column */
  width: 20%;
}

.sale-table th:nth-child(3),
.sale-table td:nth-child(3) {
  /* Status column */
  width: 20%;
}

.sale-table th:nth-child(4),
.sale-table td:nth-child(4) {
  /* Actions column */
  width: 15%;
}

.sale-table th:nth-child(5),
.sale-table td:nth-child(5) {
  /* Actions column */
  width: 15%;
}

.sale-table th:nth-child(6),
.sale-table td:nth-child(6) {
  /* Actions column */
  width: 10%;
}


.sales-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.sales-table th,
.sales-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.sales-table th {
  background-color: #f8f9fa;
  font-weight: bold;
}

.sales-table td {
  background-color: #ffffff;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  /* Ensure it appears above other elements */
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-content h2 {
  margin-bottom: 20px;
}

.modal-content p {
  margin-bottom: 10px;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.status-pending-reservation {
  color: #ffc107;
}

.status-reserved {
  color: #007bff;
}

.status-pending-sold {
  color: #fd7e14;
}

.status-sold {
  color: #28a745;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.grid-item {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.sales-dropdown {
  font-size: 12px;
  padding: 1px;
  border-radius: 4px;
  border: 1px solid #ddd;
  justify-content: space-between
}
</style>
