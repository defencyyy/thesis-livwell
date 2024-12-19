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
              <DevMilestoneChart />
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
                    <!-- Sort Dropdown -->
                    <select v-model="sortBy" class="dropdown">
                      <option value="total_sales">Sort: Sales</option>
                      <option value="total_commissions">
                        Sort: Commissions
                      </option>
                      <option value="relative_id">Sort: ID</option>
                      <option value="name">Sort: Name</option>
                    </select>

                    <!-- Sort Order Dropdown -->
                    <select v-model="sortOrder" class="dropdown">
                      <option value="asc">Ascending</option>
                      <option value="desc">Descending</option>
                    </select>
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
          :title="newMilestone.id ? 'Edit Milestone' : 'Add Milestone'"
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
                  <small style="font-size: 14px; color: #6c757d; padding: 2px">Milestone Name</small>
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
                  <small style="font-size: 14px; color: #6c757d; padding: 2px">Description</small>
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
                  <small style="font-size: 14px; color: #6c757d; padding: 2px">Reward</small>
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
                  <small style="font-size: 14px; color: #6c757d; padding: 2px">Milestone Type</small>
                  <select
                    class="form-select"
                    v-model="newMilestone.type"
                    @change="onMilestoneTypeChange"
                    :disabled="newMilestone.id"
                  >
                    <option value="sales">Sales</option>
                    <option value="commission">Commission</option>
                  </select>
                </div>

                <!-- Conditional Fields -->
                <div v-if="newMilestone.type === 'sales'" class="mb-3">
                  <small style="font-size: 14px; color: #6c757d; padding: 2px">Sales Threshold</small>
                  <input
                    type="number"
                    class="form-control"
                    id="salesThreshold"
                    v-model="newMilestone.sales_threshold"
                    placeholder="Enter sales threshold"
                    :disabled="newMilestone.id"
                  />
                </div>

                <div v-if="newMilestone.type === 'commission'" class="mb-3">
                  <small style="font-size: 14px; color: #6c757d; padding: 2px">Commission Threshold</small>
                  <input
                    type="number"
                    class="form-control"
                    id="commissionThreshold"
                    v-model="newMilestone.commission_threshold"
                    placeholder="Enter commission threshold"
                    :disabled="newMilestone.id"
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
              {{ newMilestone.id ? "Save Changes" : "Add Milestone" }}
            </button>
            <button type="button" class="btn-cancel" @click="closeForm">
              Cancel
            </button>
          </div>
        </b-modal>

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
            v-for="broker in paginatedMilestones"
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
                      <div class="broker-actions d-flex gap-2">
                        <button
                          @click="viewBrokerMilestones(broker)"
                          style="
                            border: none;
                            background-color: transparent;
                            color: #343a40;
                            cursor: pointer;
                            font-size: 18px;
                          "
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <nav aria-label="Page navigation example" style="max-width: 1100px; width: 100%; padding: 0 !important;">
          <ul class="pagination">
            <li :class="['page-item', { disabled: currentPage === 1 }]">
              <a
                class="page-link"
                href="#"
                @click.prevent="goToPage(currentPage - 1)"
                aria-label="Previous"
              >
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
            <li
              v-for="page in totalPages"
              :key="page"
              :class="['page-item', { active: page === currentPage }]"
            >
              <a class="page-link" href="#" @click.prevent="goToPage(page)">
                {{ page }}
              </a>
            </li>
            <li
              :class="['page-item', { disabled: currentPage === totalPages }]"
            >
              <a
                class="page-link"
                href="#"
                @click.prevent="goToPage(currentPage + 1)"
                aria-label="Next"
              >
                <span aria-hidden="true">&raquo;</span>
              </a>
            </li>
          </ul>
        </nav>

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
        <b-modal
          v-model="showConfirmModal"
          :title="'Confirmation'"
          hide-footer
          centered
        >
          <p>{{ confirmMessage }}</p>
          <div
            class="d-flex justify-content-end gap-2 mt-30"
            style="padding-top: 15px"
          >
            <button
              type="button"
              @click="confirmAction"
              class="btn btn-primary"
            >
              Confirm
            </button>
            <!-- Cancel Button -->
            <button
              type="button"
              @click="cancelAction"
              class="btn btn-secondary"
            >
              Cancel
            </button>
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
import DevMilestoneChart from "@/components/DevMilestoneChart.vue"; // Adjust the path to your actual file location

export default {
  name: "DeveloperMilestones",
  components: { SideNav, AppHeader, BModal, DevMilestoneChart },
  data() {
    return {
      milestones: [],
      selectedMilestone: {},
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

      // Notifications
      showNotification: false,
      notificationTitle: "",
      notificationMessage: "",
      showConfirmModal: false, // Controls modal visibility
      confirmMessage: "", // Stores the confirmation message
      actionToConfirm: null, // Renamed this from 'confirmAction'
      confirmParams: [],
      sortBy: "total_sales", // Default sort by name
      sortOrder: "desc", // Default ascending order
       // Pagination
      currentPage: 1,
      itemsPerPage: 10,
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
        )
        .sort((a, b) => {
          let fieldA, fieldB;

          switch (this.sortBy) {
            case "relative_id":
              fieldA = a.relative_id || 0;
              fieldB = b.relative_id || 0;
              break;
            case "name":
              fieldA =
                a.first_name.toLowerCase() + " " + a.last_name.toLowerCase();
              fieldB =
                b.first_name.toLowerCase() + " " + b.last_name.toLowerCase();
              break;
            case "total_sales":
              fieldA = a.total_sales || 0;
              fieldB = b.total_sales || 0;
              break;
            case "total_commissions":
              fieldA = a.total_commissions || 0;
              fieldB = b.total_commissions || 0;
              break;
            default:
              fieldA = a.first_name.toLowerCase();
              fieldB = b.first_name.toLowerCase();
          }

          if (this.sortOrder === "asc") {
            return fieldA > fieldB ? 1 : fieldA < fieldB ? -1 : 0;
          } else {
            return fieldA < fieldB ? 1 : fieldA > fieldB ? -1 : 0;
          }
        });
    },
    paginatedMilestones() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredBrokers.slice(
        startIndex,
        startIndex + this.itemsPerPage
      );
    },

    totalPages() {
      return Math.ceil(this.filteredBrokers.length / this.itemsPerPage);
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
      goToPage(pageNumber) {
      if (pageNumber > 0 && pageNumber <= this.totalPages) {
        this.currentPage = pageNumber;
      }
    },
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
        broker.salesCompleted = this.getSalesCompleted(broker);
        broker.salesMilestoneCount = this.getSalesMilestoneCount(broker);
        broker.commissionsCollected = this.getCommissionsCollected(broker);
        broker.commissionMilestoneCount =
          this.getCommissionMilestoneCount(broker);
      });
    },

    getSalesCompleted(broker) {
      return broker.total_sales; // Using the total_sales property from the backend
    },

    getSalesMilestoneCount(broker) {
      const milestone = this.milestones.find((m) => m.type === "sales");
      if (milestone) {
        const milestoneReached =
          broker.total_sales >= milestone.sales_threshold;
        return milestoneReached ? 1 : 0;
      }
      return 0;
    },

    getCommissionsCollected(broker) {
      return broker.total_commissions; // Using the total_commissions property from the backend
    },

    getCommissionMilestoneCount(broker) {
      const milestone = this.milestones.find((m) => m.type === "commission");
      if (milestone) {
        const commissionThresholdReached =
          broker.total_commissions >= milestone.commission_threshold;
        return commissionThresholdReached ? 1 : 0;
      }
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
          this.notificationTitle = "Success";
          this.notificationMessage = "Milestone created successfully.";
          this.showNotification = true;
          this.fetchMilestones();
          this.closeForm();
        }
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage =
          "An error occured while creating the new milestone.";
        this.showNotification = true;
      }
    },

    // Update an existing milestone
    updateMilestone() {
      // Check if the milestone has been modified
      if (
        this.newMilestone.name === this.selectedMilestone.name &&
        this.newMilestone.description === this.selectedMilestone.description &&
        this.newMilestone.reward === this.selectedMilestone.reward &&
        this.newMilestone.type === this.selectedMilestone.type &&
        this.newMilestone.sales_threshold ===
          this.selectedMilestone.sales_threshold &&
        this.newMilestone.commission_threshold ===
          this.selectedMilestone.commission_threshold
      ) {
        // If no changes were made
        this.notificationTitle = "Invalid";
        this.notificationMessage = "No changes were made.";
        this.showNotification = true;
        return; // Exit without proceeding further
      }

      // Show the confirmation modal instead of using window.confirm
      const message = "Unsaved changes will be lost. Proceed?";
      const action = this.confirmUpdateMilestone; // The function that handles the update
      const params = [this.newMilestone.id]; // Pass the necessary parameters (milestone ID)

      this.showConfirmation(message, action, params);
    },

    // Action to confirm the update
    async confirmUpdateMilestone(milestoneId) {
      const axiosInstance = this.getAxiosInstance();
      const url = `http://localhost:8000/developer/milestones/${milestoneId}/`;

      // Add the company ID from Vuex state to the milestone
      const milestoneData = { ...this.newMilestone, company: this.companyId };

      try {
        const response = await axiosInstance.put(url, milestoneData);
        if (response.status === 200) {
          this.notificationTitle = "Success";
          this.notificationMessage = "Milestone updated successfully.";
          this.showNotification = true;
          this.fetchMilestones();
          this.closeForm();
        }
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage =
          "An error occurred while editing the milestone.";
        this.showNotification = true;
      }
    },

    // Delete a milestone
    deleteMilestone(milestoneId) {
      // Show the confirmation modal before deleting
      const message = "Are you sure you want to delete this milestone?";
      const action = this.confirmDeleteMilestone; // The function that handles the deletion
      const params = [milestoneId]; // Pass the necessary parameters (milestone ID)

      this.showConfirmation(message, action, params);
    },

    // Action to confirm the deletion
    async confirmDeleteMilestone(milestoneId) {
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

    showConfirmation(message, action, params) {
      this.confirmMessage = message;
      this.actionToConfirm = action;
      this.confirmParams = params;
      this.showConfirmModal = true;
    },
    cancelAction() {
      this.showConfirmModal = false;
    },
    async confirmAction() {
      try {
        await this.actionToConfirm(...this.confirmParams);
        this.showConfirmModal = false; // Close modal after confirmation
      } catch (error) {
        this.showConfirmModal = false; // Close modal on error
        this.notificationTitle = "Error";
        this.notificationMessage = "An error occurred during the action.";
        this.showNotification = true;
      }
    },

    // When clicking the "Edit" button for a milestone
    editMilestone(milestone) {
      // Set the selected milestone to the clicked milestone's data
      this.selectedMilestone = { ...milestone }; // Using spread to avoid direct reference
      this.newMilestone = { ...milestone }; // Initialize newMilestone with selected data
      this.showAddForm = true; // Show the form to edit
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
  font-size: 14px;
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
  appearance: none;
  padding: 8px 12px;
  height: 38px;
  /* Explicitly set height */
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  width: 80%;
  max-width: 150px;
  background-color: white;
  color: #333;
  padding-right: 30px;
  background-image: url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"%3E%3Cpath d="M7 10l5 5 5-5z"/%3E%3C/svg%3E');
  background-position: right 10px center;
  background-repeat: no-repeat;
  background-size: 14px;
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
.pagination {
  display: flex;
  justify-content: flex-end;
  max-width: 1100px;
  width: 100%;
  /* Reduce padding */
  font-size: 12px;
  /* Smaller font size */
  line-height: 1;
  padding: 30px 0;

  /* Adjust line height for compactness */
}

.page-item {
  margin: 0 3px;
  /* Reduce spacing between buttons */
}

/* Ensure the arrow button container has a white background */
.pagination .page-item .page-link {
  background-color: white; /* White background for the arrow container */
  color: #6c757d; /* Default color for inactive arrows */
  border: 1px solid #ddd; /* Optional: Add border if you want the arrow container to have a border */
  padding: 8px 12px;
  font-size: 11px;
}

/* Active page color */
.pagination .page-item.active .page-link {
  background-color: #007bff; /* Blue background for active page */
  color: white; /* White text for active page */
}
</style>
