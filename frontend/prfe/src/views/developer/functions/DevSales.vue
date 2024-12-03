<template>
  <div class="developer-sales-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <h1>Manage Sales</h1>
        <p>
          View and manage sales details for your company. Lagay siguro to sa
          header?
        </p>

        <!-- Grid displaying summary info -->
        <div class="info-grid">
          <div class="grid-item">
            <strong>Sales:</strong>
            <select
              v-model="salesPeriod"
              @change="calculateSalesStatistics"
              class="sales-dropdown"
            >
              <option value="monthly">Monthly</option>
              <option value="yearly">Yearly</option>
              <option value="all">All-Time</option>
            </select>
            {{ displayedSales }}
          </div>

          <div class="grid-item">
            <strong>Ongoing Sales:</strong> {{ ongoingSales }}
          </div>
          <div class="grid-item">
            <strong>Total Units:</strong> {{ totalUnits }}
          </div>
          <div class="grid-item">
            <strong>Available Units:</strong> {{ availableUnits }}
          </div>
          <div class="grid-item">
            <strong>Sold Units:</strong> {{ soldUnits }}
          </div>
        </div>

        <SalesChart v-if="sales.length" :salesData="sales" />

        <!-- Search and Filter Controls -->
        <div class="search-filter-controls">
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
        </div>

        <!-- Sales Table -->
        <table v-if="filteredSales.length" class="sales-table">
          <thead>
            <tr>
              <th>Customer Name</th>
              <th>Broker Name</th>
              <th>Unit Title</th>
              <th>Site Name</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sale in filteredSales" :key="sale.id">
              <td>
                {{ sale.customer.first_name }} {{ sale.customer.last_name }}
              </td>
              <td>{{ sale.broker.first_name }} {{ sale.broker.last_name }}</td>
              <td>{{ sale.unit.unit_title }}</td>
              <td>{{ sale.site.name || "N/A" }}</td>
              <td :class="getStatusClass(sale.status)">{{ sale.status }}</td>
              <td>
                <button
                  @click="openSalesDetailModal(sale)"
                  class="btn btn-primary"
                >
                  Manage Sale
                </button>
              </td>
            </tr>
          </tbody>
        </table>
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
              <a
                :href="getFileUrl(selectedSale.reservation_file)"
                target="_blank"
                >View File</a
              >
            </p>
            <!-- Update Status -->
            <div class="update-status">
              <label for="status">Update Status:</label>
              <select
                v-model="selectedSale.status"
                id="status"
                class="filter-dropdown"
              >
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
  background-color: #ebebeb; /* Gray background */
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

.search-filter-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-input {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.filter-dropdown {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.search-button {
  padding: 8px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
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
  z-index: 1000; /* Ensure it appears above other elements */
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
  padding: 4px;
  margin-left: 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
}
</style>
