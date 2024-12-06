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

        <!-- Add a search filter for brokers -->
        <div class="mb-3">
          <input
            type="text"
            v-model="searchQuery"
            class="form-control"
            placeholder="Search brokers by name"
          />
        </div>

        <!-- Table for displaying brokers -->
        <table class="table">
          <thead>
            <tr>
              <th>Broker Name</th>
              <th>Sales Completed</th>
              <th>Sales Milestone Achieved Count</th>
              <th>Commissions Collected</th>
              <th>Commission Milestone Achieved Count</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="broker in filteredBrokers" :key="broker.id">
              <td>{{ broker.first_name }} {{ broker.last_name }}</td>
              <!-- Show full name -->
              <td>{{ broker.total_sales }}</td>
              <td>{{ broker.salesMilestoneCount }}</td>
              <td>P {{ broker.total_commissions }}</td>
              <td>{{ broker.commissionMilestoneCount }}</td>
              <td>
                <button
                  @click="viewBrokerMilestones(broker)"
                  class="btn btn-info btn-sm"
                >
                  View
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <!-- Broker Milestones Modal -->
        <div v-if="showBrokerModal" class="modal show d-block" tabindex="-1">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">
                  Broker Milestones: {{ selectedBroker.first_name }}
                  {{ selectedBroker.last_name }}
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  @click="closeBrokerModal"
                ></button>
              </div>
              <div class="modal-body">
                <!-- Broker Info -->
                <p>
                  <strong>Sales Completed:</strong>
                  {{ selectedBroker.total_sales }}
                </p>
                <p>
                  <strong>Commissions Collected:</strong> P
                  {{ selectedBroker.total_commissions }}
                </p>

                <!-- Milestones Table -->
                <table class="table">
                  <thead>
                    <tr>
                      <th>Milestone Type</th>
                      <th>Milestone Name</th>
                      <th>Completed</th>
                      <th>Description</th>
                      <th>Reward</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="milestone in milestones" :key="milestone.id">
                      <td>
                        {{
                          milestone.type === "sales" ? "Sales" : "Commission"
                        }}
                      </td>
                      <td>{{ milestone.name }}</td>
                      <td>
                        <input
                          type="checkbox"
                          :checked="
                            checkMilestoneCompletion(milestone, selectedBroker)
                          "
                          disabled
                        />
                      </td>
                      <td>{{ milestone.description || "N/A" }}</td>
                      <td>{{ milestone.reward }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click="closeBrokerModal"
                >
                  Close
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
      selectedMilestoneType: "sales", // Default selection
      brokers: [], // List of brokers
      isLoading: false,
      errorMessage: null, // Error message
      searchQuery: "",
      showBrokerModal: false, // This will handle the modal visibility
      selectedBroker: null,
    };
  },
  computed: {
    ...mapState({
      companyId: (state) => state.companyId, // Using Vuex to access company ID
    }),
    filteredBrokers() {
      return this.brokers
        .map((broker) => {
          // Add milestone counts dynamically when mapping the brokers
          broker.salesMilestoneCount = this.getSalesMilestoneCount(broker);
          broker.commissionMilestoneCount =
            this.getCommissionMilestoneCount(broker);
          return broker;
        })
        .filter(
          (broker) =>
            broker.first_name
              .toLowerCase()
              .includes(this.searchQuery.toLowerCase()) ||
            broker.last_name
              .toLowerCase()
              .includes(this.searchQuery.toLowerCase())
        );
    },
  },
  mounted() {
    if (!this.companyId) {
      this.$router.push({ name: "DevLogin" }); // Redirect if company ID is not available
    } else {
      this.fetchMilestones();
      this.fetchBrokers();
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
              this.$router.push({ name: "DevLogin" }); // Redirect to login if token refresh fails
            }
          }
          return Promise.reject(error);
        }
      );

      return instance;
    },

    // Fetch all milestones
    async fetchMilestones() {
      this.isLoading = true;
      this.errorMessage = null;
      const axiosInstance = this.getAxiosInstance();
      try {
        const response = await axiosInstance.get("milestones/");
        if (response.status === 200) {
          this.milestones = response.data;
        }
      } catch (error) {
        this.errorMessage = "Failed to load milestones.";
        console.error("Error fetching milestones:", error);
      } finally {
        this.isLoading = false;
      }
    },

    // Fetch brokers
    async fetchBrokers() {
      const axiosInstance = this.getAxiosInstance();
      try {
        const response = await axiosInstance.get(
          "http://localhost:8000/developer/brokers/"
        );
        if (response.status === 200) {
          this.brokers = response.data;
          this.fetchBrokerProgress(); // Call it here to update counts after brokers are fetched
        }
      } catch (error) {
        console.error("Error fetching brokers:", error);
      }
    },

    async fetchBrokerProgress() {
      this.brokers.forEach((broker) => {
        console.log(broker); // Log broker data

        // No need to check if `broker.sales` is an array, just use the properties
        broker.salesCompleted = this.getSalesCompleted(broker);
        broker.salesMilestoneCount = this.getSalesMilestoneCount(broker);
        broker.commissionsCollected = this.getCommissionsCollected(broker);
        broker.commissionMilestoneCount =
          this.getCommissionMilestoneCount(broker);

        console.log(broker); // Log updated broker data
      });
    },
    getSalesCompleted(broker) {
      console.log("Getting total_sales for broker:", broker);
      console.log("Total sales from backend:", broker.total_sales);
      return broker.total_sales; // Using the total_sales property from the backend
    },

    getSalesMilestoneCount(broker) {
      console.log("Getting sales milestone count for broker:", broker);
      const milestone = this.milestones.find((m) => m.type === "sales");
      console.log("Found milestone:", milestone);
      if (milestone) {
        const milestoneReached =
          broker.total_sales >= milestone.sales_threshold;
        console.log("Sales threshold:", milestone.sales_threshold);
        console.log("Broker total_sales:", broker.total_sales);
        console.log("Milestone reached:", milestoneReached);
        return milestoneReached ? 1 : 0;
      }
      console.log("No milestone found for sales type");
      return 0;
    },

    getCommissionsCollected(broker) {
      console.log("Getting total_commissions for broker:", broker);
      console.log("Total commissions from backend:", broker.total_commissions);
      return broker.total_commissions; // Using the total_commissions property from the backend
    },

    getCommissionMilestoneCount(broker) {
      console.log("Getting commission milestone count for broker:", broker);
      const milestone = this.milestones.find((m) => m.type === "commission");
      console.log("Found commission milestone:", milestone);
      if (milestone) {
        const commissionThresholdReached =
          broker.total_commissions >= milestone.commission_threshold;
        console.log("Commission threshold:", milestone.commission_threshold);
        console.log("Broker total_commissions:", broker.total_commissions);
        console.log(
          "Commission milestone reached:",
          commissionThresholdReached
        );
        return commissionThresholdReached ? 1 : 0;
      }
      console.log("No commission milestone found");
      return 0;
    },
    // Action to view broker's milestones
    viewBrokerMilestones(broker) {
      this.selectedBroker = broker;
      this.showBrokerModal = true;
    },
    // Method to close the broker modal
    closeBrokerModal() {
      this.showBrokerModal = false;
      this.selectedBroker = null;
    },
    // Method to check if a broker has completed a milestone
    checkMilestoneCompletion(milestone, broker) {
      if (milestone.type === "sales") {
        return broker.total_sales >= milestone.sales_threshold;
      } else if (milestone.type === "commission") {
        return broker.total_commissions >= milestone.commission_threshold;
      }
      return false;
    },

    brokerProgress(broker) {
      if (this.selectedMilestoneType === "sales") {
        return broker.total_sales; // Using total sales from the backend
      } else if (this.selectedMilestoneType === "commission") {
        return broker.total_commissions; // Using total commissions from the backend
      }
      return 0;
    },
    // Check if broker meets the milestone
    brokerMeetsMilestone(broker) {
      const milestone = this.milestones.find(
        (m) => m.type === this.selectedMilestoneType
      );

      if (milestone) {
        if (milestone.type === "sales") {
          return (
            (broker.sales || []).filter((sale) => sale.status === "confirmed")
              .length >= milestone.sales_threshold
          );
        } else if (milestone.type === "commission") {
          const totalCommission = (broker.sales || []).reduce(
            (total, sale) => total + (sale.commission || 0),
            0
          );
          return totalCommission >= milestone.commission_threshold;
        }
      }
      return false;
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
        this.errorMessage = "Failed to create milestone.";
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
        this.errorMessage = "Failed to update milestone.";
        console.error("Error updating milestone:", error);
      }
    },

    // Delete a milestone
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
        this.errorMessage = "Failed to delete milestone.";
        console.error("Error deleting milestone:", error);
      }
    },

    // Edit a milestone
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
html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

.main-page {
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
  background-color: #343a40; /* Dark background */
  z-index: 1;
  color: white;
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
  padding: 20px;
}

.content {
  flex: 1;
  text-align: center;
  margin-top: 60px;
}

.title-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1100px;
  margin: 20px auto;
}

.title-left {
  display: flex;
  align-items: center;
}

.edit-title {
  color: #000;
  font-size: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.toggle-button {
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  padding: 5px 10px;
  cursor: pointer;
  font-size: 14px;
}

.toggle-button:hover {
  background-color: #e0e0e0;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-bar-container {
  position: relative;
  width: 100%;
  max-width: 400px;
}

.search-bar {
  width: 100%;
  padding: 8px 12px 8px 40px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.search-icon {
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
  color: #777;
  font-size: 16px;
  pointer-events: none;
}

.dropdown-container {
  position: relative;
}

.dropdown {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  background-color: white;
  color: #333;
}

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  margin-left: auto;
  margin-right: auto;
  max-width: 1100px;
}

.broker-info {
  display: flex;
  align-items: center;
}

.broker-icon {
  width: 20px;
  height: 20px;
  object-fit: cover;
  margin-right: 10px;
  border-radius: 50%;
}

.broker-name {
  font-size: 15px;
  font-weight: bold;
}

.broker-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.broker-table th,
.broker-table td {
  padding: 8px;
  text-align: left;
  vertical-align: middle;
  border-bottom: 1px solid #ddd;
}

.broker-table th {
  background-color: #f8f9fa;
}

.outside-headers {
  display: grid;
  grid-template-columns: 25% 20% 25% 20% 10%;
  padding: 0px 18px;
  margin: 20px auto;
  max-width: 1100px;
}

.header-item {
  font-size: 15px;
  color: #333;
  font-weight: bold;
  text-align: left;
}

.form-group .form-label,
.row .form-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.btn-add,
.btn-cancel {
  padding: 10px;
  border-radius: 3px;
  border: none;
  color: white;
  font-size: 14px;
  cursor: pointer;
}

.btn-add {
  background-color: #42b983;
}

.btn-add:hover {
  background-color: #38a169;
}

.btn-cancel {
  background-color: #343a40;
}

.btn-cancel:hover {
  background-color: #495057;
}
</style>
