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
import { mapState } from "vuex";
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
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId,
      authToken: (state) => state.authToken,
    }),
  },
  mounted() {
    this.setupAxiosInterceptor();
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
        this.successMessage = "Account updated successfully!";
        this.resetPasswordFields();
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
    setupAxiosInterceptor() {
      axios.interceptors.request.use((config) => {
        const token = this.authToken;
        if (token) config.headers["Authorization"] = `Bearer ${token}`;
        return config;
      });
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
.developer-account-page {
  display: flex;
  min-height: 100vh;
  /* Ensures it spans the full viewport height */
  background-color: #e8f0fa;
  /* Gray background */
}

.SideNav {
  width: 250px;
  /* Set fixed width for the sidebar */
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
  /* Adjust height as needed */
  background-color: #343a40;
  display: flex;
  align-items: center;
  padding-left: 10px;
}

.main-content {
  display: flex;
  flex-direction: column;
  margin-top: 80px;
  margin-left: 250px;
  /* Offset for header height */
  flex: 1;
  /* margin-left: 250px; */
  /* Set margin equal to sidebar width */
}

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
}

.card-body {
  padding: 2.5rem;
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

.edit-title {
  color: #000000;
  margin-bottom: 0.8rem;
  text-align: left;
  /* Align the text to the left */
}

.title-icon {
  width: 15px;
  /* Short horizontal line */
  height: 5px;
  /* Thin line */
  background-color: #343a40;
  /* Line color */
  border-radius: 5px;
  /* Rounded corners */
  margin-right: 10px;
  /* Space between the icon and the title */
  margin-bottom: 15px;
}

.row {
  display: flex;
  justify-content: space-between;
  /* Ensures there's space between the columns */
}

.col-md-6 {
  width: 47%; /* You can tweak the width to suit your design */
  margin-bottom: 20px; /* Spacing between sections */
  padding-right: 10px; /* Optional: add some padding to prevent overlap */
}

h5 {
  text-align: left;
  margin-bottom: 1rem; /* Adjust spacing below the title */
  font-size: 1.1rem; /* Optional: Adjust font size if needed */
  font-style: italic; /* Italicize the titles */
}

.form-label {
  font-size: 0.9rem;
  color: #6c757d;
  /* Adjust the value to your preferred size */
}

.btn-update {
  background-color: #42b983; /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px; /* Adjust the border radius */
  padding: 10px; /* Adjust the padding at the bottom */
  width: 100px;
}

.btn-cancel {
  background-color: #343a40; /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px; /* Adjust the border radius */
  padding: 10px;
}
</style>
