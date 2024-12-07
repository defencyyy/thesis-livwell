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
            <div class="title-wrapper">
              <div class="title-left">
                <div class="title-icon"></div>
                <div class="edit-title">Unit Templates</div>
              </div>
              <div class="total-templates">
                <div>Total Unit Templates: {{ templates.length }}</div>
              </div>
            </div>

            <!-- Search and Create Template -->
            <div
              class="card border-0 rounded-1 mx-auto"
              style="
                max-width: 1100px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
              "
            >
              <div class="card-body">
                <div class="toolbar">
                  <div class="left-section">
                    <div class="search-bar-container">
                      <input
                        v-model="searchQuery"
                        type="text"
                        class="search-bar"
                        placeholder="Search by template name"
                        @input="filterTemplates"
                      />
                      <i class="fa fa-search search-icon"></i>
                    </div>
                  </div>
                  <div class="right-section">
                    <button
                      @click="openCreateTemplateModal"
                      class="btn-primary add-button"
                    >
                      Create Unit Template
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Templates Table -->
            <div>
              <!-- Headers outside the card -->
              <div class="outside-headers">
                <span class="header-item">Relative ID</span>
                <span class="header-item">Name</span>
                <span class="header-item">Bedrooms</span>
                <span class="header-item">Bathrooms</span>
                <span class="header-item">Price</span>
                <span class="header-item">Floor Area</span>
                <span class="header-item">Lot Area</span>
                <span class="header-item">Actions</span>
              </div>

              <div
                v-for="template in filteredTemplates"
                :key="template.id"
                class="card border-0 rounded-1 mx-auto my-2"
                style="box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
              >
                <div class="card-body">
                  <table class="template-table">
                    <tbody>
                      <tr>
                        <td>
                          <span>{{ template.relativeId }}</span>
                        </td>
                        <td>
                          <span>{{ template.name }}</span>
                        </td>
                        <td>
                          <span>{{ template.bedroom }}</span>
                        </td>
                        <td>
                          <span>{{ template.bathroom }}</span>
                        </td>
                        <td>
                          <span>{{ template.price }}</span>
                        </td>
                        <td>
                          <span>{{ template.floor_area }}</span>
                        </td>
                        <td>
                          <span>{{ template.lot_area }}</span>
                        </td>
                        <td>
                          <div class="broker-actions d-flex gap-2">
                            <button
                              @click="openEditTemplateModal(template)"
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
                              @click="deleteTemplate(template.id)"
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
      <div class="p-3">
        <form @submit.prevent="createTemplate" enctype="multipart/form-data">
          <div class="row mb-3">
            <!-- Name Field -->
            <div class="form-group mb-3">
              <label for="name">Name</label>
              <input
                type="text"
                v-model="newTemplate.name"
                class="form-control"
                required
              />
            </div>

            <!-- Description Field -->
            <div class="form-group mb-3">
              <label for="description">Description</label>
              <textarea
                v-model="newTemplate.description"
                class="form-control"
                rows="3"
              ></textarea>
            </div>

            <!-- Unit Type Dropdown -->
            <div class="form-group mb-3">
              <label for="unit_type">Unit Type</label>
              <b-form-select
                v-model="newTemplate.unit_type"
                :options="unitTypesOptions"
                required
              />
            </div>

            <!-- Bedrooms Field -->
            <div class="form-group mb-3">
              <label for="bedroom">Bedrooms</label>
              <input
                type="number"
                v-model="newTemplate.bedroom"
                class="form-control"
                required
              />
            </div>

            <!-- Bathrooms Field -->
            <div class="form-group mb-3">
              <label for="bathroom">Bathrooms</label>
              <input
                type="number"
                v-model="newTemplate.bathroom"
                class="form-control"
                required
              />
            </div>

            <!-- Price Field -->
            <div class="form-group mb-3">
              <label for="price">Price</label>
              <input
                type="number"
                v-model="newTemplate.price"
                class="form-control"
                required
              />
            </div>

            <!-- Floor Area Field -->
            <div class="form-group mb-3">
              <label for="floor_area">Floor Area</label>
              <input
                type="number"
                v-model="newTemplate.floor_area"
                class="form-control"
              />
            </div>

            <!-- Lot Area Field -->
            <div class="form-group mb-3">
              <label for="lot_area">Lot Area</label>
              <input
                type="number"
                v-model="newTemplate.lot_area"
                class="form-control"
              />
            </div>

            <!-- Image Upload -->
            <div class="form-group mb-3">
              <label for="image">Upload Images</label>
              <input
                type="file"
                @change="handleImageUpload"
                class="form-control"
                accept="image/*"
                multiple
              />
            </div>

            <!-- Image Previews -->
            <div v-if="imagePreviews.length" class="image-previews">
              <h5>Uploaded Images</h5>
              <div class="d-flex gap-2">
                <img
                  v-for="(image, index) in imagePreviews"
                  :key="index"
                  :src="image"
                  class="img-thumbnail"
                  style="width: 100px; height: 100px"
                />
              </div>
            </div>
          </div>

          <!-- Modal Buttons -->
          <div
            class="d-flex justify-content-end gap-2 mt-30"
            style="padding-top: 15px"
          >
            <button type="submit" class="btn-add">Create</button>
            <button @click="closeCreateModal" class="btn-cancel">Cancel</button>
          </div>
        </form>
      </div>
    </b-modal>

    <!-- Edit Template Modal -->
    <b-modal
      v-model="isEditModalOpen"
      title="Edit Unit Template"
      hide-footer
      centered
    >
      <div class="p-3">
        <form
          @submit.prevent="saveTemplateChanges"
          enctype="multipart/form-data"
        >
          <div class="row mb-3">
            <div v-if="selectedTemplate" class="form-group mb-3">
              <label for="name">Name</label>
              <input
                type="text"
                v-model="selectedTemplate.name"
                class="form-control"
                required
              />
            </div>
            <div v-if="selectedTemplate" class="form-group mb-3">
              <label for="bedroom">Bedrooms</label>
              <input
                type="number"
                v-model="selectedTemplate.bedroom"
                class="form-control"
                required
              />
            </div>
            <div v-if="selectedTemplate" class="form-group mb-3">
              <label for="bathroom">Bathrooms</label>
              <input
                type="number"
                v-model="selectedTemplate.bathroom"
                class="form-control"
                required
              />
            </div>
            <div v-if="selectedTemplate" class="form-group mb-3">
              <label for="price">Price</label>
              <input
                type="number"
                v-model="selectedTemplate.price"
                class="form-control"
                required
              />
            </div>
            <div v-if="selectedTemplate" class="form-group mb-3">
              <label for="floor_area">Floor Area</label>
              <input
                type="number"
                v-model="selectedTemplate.floor_area"
                class="form-control"
              />
            </div>
            <div v-if="selectedTemplate" class="form-group mb-3">
              <label for="lot_area">Lot Area</label>
              <input
                type="number"
                v-model="selectedTemplate.lot_area"
                class="form-control"
              />
            </div>
            <!-- Display existing images in Edit Template Modal -->
            <div
              v-if="
                selectedTemplate &&
                selectedTemplate.images &&
                selectedTemplate.images.length > 0
              "
              class="existing-images"
            >
              <h5>Existing Images</h5>
              <div class="d-flex gap-2">
                <img
                  v-for="(image, index) in selectedTemplate.images"
                  :key="index"
                  :src="image.image_url"
                  class="img-thumbnail"
                  style="width: 100px; height: 100px"
                />
              </div>
            </div>

            <!-- Display existing images -->
            <div
              v-if="selectedTemplate && selectedTemplate.images"
              class="existing-images"
            >
              <h5>Existing Images</h5>
              <div class="d-flex gap-2">
                <img
                  v-for="(image, index) in selectedTemplate.images"
                  :key="index"
                  :src="image.image_url"
                  class="img-thumbnail"
                  style="width: 100px; height: 100px"
                />
              </div>
            </div>
          </div>
          <div
            class="d-flex justify-content-end gap-2 mt-30"
            style="padding-top: 15px"
          >
            <button type="submit" class="btn-add">Save</button>
            <button @click="closeEditModal" class="btn-cancel">Cancel</button>
          </div>
        </form>
      </div>
    </b-modal>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";
import { BFormSelect, BModal } from "bootstrap-vue-3";

export default {
  name: "DevUnitTemplates",
  components: { SideNav, AppHeader, BModal, BFormSelect },
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
        description: "",
        unit_type: "",
        bedroom: 1,
        bathroom: 1,
        price: 0,
        floor_area: 0,
        lot_area: 0,
      },
      imagePreviews: [], // To hold image preview URLs
      selectedImages: [],
      isCreateModalOpen: false,
      isEditModalOpen: false,
      unitTypes: [], // The array to hold the unit types (this will come from your backend or be defined statically)
    };
  },
  computed: {
    unitTypesOptions() {
      return [
        { value: null, text: "Select Unit Type" },
        ...this.unitTypes.map((type) => ({
          value: type.id,
          text: type.name,
        })),
      ];
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

    openCreateTemplateModal() {
      this.isCreateModalOpen = true;
    },

    closeCreateModal() {
      this.isCreateModalOpen = false;
      this.newTemplate = {
        name: "",
        description: "",
        bedroom: 1,
        bathroom: 1,
        price: 0,
        floor_area: 0,
        lot_area: 0,
      };
      this.imagePreviews = [];
      this.selectedImages = [];
    },

    closeEditModal() {
      this.isEditModalOpen = false;
      this.selectedTemplate = null;
      this.selectedImages = []; // Reset images after editing
      this.imagePreviews = [];
    },

    openEditTemplateModal(template) {
      if (template) {
        this.selectedTemplate = { ...template };
        this.isEditModalOpen = true;
      }
    },

    // Handle image upload
    handleImageUpload(event) {
      const files = event.target.files;
      this.selectedImages = Array.from(files); // Store file references
      this.imagePreviews = Array.from(files).map((file) =>
        URL.createObjectURL(file)
      ); // Show previews
    },

    async createTemplate() {
      const formData = new FormData();

      // Log the formData before appending it, to see if the data structure is correct
      console.log("FormData before appending:", this.newTemplate);

      for (let key in this.newTemplate) {
        formData.append(key, this.newTemplate[key]);
      }

      // Log image files to check if they are correctly added
      this.selectedImages.forEach((file) => {
        // Assuming you are uploading images for 'unit_template' type
        const imageType = "unit_template"; // or set this dynamically depending on context
        formData.append("images", file);
        formData.append("image_type", imageType); // Ensure 'image_type' is appended
      });

      // Log the complete FormData to see if everything is correctly appended
      for (let pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
      }

      try {
        const response = await axios.post(
          "http://localhost:8000/developer/units/templates/",
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );
        this.templates.push(response.data.data);
        this.closeCreateModal();
        alert("Template created successfully!");
      } catch (error) {
        console.error("Error response:", error.response); // Log error response for debugging
        alert("Failed to create template.");
      }
    },

    // Save changes to an edited template with image upload
    async saveTemplateChanges() {
      if (!this.selectedTemplate) return;

      const formData = new FormData();
      for (let key in this.selectedTemplate) {
        formData.append(key, this.selectedTemplate[key]);
      }
      this.selectedImages.forEach((file) => formData.append("images", file));

      try {
        const response = await axios.put(
          `http://localhost:8000/developer/units/templates/${this.selectedTemplate.id}/`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );
        const index = this.templates.findIndex(
          (template) => template.id === this.selectedTemplate.id
        );
        if (index !== -1) {
          this.templates[index] = response.data.data;
        }
        this.closeEditModal();
        alert("Template updated successfully!");
      } catch (error) {
        console.error(error);
        alert("Failed to update template.");
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

    // Fetch Unit Types (from API or statically defined)
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
        console.error("Error fetching unit types:", error);
        alert("Failed to load unit types.");
      }
    },
  },
  mounted() {
    this.showUnitTemplates(); // Default view to show unit templates
    this.fetchUnitTypes(); // Fetch unit types on load
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

.template-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background: #fff;
}

.template-table th,
.template-table td {
  padding-bottom: 5px;
  text-align: left;
  vertical-align: middle;
  border: none;
  /* Remove borders from all cells */
}

.template-table th {
  background-color: #f9f9f9;
  font-weight: bold;
}

.template-table th:nth-child(1),
.template-table td:nth-child(1) {
  width: 12%;
}

.template-table th:nth-child(2),
.template-table td:nth-child(2) {
  width: 12%;
}

.template-table th:nth-child(3),
.template-table td:nth-child(3) {
  width: 12%;
}

.template-table th:nth-child(4),
.template-table td:nth-child(4) {
  width: 12%;
}

.template-table th:nth-child(5),
.template-table td:nth-child(5) {
  width: 12%;
}

.template-table th:nth-child(6),
.template-table td:nth-child(6) {
  width: 12%;
}

.template-table th:nth-child(7),
.template-table td:nth-child(7) {
  width: 12%;
}

.template-table th:nth-child(8),
.template-table td:nth-child(8) {
  width: 12%;
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

.outside-headers {
  display: grid;
  /* Change to grid layout */
  grid-template-columns: 12% 12% 12% 12% 12% 12% 12% 12%;
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
</style>
