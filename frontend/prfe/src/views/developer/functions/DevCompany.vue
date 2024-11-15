<template>
  <div class="developer-company-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="container mt-5">
        <!-- Display Company Details -->
        <div class="title-wrapper">
          <div class="title-icon"></div>
          <div class="edit-title">Company Details</div>
        </div>
        <div class="company-info">
          <p><strong>Company Name:</strong> {{ company.name || "N/A" }}</p>
          <p>
            <strong>Company Description:</strong>
            {{ company.description || "N/A" }}
          </p>
          <div>
            <strong>Company Logo:</strong>
            <img
              v-if="company.logo"
              :src="getLogoUrl(company.logo)"
              alt="Company Logo"
              width="100"
            />
            <span v-else>No Logo Available</span>
          </div>
        </div>
        <!-- Edit Company Details -->
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
              <!-- Left Section -->
              <div class="col-md-6">
                <div class="mb-3">
                  <label for="description" class="form-label"
                    >Description</label
                  >
                  <textarea
                    class="form-control"
                    id="description"
                    v-model="company.description"
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
              <!-- Right Section -->
              <div class="col-md-6 d-flex flex-column align-items-center">
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
        <!-- Debug Information -->
        <h3>Debugging Information</h3>
        <div class="debug-info">
          <p><strong>Vuex User ID:</strong> {{ vuexUserId }}</p>
          <p><strong>Vuex Company ID:</strong> {{ vuexCompanyId }}</p>
          <p><strong>LocalStorage User ID:</strong> {{ localStorageUserId }}</p>
          <p>
            <strong>LocalStorage Company ID:</strong>
            {{ localStorageCompanyId }}
          </p>
          <p><strong>User Role:</strong> {{ userType }}</p>
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
      company: {}, // Holds company details
      newLogo: null, // Stores uploaded file
      previewLogo: null, // Temporary preview of the uploaded logo
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
      return localStorage.getItem("developer_id");
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
      const userId = this.userId || localStorage.getItem("developer_id");
      const companyId = this.companyId || localStorage.getItem("company_id");

      if (!userId || !companyId) {
        alert("Developer or Company ID not found. Please log in.");
        this.$router.push({ name: "DevLogin" });
        return;
      }

      try {
        const response = await axios.get(
          "http://localhost:8000/developer/company/",
          {
            headers: {
              "Developer-ID": userId,
              "Company-ID": companyId,
              "Content-Type": "application/json",
            },
          }
        );

        if (response.status === 200) {
          this.company = {
            name: response.data.company_name,
            description: response.data.company_description,
            logo: response.data.company_logo,
          };
        } else {
          alert("Error fetching company data.");
        }
      } catch (error) {
        console.error("Error fetching company data:", error);
        alert("Error fetching company data.");
      }
    },
    getLogoUrl(logoPath) {
      return logoPath ? `http://localhost:8000${logoPath}` : null;
    },
    onFileChange(event) {
      this.newLogo = event.target.files[0];
      if (this.newLogo) {
        this.previewLogo = URL.createObjectURL(this.newLogo);
      }
    },
    async updateCompany() {
      try {
        const formData = new FormData();
        formData.append("description", this.company.description);

        if (this.newLogo) {
          formData.append("logo", this.newLogo);
        }

        const response = await axios.put(
          "http://localhost:8000/developer/company/edit/",
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
              "Developer-ID": localStorage.getItem("developer_id"),
              "Company-ID": localStorage.getItem("company_id"),
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.status === 200) {
          alert("Company updated successfully!");
          this.fetchCompany(); // Refresh details after update
          this.previewLogo = null; // Clear preview
        } else {
          alert("Error updating company.");
        }
      } catch (error) {
        console.error("Error updating company:", error);
        alert("Error updating company. Please try again.");
      }
    },
  },
};
</script>

<style scoped>
.developer-company-page {
  display: flex;
  height: 100vh;
}

.SideNav {
  width: 250px; /* Set fixed width for the sidebar */
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #343a40;
  z-index: 1;
}

.AppHeader {
  width: 100%;
  height: 60px; /* Adjust height as needed */
  background-color: #343a40;
  display: flex;
  align-items: center;
  padding-left: 10px;
}

.main-content {
  display: flex;
  margin-left: 250px; /* Set margin equal to sidebar width */
  flex-direction: column;
  /* Stack header and content vertically */
  flex: 1;
}

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 2.5rem;
}

.title-wrapper {
  display: flex; /* Align line and title horizontally */
  align-items: center;
  width: 100%;
  max-width: 900px;
  /* Ensure the title width matches the card's width */
  margin-left: auto;
  margin-right: auto;
  /* Center the wrapper */
}

.edit-title {
  color: #000000;
  margin-bottom: 1rem;
  text-align: left;
  /* Align the text to the left */
  background-color: #fff;
  /* Match background with card */
}

.title-icon {
  width: 15px; /* Short horizontal line */
  height: 5px; /* Thin line */
  background-color: #6c757d; /* Line color */
  border-radius: 5px; /* Rounded corners */
  margin-right: 10px; /* Space between the icon and the title */
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

/* .developer-company-page {
  display: flex;
}
.content {
  flex: 1;
  padding: 20px;
  text-align: center;

} */

.user-info {
  margin-bottom: 20px;
  text-align: left;
}
</style>
