<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-icon"></div>
          <div class="edit-title">Customer Management</div>
        </div>

        <div
          class="card shadow-lg border-0 rounded-3 mx-auto"
          style="max-width: 1100px"
        >
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

            <!-- Customer Table -->
            <table v-if="currentCustomers.length" class="table">
              <thead>
                <tr>
                  <th>First Name</th>
                  <th>Last Name</th>
                  <th>Email</th>
                  <th>Contact</th>
                  <th>Broker</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="customer in currentCustomers" :key="customer.id">
                  <td>{{ customer.first_name }}</td>
                  <td>{{ customer.last_name }}</td>
                  <td>{{ customer.email }}</td>
                  <td>{{ customer.contact_number }}</td>
                  <td>
                    {{
                      customer.broker
                        ? customer.broker.first_name +
                          " " +
                          customer.broker.last_name
                        : "N/A"
                    }}
                  </td>

                  <td>
                    <button
                      @click="viewCustomer(customer)"
                      class="btn btn-info"
                    >
                      View
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <p v-else>No customers found.</p>

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
.main-page {
  display: flex;
  height: 100vh;
}

.main-content {
  flex: 1;
  margin-left: 250px;
}

.content {
  padding: 20px;
  text-align: center;
}

.title-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
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
