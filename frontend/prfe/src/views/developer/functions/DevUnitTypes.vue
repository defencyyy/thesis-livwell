<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <!-- Actions -->
        <div class="actions" v-if="!isLoading && !errorMessage">
          <div class="nav nav-tabs">
            <!-- Manage Units Tab -->
            <button
              class="nav-link"
              id="units-tab"
              type="button"
              role="tab"
              aria-selected="false"
              @click="redirectToUnits"
            >
              Manage Units
            </button>

            <!-- Manage Unit Templates Tab -->
            <button
              class="nav-link"
              id="unit-templates-tab"
              type="button"
              role="tab"
              aria-selected="false"
              @click="redirectToUnitTemplates"
            >
              Manage Unit Templates
            </button>

            <!-- Manage Unit Types Tab -->
            <button
              class="nav-link active"
              id="unit-types-tab"
              type="button"
              role="tab"
              aria-selected="true"
              @click="redirectToUnitTypes"
            >
              Manage Unit Types
            </button>
          </div>
        </div>

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
        >
          <form @submit.prevent="createUnitType">
            <div class="form-group">
              <label for="unitTypeName">Unit Type Name:</label>
              <input
                v-model="newUnitType.name"
                id="unitTypeName"
                type="text"
                class="form-control"
                placeholder="Enter Unit Type"
                required
              />
            </div>
            <div class="d-flex justify-content-end mt-3">
              <button
                type="button"
                class="btn btn-secondary"
                @click="isCreateModalOpen = false"
              >
                Cancel
              </button>
              <button type="submit" class="btn btn-primary ml-2">Create</button>
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
            <div class="title-wrapper">
              <div class="title-left">
                <div class="title-icon"></div>
                <div class="edit-title">
                  {{
                    showArchived ? "Archived Unit Types" : "Existing Unit Types"
                  }}
                </div>
              </div>
            </div>

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
                            style="background-color: #fff; color: black"
                          >
                            Un-Editable
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
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { BModal } from "bootstrap-vue-3";

export default {
  components: { SideNav, AppHeader, BModal },
  data() {
    return {
      loading: true,
      isLoading: false,
      errorMessage: "",
      unitTypes: [],
      newUnitType: {
        name: "",
      },
      showArchived: false, // Flag to toggle between archived and active unit types
      searchQuery: "", // Search query for filtering unit types
      isCreateModalOpen: false,
    };
  },
  computed: {
    // Filter and sort unit types based on the search query and archived status
    filteredUnitTypes() {
      // Filter by name and archived status
      const filtered = this.unitTypes.filter((unitType) => {
        const matchesSearch = unitType.name
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase());
        const isArchived = this.showArchived
          ? unitType.is_archived
          : !unitType.is_archived;
        return matchesSearch && isArchived;
      });

      // Sort to show default unit types first, then custom ones
      return filtered.sort((a, b) => {
        if (a.is_custom && !b.is_custom) return 1;
        if (!a.is_custom && b.is_custom) return -1;
        return 0;
      });
    },
  },
  methods: {
    openCreateTypeModal() {
      this.isCreateModalOpen = true;
    },

    toggleView() {
      if (this.viewFilter === "active") {
        this.showArchived = false; // Set showArchived to false for Active
      } else if (this.viewFilter === "archived") {
        this.showArchived = true; // Set showArchived to true for Archived
      }
    },

    redirectToUnits() {
      this.$router.push({ name: "DevFuncUnits" });
    },

    redirectToUnitTemplates() {
      this.$router.push({ name: "DevUnitTemplates" });
    },

    redirectToUnitTypes() {
      this.$router.push({ name: "DevUnitTypes" });
    },
    async fetchUnitTypes() {
      try {
        console.log("Fetching unit types...");
        const response = await axios.get(
          "http://localhost:8000/developer/units/types/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );
        console.log("Unit types fetched successfully:", response.data);

        if (response.status === 200) {
          this.unitTypes = response.data.data; // Update based on actual response structure
        } else {
          console.error("Error fetching unit types:", response);
          alert("Error fetching unit types.");
        }
      } catch (error) {
        console.error("Error fetching unit types:", error);
        alert("An error occurred while fetching unit types.");
      } finally {
        this.loading = false;
      }
    },

    // Create new unit type with debug info
    async createUnitType() {
      const data = {
        name: this.newUnitType.name,
        is_custom: true,
      };

      try {
        console.log("Creating unit type:", data);
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
        console.log("Unit type created successfully:", response.data);

        if (response.status === 201) {
          this.unitTypes.push(response.data.data);
          this.newUnitType.name = "";
          console.log(this.newUnitType);
          this.$refs.createUnitTypeModal.hide();
        } else {
          alert("Error creating unit type.");
        }
      } catch (error) {
        console.error("Error creating unit type:", error);
        alert("An error occurred while creating unit type.");
      }
    },

    // Archive a unit type with debug info
    async archiveUnitType(unitTypeId) {
      if (confirm("Are you sure you want to archive this unit type?")) {
        try {
          console.log(`Archiving unit type with ID: ${unitTypeId}`);
          const response = await axios.put(
            `http://localhost:8000/developer/units/types/${unitTypeId}/`,
            { is_archived: true },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                "Content-Type": "application/json",
              },
            }
          );
          console.log("Unit type archived successfully:", response.data);
          alert("Unit type archived successfully!");

          // Re-fetch the unit types to ensure the UI is up-to-date
          this.fetchUnitTypes();
        } catch (error) {
          console.error("Error archiving unit type:", error.response || error);
          alert("Failed to archive unit type. Please try again.");
        }
      }
    },

    // Unarchive a unit type with debug info
    async unarchiveUnitType(unitTypeId) {
      if (confirm("Are you sure you want to unarchive this unit type?")) {
        try {
          console.log(`Unarchiving unit type with ID: ${unitTypeId}`);
          const response = await axios.put(
            `http://localhost:8000/developer/units/types/${unitTypeId}/`,
            { is_archived: false }, // Set to false to unarchive
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                "Content-Type": "application/json",
              },
            }
          );
          console.log("Unit type unarchived successfully:", response.data);
          alert("Unit type unarchived successfully!");

          // Re-fetch the unit types to ensure the UI is up-to-date
          this.fetchUnitTypes();
        } catch (error) {
          console.error(
            "Error unarchiving unit type:",
            error.response || error
          );
          alert("Failed to unarchive unit type. Please try again.");
        }
      }
    },
  },
  created() {
    this.fetchUnitTypes(); // Fetch the unit types when the component is created
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

button {
  margin-left: 10px;
  padding: 5px 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
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

button {
  margin-left: 10px;
  padding: 5px 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
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
}

.nav-tabs .nav-link.active {
  color: #000; /* Active tab color */
  border-bottom: 2px solid #0d6efd;
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
  width: 100%;
  max-width: 1100px;
}

.header-item {
  flex: 1;
  text-align: left;
  font-size: 15px;
  color: #333;
  font-weight: bold;
}

.types-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background: #fff;
  table-layout: fixed;
}

.types-table th,
.types-table td {
  padding-bottom: 5px;
  text-align: left;
  vertical-align: middle;
  border: none;
  padding: 10px;
  /* Remove borders from all cells */
}

.types-table th {
  background-color: #f9f9f9;
  font-weight: bold;
}

.types-table th:nth-child(1),
.types-table td:nth-child(1) {
  /* Location column */
  width: 50%;
}

.types-table th:nth-child(2),
.types-table td:nth-child(2) {
  /* Location column */
  width: 25%;
}

.types-table th:nth-child(2),
.types-table td:nth-child(2) {
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
</style>
