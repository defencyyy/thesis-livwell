<template>
  <div class="developer-account-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <h1>Manage Your Account</h1>
        <form @submit.prevent="updateAccount">
          <!-- Display current data in form fields -->
          <h2>Personal Details</h2>
          <div class="form-group">
            <label for="username">Username:</label>
            <input
              type="text"
              class="form-control"
              v-model="username"
              id="username"
            />
          </div>

          <div class="form-group">
            <label for="firstName">First Name:</label>
            <input
              type="text"
              class="form-control"
              v-model="firstName"
              id="firstName"
            />
          </div>

          <div class="form-group">
            <label for="lastName">Last Name:</label>
            <input
              type="text"
              class="form-control"
              v-model="lastName"
              id="lastName"
            />
          </div>

          <div class="form-group">
            <label for="email">Email:</label>
            <input
              type="email"
              class="form-control"
              v-model="email"
              id="email"
            />
          </div>

          <div class="form-group">
            <label for="contactNumber">Contact Number:</label>
            <input
              type="text"
              class="form-control"
              v-model="contactNumber"
              id="contactNumber"
            />
          </div>

          <!-- Password Section -->
          <h2>Change Password</h2>
          <div class="form-group">
            <label for="currentPassword">Current Password:</label>
            <input
              type="password"
              class="form-control"
              v-model="currentPassword"
              id="currentPassword"
              required
            />
          </div>

          <div class="form-group">
            <label for="newPassword">New Password:</label>
            <input
              type="password"
              class="form-control"
              v-model="newPassword"
              id="newPassword"
            />
          </div>

          <div class="form-group">
            <label for="confirmNewPassword">Confirm New Password:</label>
            <input
              type="password"
              class="form-control"
              v-model="confirmNewPassword"
              id="confirmNewPassword"
            />
          </div>

          <!-- Regular Submit Button -->
          <button
            type="button"
            class="btn btn-primary"
            :disabled="loading"
            @click="prepareUpdate"
          >
            {{ loading ? "Updating..." : "Update Account" }}
          </button>
        </form>

        <!-- Confirmation Modal -->
        <div v-if="showConfirmModal" class="modal-overlay">
          <div class="modal-content">
            <h3>Confirm Update</h3>
            <p>Are you sure you want to update your account details?</p>
            <div class="modal-buttons">
              <button class="btn btn-secondary" @click="cancelUpdate">
                Cancel
              </button>
              <button class="btn btn-primary" @click="submitUpdate">
                Confirm
              </button>
            </div>
          </div>
        </div>

        <!-- Error/Success Message -->
        <p v-if="error" class="text-danger">{{ error }}</p>
        <p v-if="successMessage" class="text-success">{{ successMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";

export default {
  name: "DevFuncAccount",
  components: {
    SideNav,
    AppHeader,
  },
  data() {
    return {
      username: "",
      firstName: "",
      lastName: "",
      email: "",
      contactNumber: "",
      currentPassword: "",
      newPassword: "",
      confirmNewPassword: "",
      error: null,
      successMessage: null,
      loading: false,
      showConfirmModal: false, // Control modal visibility
    };
  },
  computed: {
    ...mapGetters(["getUserId", "getAuthToken"]),
  },
  mounted() {
    this.fetchAccountDetails();
  },
  methods: {
    async fetchAccountDetails() {
      const authToken = this.getAuthToken;
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/account/",
          {
            headers: {
              Authorization: `Bearer ${authToken}`,
            },
          }
        );

        if (response.data) {
          this.username = response.data.username;
          this.firstName = response.data.first_name;
          this.lastName = response.data.last_name;
          this.email = response.data.email;
          this.contactNumber = response.data.contact_number;
        }
      } catch (error) {
        this.error = "Error loading account details.";
      }
    },

    prepareUpdate() {
      // Check if password fields match
      if (this.newPassword !== this.confirmNewPassword) {
        this.error = "Passwords do not match.";
        return;
      }

      // Ensure current password is provided if updating the password
      if (!this.currentPassword) {
        this.error = "Current password is required.";
        return;
      }

      // Show confirmation modal
      this.showConfirmModal = true;
    },

    cancelUpdate() {
      // Close the modal and reset any error or success messages
      this.showConfirmModal = false;
      this.error = null;
      this.successMessage = null;
      // Optionally, reset the password fields as well
      this.currentPassword = "";
      this.newPassword = "";
      this.confirmNewPassword = "";
    },

    async submitUpdate() {
      const userId = this.getUserId;
      const authToken = this.getAuthToken;

      if (!userId || !authToken) {
        this.error = "User not authenticated.";
        return;
      }

      this.loading = true;

      try {
        const response = await axios.put(
          `http://localhost:8000/developer/account/`,
          {
            username: this.username,
            email: this.email,
            contact_number: this.contactNumber,
            first_name: this.firstName,
            last_name: this.lastName,
            current_password: this.currentPassword,
            new_password: this.newPassword,
          },
          {
            headers: {
              Authorization: `Bearer ${authToken}`,
            },
          }
        );

        if (response.data.success) {
          this.successMessage = "Account updated successfully!";
          this.error = null;
          this.showConfirmModal = false;
          this.resetPasswordFields(); // Reset password fields on success
        } else {
          this.error = response.data.message || "Failed to update account.";
          this.successMessage = null;
        }
      } catch (error) {
        this.error = "An error occurred while updating your account.";
        this.successMessage = null;
      } finally {
        this.loading = false;
      }
    },

    resetPasswordFields() {
      this.currentPassword = "";
      this.newPassword = "";
      this.confirmNewPassword = "";
    },
  },
};
</script>

<style scoped>
.developer-account-page {
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
  margin-top: 60px; /* Adjust for the header */
}

form {
  margin-top: 20px;
}

.action-buttons {
  margin-top: 20px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
  width: 300px;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
</style>
