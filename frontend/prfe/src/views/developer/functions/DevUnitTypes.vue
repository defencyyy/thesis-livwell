<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">Unit Types Management</div>
          </div>
        </div>

        <b-modal
          ref="createUnitTypeModal"
          v-model="isCreateModalOpen"
          title="Create New Unit Type"
          hide-footer
          hide-header
          centered
        >
          <div class="modal-title p-3">
            <h5 class="mb-0">New Unit Type</h5>
          </div>
          <div class="p-3">
            <form @submit.prevent="createUnitType">
              <div class="form-group">
                <label for="unitTypeName">Unit Type Name:</label>
                <input
                  v-model="newUnitType.name"
                  id="unitTypeName"
                  type="text"
                  class="form-control"
                  placeholder="Enter Unit Type Name"
                  required
                />
              </div>
              <div
                class="d-flex justify-content-end gap-2 mt-3"
                style="padding-top: 15px"
              >
                <button type="submit" class="btn-add">Add Unit Type</button>
                <button
                  type="button"
                  class="btn-cancel"
                  @click="isCreateModalOpen = false"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </b-modal>

        <b-modal
          ref="editUnitTypeModal"
          v-model="isEditModalOpen"
          title="Edit Unit Type"
          hide-footer
          centered
        >
          <form @submit.prevent="updateUnitTypeWithConfirmation">
            <div class="form-group">
              <label for="editUnitTypeName">Unit Type Name:</label>
              <input
                v-model="editedUnitType.name"
                id="editUnitTypeName"
                type="text"
                class="form-control"
                placeholder="Enter Unit Type"
                required
              />
            </div>
            <div
              class="d-flex justify-content-end gap-2 mt-3"
              style="padding-top: 15px"
            >
              <button type="submit" class="btn-add">Update</button>
              <button
                type="button"
                class="btn-cancel"
                @click="isEditModalOpen = false"
              >
                Cancel
              </button>
            </div>
          </form>
        </b-modal>

        <div v-if="loading" class="loading">Loading...</div>

        <div v-else>
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
                        class="search-bar"
                        placeholder="Search by Unit Type Name"
                      />
                      <i class="fa fa-search search-icon"></i>
                    </div>
                    <select
                      v-model="viewFilter"
                      @change="toggleView"
                      class="dropdown"
                    >
                      <option value="active">View: Existing</option>
                      <option value="archived">View: Archived</option>
                    </select>
                  </div>
                  <div class="right-section">
                    <button
                      @click="openCreateTypeModal"
                      class="btn-primary add-button"
                    >
                      Create Unit Type
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="unit-types-list">
            <div>
              <div class="outside-headers">
                <span class="header-item">Name</span>
                <span class="header-item">Category</span>
                <span class="header-item">Actions</span>
              </div>

              <div
                v-for="unitType in filteredUnitTypes"
                :key="unitType.id"
                class="card border-0 rounded-1 mx-auto my-2"
                style="box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
              >
                <div class="card-body">
                  <table class="types-table">
                    <tbody>
                      <tr>
                        <td>
                          {{ unitType.name }}
                        </td>
                        <td>
                          <span v-if="unitType.is_custom">Custom</span>
                          <span v-else>Default</span>
                        </td>
                        <td>
                          <button
                            v-if="!unitType.is_custom && !showArchived"
                            disabled
                            style="
                              background-color: #fff;
                              color: black;
                              border: none;
                            "
                          >
                            Un-Editable
                          </button>
                          <button
                            v-if="
                              unitType.is_custom &&
                              !unitType.is_archived &&
                              !showArchived
                            "
                            @click="openEditModal(unitType)"
                            class="btn btn-sm btn-info"
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

                          <button
                            v-if="
                              unitType.is_custom &&
                              !unitType.is_archived &&
                              !showArchived
                            "
                            @click="archiveUnitType(unitType.id)"
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
                          <button
                            v-if="unitType.is_archived && showArchived"
                            @click="unarchiveUnitType(unitType.id)"
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
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
        <b-modal
          v-model="showConfirmModal"
          :title="'Confirmation'"
          hide-footer
          centered
        >
          <p>{{ confirmMessage }}</p>
          <div class="button-container">
            <!-- Cancel Button -->
            <button
              type="button"
              @click="cancelAction"
              class="btn btn-secondary"
            >
              Cancel
            </button>

            <!-- Confirm Button -->
            <button
              type="button"
              @click="confirmAction"
              class="btn btn-primary"
            >
              Confirm
            </button>
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
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { BModal } from "bootstrap-vue-3";
import { mapState } from "vuex";

export default {
  components: { SideNav, AppHeader, BModal },
  data() {
    return {
      loading: true,
      isLoading: false,
      errorMessage: "",
      unitTypes: [],
      newUnitType: { name: "" },
      isEditModalOpen: false,
      editedUnitType: { id: null, name: "" },
      showArchived: false,
      searchQuery: "",
      isCreateModalOpen: false,
      viewFilter: "active",
      showNotification: false,
      notificationTitle: "",
      notificationMessage: "",
      showConfirmModal: false,
      confirmMessage: "",
      actionToConfirm: null,
      confirmParams: [],
    };
  },

  computed: {
    ...mapState(["companyId"]),
    filteredUnitTypes() {
      const filtered = this.unitTypes.filter((unitType) => {
        const matchesSearch = unitType.name
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase());
        const isArchived = this.showArchived
          ? unitType.is_archived
          : !unitType.is_archived;
        return matchesSearch && isArchived;
      });

      return filtered.sort((a, b) => {
        if (a.is_custom && !b.is_custom) return 1;
        if (!a.is_custom && b.is_custom) return -1;
        return 0;
      });
    },
  },

  methods: {
    // Modal Controls
    openCreateTypeModal() {
      this.isCreateModalOpen = true;
    },

    openEditModal(unitType) {
      this.editedUnitType.id = unitType.id;
      this.editedUnitType.name = unitType.name;
      this.isEditModalOpen = true;
    },

    toggleView() {
      this.showArchived = this.viewFilter === "archived";
    },

    // Fetch Unit Types
    async fetchUnitTypes() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/units/types/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );
        this.unitTypes = response.data.data;
      } catch (error) {
        alert("An error occurred while fetching unit types.");
      } finally {
        this.loading = false;
      }
    },

    // Create Unit Type
    async createUnitType() {
      const data = {
        name: this.newUnitType.name,
        is_custom: true,
        company_id: this.companyId,
      };

      try {
        const response = await axios.post(
          "http://localhost:8000/developer/units/types/",
          data,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (response.status === 201) {
          this.notificationTitle = "Success";
          this.notificationMessage = "Unit-Type created successfully!";
          this.showNotification = true;

          this.unitTypes.push(response.data.data);
          this.newUnitType.name = "";
          this.isCreateModalOpen = false;
        } else {
          this.notificationTitle = "Error";
          this.notificationMessage =
            "An error occurred while creating unit-type.";
          this.showNotification = true;
        }
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage = "Error creating unit type.";
        this.showNotification = true;
      }
    },

    // Update Unit Type
    updateUnitTypeWithConfirmation() {
      this.showConfirmation(
        `Are you sure you want to update this unit type to "${this.editedUnitType.name}"?`,
        this.updateUnitTypeConfirmed,
        []
      );
    },

    async updateUnitTypeConfirmed() {
      try {
        await axios.put(
          `http://localhost:8000/developer/units/types/${this.editedUnitType.id}/`,
          { name: this.editedUnitType.name },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.notificationTitle = "Success";
        this.notificationMessage = "Unit type updated successfully!";
        this.showNotification = true;

        this.fetchUnitTypes();
        this.isEditModalOpen = false;
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage =
          "Failed to update unit type. Please try again.";
        this.showNotification = true;
      }
    },

    // Archive Unit Type
    archiveUnitType(unitTypeId) {
      this.showConfirmation(
        "Are you sure you want to archive this unit type?",
        this.archiveUnitTypeConfirmed,
        [unitTypeId]
      );
    },

    async archiveUnitTypeConfirmed(unitTypeId) {
      try {
        await axios.put(
          `http://localhost:8000/developer/units/types/${unitTypeId}/`,
          { is_archived: true },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.notificationTitle = "Success";
        this.notificationMessage = "Unit type archived successfully!";
        this.showNotification = true;

        this.fetchUnitTypes();
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage =
          "Failed to archive unit type. Please try again.";
        this.showNotification = true;
      }
    },

    // Unarchive Unit Type
    unarchiveUnitType(unitTypeId) {
      this.showConfirmation(
        "Are you sure you want to unarchive this unit type?",
        this.unarchiveUnitTypeConfirmed,
        [unitTypeId]
      );
    },

    async unarchiveUnitTypeConfirmed(unitTypeId) {
      try {
        await axios.put(
          `http://localhost:8000/developer/units/types/${unitTypeId}/`,
          { is_archived: false },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.notificationTitle = "Success";
        this.notificationMessage = "Unit type unarchived successfully!";
        this.showNotification = true;

        this.fetchUnitTypes();
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage =
          "Failed to unarchive unit type. Please try again.";
        this.showNotification = true;
      }
    },

    // Confirmation Modal
    showConfirmation(message, action, params) {
      this.confirmMessage = message;
      this.actionToConfirm = action;
      this.confirmParams = params;
      this.showConfirmModal = true;
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

    cancelAction() {
      this.showConfirmModal = false;
    },
  },

  created() {
    this.fetchUnitTypes();
  },
};
</script>

<style scoped>
/* Add some styles for search input */
.unit-types-search {
  margin-bottom: 20px;
}

.unit-types-search input {
  padding: 8px;
  font-size: 14px;
  width: 300px;
}

html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.main-page {
  display: flex;
  min-height: 100vh;
  background-color: #e8f0fa;
}

.SideNav {
  width: 250px;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #343a40;
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

.unit-types-toggle {
  margin-bottom: 20px;
}

.unit-types-list {
  margin-top: 20px;
}

.unit-type-form {
  margin-bottom: 20px;
}

.loading {
  font-size: 18px;
  color: #888;
}

input {
  padding: 8px;
  font-size: 14px;
  margin-right: 10px;
}

.nav-tabs .nav-link {
  background: none; /* Removes background if you want tabs without a button-like appearance */
  border: none; /* Removes the default button border */
  color: inherit; /* Inherits the text color */
  font-weight: bold; /* Makes text bold */
  font-size: 14px;
}

.nav-tabs .nav-link.active {
  color: #000; /* Active tab color */
  border-bottom: 2px solid #0d6efd;
  font-size: 14px;
}

.title-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1100px;
  margin: 20px auto;
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

.outside-headers {
  display: grid;
  /* Change to grid layout */
  grid-template-columns: 50% 25% 25%;
  /* Match the column widths */
  padding: 0px 18px;
  margin: 20px auto 10px;
  max-width: 1100px;
}

.header-item {
  flex: 1;
  text-align: left;
  font-size: 14px;
  color: #333;
  font-weight: bold;
}

.types-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background: #fff;
  font-size: 14px;
}

.types-table th,
.types-table td {
  padding-bottom: 5px;
  text-align: left;
  vertical-align: middle;
  border: none;
  padding: 7px;
  /* Remove borders from all cells */
}

.types-table th {
  background-color: #f9f9f9;
  font-weight: bold;
}

.types-table th:nth-child(2),
.types-table td:nth-child(2) {
  /* Location column */
  width: 25%;
}

.types-table th:nth-child(3),
.types-table td:nth-child(3) {
  /* Location column */
  width: 25%;
}

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

.form-group label {
  font-size: 0.9rem; /* Lessen the font size */
  color: #6c757d; /* Change color (muted gray) */
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
