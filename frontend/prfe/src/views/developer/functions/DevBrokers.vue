<template>
  <div class="developer-brokers-page">
    <SideNav />
    <div class="content">
      <h1>Total Brokers: {{ filteredBrokers.length }}</h1>

      <!-- JWT Token Display -->
      <div>
        <p><strong>JWT Token:</strong> {{ token }}</p>
      </div>

      <!-- Add Broker Button -->
      <button @click="showModal = true">Add Broker</button>

      <!-- Search Bar -->
      <div>
        <input v-model="searchQuery" placeholder="Search Brokers" />
      </div>

      <!-- Broker Table -->
      <table v-if="filteredBrokers.length" class="table">
        <thead>
          <tr>
            <th>Email</th>
            <th>Username</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Contact Number</th>
            <th>Actions</th>
            <!-- New column for actions -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="broker in filteredBrokers" :key="broker.id">
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
      <p v-else>No brokers found for this company.</p>

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
            <p class="text-muted">Leave blank to keep the existing password.</p>
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
          <div>
            <label for="email">Email:</label>
            <input type="email" v-model="email" id="email" required />
            <p v-if="emailError" class="text-danger">{{ emailError }}</p>
          </div>

          <div>
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

          <div>
            <label for="lastName">Last Name:</label>
            <input type="text" v-model="lastName" id="lastName" required />
            <p v-if="lastNameError" class="text-danger">{{ lastNameError }}</p>
          </div>

          <div>
            <label for="firstName">First Name:</label>
            <input type="text" v-model="firstName" id="firstName" required />
            <p v-if="firstNameError" class="text-danger">
              {{ firstNameError }}
            </p>
          </div>

          <div>
            <label for="password">Password:</label>
            <input type="password" v-model="password" id="password" required />
            <p v-if="passwordError" class="text-danger">{{ passwordError }}</p>
          </div>

          <button type="submit">Submit</button>
          <button type="button" @click="showModal = false">Cancel</button>
        </form>

        <p v-if="error" class="text-danger">{{ error }}</p>
        <p v-if="successMessage">{{ successMessage }}</p>
      </b-modal>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import { BModal } from "bootstrap-vue-3";
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "DevFuncBroker",
  components: {
    SideNav,
    BModal,
  },
  data() {
    return {
      token: localStorage.getItem("authToken"), // Get token to display
      showModal: false,
      email: "",
      contactNumber: "",
      lastName: "",
      firstName: "",
      password: "12345", // Default password can be pre-filled
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
    async addBroker() {
      const companyId = localStorage.getItem("company_id");
      const token = localStorage.getItem("authToken");

      try {
        const response = await fetch(
          "http://localhost:8000/developer/broker/create/",
          {
            method: "POST",
            headers: {
              Authorization: `Token ${token}`, // Pass the token in the Authorization header
              "Content-Type": "application/json",
              "Company-ID": companyId, // Pass the company ID in the headers
            },
            body: JSON.stringify({
              email: this.email,
              contact_number: this.contactNumber,
              last_name: this.lastName,
              first_name: this.firstName,
              password: this.password,
            }),
          }
        );

        if (response.ok) {
          this.successMessage = "Broker added successfully!";
          this.error = null;
          this.resetForm();
          this.showModal = false;
          this.fetchBrokers(); // Refresh the brokers list
        } else {
          const errorData = await response.json();
          this.error = errorData.message || "Failed to add broker.";
        }
      } catch (error) {
        this.error = "An error occurred while adding the broker.";
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
