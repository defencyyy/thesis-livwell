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
              <select
                v-model="salesPeriod"
                @change="calculateSalesStatistics"
                class="sales-dropdown"
              >
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
        <div style="max-width: 1100px; width: 100%">
          <div
            class="card border-0 rounded-1 mx-auto"
            style="box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
          >
            <div class="card-body">
              <div class="row">
                <div class="toolbar">
                  <div class="left-section">
                    <div class="search-bar-container">
                      <input
                        type="text"
                        v-model="searchQuery"
                        @input="filterSales"
                        placeholder="Search Customer/Broker/Unit/Site "
                        class="search-bar"
                      />
                      <i class="fa fa-search search-icon"></i>
                    </div>

                    <select
                      v-model="selectedStatus"
                      @change="filterSales"
                      class="dropdown"
                    >
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
        </div>

        <div class="outside-headers">
          <span class="header-item">Customer Name</span>
          <span class="header-item">Broker Name</span>
          <span class="header-item">Site Name</span>
          <span class="header-item">Unit #</span>
          <span class="header-item">Status</span>
          <span class="header-item">Action</span>
        </div>

        <div v-if="filteredSales.length > 0">
          <div
            v-for="sale in paginatedSales"
            :key="sale.id"
            class="card border-0 rounded-1 mx-auto"
            style="
              max-width: 1100px;
              box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
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
                      <button
                        @click="openSalesDetailModal(sale)"
                        class="btn-manage"
                      >
                        Manage
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <!-- Pagination Controls -->
          <nav aria-label="Page navigation example">
            <ul class="pagination">
              <li :class="['page-item', { disabled: currentPage === 1 }]">
                <a
                  class="page-link"
                  href="#"
                  @click.prevent="goToPage(currentPage - 1)"
                  aria-label="Previous"
                >
                  <span aria-hidden="true">&laquo;</span>
                </a>
              </li>
              <li
                v-for="page in totalPages"
                :key="page"
                :class="['page-item', { active: page === currentPage }]"
              >
                <a class="page-link" href="#" @click.prevent="goToPage(page)">
                  {{ page }}
                </a>
              </li>
              <li
                :class="['page-item', { disabled: currentPage === totalPages }]"
              >
                <a
                  class="page-link"
                  href="#"
                  @click.prevent="goToPage(currentPage + 1)"
                  aria-label="Next"
                >
                  <span aria-hidden="true">&raquo;</span>
                </a>
              </li>
            </ul>
          </nav>
        </div>
        <p v-else>No sales match the selected criteria.</p>

        <b-modal
          v-model="showModal"
          title="Manage Sale"
          hide-header
          hide-footer
          centered
        >
          <div class="p-3" v-if="selectedSale && selectedSale.customer">
            <div class="modal-title">
              <h5 class="mb-4">
                Customer: {{ selectedSale.customer.first_name.toUpperCase() }}
                {{ selectedSale.customer.last_name.toUpperCase() }}
              </h5>
            </div>
            <div class="customer-sales-info" style="margin-bottom: 30px">
              <p><strong>Unit:</strong> {{ selectedSale.unit.unit_title }}</p>
              <p>
                <strong>Site:</strong> {{ selectedSale.site.name || "N/A" }}
              </p>
              <p>
                <strong>Reservation Fee:</strong>
                {{ formatCurrency(selectedSale.reservation_fee) }}
              </p>
              <p>
                <strong>Payment Method:</strong>
                {{ selectedSale.payment_method }}
              </p>
              <p v-if="selectedSale.reservation_file">
                <strong>Reservation File: </strong>
                <a
                  :href="getFileUrl(selectedSale.reservation_file)"
                  target="_blank"
                  >View File</a
                >
              </p>
            </div>

            <div class="update-status mb-3">
              <label for="status" class="form-label"
                ><strong> Status:</strong></label
              >
              <select
                v-model="selectedSale.status"
                id="status"
                class="form-select"
              >
                <option value="Pending Reservation">Pending Reservation</option>
                <option value="Reserved">Reserved</option>
                <option value="Pending Sold">Pending Sold</option>
                <option value="Sold">Sold</option>
              </select>
            </div>

            <div
              class="d-flex justify-content-end gap-2 mt-3"
              style="padding-top: 15px"
            >
              <button @click="showConfirmationModal" class="btn btn-primary">
                Save Changes
              </button>

              <button
                type="button"
                @click="showModal = false"
                class="btn btn-secondary"
              >
                Close
              </button>
            </div>
          </div>
        </b-modal>
        <b-modal
          v-model="showNotification"
          :title="notificationTitle"
          hide-footer
          centered
        >
          <p>{{ notificationMessage }}</p>
          <div class="button-container">
            <button
              type="button"
              @click="showNotification = false"
              class="btn-cancel-right"
            >
              Close
            </button>
          </div>
        </b-modal>
        <b-modal
          v-model="showConfirmModal"
          :title="'Confirmation'"
          hide-footer
          centered
        >
          <p>{{ confirmMessage }}</p>
          <div
            class="d-flex justify-content-end gap-2 mt-30"
            style="padding-top: 15px"
          >
            <button
              type="button"
              @click="confirmAction"
              class="btn btn-primary"
            >
              Confirm
            </button>
            <!-- Cancel Button -->
            <button
              type="button"
              @click="cancelAction"
              class="btn btn-secondary"
            >
              Cancel
            </button>
          </div>
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { BModal } from "bootstrap-vue-3";
import axios from "axios";
import { mapState } from "vuex";
import SalesChart from "@/components/DevSalesChart.vue";

export default {
  name: "DevSales",
  components: {
    SideNav,
    AppHeader,
    SalesChart,
    BModal,
  },
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

      showNotification: false,
      notificationTitle: "",
      notificationMessage: "",
      showConfirmModal: false, // Controls modal visibility
      confirmMessage: "", // Stores the confirmation message
      actionToConfirm: null, // Renamed this from 'confirmAction'
      confirmParams: [],
      currentPage: 1,
      itemsPerPage: 10,
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId,
      companyId: (state) => state.companyId,
      loggedIn: (state) => state.loggedIn,
    }),
    paginatedSales() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredSales.slice(
        startIndex,
        startIndex + this.itemsPerPage
      );
    },

    totalPages() {
      return Math.ceil(this.filteredSales.length / this.itemsPerPage);
    },
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
    goToPage(pageNumber) {
      if (pageNumber > 0 && pageNumber <= this.totalPages) {
        this.currentPage = pageNumber;
      }
    },
    // Fetch sales data
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
        this.calculateSalesStatistics();
        this.extractEntities();
      } catch (error) {
        console.error("Error fetching sales data:", error);
      }
    },

    // Fetch units data
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
        this.totalUnits = units.length;
        this.availableUnits = units.filter(
          (unit) => unit.status === "Available"
        ).length;
      } catch (error) {
        console.error("Error fetching units data:", error);
      }
    },

    // Calculate sales statistics
    calculateSalesStatistics() {
      const currentDate = new Date();
      let filteredSales = this.sales;

      if (this.salesPeriod === "monthly") {
        filteredSales = this.sales.filter((sale) => {
          if (!sale.date_sold) return false;
          const saleDate = new Date(sale.date_sold);
          return (
            saleDate.getMonth() === currentDate.getMonth() &&
            saleDate.getFullYear() === currentDate.getFullYear()
          );
        });
      } else if (this.salesPeriod === "yearly") {
        filteredSales = this.sales.filter((sale) => {
          if (!sale.date_sold) return false;
          const saleDate = new Date(sale.date_sold);
          return saleDate.getFullYear() === currentDate.getFullYear();
        });
      }

      this.displayedSales = filteredSales.length;
      this.ongoingSales = this.sales.filter(
        (sale) => sale.status !== "Sold"
      ).length;
      this.soldUnits = this.sales.filter(
        (sale) => sale.status === "Sold"
      ).length;
    },

    // Extract unique brokers, customers, and sites
    extractEntities() {
      this.brokers = [...new Set(this.sales.map((sale) => sale.broker))];
      this.customers = [...new Set(this.sales.map((sale) => sale.customer))];
      this.sites = [...new Set(this.sales.map((sale) => sale.site))];
    },

    // Filter sales based on selected criteria
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

      if (this.selectedStatus) {
        filtered = filtered.filter(
          (sale) => sale.status === this.selectedStatus
        );
      }

      this.filteredSales = filtered;
    },

    // Show confirmation modal
    showConfirmationModal() {
      this.confirmMessage = `Are you sure you want to update the status to ${this.selectedSale.status}?`;
      this.showConfirmModal = true;
    },

    // Handle the confirmation action
    async confirmAction() {
      try {
        await this.confirmSaleAction(this.selectedSale.id);
        this.showConfirmModal = false;
      } catch (error) {
        this.showConfirmModal = false;
        this.notificationTitle = "Error";
        this.notificationMessage = "An error occurred during the action.";
        this.showNotification = true;
      }
    },

    // Cancel the action and close the confirmation modal
    cancelAction() {
      this.showConfirmModal = false;
    },

    // Confirm the sale action (e.g., updating the sale status)
    async confirmSaleAction(saleId) {
      try {
        const response = await axios.put(
          `http://localhost:8000/developer/sales/${saleId}/`,
          { status: this.selectedSale.status },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        if (response.status === 200) {
          this.notificationTitle = "Success";
          this.notificationMessage = "Sale status updated successfully!";
          this.showNotification = true;
          this.fetchSales();
          this.closeModal();
        } else {
          this.notificationTitle = "Error";
          this.notificationMessage =
            "An error occurred while updating sale status.";
          this.showNotification = true;
        }
      } catch (error) {
        console.error("Error updating sale status:", error);
        this.notificationTitle = "Error";
        this.notificationMessage = "An error occurred during the action.";
        this.showNotification = true;
      }
    },

    // Open sales detail modal
    openSalesDetailModal(sale) {
      this.selectedSale = { ...sale };
      this.showModal = true;
    },

    // Close the modal
    closeModal() {
      this.showModal = false;
      this.selectedSale = null;
    },

    // Generate file URL
    getFileUrl(filePath) {
      // Check if the file path contains '/media/' and adjust the path
      if (filePath.startsWith("/media/")) {
        // Replace '/media/' with '/media/reservations/' to match the correct folder
        return `http://localhost:8000/media/reservations${filePath.slice(6)}`;
      }
      // If the path doesn't start with '/media/', just return the original URL
      return `http://localhost:8000${filePath}`;
    },
    // Redirect to login page
    redirectToLogin() {
      this.$router.push({ name: "DevLogin" });
    },

    // Get the CSS class for the sale status
    getStatusClass(status) {
      return {
        "status-pending-reservation": status === "Pending Reservation",
        "status-reserved": status === "Reserved",
        "status-pending-sold": status === "Pending Sold",
        "status-sold": status === "Sold",
      };
    },

    // Format currency value
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
  display: flex;
  /* Use flexbox to center the content */
  align-items: center;
  /* Center vertically */
  flex-direction: column;
  /* Stack the dashboard boxes and sales table vertically */
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
  font-weight: bold;
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

.dashboard-container h2 {
  font-size: 30px;
  font-weight: bold;
  margin-top: 50px;
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
  flex: 1; /* Distribute space equally */
}

.right-dashboard {
  display: flex;
  flex-direction: column;
  flex: 1; /* Distribute space equally */
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

.card-body {
  font-size: 14px; /* Set a smaller default font size for the card body */
}

.btn-manage {
  background-color: #0560fd;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
  font-size: 12px;

}

.outside-headers {
  display: grid;
  grid-template-columns: 20% 20% 18% 14% 18% 10%;
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
  width: 18%;
}

.sale-table th:nth-child(4),
.sale-table td:nth-child(4) {
  /* Actions column */
  width: 14%;
}

.sale-table th:nth-child(5),
.sale-table td:nth-child(5) {
  /* Actions column */
  width: 18%;
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
  justify-content: space-between;
}

.button-container {
  display: flex;
  justify-content: flex-end;
}

.btn-cancel-right {
  background-color: #0560fd;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 12px 20px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn-cancel-right:hover {
  background-color: #004bb5;
}

.btn-cancel-right:focus {
  outline: none;
}
.pagination {
  display: flex;
  justify-content: flex-end;
  max-width: 1100px;
  width: 100%;
  /* Reduce padding */
  font-size: 12px;
  /* Smaller font size */
  line-height: 1;
  margin: 0 40px;

  /* Adjust line height for compactness */
}

.page-item {
  margin: 0 3px;
  /* Reduce spacing between buttons */
}

/* Ensure the arrow button container has a white background */
.pagination .page-item .page-link {
  background-color: white; /* White background for the arrow container */
  color: #6c757d; /* Default color for inactive arrows */
  border: 1px solid #ddd; /* Optional: Add border if you want the arrow container to have a border */
  padding: 8px 12px;
  font-size: 11px;
}

/* Active page color */
.pagination .page-item.active .page-link {
  background-color: #007bff; /* Blue background for active page */
  color: white; /* White text for active page */
}
</style>
