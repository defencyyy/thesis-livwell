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

          <!-- Unit Templates Section -->
          <div v-if="view === 'templates'">
            <h2>Unit Templates</h2>
            <!-- Total Unit Templates -->
            <div>
              <p>Total Unit Templates: {{ templates.length }}</p>
            </div>

            <!-- Search and Create Template -->
            <div class="search-create">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by template name"
                @input="filterTemplates"
              />
              <button @click="openCreateTemplateModal">
                Create Unit Template
              </button>
            </div>

            <!-- Templates Table -->
            <table>
              <thead>
                <tr>
                  <th>RelativeId</th>
                  <th>Name</th>
                  <th>Bedrooms</th>
                  <th>Bathrooms</th>
                  <th>Price</th>
                  <th>Floor Area</th>
                  <th>Lot Area</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <!-- Display templates based on search/filter -->
                <tr v-for="template in filteredTemplates" :key="template.id">
                  <td>{{ template.relativeId }}</td>
                  <td>{{ template.name }}</td>
                  <td>{{ template.bedroom }}</td>
                  <td>{{ template.bathroom }}</td>
                  <td>{{ template.price }}</td>
                  <td>{{ template.floor_area }}</td>
                  <td>{{ template.lot_area }}</td>
                  <td>
                    <button @click="editTemplate(template)">Edit</button>
                    <button @click="deleteTemplate(template.id)">Delete</button>
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
  name: "DevUnitTemplates",
  components: { SideNav, AppHeader },
  data() {
    return {
      view: "templates", // Default view: templates
      templates: [], // Template data
      isLoading: false,
      errorMessage: null,
      searchQuery: "", // Search input for templates
      filteredTemplates: [], // Filtered templates based on search
      selectedTemplate: null, // Selected template for editing
    };
  },
  methods: {
    // Fetch Unit Templates
    async fetchTemplates() {
      try {
        this.isLoading = true;
        this.errorMessage = null;
        const response = await axios.get(
          "http://localhost:8000/developer/units/templates/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.templates = response.data.data;
        this.filteredTemplates = this.templates; // Initially display all templates
      } catch (error) {
        this.errorMessage = "Failed to load templates.";
      } finally {
        this.isLoading = false;
      }
    },

    // Filter templates based on search query
    filterTemplates() {
      if (this.searchQuery) {
        this.filteredTemplates = this.templates.filter((template) =>
          template.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      } else {
        this.filteredTemplates = this.templates; // Show all if no search query
      }
    },

    // Show Unit Templates
    showUnitTemplates() {
      this.view = "templates";
      this.fetchTemplates();
    },

    redirectToUnits() {
      this.$router.push({ name: "DevFuncUnits" });
    },

    // Redirect to Unit Management Page
    redirectToUnitTemplates() {
      this.$router.push({ name: "DevUnitTemplates" });
    },

    // Create Template
    async createTemplate(templateData) {
      try {
        const response = await axios.post("/units/templates/", templateData);
        this.templates.push(response.data.data); // Add new template
        this.showUnitTemplates(); // Show templates view
      } catch (error) {
        this.errorMessage = "Failed to create template.";
      }
    },

    // Delete Template
    async deleteTemplate(templateId) {
      if (confirm("Are you sure you want to delete this template?")) {
        try {
          await axios.delete(`/units/templates/${templateId}/`);
          this.templates = this.templates.filter(
            (template) => template.id !== templateId
          );
        } catch (error) {
          this.errorMessage = "Failed to delete template.";
        }
      }
    },

    // Open Modals (Template)
    openTemplateModal() {
      console.log("Open template modal for", this.selectedTemplate);
      // Open modal for adding/editing template
    },
  },
  mounted() {
    this.showUnitTemplates(); // Default view to show unit templates
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
