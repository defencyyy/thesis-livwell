<template>
  <div class="developer-milestones-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <!-- Milestones Section -->
        <div class="title-wrapper">
          <div class="title-icon"></div>
          <div class="edit-title">Milestones</div>
        </div>
        <div
          class="card shadow-lg border-0 rounded-3 mx-auto"
          style="max-width: 900px"
        >
          <div class="card-body">
            <!-- Milestones Table -->
            <table class="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Description</th>
                  <th>Reward</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="milestone in milestones" :key="milestone.id">
                  <td>{{ milestone.name }}</td>
                  <td>{{ milestone.description || "N/A" }}</td>
                  <td>{{ milestone.reward }}</td>
                  <td>
                    <button
                      @click="editMilestone(milestone)"
                      class="btn btn-warning btn-sm"
                    >
                      Edit
                    </button>
                    <button
                      @click="deleteMilestone(milestone.id)"
                      class="btn btn-danger btn-sm"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <!-- Add Milestone Button -->
            <div class="d-flex justify-content-end mt-3">
              <button @click="showAddForm = true" class="btn btn-primary">
                Add Milestone
              </button>
            </div>
          </div>
        </div>

        <!-- Add/Edit Milestone Modal -->
        <div v-if="showAddForm" class="modal show d-block" tabindex="-1">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">
                  {{ newMilestone.id ? "Edit Milestone" : "Add Milestone" }}
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  @click="closeForm"
                ></button>
              </div>
              <div class="modal-body">
                <div class="mb-3">
                  <label for="milestoneName" class="form-label">Name</label>
                  <input
                    type="text"
                    class="form-control"
                    id="milestoneName"
                    v-model="newMilestone.name"
                    placeholder="Enter milestone name"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="milestoneDescription" class="form-label"
                    >Description</label
                  >
                  <textarea
                    class="form-control"
                    id="milestoneDescription"
                    v-model="newMilestone.description"
                    rows="4"
                    placeholder="Enter description"
                    required
                  ></textarea>
                </div>
                <div class="mb-3">
                  <label for="milestoneReward" class="form-label">Reward</label>
                  <input
                    type="text"
                    class="form-control"
                    id="milestoneReward"
                    v-model="newMilestone.reward"
                    placeholder="Enter reward"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="milestoneType" class="form-label"
                    >Milestone Type</label
                  >
                  <select
                    class="form-select"
                    v-model="newMilestone.type"
                    @change="onMilestoneTypeChange"
                  >
                    <option value="sales">Sales</option>
                    <option value="commission">Commission</option>
                  </select>
                </div>
                <!-- Conditional input fields -->
                <div v-if="newMilestone.type === 'sales'" class="mb-3">
                  <label for="salesThreshold" class="form-label"
                    >Sales Threshold</label
                  >
                  <input
                    type="number"
                    class="form-control"
                    id="salesThreshold"
                    v-model="newMilestone.sales_threshold"
                    placeholder="Enter sales threshold"
                  />
                </div>
                <div v-if="newMilestone.type === 'commission'" class="mb-3">
                  <label for="commissionThreshold" class="form-label"
                    >Commission Threshold</label
                  >
                  <input
                    type="number"
                    class="form-control"
                    id="commissionThreshold"
                    v-model="newMilestone.commission_threshold"
                    placeholder="Enter commission threshold"
                  />
                </div>
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click="closeForm"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  class="btn btn-primary"
                  @click="
                    newMilestone.id ? updateMilestone() : createMilestone()
                  "
                >
                  Save
                </button>
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
  name: "DeveloperMilestones",
  components: { SideNav, AppHeader },
  data() {
    return {
      milestones: [],
      showAddForm: false,
      newMilestone: {
        name: "",
        description: "",
        reward: "",
        type: "sales", // Default to 'sales'
        sales_threshold: null,
        commission_threshold: null,
      },
    };
  },
  computed: {
    ...mapState({
      companyId: (state) => state.companyId, // Using Vuex to access company ID
    }),
  },
  mounted() {
    if (!this.companyId) {
      this.$router.push({ name: "DevLogin" }); // Redirect if company ID is not available
    } else {
      this.fetchMilestones();
    }
  },
  methods: {
    // Axios instance with token handling
    getAxiosInstance() {
      const instance = axios.create({
        baseURL: "http://localhost:8000/developer/",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          "Content-Type": "application/json",
        },
      });

      // Interceptor for refreshing token if expired
      instance.interceptors.response.use(
        (response) => response,
        async (error) => {
          if (error.response && error.response.status === 401) {
            // Handle token refresh if expired
            try {
              const refreshResponse = await axios.post(
                "http://localhost:8000/auth/refresh/",
                { refresh: localStorage.getItem("refreshToken") }
              );

              if (refreshResponse.status === 200) {
                localStorage.setItem(
                  "accessToken",
                  refreshResponse.data.access
                );
                error.config.headers.Authorization = `Bearer ${refreshResponse.data.access}`;
                return axios(error.config); // Retry the original request with new token
              }
            } catch (refreshError) {
              console.error("Error refreshing token:", refreshError);
              this.$router.push({ name: "Login" }); // Redirect to login if token refresh fails
            }
          }
          return Promise.reject(error);
        }
      );

      return instance;
    },

    // Fetch all milestones
    async fetchMilestones() {
      const axiosInstance = this.getAxiosInstance();
      try {
        const response = await axiosInstance.get("milestones/");
        if (response.status === 200) {
          this.milestones = response.data;
        }
      } catch (error) {
        console.error("Error fetching milestones:", error);
      }
    },

    // Create a new milestone
    async createMilestone() {
      const axiosInstance = this.getAxiosInstance();
      const url = "http://localhost:8000/developer/milestones/";

      // Add the company ID from Vuex state to the milestone
      const milestoneData = { ...this.newMilestone, company: this.companyId };

      try {
        const response = await axiosInstance.post(url, milestoneData);
        if (response.status === 201) {
          this.fetchMilestones();
          this.closeForm();
        }
      } catch (error) {
        console.error("Error saving new milestone:", error);
      }
    },

    // Update an existing milestone
    async updateMilestone() {
      if (
        !window.confirm(
          "Are you sure you want to edit this milestone? Unsaved changes will be lost."
        )
      ) {
        return; // Exit if the user cancels
      }
      const axiosInstance = this.getAxiosInstance();
      const url = `http://localhost:8000/developer/milestones/${this.newMilestone.id}/`;

      // Add the company ID from Vuex state to the milestone
      const milestoneData = { ...this.newMilestone, company: this.companyId };

      try {
        const response = await axiosInstance.put(url, milestoneData);
        if (response.status === 200) {
          this.fetchMilestones();
          this.closeForm();
        }
      } catch (error) {
        console.error("Error updating milestone:", error);
      }
    },

    async deleteMilestone(milestoneId) {
      if (!window.confirm("Are you sure you want to delete this milestone?")) {
        return; // Exit if the user cancels
      }

      const axiosInstance = this.getAxiosInstance();
      const url = `http://localhost:8000/developer/milestones/${milestoneId}/`;

      try {
        const response = await axiosInstance.delete(url);
        if (response.status === 204) {
          this.fetchMilestones(); // Refresh the list after deletion
        }
      } catch (error) {
        console.error("Error deleting milestone:", error);
      }
    },

    editMilestone(milestone) {
      this.newMilestone = { ...milestone };
      this.showAddForm = true;
    },

    // Handle changes in milestone type selection
    onMilestoneTypeChange() {
      // Reset thresholds when changing type
      if (this.newMilestone.type === "sales") {
        this.newMilestone.sales_threshold = null;
      } else if (this.newMilestone.type === "commission") {
        this.newMilestone.commission_threshold = null;
      }
    },

    // Close the form modal
    closeForm() {
      this.showAddForm = false;
      this.newMilestone = {
        name: "",
        description: "",
        reward: "",
        type: "sales",
        sales_threshold: null,
        commission_threshold: null,
      };
    },
  },
};
</script>

<style scoped>
/* Styles similar to the Document page */
html,
body {
  height: 100%;
  margin: 0;
  /* Removes default margin */
  padding: 0;
  /* Removes default padding */
}

/* Ensure .main-page fills the available space */
.developer-milestones-page {
  display: flex;
  min-height: 100vh;
  /* Ensures it spans the full viewport height */
  background-color: #e8f0fa;
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

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.card-body {
  padding: 2.5rem;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  vertical-align: middle;
}

.table th {
  background-color: #f8f9fa;
  font-weight: bold;
}

.table td {
  background-color: #ffffff;
}

.btn-warning {
  background-color: #ffc107;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-primary {
  padding: 8px 12px;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  font-size: 14px;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.modal-dialog {
  max-width: 500px;
}

.modal-header {
  background-color: #f8f9fa;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  background-color: #f8f9fa;
}

.btn-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: #000;
}
</style>
