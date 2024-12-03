<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="dashboard-container">
          <!-- Loading Indicator -->
          <div v-if="isLoading" class="loading-indicator">Loading...</div>
          <!-- Error Message -->
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <!-- Actions -->
          <div class="actions" v-if="!isLoading && !errorMessage">
            <button @click="redirectToUnits">Manage Units</button>
            <button @click="redirectToUnitTemplates">
              Manage Unit Templates
            </button>
          </div>

          <!-- Units Section -->
          <div>
            <h2>Units</h2>
            <button @click="addUnit">Add Unit</button>
            <table>
              <thead>
                <tr>
                  <th>Unit Number</th>
                  <th>Title</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="unit in units" :key="unit.id">
                  <td>{{ unit.unit_number }}</td>
                  <td>{{ unit.unit_title }}</td>
                  <td>{{ unit.status }}</td>
                  <td>
                    <button @click="editUnit(unit)">Edit</button>
                    <button @click="deleteUnit(unit.id)">Delete</button>
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
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";

export default {
  name: "DevFuncUnits",
  components: { SideNav, AppHeader },
  data() {
    return {
      units: [],
      isLoading: false,
      errorMessage: null,
    };
  },
  methods: {
    async fetchUnits() {
      try {
        this.isLoading = true;
        this.errorMessage = null;
        const response = await axios.get(
          "http://localhost:8000/developer/units/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.units = response.data.data;
      } catch (error) {
        this.errorMessage = "Failed to load units.";
      } finally {
        this.isLoading = false;
      }
    },
    addUnit() {
      console.log("Add unit logic.");
    },
    editUnit(unit) {
      console.log("Edit unit logic for:", unit);
    },
    deleteUnit(unitId) {
      if (confirm("Are you sure you want to delete this unit?")) {
        this.units = this.units.filter((unit) => unit.id !== unitId);
      }
    },

    redirectToUnits() {
      this.$router.push({ name: "DevFuncUnits" });
    },

    // Redirect to Unit Management Page
    redirectToUnitTemplates() {
      this.$router.push({ name: "DevUnitTemplates" });
    },
  },
  mounted() {
    this.fetchUnits();
  },
};
</script>

<style scoped>
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

.actions {
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

.search-create {
  margin-bottom: 20px;
}

.search-create input {
  padding: 8px;
  margin-right: 10px;
}

.search-create button {
  padding: 8px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.search-create button:hover {
  background-color: #0056b3;
}

.loading-indicator {
  text-align: center;
  font-size: 16px;
  font-weight: bold;
  color: #007bff;
}

.error-message {
  text-align: center;
  color: red;
  font-weight: bold;
}
</style>
