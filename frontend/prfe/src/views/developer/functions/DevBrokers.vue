<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">Company Broker Management</div>
          </div>
          <!-- Header Section -->
          <div class="total-brokers">
            <div>Total Brokers: {{ filteredBrokers.length }}</div>
          </div>
        </div>

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
        <div class="card border-0 rounded-1 mx-auto"
          style="max-width: 1100px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)">
          <div class="card-body">
            <div class="row">
              <!-- Toolbar -->
              <div class="toolbar">
                <div class="left-section">
                  <div class="search-bar-container">
                    <input type="text" v-model="searchQuery" placeholder="Search Broker" class="search-bar" />
                    <i class="fa fa-search search-icon"></i>
                  </div>
                </div>
                <div class="right-section">
                  <button @click="showModal = true" class="btn-primary add-button">
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

        <!-- Broker Table -->
        <div>
          <!-- Headers outside the card -->
          <div class="outside-headers">
            <span class="header-item">Name</span>
            <span class="header-item">Username</span>
            <span class="header-item">Email</span>
            <span class="header-item">Contact</span>
            <span class="header-item">Actions</span>
          </div>

          <div v-for="(broker, index) in currentBrokers" :key="broker.id || index"
            class="card border-0 rounded-1 mx-auto my-2"
            style="max-width: 1100px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)">
            <div class="card-body">
              <table class="broker-table">
                <tbody>
                  <tr>
                    <td>
                      <img :src="require('@/assets/home.png')" alt="Broker Image" class="broker-image" />
                      <span class="broker-name">
                        {{ broker.first_name }} {{ broker.last_name }}
                      </span>
                    </td>
                    <td>
                      <span class="broker-username">{{ broker.username }}</span>
                    </td>
                    <td>
                      <span class="broker-email">{{ broker.email }}</span>
                    </td>
                    <td>
                      <span class="broker-contact">{{ broker.contact_number }}</span>
                    </td>
                    <td>
                      <div class="broker-actions d-flex gap-2">
                        <!-- Edit Button as Icon (Blue) -->
                        <button @click="openEditModal(broker)" style="border: none;
                          background-color: transparent;
                          color: #343a40;
                          cursor: pointer;
                          font-size: 18px;">
                          <i class="fas fa-edit"></i>
                        </button>
                        <!-- Delete Button as Icon (Red) -->
                        <button @click="deleteBroker(broker)" style="border: none;
                          background-color: transparent;
                          color: #343a40;
                          cursor: pointer;
                          font-size: 18px;">
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>


        <!-- Editing Brokers -->
        <b-modal v-model="editModalVisible" title="Edit Broker" hide-footer hide-header>
          <div class="modal-title p-3">
            <h5 class="mb-0">Edit Broker</h5>
          </div>
          <div class="p-3">
            <form @submit.prevent="confirmEdit">

              <!-- First Name -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="editFirstName" class="form-label">First Name:</label>
                  <input type="text" v-model="editBroker.first_name" id="editFirstName" class="form-control" required />
                </div>

                <!-- Last Name -->
                <div class="col-md-6">
                  <label for="editLastName" class="form-label">Last Name:</label>
                  <input type="text" v-model="editBroker.last_name" id="editLastName" class="form-control" required />
                </div>
              </div>

              <!-- Username -->
              <div class="form-group mb-3">
                <label for="editUsername" class="form-label">Username:</label>
                <input type="text" v-model="editBroker.username" id="editUsername" class="form-control" required />
              </div>

              <!-- Email -->
              <div class="form-group mb-3">
                <label for="editEmail" class="form-label">Email:</label>
                <input type="email" v-model="editBroker.email" id="editEmail" class="form-control" required />
              </div>

              <!-- Contact Number -->
              <div class="form-group mb-3">
                <label for="editContactNumber" class="form-label">Contact Number:</label>
                <input type="text" v-model="editBroker.contact_number" id="editContactNumber" class="form-control"
                  required />
                <p v-if="contactNumberError" class="text-danger">{{ contactNumberError }}</p>
              </div>

              <!-- Buttons -->
              <div class="d-flex justify-content-end gap-3 mt-3" style="padding-top: 15px;">
                <button type="submit" class="btn-add" style="width: 150px">
                  Save Changes
                </button>
                <button type="button" @click="editModalVisible = false" class="btn-cancel">
                  Cancel
                </button>
              </div>
            </form>

            <p v-if="error" class="text-danger">{{ error }}</p>
          </div>
        </b-modal>
        <!-- Pagination -->
        <div class="pagination" v-if="filteredBrokers.length > brokersPerPage">
          <button v-for="page in totalPages" :key="page" @click="currentPage = page"
            :class="{ active: currentPage === page }">
            {{ page }}
          </button>
        </div>

        <!-- Modal for Adding Broker -->
        <b-modal v-model="showModal" hide-header hide-footer>
          <div class="modal-title p-3">
            <h5 class="mb-0">New Broker</h5>
          </div>

          <div class="p-3">
            <form @submit.prevent="addBroker">
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="firstName" class="form-label">First Name:</label>
                  <input type="text" v-model="firstName" id="firstName" class="form-control" required />
                  <p v-if="firstNameError" class="text-danger">{{ firstNameError }}</p>
                </div>

                <div class="col-md-6">
                  <label for="lastName" class="form-label">Last Name:</label>
                  <input type="text" v-model="lastName" id="lastName" class="form-control" required />
                  <p v-if="lastNameError" class="text-danger">{{ lastNameError }}</p>
                </div>
              </div>

              <div class="form-group mb-3">
                <label for="email" class="form-label">Email:</label>
                <input type="email" v-model="email" id="email" class="form-control" required />
                <p v-if="emailError" class="text-danger">{{ emailError }}</p>
              </div>

              <div class="form-group mb-3">
                <label for="contactNumber" class="form-label">Contact Number:</label>
                <input type="text" v-model="contactNumber" id="contactNumber" class="form-control"
                  :required="!editModalVisible" />
                <p v-if="contactNumberError" class="text-danger">{{ contactNumberError }}</p>
              </div>

              <div class="form-group mb-3">
                <label for="password" class="form-label">Password:</label>
                <input type="password" v-model="password" id="password" class="form-control" required />
                <p v-if="passwordError" class="text-danger">{{ passwordError }}</p>
              </div>

              <!-- Optional: Add Image Upload Section if needed -->
              <!-- <div class="form-group mb-3">
        <label for="brokerPicture" class="form-label">Upload Photo</label>
        <input type="file" @change="handleFileUpload" id="brokerPicture" class="form-control" accept="image/*" />
      </div> -->

              <!-- Image Preview Section (Optional) -->
              <!-- <div v-if="imagePreview" class="text-center mb-3">
        <h6>Image Preview</h6>
        <img :src="imagePreview" alt="Image Preview" class="img-fluid" style="max-height: 200px; object-fit: cover" />
      </div> -->

              <!-- Submit & Cancel Buttons -->
              <div class="d-flex justify-content-end gap-2 mt-30" style="padding-top: 15px;">
                <button type="submit" class="btn-add" style="width: 150px">Add New Broker</button>
                <button type="button" @click="showModal = false" class="btn-cancel">Cancel</button>
              </div>
            </form>
          </div>

          <!-- Error & Success Message -->
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
    AppHeader,
    BModal,
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
}

.total-broker {
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
  border: 1px solid #42b983;
  border-radius: 3px;
  font-size: 14px;
  background-color: #42b983;
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

.broker-info {
  flex-direction: row;
}

.broker-image {
  width: 30px;
  /* Small size for the table */
  height: 30px;
  /* Make the image smaller */
  object-fit: cover;
  /* Crop the image if necessary */
  margin-right: 10px;
  /* Adds some spacing between the image and the name */
  border-radius: 50%;
  /* Makes the image circular */
}

.broker-name {
  font-size: 15px;
  font-weight: bold;
  margin-top: 10px;
}


.broker-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background: #fff;
}

.broker-table th,
.broker-table td {
  padding-bottom: 5px;
  text-align: left;
  vertical-align: middle;
  border: none;
  /* Remove borders from all cells */
}

.broker-table th {
  background-color: #f9f9f9;
  font-weight: bold;
}

.broker-table th:nth-child(2),
.broker-table td:nth-child(2) {
  /* Location column */
  width: 20%;
}

.broker-table th:nth-child(3),
.broker-table td:nth-child(3) {
  /* Status column */
  width: 25%;
}

.broker-table th:nth-child(4),
.broker-table td:nth-child(4) {
  /* Actions column */
  width: 20%;
}

.broker-table th:nth-child(5),
.broker-table td:nth-child(5) {
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


.form-group .form-label,
.row .form-label {
  font-size: 0.9rem;
  color: #6c757d;
  /* Adjust the value to your preferred size */
}

.btn-add {
  background-color: #42b983;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
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
