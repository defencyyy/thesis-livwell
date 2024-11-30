<template>
  <div class="developer-account-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-icon"></div>
          <div class="edit-title">Account Settings</div>
        </div>
        <div
          class="card shadow-lg border-0 rounded-1 mx-auto"
          style="max-width: 900px"
        >
          <div class="card-body">
            <form @submit.prevent="prepareUpdate">
              <div class="row">
                <!-- Personal Information Section -->
                <div class="col-md-6">
                  <h5 class="mb-4">Personal Information</h5>
                  <div class="mb-3">
                    <label for="firstName" class="form-label">First Name</label>
                    <input
                      type="text"
                      id="firstName"
                      v-model="firstName"
                      class="form-control"
                    />
                  </div>
                  <div class="mb-3">
                    <label for="lastName" class="form-label">Last Name</label>
                    <input
                      type="text"
                      id="lastName"
                      v-model="lastName"
                      class="form-control"
                    />
                  </div>
                  <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input
                      type="email"
                      id="email"
                      v-model="email"
                      class="form-control"
                    />
                  </div>
                  <div class="mb-3">
                    <label for="contactNumber" class="form-label"
                      >Phone Number</label
                    >
                    <input
                      type="text"
                      id="contactNumber"
                      v-model="contactNumber"
                      class="form-control"
                    />
                  </div>
                </div>

                <!-- Password Settings Section -->
                <div class="col-md-6">
                  <h5 class="mb-4">Password Settings</h5>
                  <div class="mb-3">
                    <label for="currentPassword" class="form-label"
                      >Current Password</label
                    >
                    <input
                      type="password"
                      id="currentPassword"
                      v-model="currentPassword"
                      class="form-control"
                    />
                  </div>
                  <div class="mb-3">
                    <label for="newPassword" class="form-label"
                      >New Password</label
                    >
                    <input
                      type="password"
                      id="newPassword"
                      v-model="newPassword"
                      class="form-control"
                    />
                  </div>
                  <div class="mb-3">
                    <label for="confirmNewPassword" class="form-label"
                      >Confirm New Password</label
                    >
                    <input
                      type="password"
                      id="confirmNewPassword"
                      v-model="confirmNewPassword"
                      class="form-control"
                    />
                  </div>
                </div>
              </div>

              <div class="d-flex justify-content-end gap-2 mt-4">
                <button
                  type="button"
                  class="btn-update"
                  :disabled="loading"
                  @click="submitUpdate"
                >
                  {{ loading ? "Updating..." : "Update" }}
                </button>
                <button type="button" class="btn-cancel" @click="cancelUpdate">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
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
      showConfirmModal: false, // Modal visibility control
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
      try {
        const response = await axios.get("/developer/account/", {
          headers: { Authorization: `Bearer ${this.getAuthToken}` },
        });
        const { username, first_name, last_name, email, contact_number } =
          response.data;
        Object.assign(this, {
          username,
          firstName: first_name,
          lastName: last_name,
          email,
          contactNumber: contact_number,
        });
      } catch {
        this.error = "Error loading account details.";
      }
    },
    prepareUpdate() {
      if (this.newPassword !== this.confirmNewPassword) {
        this.error = "Passwords do not match.";
        return;
      }
      if (
        !this.currentPassword &&
        (this.newPassword || this.confirmNewPassword)
      ) {
        this.error = "Current password is required to change your password.";
        return;
      }
      this.showConfirmModal = true;
    },
    cancelUpdate() {
      Object.assign(this, {
        showConfirmModal: false,
        error: null,
        successMessage: null,
        currentPassword: "",
        newPassword: "",
        confirmNewPassword: "",
      });
    },
    async submitUpdate() {
      this.loading = true;
      try {
        const response = await axios.put("/developer/account/", {
          username: this.username,
          email: this.email,
          contact_number: this.contactNumber,
          first_name: this.firstName,
          last_name: this.lastName,
          current_password: this.currentPassword,
          new_password: this.newPassword,
        });
        const { success, message } = response.data;
        if (success) {
          this.successMessage = "Account updated successfully!";
          this.error = null;
          this.resetPasswordFields();
        } else {
          this.error = message || "Failed to update account.";
        }
      } catch {
        this.error = "An error occurred while updating your account.";
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
/* Styles remain largely unchanged, but added meaningful comments */
html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.developer-account-page {
  display: flex;
  min-height: 100vh;
  background-color: #f6f6f6;
}

.main-content {
  display: flex;
  flex-direction: column;
  margin-top: 80px;
  margin-left: 250px;
  flex: 1;
}

.title-wrapper {
  display: flex;
  /* Align line and title horizontally */
  align-items: center;
  width: 100%;
  max-width: 900px;

  /* Ensure the title width matches the card's width */
  margin-left: auto;
  margin-right: auto;
  margin-top: 20px;
  /* Center the wrapper */
}

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-update,
.btn-cancel {
  padding: 10px;
  border: none;
  border-radius: 3px;
}

.btn-update {
  background-color: #42b983;
  color: #fff;
}

.btn-cancel {
  background-color: #343a40;
  color: #fff;
}
</style>
