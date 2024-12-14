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
            <form @submit.prevent="updateAccount">
              <div class="row">
                <!-- Personal Information Section -->
                <div class="col-md-6">
                  <h5 class="mb-4">Personal Information</h5>
                  <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input
                      type="text"
                      id="username"
                      v-model="username"
                      class="form-control"
                    />
                  </div>
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
                      required
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
                <button type="submit" class="btn-update" :disabled="loading">
                  {{ loading ? "Updating..." : "Update" }}
                </button>
              </div>
            </form>
          </div>
        </div>

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
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";
import { BModal } from "bootstrap-vue-3";

export default {
  name: "DevFuncAccount",
  components: {
    SideNav,
    AppHeader,
    BModal,
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
      showNotification: false,
      notificationTitle: "",
      notificationMessage: "",
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId,
      authToken: (state) => state.authToken,
    }),
  },
  mounted() {
    this.fetchAccountDetails();
  },
  methods: {
    async fetchAccountDetails() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/account/",
          {
            headers: {
              Authorization: `Bearer ${this.authToken}`,
            },
          }
        );
        const { username, first_name, last_name, email, contact_number } =
          response.data;
        this.username = username;
        this.firstName = first_name;
        this.lastName = last_name;
        this.email = email;
        this.contactNumber = contact_number;
      } catch (error) {
        this.error = "Error loading account details.";
      }
    },

    async updateAccount() {
      this.loading = true;
      try {
        await axios.put(
          "http://localhost:8000/developer/account/",
          {
            username: this.username,
            first_name: this.firstName,
            last_name: this.lastName,
            email: this.email,
            contact_number: this.contactNumber,
            current_password: this.currentPassword,
            new_password: this.newPassword,
          },
          {
            headers: {
              Authorization: `Bearer ${this.authToken}`,
            },
          }
        );
        this.notificationTitle = "Success";
        this.notificationMessage = "Account updated successfully!";
        this.showNotification = true;
        this.resetPasswordFields();
      } catch {
        this.notificationTitle = "Error";
        this.notificationMessage =
          "An error occurred while updating your account.";
        this.showNotification = true;
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
html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

/* Main page container */
.developer-account-page {
  display: flex;
  min-height: 100vh;
  background-color: #e8f0fa;
}

/* Sidebar */
.SideNav {
  width: 250px;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #343a40;
  z-index: 1;
}

/* Header */
.AppHeader {
  width: 100%;
  height: 60px;
  background-color: #343a40;
  display: flex;
  align-items: center;
  padding-left: 10px;
}

/* Main content */
.main-content {
  display: flex;
  flex-direction: column;
  margin-top: 80px;
  margin-left: 250px;
  flex: 1;
}

/* Card styling */
.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
}

.card-body {
  padding: 2.5rem;
}

/* Title wrapper */
.title-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 900px;
  margin: 20px auto 0;
}

.edit-title {
  color: #000;
  margin-bottom: 0.8rem;
  text-align: left;
}

.title-icon {
  width: 15px;
  height: 5px;
  background-color: #343a40;
  border-radius: 5px;
  margin-right: 10px;
  margin-bottom: 15px;
}

/* Form layout */
.row {
  display: flex;
  justify-content: space-between;
}

.col-md-6 {
  width: 47%;
  margin-bottom: 20px;
  padding-right: 10px;
}

h5 {
  text-align: left;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  font-style: italic;
}

.form-label {
  display: block;
  font-size: 0.9rem;
  color: #6c757d;
  text-align: left;
}

/* Buttons */
.btn-update {
  background-color: #0560fd;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 10px;
  width: 100px;
}

.btn-cancel {
  background-color: #343a40;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 10px;
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
</style>
