<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">Customer Details</div>
          </div>
          <!-- Header Section -->
          <div class="total-customers">
            <div>Total Customers: {{ filteredCustomers.length }}</div>
          </div>
        </div>

        <div class="card border-0 rounded-1 mx-auto"
          style="max-width: 1100px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)">
          <div class="card-body">
            <!-- Toolbar -->
            <div class="toolbar">
              <div class="left-section">
                <div class="search-bar-container">
                  <input type="text" v-model="searchQuery" placeholder="Search Customers" class="search-bar" />
                  <i class="fa fa-search search-icon"></i>
                </div>
              </div>
              <div class="right-section"></div>
            </div>
          </div>
        </div>

        <div>
          <!-- Headers outside the card -->
          <div class="outside-headers">
            <span class="header-item">Name</span>
            <span class="header-item">Email</span>
            <span class="header-item">Contact</span>
            <span class="header-item">Broker Name</span>
            <!-- <span class="header-item">Units Connected</span> -->
            <span class="header-item">Actions</span>
          </div>

          <!-- Conditional Rendering -->
          <div v-if="currentCustomers.length === 0" class="no-customers-message">
            No customers found.
          </div>

          <div v-else v-for="(customer, index) in currentCustomers" :key="customer.id || index"
            class="card border-0 rounded-1 mx-auto my-2" style="
              max-width: 1100px;
              box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            ">
            <div class="card-body">
              <table class="customer-table">
                <tbody>
                  <tr>
                    <td>
                      <span class="customer-name">
                        {{ customer.first_name + " " + customer.last_name }}
                      </span>
                    </td>

                    <td>
                      <span class="customer-email">
                        {{ customer.email }}
                      </span>
                    </td>
                    <td>
                      <span class="customer-number">
                        {{ customer.contact_number }}
                      </span>
                    </td>
                    <!-- <td>
                      <span class="customer-units">
                        {{
                          customer.broker_sales
                            ? customer.broker_sales.reduce(
                                (count, sale) =>
                                  sale.site && sale.unit ? count + 1 : count,
                                0
                              )
                            : 0
                        }}
                      </span>
                    </td> -->
                    <td>
                      <span class="customer-broker">
                        {{
                          customer.broker
                            ? customer.broker.first_name +
                            " " +
                            customer.broker.last_name
                            : "N/A"
                        }}
                      </span>
                    </td>
                    <td>
                      <div class="broker-actions d-flex gap-2">
                        <button @click="viewCustomer(customer)" style="
                            border: none;
                            background-color: transparent;
                            color: #343a40;
                            cursor: pointer;
                            font-size: 18px;
                          ">
                          <i class="fas fa-eye"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <!-- Pagination -->
          <div class="pagination-controls">
            <button :disabled="currentPage === 1" @click="prevPage" class="page-button">
              Previous
            </button>
            <button v-for="page in totalPages" :key="page" @click="changePage(page)"
              :class="['page-button', { active: currentPage === page }]">
              {{ page }}
            </button>
            <button :disabled="currentPage === totalPages" @click="nextPage" class="page-button">
              Next
            </button>
          </div>
        </div>
      </div>
    </div>


    <!-- View Customer Modal -->
    <b-modal v-model="showEditModal" title="Customer Details" hide-footer hide-header centered size="lg">

      <div class="modal-title p-3">
        <h5 class="mb-0">Customer: {{ (currentCustomer.first_name || '').toUpperCase() }} {{ (currentCustomer.last_name
          || '').toUpperCase() }}</h5>
        <h5><em>Connected Units: {{ connectedUnitsCount }} </em> </h5>
      </div>

      <!-- <div class="form-group">
        <label for="editFullName" style="font-weight: bold">Full Name: </label>
        <span id="editFullName">
          {{ currentCustomer.first_name }} {{ currentCustomer.last_name }}
        </span>
      </div> -->

      <div class="modal-body">
        <!-- Broker Info -->

        <div>
          <p style="margin-bottom: 5px;">
            <strong>Email: </strong>
            {{ currentCustomer.email }}
          </p>
          <p style="margin-bottom: 5px;">
            <strong>Contact #: </strong>
            {{ currentCustomer.contact_number }}
          </p>
        </div>

        <!-- <div class="form-group">
        <label for="editEmail" style="font-weight: bold">Email: </label>
        <span id="editEmail">{{ currentCustomer.email }}</span>
      </div>
      <div class="form-group">
        <label for="editContact" style="font-weight: bold">Contact: </label>
        <span id="editContact">{{ currentCustomer.contact_number }}</span>
      </div> -->

        <!-- Spacer -->
        <!-- <div style="margin-top: 20px"></div> -->

        <!-- Submitted Documents -->
        <!-- <h5>Submitted Documents</h5>
        <div v-if="currentCustomer.documents && currentCustomer.documents.length">
          <ul>
            <li v-for="document in currentCustomer.documents" :key="document.url">
              <span class="document-type">{{ document.type }}:</span>

              <button @click="openDocumentModal(document)" class="btn btn-link">
                {{ document.name }}
              </button>

              <a :href="document.url" target="_blank" class="btn btn-sm btn-outline-success"
                aria-label="Open document in a new tab">
                Open in New Tab
              </a>

              <a :href="document.url" :download="document.name" class="btn btn-sm btn-outline-success" aria-label="Download
              document">
                Download
              </a>
            </li>
          </ul>
        </div>
        <div v-else>No documents available.</div> -->

        <b-modal v-model="showDocumentModal" title="View Document" hide-footer centered size="lg">
          <div v-if="selectedDocument">
            <iframe :src="selectedDocument.url" width="100%" height="500px" frameborder="0"></iframe>
          </div>
          <div v-else>
            <p>No document to display.</p>
          </div>
        </b-modal>

        <!-- Spacer -->
        <div style="margin-top: 20px"></div>

        <!-- Broker Info -->
        <h6 v-if="currentCustomer.broker" style="color: #a3a3a3;"><em>**Broker Information**</em></h6>
        <div v-if="currentCustomer.broker">
          <p style="margin-bottom: 5px;">
            <strong>Broker Name: </strong>
            {{ currentCustomer.broker.first_name }}
            {{ currentCustomer.broker.last_name }}
          </p>
          <!-- <label for="brokerFullName" style="font-weight: bold">Broker Name:
          </label>
          <span id="brokerFullName">
            {{ currentCustomer.broker.first_name }}
            {{ currentCustomer.broker.last_name }}
          </span> -->
        </div>
        <div v-if="currentCustomer.broker">
          <p style="margin-bottom: 5px;">
            <strong>Broker Email: </strong>
            {{ currentCustomer.broker.email }}
          </p>
          <!-- <label for="brokerEmail" style="font-weight: bold">Broker Email:
          </label>
          <span id="brokerEmail">{{ currentCustomer.broker.email }}</span> -->
        </div>
        <div v-if="currentCustomer.broker">
          <p style="margin-bottom: 5px;">
            <strong>Broker Contact #: </strong>
            {{
              currentCustomer.broker.contact_number
            }}
          </p>
          <!-- <label for="brokerContact" style="font-weight: bold">Broker Contact:
          </label>
          <span id="brokerContact">{{
            currentCustomer.broker.contact_number
            }}</span> -->
        </div>

        <!-- Spacer -->
        <div style="margin-top: 20px"></div>

        <!-- Units Connected -->
        <h6 style="color: #a3a3a3;"><em>**Connected Units**</em></h6>
        <!-- Display count -->
        <div v-if="Object.keys(groupedSales).length">
          <table class="styled-table">
            <thead>
              <tr>
                <th>Unit Name</th>
                <th>Unit Number</th>
                <th>Site</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(units, siteName) in groupedSales" :key="siteName">
      <tr v-for="unit in units" :key="unit.id">
        <td>{{ unit.title }}</td>
        <td>{{ unit.unit_number }}</td>
        <td>{{ siteName }}</td>
        <td>{{ unit.status }}</td>
      </tr>
    </template>
</tbody>
</table>
</div>
<div v-else>No connected units available.</div>
<div
              class="d-flex justify-content-end gap-3 mt-3"
              style="padding: 15px"
            >
              <button
                type="button"
                class="btn-cancel"
                @click="showEditModal = false"
                style="width: 100px"
              >
                Close
              </button>
            </div>
</div>
</b-modal>
</div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { BModal } from "bootstrap-vue-3";
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "DeveloperCustomers",
  components: {
    SideNav,
    AppHeader,
    BModal,
  },
  data() {
    return {
      customers: [],
      searchQuery: "",
      customersPerPage: 5,
      currentPage: 1,
      showEditModal: false,
      connectedUnitsCount: 0,
      newCustomer: {
        first_name: "",
        last_name: "",
        email: "",
        contact_number: "",
      },
      currentCustomer: {
        broker: {},
        broker_sales: [], // Ensure this exists
      },
      error: null,
      showDocumentModal: false,
      selectedDocument: {}, // Initialize as an empty object
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId,
      userType: (state) => state.userType,
      companyId: (state) => state.companyId,
      loggedIn: (state) => state.loggedIn,
    }),
    filteredCustomers() {
      return this.customers.filter(
        (customer) =>
          customer.first_name
            .toLowerCase()
            .includes(this.searchQuery.toLowerCase()) ||
          customer.last_name
            .toLowerCase()
            .includes(this.searchQuery.toLowerCase()) ||
          customer.email.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    totalPages() {
      return Math.ceil(this.filteredCustomers.length / this.customersPerPage);
    },
    currentCustomers() {
      const start = (this.currentPage - 1) * this.customersPerPage;
      const end = start + this.customersPerPage;
      return this.filteredCustomers.slice(start, end);
    },

    groupedSales() {
      if (!this.currentCustomer.broker_sales) {
        return {};
      }
      return this.currentCustomer.broker_sales.reduce((acc, sale) => {
        if (sale.site && sale.unit) {
          acc[sale.site.name] = [...(acc[sale.site.name] || []), sale.unit];
        }
        return acc;
      }, {});
    },
  },
  mounted() {
    if (!this.loggedIn || this.userType !== "developer" || !this.companyId) {
      this.redirectToLogin();
    } else {
      this.fetchCustomers();
    }
  },
  watch: {
    loggedIn(newVal) {
      if (!newVal || this.userType !== "developer" || !this.companyId) {
        this.redirectToLogin();
      }
    },
    userType(newVal) {
      if (newVal !== "developer" || !this.companyId) {
        this.redirectToLogin();
      }
    },
    companyId(newVal) {
      if (!newVal || this.userType !== "developer") {
        this.redirectToLogin();
      }
    },
    groupedSales(newGroupedSales) {
      this.connectedUnitsCount = Object.values(newGroupedSales).reduce(
        (acc, units) => acc + units.length,
        0
      );
    },
  },
  methods: {
    changePage(page) {
      this.currentPage = page;
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    async fetchCustomers() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/customers/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        console.log("Fetched customers:", response.data);
        this.customers = response.data;
      } catch (error) {
        console.error("Error fetching customers:", error);
        this.error = "Failed to load customers.";
      }
    },
    async viewCustomer(customer) {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/customers/${customer.id}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.currentCustomer = response.data;
        this.fetchCustomerDocuments(customer.id); // Make sure this is called
        this.showEditModal = true;
      } catch (error) {
        console.error("Error fetching customer details:", error);
      }
    },
    async fetchCustomerDocuments(customerId) {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/customers/${customerId}/documents/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        console.log("Fetched documents:", response.data);
        this.currentCustomer.documents = response.data.data.map((doc) => ({
          name: doc.file.split("/").pop(), // Extract file name
          url: doc.file,
          type: doc.document_type.name,
        }));
      } catch (error) {
        console.error("Error fetching customer documents:", error);
        this.error = "Failed to load customer documents.";
      }
    },
    async fetchBrokerDetails(brokerId) {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/brokers/${brokerId}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.currentCustomer.broker = response.data;
      } catch (error) {
        console.error("Error fetching broker details:", error);
        this.error = "Failed to load broker details.";
      }
    },
    async updateCustomer() {
      try {
        console.log("Updating customer with ID:", this.currentCustomer.id);
        await axios.put(
          `http://localhost:8000/developer/customers/${this.currentCustomer.id}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.showEditModal = false;
        this.fetchCustomers();
      } catch (error) {
        console.error("Error updating customer:", error);
        this.error = "Failed to update customer.";
      }
    },
    openDocumentModal(document) {
      if (document && document.url) {
        this.selectedDocument = document;
        this.showDocumentModal = true;
      } else {
        console.error("Invalid document or missing URL:", document);
      }
    },
    redirectToLogin() {
      this.$router.push({ name: "DevLogin" });
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
/* Reuse styles from DeveloperBrokers */
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
  background-color: #eff4fb;
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
  /* Align items vertically */
  gap: 10px;
  /* Add space between the icon and title */
}

.title-icon {
  width: 15px;
  height: 5px;
  background-color: #343a40;
  border-radius: 5px;
}

.edit-title {
  color: #000000;
  font-size: 16px;
  /* Adjust as needed */
  font-weight: bold;
  margin: 0;
  /* Remove default margin */
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
  border-radius: 4px;
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

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  margin-top: 0;
  max-width: 1100px;
  /* Ensures the card and grid align */
  margin-left: auto;
  /* Centers the card */
  margin-right: auto;
}

.customer-name {
  font-size: 14px;
  font-weight: bold;
  margin-top: 10px;
}

.customer-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background: #fff;
  font-size: 14px;
}

.customer-table th,
.customer-table td {
  padding-bottom: 5px;
  text-align: left;
  vertical-align: middle;
  border: none;
  /* Remove borders from all cells */
}

.customer-table th {
  background-color: #f9f9f9;
  font-weight: bold;
}

.customer-table th:nth-child(2),
.customer-table td:nth-child(2) {
  /* Location column */
  width: 22%;
}

.customer-table th:nth-child(3),
.customer-table td:nth-child(3) {
  /* Status column */
  width: 22%;
}

.customer-table th:nth-child(4),
.customer-table td:nth-child(4) {
  /* Actions column */
  width: 22%;
}

.customer-table th:nth-child(5),
.customer-table td:nth-child(5) {
  /* Actions column */
  width: 7%;
}

.outside-headers {
  display: grid;
  /* Change to grid layout */
  grid-template-columns: 27% 22% 22% 22% 7%;
  /* Match the column widths */
  padding: 0px 15px;
  margin: 20px auto 10px;
  max-width: 1100px;
}

.header-item {
  flex: 1;
  text-align: left;
  font-size: 14px;
  color: #333;
  font-weight: bold;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  margin: 0 5px;
}

.pagination .active {
  font-weight: bold;
}

.pagination-controls {
  display: flex;
  justify-content: flex-end;
  /* Align to the right */
  margin-top: 20px;
  /* Add spacing from the content above */
  gap: 10px;
  /* Spacing between buttons */
  padding-right: 20px;
  /* Add padding to push it away from the edge */
}

.page-button {
  padding: 5px 10px;
  font-size: 12px;
  /* Slightly smaller font */
  border: 1px solid #ddd;
  background-color: #fff;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.page-button.active {
  background-color: #007bff;
  color: white;
}

.page-button:disabled {
  cursor: not-allowed;
  background-color: #f5f5f5;
}

.page-button:hover:not(:disabled) {
  background-color: #e9ecef;
  /* Light gray */
}

.pagination-controls {
  display: flex;
  justify-content: flex-end;
  /* Align to the right */
  margin-top: 20px;
  /* Add spacing from the content above */
  gap: 10px;
  /* Spacing between buttons */
  padding-right: 20px;
  /* Add padding to push it away from the edge */
}

.page-button {
  padding: 5px 10px;
  font-size: 12px;
  /* Slightly smaller font */
  border: 1px solid #ddd;
  background-color: #fff;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.page-button.active {
  background-color: #007bff;
  color: white;
}

.page-button:disabled {
  cursor: not-allowed;
  background-color: #f5f5f5;
}

.page-button:hover:not(:disabled) {
  background-color: #e9ecef;
  /* Light gray */
}

.modal-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.styled-table {
  font-size: 14px; /* Adjust as needed */
  width: 100%;
}

.styled-table thead tr {
  background-color: #eff4fb;
  color: #333;
  font-weight: bold;
}

.styled-table th,
.styled-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #ddd;
  text-align: center; /* Center alignment for all cells */
  vertical-align: middle;
}

.styled-table tbody tr {
  border-bottom: 1px solid #f3f3f3;
}

.styled-table td.text-center {
  text-align: center;
}

.styled-table th {
  cursor: pointer;
  /* Optional if you add sortable columns */
}

.btn-cancel {
  background-color: #343a40;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
}
</style>
