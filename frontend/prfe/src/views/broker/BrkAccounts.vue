<template>
  <header>
    <AppHeaderLivwell/>
  </header>
  <div class="accounts-page">
    <SideNav />
    <div class="content row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <div class="card mt-5">
          <div class="card-header text-center">
            <h1>Welcome to Account</h1>
            <p>Here you can manage your account</p>
          </div>
          <div class="card-body">
            <form @submit.prevent="updateAccount">
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

              <div class="form-group">
                <label for="password">Password:</label>
                <input
                  type="password"
                  class="form-control"
                  v-model="password"
                  id="password"
                />
              </div>

              <button
                type="submit"
                class="btn btn-primary btn-block"
                :disabled="loading"
              >
                {{ loading ? "Updating..." : "Update Account" }}
              </button>
            </form>

            <p v-if="error" class="text-danger">{{ error }}</p>
            <p v-if="successMessage" class="text-success">
              {{ successMessage }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import SideNav from "@/components/SideNav.vue";
import AppHeaderLivwell from "@/components/Header.vue";

export default {
  name: "BrkAccounts",
  components: {
    SideNav,
    AppHeaderLivwell,
  },
  data() {
    return {
      username: "",
      email: "",
      contactNumber: "",
      password: "",
      error: null,
      successMessage: null,
      loading: false, // For showing loading state
    };
  },
  computed: {
    ...mapGetters(["getUserId", "getAuthToken"]),
  },
  methods: {
    async updateAccount() {
      // Validate password on client-side
      if (this.password) {
        if (this.password.length < 8) {
          this.error = "Password must be at least 8 characters long.";
          this.successMessage = null;
          return;
        }
        if (!/[A-Z]/.test(this.password)) {
          this.error = "Password must contain at least one uppercase letter.";
          this.successMessage = null;
          return;
        }
        if (!/[a-z]/.test(this.password)) {
          this.error = "Password must contain at least one lowercase letter.";
          this.successMessage = null;
          return;
        }
        if (!/\d/.test(this.password)) {
          this.error = "Password must contain at least one number.";
          this.successMessage = null;
          return;
        }
        if (!/[!@#$%^&*(),.?":{}|<>]/.test(this.password)) {
          this.error = "Password must contain at least one special character.";
          this.successMessage = null;
          return;
        }
      }

      const brokerId = this.getUserId; // Fetch brokerId from Vuex
      const authToken = this.getAuthToken; // Fetch authToken from Vuex

      if (!brokerId || !authToken) {
        this.error =
          "No broker ID or authentication token found. Please log in again.";
        return;
      }

      this.loading = true; // Set loading state

      try {
        const response = await fetch(
          `http://localhost:8000/broker/manage-account/${brokerId}/`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${authToken}`,
            },
            body: JSON.stringify({
              username: this.username || undefined,
              email: this.email || undefined,
              contact_number: this.contactNumber || undefined,
              password: this.password || undefined,
            }),
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          this.error = errorData.message || "Failed to update account.";
          this.successMessage = null;
        } else {
          const data = await response.json();
          if (data.success) {
            this.successMessage = "Account updated successfully!";
            this.error = null;
            // Reset form fields
            this.username = "";
            this.email = "";
            this.contactNumber = "";
            this.password = "";
          } else {
            this.error = data.message || "Failed to update account.";
            this.successMessage = null;
          }
        }
      } catch (error) {
        console.error("Error updating account:", error);
        this.error = "An error occurred while updating your account.";
        this.successMessage = null;
      } finally {
        this.loading = false; // Reset loading state
      }
    },
  },
};
</script>

<style scoped>
/* Account Page Layout */
.accounts-page {
  display: flex;
  height: 100vh; /* Ensure it fills the full viewport height */
}

/* Content Area (form container) */
.content {
  flex-grow: 1;
  background-color: #f8f9fa; /* Light background for the form */
  display: flex;
  justify-content: center;
  align-items: start;
  padding-top: 20px;
}

/* Card Styling */
.card {
  width: 100%;
  max-width: 600px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.card-header {
  background-color: #007bff; /* Blue background for header */
  color: white;
  padding: 20px;
  text-align: center;
}

.card-body {
  padding: 30px;
  background-color: white;
  text-align: left;
}

/* Form Input Styling */
.form-group {
  margin-bottom: 1.5rem; /* Spacing between form groups */
}

label {
  font-weight: bold;
  margin-bottom: 0.5rem;
  display: block;
}

input.form-control {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ced4da;
}

input.form-control:focus {
  border-color: #007bff;
  outline: none;
}

button {
  width: 100%;
  padding: 12px;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:disabled {
  background-color: #c0c0c0;
  cursor: not-allowed;
}

button:not(:disabled):hover {
  background-color: #0056b3; /* Darken button on hover */
}

/* Success/Error Message */
.text-success, .text-danger {
  margin-top: 15px;
  text-align: center;
  font-weight: bold;
}

/* Media Query for Responsiveness */
@media (max-width: 768px) {
  .card {
    margin: 0 20px;
  }

  .content {
    padding: 15px;
  }
}




</style>
