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
                    class="img-fluid shadow-sm rounded"
                    style="width: 100%; height: 100%; object-fit: contain"
                  />
                  <span v-else>No Logo Available</span>
                </div>
                <h5 class="mt-4" style="font-weight: bold">
                  {{ company.name || "Company Information" }}
                </h5>
              </div>

              <div class="col-md-8">
                <div class="mb-3">
                  <small style="font-size: 14px; color: #6c757d; padding: 2px; text-align: left; display: block">Upload Logo</small>
                  <input
                    type="file"
                    class="form-control"
                    id="logo"
                    accept="image/*"
                    @change="onFileChange"
                  />
                </div>

                <div class="mb-3">
                  <small style="font-size: 14px; color: #6c757d; padding: 2px; text-align: left; display: block">Company Description</small>
                  <textarea
                    class="form-control"
                    id="companyDescription"
                    v-model="company.description"
                    rows="6"
                    placeholder="Enter company description"
                  ></textarea>
                </div>

                <div
                  class="d-flex justify-content-end gap-2 mt-30"
                  style="padding-top: 15px"
                >
                  <button
                    @click="
                      showConfirmation(
                        'Are you sure you want to save these changes?',
                        updateCompany,
                        []
                      )
                    "
                    class="btn-save"
                  >
                    Save Changes
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <b-modal
          v-model="showNotification"
          :title="notificationTitle"
          hide-footer
          hide-header
          centered
        >
          <div class="modal-title p-3">
            <i
              :class="notificationIcon()"
              style="margin-right: 10px; font-size: 22px"
            ></i>
            <h5 class="custom-title mb-0">{{ notificationTitle }}</h5>
          </div>

          <div class="p-3">
            <p>{{ notificationMessage }}</p>
            <div
              class="d-flex justify-content-end gap-2"
              style="margin-top: 30px"
            >
              <button
                type="button"
                @click="showNotification = false"
                class="btn-cancel"
                style="width: 100px"
              >
                Close
              </button>
            </div>
          </div>
        </b-modal>

        <!-- Confirmation Modal -->
        <!-- Confirmation Modal -->
        <b-modal
          v-model="showConfirmModal"
          :title="'Confirmation'"
          hide-footer
          hide-header
          centered
        >
          <div class="modal-title p-3">
            <i
              class="fas fa-info-circle text-secondary"
              style="margin-right: 10px; font-size: 22px"
            ></i>
            <h5 class="custom-title mb-0">Confirmation</h5>
          </div>

          <div class="p-3">
            <p>{{ confirmMessage }}</p>

            <div
              class="d-flex justify-content-end gap-2"
              style="margin-top: 30px"
            >
              <button type="button" @click="confirmAction" class="btn-add">
                Confirm
              </button>

              <button type="button" @click="cancelAction" class="btn-cancel">
                Cancel
              </button>
            </div>
          </div>
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";
import { mapState } from "vuex";
import { BModal } from "bootstrap-vue-3";

export default {
  name: "DevCompany",
  components: { SideNav, AppHeader, BModal },

  data() {
    return {
      company: {},
      newLogo: null,
      showNotification: false,
      notificationTitle: "",
      notificationType: "",
      notificationMessage: "",

      // Modal confirmation states
      showConfirmModal: false,
      confirmMessage: "",
      actionToConfirm: null,
      confirmParams: [],
    };
  },

  computed: {
    ...mapState({
      userId: (state) => state.userId,
      userType: (state) => state.userType,
      companyId: (state) => state.companyId,
      loggedIn: (state) => state.loggedIn,
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
    }
  },

  methods: {

    promptCompanyUpdate() {
      this.showConfirmation(
        "Are you sure you want to update your account?",
        this.updateCompany,
        []
      );
    },

    notificationIcon() {
      if (this.notificationType === "success") {
        return "fas fa-check-circle text-success"; // Green check icon
      } else if (this.notificationType === "error") {
        return "fas fa-exclamation-circle text-danger"; // Red error icon
      }
      return ""; // Default or no icon
    },

    // Fetch company data
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
        console.error("Error fetching company data:", error);
        alert("Error fetching company data.");
      }
    },

    // Show the confirmation modal with dynamic message and action
    showConfirmation(message, action, params) {
      this.confirmMessage = message;
      this.actionToConfirm = action;
      this.confirmParams = params;
      this.showConfirmModal = true;
    },

    // Cancel the action
    cancelAction() {
      this.showConfirmModal = false; // Close modal on cancel
    },

    // Confirm the action
    async confirmAction() {
      try {
        await this.actionToConfirm(...this.confirmParams);
        this.showConfirmModal = false; // Close modal after confirmation
      } catch (error) {
        this.showConfirmModal = false; // Close modal on error
        this.notificationTitle = "Error";
        this.notificationType = "error";
        this.notificationMessage = "An error occurred during the action.";
        this.showNotification = true;
      }
    },

    // Handle file change
    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.newLogo = file;
      }
    },

    // Get logo URL
    getLogoUrl(logo) {
      return `http://localhost:8000${logo}`;
    },

    // Update company details
    async updateCompany() {
      try {
        const formData = new FormData();

        if (this.company.description !== this.company.originalDescription) {
          formData.append("description", this.company.description);
        }

        if (this.newLogo) {
          formData.append("logo", this.newLogo);
        }

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
          this.fetchCompany();
          this.notificationTitle = "Success";
          this.notificationType = "success";
          this.notificationMessage = "Company updated successfully!";
          this.showNotification = true;
          this.company.originalDescription = this.company.description;
        } else {
          this.notificationTitle = "Error";
          this.notificationType = "error";
          this.notificationMessage =
            "An error occurred while updating the company.";
          this.showNotification = true;
        }
      } catch (error) {
        console.error("Error updating company:", error);
        this.notificationTitle = "Error";
        this.notificationType = "error";
        this.notificationMessage = "An unexpected error occurred.";
        this.showNotification = true;
      }
    },

    // Redirect to login page
    redirectToLogin() {
      this.$router.push({ name: "DevLogin" });
    },
  },
};
</script>

<style scoped>
/* Global styles */
html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

/* Developer page styles */
.developer-company-page {
  display: flex;
  min-height: 100vh;
  background-color: #eff4fb;
}

.SideNav {
  width: 250px;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  z-index: 1;
}

.AppHeader {
  width: 100%;
  height: 60px;
  display: flex;
  align-items: center;
  padding-left: 10px;
}

.main-content {
  display: flex;
  flex-direction: column;
  margin-top: 30px;
  margin-left: 250px;
  flex: 1;
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

/* Title wrapper and text styles */
.title-wrapper {
  display: flex;
  align-items: center;
  margin-top: 20px;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.edit-title {
  color: #000;
  margin-bottom: 0.8rem;
  text-align: left;
  font-weight: bold;
}

.title-icon {
  width: 15px;
  height: 5px;
  background-color: #343a40;
  border-radius: 5px;
  margin-right: 10px;
  margin-bottom: 15px;
}

/* Input and textarea styles */
input[type="file"] {
  border: 1px solid #ccc;
  border-radius: 8px;
}

textarea {
  border-radius: 8px;
  border: 1px solid #ccc;
  padding: 10px;
}

textarea:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* Button styles */
.btn-save {
  background-color: #0560fd;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 10px;
  font-size: 14px;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
  font-weight: 600;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
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

.custom-title {
  font-style: normal;
  font-size: 20px;
}

.modal-title {
  display: flex;
  /* Use Flexbox for side-by-side layout */
  align-items: center;
  /* Align icon and text vertically */
}

.btn-cancel {
  background-color: #343a40;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 10px;
}

.btn-add {
  background-color: #0560fd;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
  font-size: 14px;
}
</style>
