<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <!-- Actions -->
        <div class="actions" v-if="!isLoading && !errorMessage">
          <button @click="redirectToUnits">Manage Units</button>
          <button @click="redirectToUnitTemplates">
            Manage Unit Templates
          </button>
          <button @click="redirectToUnitTypes">Manage Unit Types</button>
        </div>
        <h1>Unit Types Management</h1>

        <div v-if="loading" class="loading">Loading...</div>

        <div v-else>
          <div class="unit-type-form">
            <h2>Create New Unit Type</h2>
            <form @submit.prevent="createUnitType">
              <div>
                <label for="unitTypeName">Unit Type Name:</label>
                <input
                  v-model="newUnitType.name"
                  id="unitTypeName"
                  type="text"
                  placeholder="Enter Unit Type"
                  required
                />
              </div>
              <button type="submit">Create Unit Type</button>
            </form>
          </div>

          <div class="unit-types-toggle">
            <button @click="showArchived = !showArchived">
              {{
                showArchived
                  ? "Show Active Unit Types"
                  : "Show Archived Unit Types"
              }}
            </button>
          </div>

          <div class="unit-types-search">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by Unit Type Name"
            />
          </div>

          <div class="unit-types-list">
            <h2>
              {{ showArchived ? "Archived Unit Types" : "Existing Unit Types" }}
            </h2>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="unitType in filteredUnitTypes" :key="unitType.id">
                  <td>{{ unitType.name }}</td>
                  <td>
                    <button
                      v-if="!unitType.is_custom && !showArchived"
                      disabled
                    >
                      Default Unit Type
                    </button>
                    <button
                      v-if="
                        unitType.is_custom &&
                        !unitType.is_archived &&
                        !showArchived
                      "
                      @click="archiveUnitType(unitType.id)"
                    >
                      Archive
                    </button>
                    <button
                      v-if="unitType.is_archived && showArchived"
                      @click="unarchiveUnitType(unitType.id)"
                    >
                      Unarchive
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
</template>

<script>
import axios from "axios";
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";

export default {
  components: { SideNav, AppHeader },
  data() {
    return {
      loading: true,
      unitTypes: [],
      newUnitType: {
        name: "",
      },
      showArchived: false, // Flag to toggle between archived and active unit types
      searchQuery: "", // Search query for filtering unit types
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
  background-color: #ebebeb;
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

table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

th,
td {
  padding: 10px;
  text-align: left;
  border: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
}
</style>
