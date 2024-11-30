<template>
  <div class="developer-company-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="container mt-5">
        <!-- Company Details Section -->
        <div class="title-wrapper">
          <div class="title-icon"></div>
          <div class="edit-title">Company Details</div>
        </div>
        <div
          class="card shadow-lg border-0 rounded-3 mx-auto"
          style="max-width: 900px"
        >
          <div class="card-body">
            <div class="row">
              <!-- Company Information -->
              <div class="col-md-8">
                <p class="mb-2">
                  <strong>Company Name:</strong> {{ company.name || "N/A" }}
                </p>
                <p>
                  <strong>Company Description:</strong>
                  {{ company.description || "N/A" }}
                </p>
              </div>
              <!-- Company Logo -->
              <div class="col-md-4 text-center">
                <strong>Company Logo:</strong>
                <div class="mt-2">
                  <img
                    v-if="company.logo"
                    :src="getLogoUrl(company.logo)"
                    alt="Company Logo"
                    class="img-fluid rounded shadow-sm"
                    style="max-width: 150px; max-height: 150px"
                  />
                  <span v-else>No Logo Available</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="title-wrapper">
          <div class="title-icon"></div>
          <div class="edit-title">Edit Company Details</div>
        </div>
        <div
          class="card shadow-lg border-0 rounded-3 mx-auto"
          style="max-width: 900px"
        >
          <div class="card-body">
            <div class="row">
              <!-- Right Section: Description -->
              <div class="col-md-6 order-md-2">
                <div class="mb-3">
                  <label for="tempDescription" class="form-label"
                    >Description</label
                  >
                  <textarea
                    class="form-control"
                    id="description"
                    v-model="tempDescription"
                    rows="6"
                    placeholder="Enter company description"
                  ></textarea>
                </div>
                <div class="d-flex justify-content-end">
                  <button @click="updateCompany" class="btn btn-primary">
                    Save Changes
                  </button>
                </div>
              </div>

              <!-- Left Section: Upload Photo -->
              <div
                class="col-md-6 order-md-1 d-flex flex-column align-items-center"
              >
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
                  <strong>Preview:</strong>
                  <img
                    v-if="previewLogo"
                    :src="previewLogo"
                    alt="Logo Preview"
                    width="100"
                  />
                  <p v-else>No logo selected</p>
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
      tempDescription: "",
      newLogo: null,
      previewLogo: null,
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
    localStorageUserId() {
      return localStorage.getItem("user_id");
    },
    localStorageCompanyId() {
      return localStorage.getItem("company_id");
    },
  },

  mounted() {
    this.fetchCompany();
  },

  methods: {
    async fetchCompany() {
      const companyId = this.vuexCompanyId;

      if (!companyId) {
        alert("Company ID not found. Please log in.");
        this.$router.push({ name: "DevLogin" });
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
          this.tempDescription = response.data.description; // Set tempDescription
        } else {
          alert("Error fetching company details.");
        }
      } catch (error) {
        if (error.response.status === 401) {
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
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      this.$router.push({ name: "DevLogin" });
    },
    async updateCompany() {
      try {
        const formData = new FormData();

        // Only append the description if it has changed
        if (this.tempDescription !== this.company.description) {
          formData.append("description", this.tempDescription); // Use tempDescription
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
          // Update company description after saving
          this.company.description = this.tempDescription;
          this.fetchCompany(); // Refresh company data
          this.previewLogo = null; // Clear preview after successful update
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
      console.log("File selected:", file);
      if (file) {
        this.newLogo = file;
        const reader = new FileReader();
        reader.onload = () => {
          this.previewLogo = reader.result;
          console.log("Preview logo set:", this.previewLogo);
        };
        reader.readAsDataURL(file);
      }
    },
    getLogoUrl(logo) {
      return `http://localhost:8000${logo}`;
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
  background-color: #6c757d;
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

img {
  object-fit: cover;
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
</style>
