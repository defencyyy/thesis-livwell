<template>
  <div class="developer-milestones-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <!-- Milestones Section -->
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">Milestone Management</div>
          </div>
        </div>

        <div class="grid-layout">
          <!-- Left Section -->
          <div class="left-content">
            <div>
              <div class="add-milestones-headers">
                <span class="header-item">Name</span>
                <span class="header-item">Description</span>
                <span class="header-item">Reward</span>
                <span class="header-item">Actions</span>
              </div>

              <div
                v-for="milestone in milestones"
                :key="milestone.id"
                class="card border-0 rounded-1 mx-auto my-2"
                style="box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
              >
                <div class="card-body">
                  <table class="add-milestones-table">
                    <tbody>
                      <tr>
                        <td>
                          <span class="milestone-name">
                            {{ milestone.name }}
                          </span>
                        </td>
                        <td>
                          <span class="milestone-description">
                            {{ milestone.description || "N/A" }}
                          </span>
                        </td>
                        <td>
                          <span class="milestone-reward">
                            {{ milestone.reward }}
                          </span>
                        </td>
                        <td>
                          <div class="broker-actions d-flex gap-2">
                            <button
                            @click="editMilestone(milestone)"
                            style="
                              border: none;
                              background-color: transparent;
                              color: #343a40;
                              cursor: pointer;
                              font-size: 18px;
                            "
                            >
                              <i class="fas fa-edit"></i>
                            </button>
                            <!-- <button
                              @click="deleteMilestone(milestone.id)"
                              style="
                                border: none;
                                background-color: transparent;
                                color: #343a40;
                                cursor: pointer;
                                font-size: 18px;
                              "
                            >
                              <i class="fas fa-archive"></i>
                            </button> -->
                          </div>
                    
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            <div class="d-flex justify-content-end mt-3">
              <button @click="showAddForm = true" class="btn-add">
                Add Milestone
              </button>
            </div>
          </div>
          <div class="right-content">
            <div
              class="card border-0 rounded-1 mx-auto"
              style="
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                height: 55vh;
                width: 100%;
              "
            >
              <div class="card-body">
                <div class="row">
                  <div class="toolbar">
                    <div class="left-section"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div style="max-width: 1100px; width: 100%">
          <div
            class="card border-0 rounded-1 mx-auto"
            style="box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
          >
            <div class="card-body">
              <div class="row">
                <div class="toolbar">
                  <div class="left-section">
                    <div class="search-bar-container">
                      <input
                        type="text"
                        v-model="searchQuery"
                        @input="filterSales"
                        placeholder="Search Broker "
                        class="search-bar"
                      />
                      <i class="fa fa-search search-icon"></i>
                    </div>
                    <!-- <select v-model="selectedBroker" @change="filterSales" class="dropdown">
                      <option value="">All Brokers</option>
                      <option v-for="broker in brokers" :key="broker.id" :value="broker.id">
                        {{ broker.first_name }} {{ broker.last_name }}
                      </option>
                    </select>
                    <select v-model="selectedStatus" @change="filterSales" class="dropdown">
                      <option value="">All Status</option>
                      <option value="Pending Reservation">
                        Pending Reservation
                      </option>
                      <option value="Reserved">Reserved</option>
                      <option value="Pending Sold">Pending Sold</option>
                      <option value="Sold">Sold</option>
                    </select> -->
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Add/Edit Milestone Modal -->
        <b-modal
          v-model="showAddForm"
          hide-header
          hide-footer
          centered
          size="lg"
          title="Add/Edit Milestone"
          @hide="closeForm"
        >
          <!-- Modal Title -->
          <div class="modal-title p-3">
            <h5 class="mb-0">
              {{
                newMilestone.id ? "Milestone Details / Edit" : "New Milestone"
              }}
            </h5>
          </div>

          <!-- Modal Body -->
          <div class="p-3">
            <div class="row">
              <!-- Left Section -->
              <div class="col-md-6">
                <!-- Name -->
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

                <!-- Description -->
                <div class="mb-3">
                  <label for="milestoneDescription" class="form-label"
                    >Description</label
                  >
                  <textarea
                    class="form-control"
                    id="milestoneDescription"
                    v-model="newMilestone.description"
                    rows="6"
                    placeholder="Enter description"
                    required
                  ></textarea>
                </div>
              </div>

              <!-- Right Section -->
              <div class="col-md-6">
                <!-- Reward -->
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

                <!-- Milestone Type -->
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

                <!-- Conditional Fields -->
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
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="d-flex justify-content-end gap-3 p-3">
            <button
              type="button"
              class="btn-add"
              style="width: 150px"
              @click="newMilestone.id ? updateMilestone() : createMilestone()"
            >
              Save Changes
            </button>
            <button type="button" class="btn-cancel" @click="closeForm">
              Cancel
            </button>
          </div>
        </b-modal>

        <!-- <div class="mb-3">
          <input type="text" v-model="searchQuery" class="form-control" placeholder="Search brokers by name" />
        </div> -->

        <!-- Table for displaying brokers -->
        <div style="max-width: 1100px; width: 100%">
          <div class="broker-display-headers">
            <span class="header-item">Broker Name</span>
            <span class="header-item">Sales Completed</span>
            <span class="header-item">Milestones Achieved</span>
            <span class="header-item">Commission Collected</span>
            <span class="header-item">Commission Achieved</span>
            <span class="header-item">Action</span>
          </div>
          <div
            v-for="broker in filteredBrokers"
            :key="broker.id"
            class="card border-0 rounded-1 mx-auto my-2"
            style="box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
          >
            <div class="card-body">
              <table class="broker-milestones-table">
                <tbody>
                  <tr>
                    <td>
                      <i class="fas fa-user-tie broker-icon"></i>
                      <span class="broker-name">
                        {{ broker.first_name }} {{ broker.last_name }}
                      </span>
                    </td>
                    <td>
                      <span class="broker-sales">
                        {{ broker.total_sales }}
                      </span>
                    </td>
                    <td>
                      <span class="broker-milestone-count">
                        {{ broker.salesMilestoneCount }}
                      </span>
                    </td>
                    <td>
                      <span class="broker-commission">
                        {{ broker.total_commissions }}
                      </span>
                    </td>
                    <td>
                      <span class="broker-commission-milestone-count">
                        {{ broker.commissionMilestoneCount }}
                      </span>
                    </td>

                    <td>
                      <button
                        @click="viewBrokerMilestones(broker)"
                        class="btn btn-info btn-sm"
                      >
                        View
                      </button>
                      <!-- <button @click="deleteMilestone(milestone.id)" class="btn btn-danger btn-sm">
                            Delete
                          </button> -->
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Broker Milestones Modal -->
        <b-modal
          v-model="showBrokerModal"
          title="Broker Milestones"
          hide-footer
          hide-header
          centered
          size="lg"
        >
          <!-- Modal Header -->
          <div v-if="selectedBroker">
            <div class="modal-title p-3">
              <h5 class="mb-0">
                Broker: {{ selectedBroker.first_name.toUpperCase() }}
                {{ selectedBroker.last_name.toUpperCase() }}
              </h5>
            </div>

            <!-- Modal Body -->
            <div class="modal-body">
              <!-- Broker Info -->
              <div class="mb-4">
                <p>
                  <strong>Sales Completed:</strong>
                  {{ selectedBroker.total_sales }}
                </p>
                <p>
                  <strong>Commissions Collected:</strong> P
                  {{ selectedBroker.total_commissions }}
                </p>
              </div>

              <!-- Milestones Table -->
              <table class="styled-table">
                <thead>
                  <tr>
                    <th>Milestone Name</th>
                    <th>Milestone Type</th>
                    <th>Completed</th>
                    <th>Reward</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="milestone in milestones" :key="milestone.id">
                    <td>{{ milestone.name }}</td>
                    <td>
                      {{ milestone.type === "sales" ? "Sales" : "Commission" }}
                    </td>
                    <td class="text-center">
                      <input
                        type="checkbox"
                        :checked="
                          checkMilestoneCompletion(milestone, selectedBroker)
                        "
                        disabled
                      />
                    </td>
                    <td>{{ milestone.reward }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Modal Footer -->
            <div
              class="d-flex justify-content-end gap-3 mt-3"
              style="padding: 15px"
            >
              <button
                type="button"
                class="btn-cancel"
                @click="showBrokerModal = false"
                style="width: 100px"
              >
                Close
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
import { BModal } from "bootstrap-vue-3";
import axios from "axios";
import { mapState } from "vuex";

export default {
  name: "DeveloperMilestones",
  components: { SideNav, AppHeader, BModal },
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
    formatCurrency(value) {
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "PHP",
      }).format(value);
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
  /* Removes default margin */
  padding: 0;
  /* Removes default padding */
}

/* Ensure .main-page fills the available space */
.developer-milestones-page {
  display: flex;
  min-height: 100vh;
  /* Ensures it spans the full viewport height */
  background-color: #eff4fb;
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
  display: flex;
  /* Use flexbox to center the content */
  align-items: center;
  /* Center vertically */
  flex-direction: column;
  /* Stack the dashboard boxes and sales table vertically */
}

.title-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1100px;
  width: 100%;
  margin: 20px auto;
  /* Center the wrapper */
}

.title-left {
  display: flex;
  align-items: center;
}

.title-icon {
  width: 15px;
  height: 5px;
  background-color: #343a40;
  border-radius: 5px;
  margin-right: 10px;
}

.edit-title {
  color: #000000;
  text-align: left;
  font-weight: bold;
}

.grid-layout {
  display: grid;
  grid-template-columns: 3fr 2fr;
  /* Equal width for both columns */

  gap: 20px;
  /* Match the spacing of the dashboard boxes */
  width: 100%;
  max-width: 1100px;
  /* Match the max-width of the dashboard-boxes */
  margin-bottom: 20px;
}

.left-content {
  display: flex;
  flex-direction: column;
}

.right-content {
  display: flex;
  flex-direction: column;
}

.add-milestones-headers {
  display: grid;
  grid-template-columns: 25% 40% 25% 10%;
  /* Adjust widths for better layout */
  width: 100%;
  padding: 0 15px;
  margin: 12px auto 10px;
}

.broker-display-headers {
  display: grid;
  grid-template-columns: 30% 16% 16% 16% 16% 6%;
  /* Adjust widths for better layout */
  max-width: 1100px;
  width: 100%;
  padding: 0 15px;
  margin: 5px auto 10px;
}

.add-milestones-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background: #fff;
}

.broker-milestones-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background: #fff;
}

.broker-milestones-table th,
.broker-milestones-table td {
  padding-bottom: 5px;
  text-align: left;
  vertical-align: middle;
  border: none;
  /* Remove borders from all cells */
}

.broker-milestones-table th {
  background-color: #f9f9f9;
  font-weight: bold;
}

.add-milestones-table th,
.add-milestones-table td {
  padding-bottom: 5px;
  text-align: left;
  vertical-align: middle;
  border: none;
  /* Remove borders from all cells */
}

.add-milestones-table th {
  background-color: #f9f9f9;
  font-weight: bold;
}

.add-milestones-table th:nth-child(2),
.add-milestones-table td:nth-child(2) {
  /* Location column */
  width: 40%;
}

.add-milestones-table th:nth-child(3),
.add-milestones-table td:nth-child(3) {
  /* Status column */
  width: 25%;
}

.add-milestones-table th:nth-child(4),
.add-milestones-table td:nth-child(4) {
  /* Actions column */
  width: 10%;
}

.broker-milestones-table th:nth-child(2),
.broker-milestones-table td:nth-child(2) {
  /* Location column */
  width: 16%;
}

.broker-milestones-table th:nth-child(3),
.broker-milestones-table td:nth-child(3) {
  /* Status column */
  width: 16%;
}

.broker-milestones-table th:nth-child(4),
.broker-milestones-table td:nth-child(4) {
  /* Actions column */
  width: 16%;
}

.broker-milestones-table th:nth-child(5),
.broker-milestones-table td:nth-child(5) {
  /* Status column */
  width: 16%;
}

.broker-milestones-table th:nth-child(6),
.broker-milestones-table td:nth-child(6) {
  /* Actions column */
  width: 6%;
}

td {
  font-size: 14px;
}

.broker-name {
  font-weight: bold;
  font-size: 14px;
}

.broker-icon {
  font-size: 18px;
  object-fit: cover;
  /* Crop the image if necessary */
  margin-right: 10px;
  /* Adds some spacing between the image and the name */
  color: #343a40;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.btn-add {
  background-color: #0560fd;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
}

.btn-cancel {
  background-color: #343a40;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
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
  /* Space between search bar and dropdown */
}

.search-bar-container {
  position: relative;
  width: 100%;
  max-width: 400px;
  /* Adjust the width as needed */
}

.search-bar {
  width: 400px;
  padding: 8px 12px 8px 40px;
  /* Add left padding to make space for the icon */
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 14px;
}

.search-icon {
  position: absolute;
  top: 50%;
  left: 10px;
  /* Position the icon inside the input */
  transform: translateY(-50%);
  color: #777;
  font-size: 16px;
  pointer-events: none;
  /* Prevent the icon from blocking clicks in the input */
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

.header-item {
  font-size: 14px;
  color: #333;
  font-weight: bold;
  text-align: left;
}

.form-group .form-label,
.row .form-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 14px;
  text-align: center;
}

.styled-table thead tr {
  background-color: #eff4fb;
  color: #333;
  font-weight: bold;
}

.styled-table th,
.styled-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #ddd;
}

.styled-table tbody tr {
  border-bottom: 1px solid #f3f3f3;
}

.styled-table td.text-center {
  text-align: center;
}

.styled-table th {
  cursor: pointer;
  /* Optional if you add sortable columns */
}
</style>
