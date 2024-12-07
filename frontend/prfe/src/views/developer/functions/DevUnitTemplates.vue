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
                class="nav-link active"
                id="unit-templates-tab"
                type="button"
                role="tab"
                aria-selected="true"
                @click="redirectToUnitTemplates"
              >
                Manage Unit Templates
              </button>

              <!-- Manage Unit Types Tab -->
              <button
                class="nav-link"
                id="unit-types-tab"
                type="button"
                role="tab"
                aria-selected="false"
                @click="redirectToUnitTypes"
              >
                Manage Unit Types
              </button>
            </div>
          </div>

          <!-- Unit Templates Section -->
          <div v-if="view === 'templates'">
            <div class = "title-wrapper">
              <div class="title-left">
                <div class="title-icon"></div>
                <div class="edit-title">Unit Templates</div>
              </div>
              <div class = "total-templates">
                <div>Total Unit Templates: {{ templates.length }}</div>
              </div>
            </div>

            <!-- Search and Create Template -->
            <div
            class="card border-0 rounded-1 mx-auto"
            style="max-width: 1100px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
            >
              <div class = "card-body">
                <div class = "toolbar">
                  <div class = "left-section">
                    <div class = "search-bar-container">
                      <input
                      v-model="searchQuery"
                      type="text"
                      class = "search-bar"
                      placeholder="Search by template name"
                      @input="filterTemplates"
                      />
                      <i class="fa fa-search search-icon"></i>
                    </div>
                  </div>
                  <div class="right-section">
                    <button @click="openCreateTemplateModal" class = "btn-primary add-button">
                      Create Unit Template
                    </button>
                  </div>
                </div>
              </div>
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
                <tr v-for="template in filteredTemplates" :key="template.id">
                  <td>{{ template.relativeId }}</td>
                  <td>{{ template.name }}</td>
                  <td>{{ template.bedroom }}</td>
                  <td>{{ template.bathroom }}</td>
                  <td>{{ template.price }}</td>
                  <td>{{ template.floor_area }}</td>
                  <td>{{ template.lot_area }}</td>
                  <td>
                    <button @click="openEditTemplateModal(template)">
                      Edit
                    </button>
                    <button @click="deleteTemplate(template.id)">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Template Modal -->
    <b-modal
      v-model="isCreateModalOpen"
      title="Create Unit Template"
      hide-footer
      centered
    >
      <form @submit.prevent="createTemplate">
        <div>
          <label for="name">Name</label>
          <input type="text" v-model="newTemplate.name" required />
        </div>
        <div>
          <label for="bedroom">Bedrooms</label>
          <input type="number" v-model="newTemplate.bedroom" required />
        </div>
        <div>
          <label for="bathroom">Bathrooms</label>
          <input type="number" v-model="newTemplate.bathroom" required />
        </div>
        <div>
          <label for="price">Price</label>
          <input type="number" v-model="newTemplate.price" required />
        </div>
        <div>
          <label for="floor_area">Floor Area</label>
          <input type="number" v-model="newTemplate.floor_area" />
        </div>
        <div>
          <label for="lot_area">Lot Area</label>
          <input type="number" v-model="newTemplate.lot_area" />
        </div>
        <div class="modal-actions">
          <button type="submit">Create</button>
          <button @click="closeCreateModal">Cancel</button>
        </div>
      </form>
    </b-modal>

    <!-- Edit Template Modal -->
    <b-modal
      v-model="isEditModalOpen"
      title="Edit Unit Template"
      hide-footer
      centered
    >
      <form @submit.prevent="saveTemplateChanges">
        <div v-if="selectedTemplate">
          <label for="name">Name</label>
          <input type="text" v-model="selectedTemplate.name" required />
        </div>
        <div v-if="selectedTemplate">
          <label for="bedroom">Bedrooms</label>
          <input type="number" v-model="selectedTemplate.bedroom" required />
        </div>
        <div v-if="selectedTemplate">
          <label for="bathroom">Bathrooms</label>
          <input type="number" v-model="selectedTemplate.bathroom" required />
        </div>
        <div v-if="selectedTemplate">
          <label for="price">Price</label>
          <input type="number" v-model="selectedTemplate.price" required />
        </div>
        <div v-if="selectedTemplate">
          <label for="floor_area">Floor Area</label>
          <input type="number" v-model="selectedTemplate.floor_area" />
        </div>
        <div v-if="selectedTemplate">
          <label for="lot_area">Lot Area</label>
          <input type="number" v-model="selectedTemplate.lot_area" />
        </div>
        <div class="modal-actions">
          <button type="submit">Save Changes</button>
          <button @click="closeEditModal">Cancel</button>
        </div>
      </form>
    </b-modal>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";
import { BModal } from "bootstrap-vue-3";

export default {
  name: "DevUnitTemplates",
  components: { SideNav, AppHeader, BModal },
  data() {
    return {
      view: "templates",
      templates: [],
      isLoading: false,
      errorMessage: null,
      searchQuery: "",
      filteredTemplates: [],
      selectedTemplate: null,
      newTemplate: {
        name: "",
        bedroom: 1,
        bathroom: 1,
        price: 0,
        floor_area: 0,
        lot_area: 0,
      },
      isCreateModalOpen: false,
      isEditModalOpen: false,
    };
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
    // Open the modal for creating a new template
    openCreateTemplateModal() {
      this.isCreateModalOpen = true;
    },
    closeCreateModal() {
      this.isCreateModalOpen = false;
      this.newTemplate = {
        name: "",
        bedroom: 1,
        bathroom: 1,
        price: 0,
        floor_area: 0,
        lot_area: 0,
      };
    },
    openEditTemplateModal(template) {
      if (template) {
        this.selectedTemplate = { ...template };
        this.isEditModalOpen = true;
      } else {
        this.selectedTemplate = null;
        this.isEditModalOpen = false;
        console.error("Invalid template data passed to the modal");
      }
    },
    closeEditModal() {
      this.isEditModalOpen = false;
      this.selectedTemplate = null;
    },

    // Create Template
    async createTemplate() {
      try {
        const response = await axios.post(
          "http://localhost:8000/developer/units/templates/",
          this.newTemplate,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );
        this.templates.push(response.data.data); // Add new template
        this.closeCreateModal();
        alert("Template created successfully!");
      } catch (error) {
        this.errorMessage = "Failed to create template.";
        console.error(error);
      }
    },
    // Save changes to an edited template
    async saveTemplateChanges() {
      if (!this.selectedTemplate) {
        this.errorMessage = "No template selected for editing.";
        console.error("No template selected for editing.");
        return;
      }

      // Validate template fields
      if (
        !this.selectedTemplate.name ||
        !this.selectedTemplate.bedroom ||
        !this.selectedTemplate.bathroom ||
        !this.selectedTemplate.price
      ) {
        this.errorMessage = "Please fill in all required fields.";
        console.error("Missing required fields");
        return; // Prevent sending invalid data
      }

      try {
        const response = await axios.put(
          `http://localhost:8000/developer/units/templates/${this.selectedTemplate.id}/`,
          this.selectedTemplate,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );
        const index = this.templates.findIndex(
          (template) => template.id === this.selectedTemplate.id
        );
        if (index !== -1) {
          this.templates[index] = response.data.data; // Update the template in the list
        }
        this.closeEditModal();
        alert("Template updated successfully!");
      } catch (error) {
        this.errorMessage = "Failed to update template.";
        console.error(error);
      }
    },
    // Delete Template
    async deleteTemplate(templateId) {
      if (confirm("Are you sure you want to delete this template?")) {
        try {
          await axios.delete(
            `http://localhost:8000/developer/units/templates/${templateId}/`,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                "Content-Type": "application/json",
              },
            }
          );
          this.templates = this.templates.filter(
            (template) => template.id !== templateId
          );
          alert("Template deleted successfully!");
        } catch (error) {
          this.errorMessage = "Failed to delete template.";
          console.error(error);
        }
      }
    },

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
      this.closeCreateModal(); // Close the create modal when navigating
      this.closeEditModal(); // Close the edit modal when navigating
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
  background-color:  #e8f0fa;
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
  z-index: 10; /* Ensure main content is below the modal */
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Ensure the modal is on top */
}

.modal {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  max-width: 600px;
  width: 100%;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.modal-actions button {
  padding: 10px 20px;
}

button {
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
  color: #fff;
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
