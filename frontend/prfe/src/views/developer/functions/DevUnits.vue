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
            <button @click="showUnitTemplates">Manage Unit Templates</button>
            <button @click="showUnits">Manage Units</button>
          </div>

          <!-- Unit Templates Section -->
          <div v-if="view === 'templates'">
            <h2>Unit Templates</h2>
            <button @click="openCreateTemplateModal">
              Create New Template
            </button>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Bedrooms</th>
                  <th>Bathrooms</th>
                  <th>Floor Area</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <!-- Use dummy data for templates -->
                <tr v-for="template in templates" :key="template.id">
                  <td>{{ template.name }}</td>
                  <td>{{ template.bedroom }}</td>
                  <td>{{ template.bathroom }}</td>
                  <td>{{ template.floor_area }}</td>
                  <td>
                    <button @click="editTemplate(template)">Edit</button>
                    <button @click="deleteTemplate(template.id)">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Units Section -->
          <div v-if="view === 'units'">
            <h2>Units</h2>
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
                <!-- Use dummy data for units -->
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
            <button @click="addUnit">Add Unit</button>
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

export default {
  name: "DevFuncUnits",
  components: { SideNav, AppHeader },
  data() {
    return {
      view: "units", // Default view: units or templates
      templates: [], // Dummy data
      units: [], // Dummy data
      isLoading: false,
      errorMessage: null,
      selectedUnit: null, // To hold the selected unit for editing
      selectedTemplate: null, // To hold the selected template for editing
    };
  },
  methods: {
    // Fetch Unit Templates (dummy function)
    async fetchTemplates() {
      try {
        this.isLoading = true;
        this.errorMessage = null;
        const response = await axios.get(
          "http://localhost:8000/developer/units/templates/"
        );
        this.templates = response.data.data;
      } catch (error) {
        this.errorMessage = "Failed to load templates.";
      } finally {
        this.isLoading = false;
      }
    },
    async fetchUnits() {
      try {
        this.isLoading = true;
        this.errorMessage = null;
        const response = await axios.get(
          "http://localhost:8000/developer/units/"
        );
        this.units = response.data.data;
      } catch (error) {
        this.errorMessage = "Failed to load units.";
      } finally {
        this.isLoading = false;
      }
    },
    // Show Templates
    showUnitTemplates() {
      this.view = "templates";
      this.fetchTemplates();
    },
    // Show Units
    showUnits() {
      this.view = "units";
      this.fetchUnits();
    },
    // Actions
    addUnit() {
      this.selectedUnit = null; // Reset the selected unit
      this.openUnitModal();
    },
    editUnit(unit) {
      this.selectedUnit = unit; // Set selected unit for editing
      this.openUnitModal();
    },
    deleteUnit(unitId) {
      if (confirm("Are you sure you want to delete this unit?")) {
        this.units = this.units.filter((unit) => unit.id !== unitId);
      }
    },
    async openCreateTemplateModal() {
      this.selectedTemplate = null;
      this.openTemplateModal();
    },
    async createTemplate(templateData) {
      try {
        const response = await axios.post("/api/templates/", templateData);
        this.templates.push(response.data.data); // Add new template to list
        this.showUnitTemplates(); // Switch to the templates view after creation
      } catch (error) {
        this.errorMessage = "Failed to create template.";
      }
    },
    async deleteTemplate(templateId) {
      if (confirm("Are you sure you want to delete this template?")) {
        try {
          await axios.delete(`/api/templates/${templateId}/`);
          this.templates = this.templates.filter(
            (template) => template.id !== templateId
          ); // Remove deleted template from the list
        } catch (error) {
          this.errorMessage = "Failed to delete template.";
        }
      }
    },
    openUnitModal() {
      console.log("Open unit modal for", this.selectedUnit);
      // Open the modal where the unit can be added or edited
    },
    openTemplateModal() {
      console.log("Open template modal for", this.selectedTemplate);
      // Open the modal where the template can be added or edited
    },
  },
  mounted() {
    this.showUnits(); // Default view to show units
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
  background-color: #ebebeb; /* Gray background */
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
.loading-indicator {
  text-align: center;
  font-size: 16px;
  font-weight: bold;
  color: #007bff;
}
.error-message {
  text-align: center;
  font-size: 14px;
  font-weight: bold;
  color: red;
  margin-bottom: 20px;
}
</style>
