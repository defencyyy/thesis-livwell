<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class = "title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">Customer Details</div>
          </div>
          <!-- Header Section -->
          <div class = "total-customers">
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
                  <input
                    type="text"
                    v-model="searchQuery"
                    placeholder="Search Customers"
                    class="search-bar"
                  />
                  <i class="fa fa-search search-icon"></i>
                </div>
              </div>
              <div class="right-section"></div>
            </div>

            <!-- Pagination -->
            <div
              class="pagination"
              v-if="filteredCustomers.length > customersPerPage"
            >
              <button
                v-for="page in totalPages"
                :key="page"
                @click="currentPage = page"
                :class="{ active: currentPage === page }"
              >
                {{ page }}
              </button>
            </div>

          </div>
        </div>
        
        <!-- Broker Table -->
                    <div>

<!-- Headers outside the card -->
<div class="outside-headers">
  <span class="header-item">Name</span>
  <span class="header-item">Email</span>
  <span class="header-item">Contact</span>
  <span class="header-item">Broker Name</span>
  <span class="header-item">Actions</span>
</div>

<!-- Conditional Rendering -->
<div v-if="currentCustomers.length === 0" class="no-customers-message">
  No customers found.
</div>

<div
  v-else
  v-for="(customer, index) in currentCustomers"
  :key="customer.id || index"
  class="card border-0 rounded-1 mx-auto my-2"
  style="max-width: 1100px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
>
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
              <button 
                @click="viewCustomer(customer)"
                style = "
                  border: none;
                  background-color: transparent;
                  color: #343a40;
                  cursor: pointer;
                  font-size: 18px;
                ">
                <i class = "fas fa-eye"></i>  
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

</div>

      </div>
    </div>

    <!-- View/Edit Customer Modal -->
    <b-modal v-model="showEditModal" title="Customer Details" hide-footer>
      <form @submit.prevent="updateCustomer">
        <!-- Customer Info -->
        <h5>Customer Information</h5>
        <div class="form-group">
          <label for="editFirstName">First Name:</label>
          <input
            type="text"
            v-model="currentCustomer.first_name"
            id="editFirstName"
            required
          />
        </div>
        <div class="form-group">
          <label for="editLastName">Last Name:</label>
          <input
            type="text"
            v-model="currentCustomer.last_name"
            id="editLastName"
            required
          />
        </div>
        <div class="form-group">
          <label for="editEmail">Email:</label>
          <input
            type="email"
            v-model="currentCustomer.email"
            id="editEmail"
            required
          />
        </div>
        <div class="form-group">
          <label for="editContact">Contact:</label>
          <input
            type="text"
            v-model="currentCustomer.contact_number"
            id="editContact"
          />
        </div>

        <!-- Broker Info -->
        <h5 v-if="currentCustomer.broker">Broker Information</h5>
        <div v-if="currentCustomer.broker" class="form-group">
          <label for="brokerFirstName">Broker First Name:</label>
          <input
            type="text"
            v-model="currentCustomer.broker.first_name"
            id="brokerFirstName"
            disabled
          />
        </div>
        <div v-if="currentCustomer.broker" class="form-group">
          <label for="brokerLastName">Broker Last Name:</label>
          <input
            type="text"
            v-model="currentCustomer.broker.last_name"
            id="brokerLastName"
            disabled
          />
        </div>
        <div v-if="currentCustomer.broker" class="form-group">
          <label for="brokerEmail">Broker Email:</label>
          <input
            type="email"
            v-model="currentCustomer.broker.email"
            id="brokerEmail"
            disabled
          />
        </div>
        <div v-if="currentCustomer.broker" class="form-group">
          <label for="brokerContact">Broker Contact:</label>
          <input
            type="text"
            v-model="currentCustomer.broker.contact_number"
            id="brokerContact"
            disabled
          />
        </div>

        <!-- Buttons -->
        <button type="submit" class="btn btn-primary">Save Changes</button>
        <button
          type="button"
          @click="showEditModal = false"
          class="btn btn-secondary"
        >
          Cancel
        </button>
      </form>
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
      customersPerPage: 25,
      currentPage: 1,
      showEditModal: false,
      newCustomer: {
        first_name: "",
        last_name: "",
        email: "",
        contact_number: "",
      },
      currentCustomer: {
        broker: {},
      },
      error: null,
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
  },
  mounted() {
    if (!this.loggedIn || this.userType !== "developer" || !this.companyId) {
      this.redirectToLogin();
    } else {
      this.fetchCustomers();
      this.setupAxiosInterceptor();
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
  },
  methods: {
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
        if (error.response?.status === 401) {
          const refreshedToken = await this.refreshAccessToken();
          if (refreshedToken) {
            this.fetchCustomers(); // Retry with refreshed token
          }
        } else {
          console.error("Error fetching customers:", error);
          this.error = "Failed to load customers.";
        }
      }
    },
    viewCustomer(customer) {
      if (!customer || !customer.id) {
        console.error("Invalid customer data:", customer);
        return;
      }
      this.currentCustomer = { ...customer };

      if (!this.currentCustomer.broker) {
        this.fetchBrokerDetails(customer.broker_id);
      }

      this.showEditModal = true;
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
          this.currentCustomer,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.showEditModal = false;
        this.fetchCustomers();
      } catch (error) {
        if (error.response?.status === 401) {
          const refreshedToken = await this.refreshAccessToken();
          if (refreshedToken) {
            this.updateCustomer(); // Retry with refreshed token
          }
        } else {
          console.error("Error updating customer:", error);
          this.error = "Failed to update customer.";
        }
      }
    },
    async refreshAccessToken() {
      try {
        const refreshToken = localStorage.getItem("refreshToken");
        const response = await axios.post(
          "http://localhost:8000/refresh-token/",
          {
            refresh: refreshToken,
          }
        );

        const newAccessToken = response.data.access;
        localStorage.setItem("accessToken", newAccessToken);

        return newAccessToken;
      } catch (error) {
        console.error("Error refreshing access token:", error);
        this.error = "Failed to refresh access token.";
        return null;
      }
    },
    redirectToLogin() {
      this.$router.push({ name: "DevLogin" });
    },
    setupAxiosInterceptor() {
      axios.interceptors.request.use(
        (config) => {
          const token = localStorage.getItem("accessToken");
          if (token) {
            config.headers["Authorization"] = `Bearer ${token}`;
          }
          return config;
        },
        (error) => {
          return Promise.reject(error);
        }
      );

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
  background-color: #f6f6f6;
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
  /* margin-left: 250px; */
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
  margin: 20px auto; /* Center the wrapper */
}

.title-left {
  display: flex;
  align-items: center; /* Align items vertically */
  gap: 10px; /* Add space between the icon and title */
}

.title-icon {
  width: 15px;
  height: 5px;
  background-color: #343a40;
  border-radius: 5px;
}

.edit-title {
  color: #000000;
  font-size: 16px; /* Adjust as needed */
  font-weight: bold;
  margin: 0; /* Remove default margin */
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
  font-size: 15px;
  font-weight: bold;
  margin-top: 10px;
}

.customer-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background: #fff;
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
  width: 20%;
}

.customer-table th:nth-child(3),
.customer-table td:nth-child(3) {
  /* Status column */
  width: 25%;
}

.customer-table th:nth-child(4),
.customer-table td:nth-child(4) {
  /* Actions column */
  width: 20%;
}

.customer-table th:nth-child(5),
.customer-table td:nth-child(5) {
  /* Actions column */
  width: 10%;
}

.outside-headers {
  display: grid;
  /* Change to grid layout */
  grid-template-columns: 25% 20% 25% 20% 10%;
  /* Match the column widths */
  padding: 0px 18px;
  margin: 20px auto 10px;
  max-width: 1100px;
}

.header-item {
  flex: 1;
  text-align: left;
  font-size: 15px;
  color: #333;
  font-weight: bold;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 8px;
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
</style>
