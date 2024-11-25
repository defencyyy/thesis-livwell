<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-icon"></div>
          <div class="edit-title">Company Broker Management</div>
        </div>
        <!-- Header Section -->
        <!-- <div class="header">
        <h1>Total Brokers: {{ filteredBrokers.length }}</h1>
        <button @click="showModal = true">Add Broker</button>
      </div> -->

        <!-- Search & Filter -->
        <!-- <div class="filter-section">
        <input
          v-model="searchQuery"
          placeholder="Search Brokers"
          class="search-bar"
        />
        <select v-model="brokersPerPage" class="page-limit-selector">
          <option v-for="limit in [5, 10, 15, 20]" :key="limit" :value="limit">
            Show {{ limit }} per page
          </option>
        </select>
      </div> -->
        <div
          class="card shadow-lg border-0 rounded-3 mx-auto"
          style="max-width: 1100px"
        >
          <div class="card-body">
            <div class="row">
              <!-- Toolbar -->
              <div class="toolbar">
                <div class="left-section">
                  <div class="search-bar-container">
                    <input
                      type="text"
                      v-model="searchQuery"
                      placeholder="Search Broker"
                      class="search-bar"
                    />
                    <i class="fa fa-search search-icon"></i>
                  </div>
                </div>
                <div class="right-section">
                  <button
                    @click="showModal = true"
                    class="btn-primary add-button"
                  >
                    Add Broker
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Broker Table -->
        <!-- <table v-if="currentBrokers.length" class="table">
        <thead>
          <tr>
            <th>Email</th>
            <th>Username</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Contact Number</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="broker in currentBrokers" :key="broker.id">
            <td>{{ broker.email }}</td>
            <td>{{ broker.username }}</td>
            <td>{{ broker.first_name }}</td>
            <td>{{ broker.last_name }}</td>
            <td>{{ broker.contact_number }}</td>
            <td>
              <button @click="openEditModal(broker)">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No brokers found for this company.</p> -->
        <div class="outside-headers">
          <span class="header-item">First Name</span>
          <span class="header-item">Last Name</span>
          <span class="header-item">Username</span>
          <span class="header-item">Email</span>
          <span class="header-item">Contact</span>
          <span class="header-item">Actions</span>
        </div>

        <!-- <div v-for="broker in currentBrokers" :key="broker.id" class="card shadow-lg border-0 rounded-3 mx-auto"
          style="max-width: 1100px">
          <div class="card-body">
            <table class="card-table">
              <tbody>
                <tr>
                  <td>{{ broker.first_name }}</td>
                  <td>{{ broker.last_name }}</td>
                  <td>{{ broker.username }}</td>
                  <td>{{ broker.email }}</td>
                  <td>{{ broker.contact_number }}</td>
                  <td>
      
                    <button @click="openEditModal(broker)"
                      style="border: none; background-color: transparent; cursor: pointer; padding: 8px; font-size: 18px;">
                      <i class="fas fa-eye"></i>
                    </button>

                    <button @click="openEditModal(broker)"
                      style="border: none; background-color: transparent; cursor: pointer; padding: 8px; font-size: 18px;">
                      <i class="fas fa-edit"></i>
                    </button>

                    <button @click="openEditModal(broker)"
                      style="border: none; background-color: transparent; cursor: pointer; padding: 8px; font-size: 18px;">
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div> -->

        <!-- Editing Brokers -->
        <b-modal v-model="editModalVisible" title="Edit Broker" hide-footer>
          <form @submit.prevent="confirmEdit">
            <div class="form-group">
              <label for="editEmail">Email:</label>
              <input
                type="email"
                v-model="editBroker.email"
                id="editEmail"
                required
              />
            </div>

            <div class="form-group">
              <label for="editUsername">Username:</label>
              <input
                type="text"
                v-model="editBroker.username"
                id="editUsername"
                required
              />
            </div>

            <div class="form-group">
              <label for="editContactNumber">Contact Number:</label>
              <input
                type="text"
                v-model="editBroker.contact_number"
                id="editContactNumber"
                required
              />
              <p v-if="contactNumberError" class="text-danger">
                {{ contactNumberError }}
              </p>
            </div>

            <div class="form-group">
              <label for="editFirstName">First Name:</label>
              <input
                type="text"
                v-model="editBroker.first_name"
                id="editFirstName"
                required
              />
            </div>

            <div class="form-group">
              <label for="editLastName">Last Name:</label>
              <input
                type="text"
                v-model="editBroker.last_name"
                id="editLastName"
                required
              />
            </div>

            <div class="form-group">
              <label for="editPassword">Password:</label>
              <input
                type="password"
                v-model="editBroker.password"
                id="editPassword"
              />
              <p class="text-muted">
                Leave blank to keep the existing password.
              </p>
            </div>

            <button type="submit">Submit</button>
            <button type="button" @click="editModalVisible = false">
              Cancel
            </button>
          </form>

          <p v-if="error" class="text-danger">{{ error }}</p>
        </b-modal>

        <!-- Pagination -->
        <div class="pagination" v-if="filteredBrokers.length > brokersPerPage">
          <button
            v-for="page in totalPages"
            :key="page"
            @click="currentPage = page"
            :class="{ active: currentPage === page }"
          >
            {{ page }}
          </button>
        </div>

        <!-- Modal for Adding Broker -->
        <b-modal v-model="showModal" title="Add Broker" hide-footer>
          <form @submit.prevent="addBroker">
            <div class="form-group">
              <label for="email">Email:</label>
              <input type="email" v-model="email" id="email" required />
              <p v-if="emailError" class="text-danger">{{ emailError }}</p>
            </div>

            <div class="form-group">
              <label for="contactNumber">Contact Number:</label>
              <input
                type="text"
                v-model="contactNumber"
                id="contactNumber"
                :required="!editModalVisible"
              />
              <p v-if="contactNumberError" class="text-danger">
                {{ contactNumberError }}
              </p>
            </div>

            <div class="form-group">
              <label for="lastName">Last Name:</label>
              <input type="text" v-model="lastName" id="lastName" required />
              <p v-if="lastNameError" class="text-danger">
                {{ lastNameError }}
              </p>
            </div>

            <div class="form-group">
              <label for="firstName">First Name:</label>
              <input type="text" v-model="firstName" id="firstName" required />
              <p v-if="firstNameError" class="text-danger">
                {{ firstNameError }}
              </p>
            </div>

            <div class="form-group">
              <label for="password">Password:</label>
              <input
                type="password"
                v-model="password"
                id="password"
                required
              />
              <p v-if="passwordError" class="text-danger">
                {{ passwordError }}
              </p>
            </div>

            <button type="submit">Submit</button>
            <button type="button" @click="showModal = false">Cancel</button>
          </form>

          <p v-if="error" class="text-danger">{{ error }}</p>
          <p v-if="successMessage" class="text-success">{{ successMessage }}</p>
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { BModal } from "bootstrap-vue-3";
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "DeveloperBrokers",
  components: {
    SideNav,
    BModal,
    AppHeader,
  },
  data() {
    return {
      showModal: false,
      email: "",
      contactNumber: "",
      lastName: "",
      firstName: "",
      password: "",
      error: null,
      successMessage: null,
      brokers: [],
      searchQuery: "",
      brokersPerPage: 15,
      currentPage: 1,
      editModalVisible: false,
      editBroker: {},
      // Add error tracking
      emailError: null,
      contactNumberError: null,
      lastNameError: null,
      firstNameError: null,
      passwordError: null,
    };
  },

  computed: {
    ...mapState({
      userId: (state) => state.userId,
      userType: (state) => state.userType,
      companyId: (state) => state.companyId,
    }),
    vuexUserId() {
      return this.userId;
    },
    vuexCompanyId() {
      return this.companyId;
    },
    filteredBrokers() {
      return this.brokers.filter(
        (broker) =>
          broker.first_name
            .toLowerCase()
            .includes(this.searchQuery.toLowerCase()) ||
          broker.last_name
            .toLowerCase()
            .includes(this.searchQuery.toLowerCase()) ||
          broker.email.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    totalPages() {
      return Math.ceil(this.filteredBrokers.length / this.brokersPerPage);
    },
    currentBrokers() {
      const start = (this.currentPage - 1) * this.brokersPerPage;
      const end = start + this.brokersPerPage;
      return this.filteredBrokers.slice(start, end);
    },
  },

  mounted() {
    this.fetchBrokers();
  },

  methods: {
    openEditModal(broker) {
      if (!broker || !broker.id) {
        console.error("Invalid broker object:", broker);
        return;
      }
      this.editBroker = { ...broker };
      this.editModalVisible = true;
      this.resetForm(); // Reset error messages when modal opens
    },

    async fetchBrokers() {
      const companyId = this.vuexCompanyId;
      if (!companyId) {
        alert("Company ID not found. Please log in.");
        this.$router.push({ name: "DevLogin" });
        return;
      }
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/brokers/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        console.log("Brokers fetched:", response.data); // Log the response
        this.brokers = response.data;
      } catch (error) {
        if (error.response?.status === 401) {
          const refreshedToken = await this.refreshAccessToken();
          if (refreshedToken) {
            this.fetchBrokers(); // Retry after refreshing
          }
        } else {
          console.error("Error fetching brokers:", error.response || error);
          this.error = "Failed to load brokers.";
        }
      }
    },

    async confirmEdit() {
      if (
        this.editBroker.contact_number &&
        !/^\+?1?\d{9,15}$/.test(this.editBroker.contact_number)
      ) {
        this.contactNumberError =
          "Enter a valid phone number (9 to 15 digits).";
        return;
      } else {
        this.contactNumberError = null;
      }

      if (confirm("Are you sure you want to save these changes?")) {
        try {
          const payload = { ...this.editBroker };
          if (!payload.password) {
            delete payload.password; // Remove password if not updated
          }

          const response = await axios.put(
            `http://localhost:8000/developer/brokers/${this.editBroker.id}/`,
            payload,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
            }
          );
          console.log("Edit successful:", response.data);
          this.editModalVisible = false;
          this.fetchBrokers(); // Refresh brokers list
        } catch (error) {
          console.error("Error updating broker:", error);
          this.error = "Failed to update broker. Please try again.";
        }
      }
    },
    validateForm() {
      // Reset errors
      this.emailError = null;
      this.contactNumberError = null;
      this.lastNameError = null;
      this.firstNameError = null;
      this.passwordError = null;

      // Simple validation logic for each field
      if (!this.email) {
        this.emailError = "Email is required.";
      } else if (!/\S+@\S+\.\S+/.test(this.email)) {
        this.emailError = "Please enter a valid email address.";
      }

      if (!this.firstName) {
        this.firstNameError = "First Name is required.";
      }

      if (!this.lastName) {
        this.lastNameError = "Last Name is required.";
      }

      if (!this.password) {
        this.passwordError = "Password is required.";
      }

      // Contact number validation only if it's not optional in edit mode
      if (this.contactNumber && !/^\+?1?\d{9,15}$/.test(this.contactNumber)) {
        this.contactNumberError =
          "Enter a valid phone number (9 to 15 digits).";
      }

      return !(
        this.emailError ||
        this.contactNumberError ||
        this.firstNameError ||
        this.lastNameError ||
        this.passwordError
      );
    },

    async refreshAccessToken() {
      try {
        const refreshToken = localStorage.getItem("refreshToken");
        const response = await axios.post(
          "http://localhost:8000/api/token/refresh/",
          { refresh: refreshToken }
        );
        if (response.status === 200) {
          const { access } = response.data;
          localStorage.setItem("accessToken", access);
          return access;
        } else {
          this.handleTokenRefreshFailure();
        }
      } catch (error) {
        this.handleTokenRefreshFailure();
      }
    },

    handleTokenRefreshFailure() {
      alert("Session expired. Please log in again.");
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      this.$router.push({ name: "DevLogin" });
    },

    async addBroker() {
      if (this.validateForm()) {
        try {
          const response = await axios.post(
            "http://localhost:8000/developer/brokers/add/",
            {
              company: this.vuexCompanyId,
              email: this.email,
              contact_number: this.contactNumber,
              last_name: this.lastName,
              first_name: this.firstName,
              password: this.password,
            },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
            }
          );
          console.log("Broker added:", response.data); // Check response data
          this.successMessage = "Broker added successfully!";
          this.resetForm();
          this.showModal = false;
          this.fetchBrokers();
        } catch (error) {
          console.error("Error adding broker:", error.response || error); // Log full error
          this.error =
            error.response?.data?.error ||
            "Failed to add broker. Please try again.";
        }
      }
    },
    resetForm() {
      this.email = "";
      this.contactNumber = "";
      this.lastName = "";
      this.firstName = "";
      this.password = "";
      this.emailError = null;
      this.contactNumberError = null;
      this.lastNameError = null;
      this.firstNameError = null;
      this.passwordError = null;
      this.error = null;
      this.successMessage = null;
    },
  },
};
</script>

<style scoped>
.main-page {
  display: flex;
  height: 100vh;
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
  width: 100%;
  max-width: 1100px;
  margin: 20px auto;
  /* Center the wrapper */
}

.title-icon {
  width: 15px;
  height: 5px;
  background-color: #6c757d;
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

.dropdown-container {
  position: relative;
}

.dropdown {
  padding: 8px 12px;
  height: 38px;
  /* Explicitly set height */
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  width: 80%;
  max-width: 150px;
  background-color: white;
  color: #333;
}

/* Button Styles */
.btn-primary.add-button {
  padding: 8px 12px;
  border: 1px solid #007bff;
  border-radius: 4px;
  font-size: 14px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary.add-button:hover {
  background-color: #0056b3;
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

.filter-section {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.pagination {
  display: flex;
  gap: 5px;
  margin-top: 20px;
}

.pagination .active {
  font-weight: bold;
}
</style>
