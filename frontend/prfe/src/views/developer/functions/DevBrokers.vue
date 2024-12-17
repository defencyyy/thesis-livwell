<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">Company Broker Management</div>
          </div>
          <!-- Header Section -->
          <div class="total-brokers">
            <div>Total Brokers: {{ filteredBrokers.length }}</div>
          </div>
        </div>

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
                      placeholder="Search Broker"
                      class="search-bar"
                    />
                    <i class="fa fa-search search-icon"></i>
                  </div>
                  <!-- Sort Dropdown -->
                  <select v-model="sortBy" class="dropdown">
                    <option value="name">Sort: Name</option>
                    <option value="relative_id">Sort: ID</option>
                  </select>

                  <!-- Sort Order Dropdown -->
                  <select v-model="sortOrder" class="dropdown">
                    <option value="asc">Ascending</option>
                    <option value="desc">Descending</option>
                  </select>
                  <select
                    v-model="viewFilter"
                    @change="toggleView"
                    class="dropdown"
                  >
                    <option value="active">View: Active</option>
                    <option value="archived">View: Archived</option>
                  </select>
                </div>
                <div class="right-section">
                  <button
                    class="btn-primary add-button"
                    @click="showModal = true"
                  >
                    Add Broker
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Broker Table -->
        <div>
          <!-- Headers outside the card -->
          <div class="outside-headers">
            <span class="header-item">ID</span>
            <span class="header-item">Name</span>
            <span class="header-item">Username</span>
            <span class="header-item">Email</span>
            <span class="header-item">Contact</span>
            <span class="header-item">Actions</span>
          </div>

          <div
            v-for="(broker, index) in paginatedBrokers"
            :key="broker.id || index"
            class="card border-0 rounded-1 mx-auto my-2"
            style="box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
          >
            <div class="card-body">
              <table class="broker-table">
                <tbody>
                  <tr>
                    <td>
                      <span class="broker-id">{{
                        broker.relative_id || "?"
                      }}</span>
                    </td>

                    <td>
                      <!-- User Icon as Profile Picture -->
                      <i class="fas fa-user-tie broker-icon"></i>
                      <span class="broker-name">
                        {{ broker.first_name }} {{ broker.last_name }}
                      </span>
                    </td>
                    <td>
                      <span class="broker-username">{{ broker.username }}</span>
                    </td>
                    <td>
                      <span class="broker-email">{{ broker.email }}</span>
                    </td>
                    <td>
                      <span class="broker-contact">{{
                        broker.contact_number
                      }}</span>
                    </td>
                    <td>
                      <div class="broker-actions d-flex">
                        <!-- Edit Button as Icon (Blue) -->
                        <button
                          @click="openEditModal(broker)"
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
                        <!-- Unarchive button for archived view -->
                        <button
                          v-if="showArchived"
                          @click="unarchiveBroker(broker.id)"
                          class="btn btn-sm btn-success"
                          style="
                            border: none;
                            background-color: transparent;
                            color: #343a40;
                            cursor: pointer;
                            font-size: 18px;
                          "
                        >
                          <i class="fas fa-undo"></i>
                        </button>

                        <!-- Archive button for active view -->
                        <button
                          v-else
                          @click="archiveBroker(broker.id)"
                          class="btn btn-sm btn-warning"
                          style="
                            border: none;
                            background-color: transparent;
                            color: #343a40;
                            cursor: pointer;
                            font-size: 18px;
                          "
                        >
                          <i class="fas fa-archive"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Pagination Controls -->
        <nav aria-label="Page navigation example">
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

        <!-- Editing Brokers -->
        <b-modal
          v-model="editModalVisible"
          title="Edit Broker"
          hide-footer
          centered
          hide-header
        >
          <div class="modal-title p-3">
            <h5 class="mb-0">Edit Broker</h5>
          </div>
          <div class="p-3">
            <form @submit.prevent="confirmEdit">
              <!-- First Name -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="editFirstName" class="form-label"
                    >First Name:</label
                  >
                  <input
                    type="text"
                    v-model="editBroker.first_name"
                    id="editFirstName"
                    class="form-control"
                    required
                  />
                </div>

                <!-- Last Name -->
                <div class="col-md-6">
                  <label for="editLastName" class="form-label"
                    >Last Name:</label
                  >
                  <input
                    type="text"
                    v-model="editBroker.last_name"
                    id="editLastName"
                    class="form-control"
                    required
                  />
                </div>
              </div>

              <!-- Username -->
              <div class="form-group mb-3">
                <label for="editUsername" class="form-label">Username:</label>
                <input
                  type="text"
                  v-model="editBroker.username"
                  id="editUsername"
                  class="form-control"
                  required
                />
              </div>

              <!-- Email -->
              <div class="form-group mb-3">
                <label for="editEmail" class="form-label">Email:</label>
                <input
                  type="email"
                  v-model="editBroker.email"
                  id="editEmail"
                  class="form-control"
                  required
                />
              </div>

              <!-- Contact Number -->
              <div class="form-group mb-3">
                <label for="editContactNumber" class="form-label"
                  >Contact Number:</label
                >
                <input
                  type="text"
                  v-model="editBroker.contact_number"
                  id="editContactNumber"
                  class="form-control"
                  required
                />
                <p v-if="contactNumberError" class="text-danger">
                  {{ contactNumberError }}
                </p>
              </div>

              <!-- Buttons -->
              <div
                class="d-flex justify-content-end gap-3 mt-3"
                style="padding-top: 15px"
              >
                <button type="submit" class="btn-add" style="width: 150px">
                  Save Changes
                </button>
                <button
                  type="button"
                  @click="editModalVisible = false"
                  class="btn-cancel"
                >
                  Cancel
                </button>
              </div>
            </form>

            <p v-if="error" class="text-danger">{{ error }}</p>
          </div>
        </b-modal>
        <!-- Modal for Adding Broker -->
        <b-modal v-model="showModal" hide-header hide-footer centered>
          <div class="modal-title p-3">
            <h5 class="mb-0">New Broker</h5>
          </div>

          <div class="p-3">
            <form @submit.prevent="addBroker">
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="firstName" class="form-label">First Name:</label>
                  <input
                    type="text"
                    v-model="firstName"
                    id="firstName"
                    class="form-control"
                    required
                  />
                  <p v-if="firstNameError" class="text-danger">
                    {{ firstNameError }}
                  </p>
                </div>

                <div class="col-md-6">
                  <label for="lastName" class="form-label">Last Name:</label>
                  <input
                    type="text"
                    v-model="lastName"
                    id="lastName"
                    class="form-control"
                    required
                  />
                  <p v-if="lastNameError" class="text-danger">
                    {{ lastNameError }}
                  </p>
                </div>
              </div>

              <div class="form-group mb-3">
                <label for="email" class="form-label">Email:</label>
                <input
                  type="email"
                  v-model="email"
                  id="email"
                  class="form-control"
                  required
                />
                <p v-if="emailError" class="text-danger">{{ emailError }}</p>
              </div>

              <div class="form-group mb-3">
                <label for="contactNumber" class="form-label"
                  >Contact Number:</label
                >
                <input
                  type="text"
                  v-model="contactNumber"
                  id="contactNumber"
                  class="form-control"
                  :required="!editModalVisible"
                />
                <p v-if="contactNumberError" class="text-danger">
                  {{ contactNumberError }}
                </p>
              </div>

              <div class="form-group mb-3">
                <label for="password" class="form-label">Password:</label>
                <input
                  type="password"
                  v-model="password"
                  id="password"
                  class="form-control"
                  required
                />
                <p v-if="passwordError" class="text-danger">
                  {{ passwordError }}
                </p>
              </div>

              <!-- Submit & Cancel Buttons -->
              <div
                class="d-flex justify-content-end gap-2 mt-30"
                style="padding-top: 15px"
              >
                <button type="submit" class="btn-add" style="width: 150px">
                  Add New Broker
                </button>
                <button
                  type="button"
                  @click="showModal = false"
                  class="btn-cancel"
                >
                  Cancel
                </button>
              </div>
            </form>
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
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "DeveloperBrokers",

  components: {
    SideNav,
    AppHeader,
    BModal,
  },

  data() {
    return {
      // State management
      showModal: false,
      showArchived: false,
      viewFilter: "active",

      // Form fields
      firstName: "",
      lastName: "",
      email: "",
      contactNumber: "",
      password: "",

      // Brokers data
      brokers: [],
      archivedBrokers: [],
      searchQuery: "",
      sortBy: "relative_id", // Default sort field
      sortOrder: "asc",

      // Pagination
      currentPage: 1,
      itemsPerPage: 10,

      // Edit modal
      editModalVisible: false,
      editBroker: {},
      originalBroker: {},

      // Error and notification tracking
      error: null,
      successMessage: null,
      emailError: null,
      contactNumberError: null,
      lastNameError: null,
      firstNameError: null,
      passwordError: null,

      // Confirmation modal
      showConfirmModal: false,
      confirmMessage: "",
      actionToConfirm: null,
      confirmParams: [],

      // Notifications
      showNotification: false,
      notificationTitle: "",
      notificationMessage: "",
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

    filteredBrokers() {
      const brokers = this.showArchived ? this.archivedBrokers : this.brokers;

      // Apply search filter
      let filtered = brokers;
      if (this.searchQuery) {
        filtered = brokers.filter((broker) =>
          Object.values(broker)
            .join(" ")
            .toLowerCase()
            .includes(this.searchQuery.toLowerCase())
        );
      }

      // Apply sorting based on the selected field
      return filtered.sort((a, b) => {
        let fieldA, fieldB;

        if (this.sortBy === "relative_id") {
          fieldA = a.relative_id?.toString().toLowerCase() || "";
          fieldB = b.relative_id?.toString().toLowerCase() || "";
        } else {
          fieldA = a.last_name?.toString().toLowerCase() || "";
          fieldB = b.last_name?.toString().toLowerCase() || "";
        }

        if (this.sortOrder === "asc") {
          return fieldA.localeCompare(fieldB, undefined, { numeric: true });
        } else {
          return fieldB.localeCompare(fieldA, undefined, { numeric: true });
        }
      });
    },

    paginatedBrokers() {
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
    this.fetchBrokers();
    if (!this.loggedIn || this.userType !== "developer" || !this.companyId) {
      this.redirectToLogin();
    }
  },

  watch: {
    loggedIn(newVal) {
      if (!newVal || this.userType !== "developer" || !this.companyId) {
        this.redirectToLogin();
      }
    },
    userType(newVal) {
      if (newVal !== "developer" || !this.companyId) {
        this.redirectToLogin();
      }
    },
    companyId(newVal) {
      if (!newVal || this.userType !== "developer") {
        this.redirectToLogin();
      }
    },
  },

  methods: {
    // Confirmation methods
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
        this.showConfirmModal = false;
      } catch (error) {
        this.showConfirmModal = false;
        this.notificationTitle = "Error";
        this.notificationMessage = "An error occurred during the action.";
        this.showNotification = true;
      }
    },

    // Navigation methods
    goToPage(pageNumber) {
      if (pageNumber > 0 && pageNumber <= this.totalPages) {
        this.currentPage = pageNumber;
      }
    },

    redirectToLogin() {
      this.$router.push({ name: "DevLogin" });
    },

    toggleView() {
      this.showArchived = !this.showArchived;
      this.showArchived ? this.fetchArchivedBrokers() : this.fetchBrokers();
    },

    // Fetch data methods
    async fetchBrokers() {
      if (!this.vuexCompanyId) {
        alert("Company ID not found. Please log in.");
        this.redirectToLogin();
        return;
      }
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/brokers/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.brokers = response.data;
      } catch (error) {
        console.error("Error fetching brokers:", error.response || error);
        this.error = "Failed to load brokers.";
      }
    },

    async fetchArchivedBrokers() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/brokers/archived/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.archivedBrokers = response.data;
      } catch (error) {
        console.error("Error fetching archived brokers:", error);
        this.error = "Failed to load archived brokers.";
      }
    },

    // Edit broker methods
    openEditModal(broker) {
      if (!broker || !broker.id) {
        console.error("Invalid broker object:", broker);
        return;
      }
      this.editBroker = { ...broker };
      this.originalBroker = { ...broker }; // Store the original values
      this.editModalVisible = true;
      this.resetForm();
    },

    async confirmEdit() {
      // Check if any values have changed
      const hasChanges = Object.keys(this.editBroker).some(
        (key) => this.editBroker[key] !== this.originalBroker[key]
      );

      if (!hasChanges) {
        this.notificationTitle = "No Changes";
        this.notificationMessage = "No changes made to broker.";
        this.showNotification = true;
        return; // Exit early, no need to continue with save
      }

      // Continue with the update if changes exist
      this.contactNumberError = null;
      this.showConfirmation(
        "Are you sure you want to save these changes?",
        this.saveBrokerEdit,
        [this.editBroker]
      );
    },

    async saveBrokerEdit(broker) {
      try {
        const payload = { ...broker };
        if (!payload.password) delete payload.password;
        await axios.put(
          `http://localhost:8000/developer/brokers/${broker.id}/`,
          payload,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.notificationTitle = "Success";
        this.notificationMessage = "Broker updated successfully!";
        this.showNotification = true;
        this.editModalVisible = false;
        this.fetchBrokers();
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage =
          "An error occurred while updating the broker.";
        this.showNotification = true;
      }
    },

    // Archive and unarchive methods
    async archiveBroker(brokerId) {
      this.showConfirmation(
        "Are you sure you want to archive this broker?",
        this.executeArchive,
        [brokerId]
      );
    },

    async executeArchive(brokerId) {
      await this.updateBrokerArchiveStatus(brokerId, true);
    },

    async unarchiveBroker(brokerId) {
      this.showConfirmation(
        "Are you sure you want to unarchive this broker?",
        this.executeUnarchive,
        [brokerId]
      );
    },

    async executeUnarchive(brokerId) {
      await this.updateBrokerArchiveStatus(brokerId, false);
    },

    async updateBrokerArchiveStatus(brokerId, status) {
      try {
        await axios.put(
          `http://localhost:8000/developer/brokers/${brokerId}/`,
          { archived: status },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.notificationTitle = "Success";
        this.notificationMessage = `Broker ${
          status ? "archived" : "unarchived"
        } successfully!`;
        this.showNotification = true;
        status ? this.fetchBrokers() : this.fetchArchivedBrokers();
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage = `An error occurred while ${
          status ? "archiving" : "unarchiving"
        } the broker.`;
        this.showNotification = true;
      }
    },

    async addBroker() {
      if (this.validateForm()) {
        try {
          await axios.post(
            "http://localhost:8000/developer/brokers/add/",
            {
              first_name: this.firstName,
              last_name: this.lastName,
              email: this.email,
              password: this.password,
              contact_number: this.contactNumber,
            },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
            }
          );

          this.resetForm();
          this.notificationTitle = "Success";
          this.notificationMessage = "Broker created successfully!";
          this.showNotification = true;
          this.showModal = false;
          this.fetchBrokers();
        } catch (error) {
          this.notificationTitle = "Error";
          this.notificationMessage = "An error occurred while adding broker.";
          this.showNotification = true;
        }
      }
    },

    validateForm() {
      // Reset errors
      this.emailError = null;
      this.contactNumberError = null;
      this.lastNameError = null;
      this.firstNameError = null;
      this.passwordError = null;

      // Simple validation logic for each field
      if (!this.email) {
        this.emailError = "Email is required.";
      } else if (!/\S+@\S+\.\S+/.test(this.email)) {
        this.emailError = "Please enter a valid email address.";
      }

      if (!this.firstName) {
        this.firstNameError = "First Name is required.";
      }

      if (!this.lastName) {
        this.lastNameError = "Last Name is required.";
      }

      if (!this.password) {
        this.passwordError = "Password is required.";
      }

      // Contact number validation only if it's not optional in edit mode
      if (this.contactNumber && !/^\+?1?\d{9,15}$/.test(this.contactNumber)) {
        this.contactNumberError =
          "Enter a valid phone number (9 to 15 digits).";
      }

      return !(
        this.emailError ||
        this.contactNumberError ||
        this.firstNameError ||
        this.lastNameError ||
        this.passwordError
      );
    },

    // Form handling
    resetForm() {
      this.firstName =
        this.lastName =
        this.email =
        this.contactNumber =
        this.password =
          "";
      this.emailError =
        this.contactNumberError =
        this.firstNameError =
        this.lastNameError =
        this.passwordError =
          null;
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
.main-page {
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
  margin: 20px;
  text-align: center;
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

.total-broker {
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

.toolbar {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
  padding-left: 20px;
  /* Space on the left side */
  padding-right: 20px;
  /* Space on the right side */
}

.toggle-button {
  margin-left: 10px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  color: #333;
  padding: 5px 10px;
  cursor: pointer;
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
  border-radius: 4px;
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

/* Button Styles */
.btn-primary.add-button {
  padding: 8px 12px;
  border: 1px solid #0560fd;
  border-radius: 3px;
  font-size: 14px;
  background-color: #0560fd;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary.add-button:hover {
  background-color: #0056b3;
}

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  margin-top: 0;
  max-width: 1100px;
  width: 100%;
  /* Ensures the card and grid align */
  margin-left: auto;
  /* Centers the card */
  margin-right: auto;
}

.broker-icon {
  font-size: 18px;
  object-fit: cover;
  /* Crop the image if necessary */
  margin-right: 10px;
  /* Adds some spacing between the image and the name */
  color: #343a40;
}

.broker-name {
  font-size: 14px;
  font-weight: bold;
  margin-top: 10px;
}

.broker-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background: #fff;
  font-size: 14px;
}

.broker-table th,
.broker-table td {
  padding-bottom: 5px;
  text-align: left;
  vertical-align: middle;
  border: none;
  /* Remove borders from all cells */
}

.broker-table th:nth-child(2),
.broker-table td:nth-child(2) {
  /* Location column */
  width: 27%;
}

.broker-table th:nth-child(3),
.broker-table td:nth-child(3) {
  /* Status column */
  width: 25%;
}

.broker-table th:nth-child(4),
.broker-table td:nth-child(4) {
  /* Actions column */
  width: 17%;
}

.broker-table th:nth-child(5),
.broker-table td:nth-child(5) {
  /* Actions column */
  width: 17%;
}

.broker-table th:nth-child(6),
.broker-table td:nth-child(6) {
  /* Actions column */
  width: 7%;
}

.outside-headers {
  display: grid;
  /* Change to grid layout */
  grid-template-columns: 7% 27% 25% 17% 17% 7%;
  /* Match the column widths */
  padding: 0px 15px;
  margin: 20px auto 10px;
  width: 100%;
  max-width: 1100px;
}

.header-item {
  flex: 1;
  text-align: left;
  font-size: 14px;
  color: #333;
  font-weight: bold;
}

.form-group .form-label,
.row .form-label {
  font-size: 0.9rem;
  color: #6c757d;
  /* Adjust the value to your preferred size */
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
  font-size: 14px;
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
  margin: 0 40px;

  /* Adjust line height for compactness */
}

.page-item {
  margin: 0 3px;
  /* Reduce spacing between buttons */
}


/* Ensure the arrow button container has a white background */
.pagination .page-item .page-link {
  background-color: white; /* White background for the arrow container */
  color: #6c757d;  /* Default color for inactive arrows */
  border: 1px solid #ddd;  /* Optional: Add border if you want the arrow container to have a border */
  padding: 8px 12px;
  font-size: 11px;
}


/* Active page color */
.pagination .page-item.active .page-link {
  background-color: #007bff; /* Blue background for active page */
  color: white; /* White text for active page */
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
