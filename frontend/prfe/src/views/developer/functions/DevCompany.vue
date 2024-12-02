<template>
  <div class="developer-company-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="container mt-5">
        <div class="title-wrapper">
          <div class="title-icon"></div>
          <div class="edit-title">Company Details</div>
        </div>
        <div
          class="card shadow-lg border-0 rounded-1 mx-auto"
          style="max-width: 900px"
        >
          <div class="card-body">
            <div class="row">
              <div class="col-md-4 text-center">
                <div class="profile-pic" style="margin-top: 10px">
                  <img
                    v-if="company.logo"
                    :src="getLogoUrl(company.logo)"
                    alt="Company Logo"
                    class="img-fluid rounded-circle shadow-sm"
                    style="width: 200px; height: 200px; object-fit: cover"
                  />
                  <span v-else>No Logo Available</span>
                </div>
                <h5 class="mt-4" style="font-weight: bold">
                  {{ company.name || "Company Information" }}
                </h5>
              </div>

              <div class="col-md-8">
                <div class="mb-3">
                  <label for="logo" class="form-label">Upload Logo</label>
                  <input
                    type="file"
                    class="form-control"
                    id="logo"
                    accept="image/*"
                    @change="onFileChange"
                  />
                </div>

                <div class="mb-3">
                  <label for="companyDescription" class="form-label"
                    >Company Description</label
                  >
                  <textarea
                    class="form-control"
                    id="companyDescription"
                    v-model="company.description"
                    rows="6"
                    placeholder="Enter company description"
                  ></textarea>
                </div>

                <div
                  class="d-flex justify-content-end"
                  style="padding-top: 15px"
                >
                  <button @click="updateCompany" class="btn-save">
                    Save Changes
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";
import { mapState } from "vuex";

export default {
  name: "DevCompany",
  components: { SideNav, AppHeader },
  data() {
    return {
      company: {},
      newLogo: null,
      previewLogo: null,
      error: null,
    };
  },

  computed: {
    ...mapState({
      userId: (state) => state.userId,
      userType: (state) => state.userType,
      companyId: (state) => state.companyId,
      loggedIn: (state) => state.loggedIn, // Vuex loggedIn state
    }),
    vuexUserId() {
      return this.userId;
    },
    vuexCompanyId() {
      return this.companyId;
    },
    localStorageUserId() {
      return localStorage.getItem("user_id");
    },
    localStorageCompanyId() {
      return localStorage.getItem("company_id");
    },
  },

  mounted() {
    if (!this.loggedIn || this.userType !== "developer" || !this.companyId) {
      this.redirectToLogin();
    } else {
      this.fetchCompany();
      this.setupAxiosInterceptor();
    }
  },

  methods: {
    async fetchCompany() {
      const companyId = this.vuexCompanyId;

      if (!companyId) {
        alert("Company ID not found. Please log in.");
        this.redirectToLogin();
        return;
      }

      try {
        const response = await axios.get(
          `http://localhost:8000/developer/company/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );
        if (response.status === 200) {
          this.company = response.data;
        } else {
          alert("Error fetching company details.");
        }
      } catch (error) {
        if (error.response?.status === 401) {
          const refreshedToken = await this.refreshAccessToken();
          if (refreshedToken) {
            this.fetchCompany(); // Retry after refreshing
          }
        } else {
          console.error("Error fetching company data:", error);
          alert("Error fetching company data.");
        }
      }
    },

    async refreshAccessToken() {
      try {
        const refreshToken = localStorage.getItem("refreshToken");
        const response = await axios.post(
          "http://localhost:8000/api/token/refresh/",
          {
            refresh: refreshToken,
          }
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
      this.$store.dispatch("logout");
      this.$router.push({ name: "DevLogin" });
    },

    async updateCompany() {
      try {
        // Log the company.description to verify the value being saved
        console.log("Description to update:", this.company.description);

        const formData = new FormData();

        // Only append the description if it has changed
        if (this.company.description !== this.company.originalDescription) {
          formData.append("description", this.company.description); // Update with the new description
        }

        // Only append the logo if it was selected
        if (this.newLogo) {
          formData.append("logo", this.newLogo); // Include logo if selected
        }

        // Make the PUT request to update the company
        const response = await axios.put(
          "http://localhost:8000/developer/company/edit/",
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.status === 200) {
          alert("Company updated successfully!");
          this.company.originalDescription = this.company.description; // Save the current description as the original one
          this.fetchCompany();
        } else {
          alert("Error updating company.");
        }
      } catch (error) {
        console.error("Error updating company:", error);
        alert(
          error.response?.data?.error ||
            "Error updating company. Please try again."
        );
      }
    },

    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.newLogo = file;
      }
    },

    getLogoUrl(logo) {
      return `http://localhost:8000${logo}`;
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
html,
body {
  height: 100%;
  margin: 0;
  /* Removes default margin */
  padding: 0;
  /* Removes default padding */
}

/* Ensure .main-page fills the available space */
.developer-company-page {
  display: flex;
  min-height: 100vh;
  /* Ensures it spans the full viewport height */
  background-color: #f6f6f6;
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
  margin-top: 30px;
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

/* Styling for the file input and image preview section */
input[type="file"] {
  border: 1px solid #ccc;
  border-radius: 8px;
}

/* Styling for the text area */
textarea {
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
  padding: 10px;
  transition: border-color 0.3s ease;
}

textarea:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* Button Styling */
.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
  font-weight: 600;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}

.user-info {
  margin-bottom: 20px;
  text-align: left;
}

.btn-save {
  background-color: #42b983; /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px; /* Adjust the border radius */
  padding: 10px;
}
</style>
