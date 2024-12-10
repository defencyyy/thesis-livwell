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
                        placeholder="Search Unit Template"
                        @input="filterTemplates"
                      />
                      <i class="fa fa-search search-icon"></i>
                    </div>
                    <select
                    v-model="viewFilter"
                    @change="toggleView(viewFilter)"
                    class="dropdown"
                  >
                    <option value="active">View: Active</option>
                    <option value="archived">View: Archived</option>
                  </select>
      
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
              <!-- Table Headers -->
              <div class="outside-headers">
                <span class="header-item">ID</span>
                <span class="header-item">Unit Name</span>
                <span class="header-item">Unit Type</span>
                <span class="header-item">Price</span>
                <span class="header-item">Bedrooms</span>
                <span class="header-item">Bathrooms</span>
                <span class="header-item">Floor Area</span>
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
                        <!-- Relative ID: Example - Company-based and sequential order -->
                        <td>
                          <span>
                            {{ template.relativeId || "N/A" }}
                          </span>
                        </td>

                        <!-- Template Name -->
                        <td>
                          <span>{{ template.name }}</span>
                        </td>

                        <td>
                          {{
                            unitTypes.find(
                              (type) => type.id === template.unit_type
                            )?.name || "Unknown"
                          }}
                        </td>

                        <!-- Price -->
                        <td>
                          <span>{{ template.price }}</span>
                        </td>

                        <!-- Bedrooms -->
                        <td>
                          <span>{{ template.bedroom }}</span>
                        </td>

                        <!-- Bathrooms -->
                        <td>
                          <span>{{ template.bathroom }}</span>
                        </td>

                        <!-- Floor Area -->
                        <td>
                          <span>{{ template.floor_area }}</span>
                        </td>

                        <!-- Actions -->
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
                            <!-- Archive/Unarchive button -->
                            <button
                              v-if="template.is_archived === false"
                              @click="archiveTemplate(template.id)"
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
                              v-if="template.is_archived === true"
                              @click="unarchiveTemplate(template.id)"
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
      hide-header
      centered
      size="lg"
    >

    <div class="modal-title p-3">
  <h5 class="mb-0">New Unit Template</h5>
</div>

<div class="p-3">
  <form @submit.prevent="createTemplate" enctype="multipart/form-data">
    <!-- Left and Right Sections -->
    <div class="row">
      <!-- Left Section -->
      <div class="col-md-6">
        <!-- Name Field -->
        <div class="form-group mb-3">
          <label for="templateName">Name</label>
          <input
            type="text"
            v-model="newTemplate.templateName"
            class="form-control"
            required
          />
        </div>

        <!-- Description Field -->
        <div class="form-group mb-3">
          <label for="templateDescription">Description</label>
          <textarea
            v-model="newTemplate.templateDescription"
            class="form-control"
            rows="3"
          ></textarea>
        </div>

        <!-- Unit Type Dropdown -->
        <div class="form-group mb-3">
          <label for="templateType">Unit Type</label>
          <b-form-select
            v-model="newTemplate.templateType"
            :options="unitTypesOptions"
            required
          />
        </div>

        <!-- Price Field -->
        <div class="form-group mb-3">
          <label for="templatePrice">Price</label>
          <input
            type="number"
            v-model="newTemplate.templatePrice"
            class="form-control"
            required
          />
        </div>
      </div>

      <!-- Right Section -->
      <div class="col-md-6">
        <!-- Bedrooms and Bathrooms Fields -->
        <div class="row">
          <div class="col-md-6">
            <div class="form-group mb-3">
              <label for="templateBedrooms">Bedrooms</label>
              <input
                type="number"
                v-model="newTemplate.templateBedroom"
                class="form-control"
                required
              />
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-group mb-3">
              <label for="templateBathrooms">Bathrooms</label>
              <input
                type="number"
                v-model="newTemplate.templateBathroom"
                class="form-control"
                required
              />
            </div>
          </div>
        </div>

        <!-- Floor Area and Lot Area Fields -->
        <div class="row">
          <div class="col-md-6">
            <div class="form-group mb-3">
              <label for="templateFloorArea">Floor Area</label>
              <input
                type="number"
                v-model="newTemplate.templateFloorArea"
                class="form-control"
              />
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-group mb-3">
              <label for="templateLotArea">Lot Area</label>
              <input
                type="number"
                v-model="newTemplate.templateLotArea"
                class="form-control"
              />
            </div>
          </div>
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
    </div>

    <!-- Modal Buttons -->
    <div
      class="d-flex justify-content-end gap-2 mt-30"
      style="padding-top: 15px"
    >
      <button type="submit" class="btn-add">Add New Template</button>
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
              <label for="templateName">Name</label>
              <input
                type="text"
                v-model="selectedTemplate.name"
                class="form-control"
                required
              />
            </div>

            <!-- Description Field -->
            <div v-if="selectedTemplate" class="form-group mb-3">
              <label for="templateDescription">Description</label>
              <textarea
                v-model="selectedTemplate.description"
                class="form-control"
                rows="3"
              ></textarea>
            </div>

            <!-- Unit Type Dropdown -->
            <div v-if="selectedTemplate" class="form-group mb-3">
              <label for="templateType">Unit Type</label>
              <b-form-select
                v-model="selectedTemplate.unit_type"
                :options="unitTypesOptions"
                required
              />
            </div>

            <!-- Bedrooms Field -->
            <div v-if="selectedTemplate" class="form-group mb-3">
              <label for="templateBedrooms">Bedrooms</label>
              <input
                type="number"
                v-model="selectedTemplate.bedroom"
                class="form-control"
                required
              />
            </div>

            <!-- Bathrooms Field -->
            <div v-if="selectedTemplate" class="form-group mb-3">
              <label for="templateBathrooms">Bathrooms</label>
              <input
                type="number"
                v-model="selectedTemplate.bathroom"
                class="form-control"
                required
              />
            </div>

            <!-- Price Field -->
            <div v-if="selectedTemplate" class="form-group mb-3">
              <label for="templatePrice">Price</label>
              <input
                type="number"
                v-model="selectedTemplate.price"
                class="form-control"
                required
              />
            </div>

            <!-- Floor Area Field -->
            <div v-if="selectedTemplate" class="form-group mb-3">
              <label for="templateFloorArea">Floor Area</label>
              <input
                type="number"
                v-model="selectedTemplate.floor_area"
                class="form-control"
              />
            </div>

            <!-- Lot Area Field -->
            <div v-if="selectedTemplate" class="form-group mb-3">
              <label for="templateLotArea">Lot Area</label>
              <input
                type="number"
                v-model="selectedTemplate.lot_area"
                class="form-control"
              />
            </div>

            <!-- Image Previews -->
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
import { mapState } from "vuex";
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
      unitTypes: [],
      templateStatus: "", // This will hold the selected status ("active" or "archived")
      showArchived: false, // Set initial state to false for active templates
      viewFilter: "active", // Initially, show active templates

      // The array to hold the unit types (this will come from your backend or be defined statically)
    };
  },
  computed: {
    ...mapState({
      companyId: (state) => state.companyId, // Using Vuex to access company ID
    }),
    unitTypesOptions() {
      return [
        { value: null, text: "Select Unit Type" },
        ...this.unitTypes.map((type) => ({
          value: type.id,
          text: type.name,
        })),
      ];
    },

    filteredTemplates() {
      let filtered = this.templates.filter((template) => {
        // Filter by search query
        const matchesSearch = template.name
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase());

        // Filter by archived status
        const isArchived =
          this.viewFilter === "archived"
            ? template.is_archived
            : !template.is_archived;

        return matchesSearch && isArchived;
      });

      return filtered;
    },
    archivedTemplates() {
      return this.templates.filter((template) => template.is_archived);
    },
    activeTemplates() {
      return this.templates.filter((template) => !template.is_archived);
    },
  },
  methods: {
    toggleView(viewType) {
      this.viewFilter = viewType;
      if (this.viewFilter === "active") {
        this.showArchived = false; // Hides archived templates
      } else if (this.viewFilter === "archived") {
        this.showArchived = true; // Shows archived templates
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
      if (files) {
        this.selectedImages = Array.from(files);
        this.imagePreviews = this.selectedImages.map((file) =>
          URL.createObjectURL(file)
        );
      }
    },

    async createTemplate() {
      // Validate form fields (add checks based on required fields for templates)
      if (
        !this.newTemplate.templateName || // Replace with actual template fields
        !this.newTemplate.templateType || // Add all required template fields here
        !this.newTemplate.templatePrice
      ) {
        alert("Please fill in all the required fields.");
        return;
      }

      // Create a FormData object to send both template data and images
      const formData = new FormData();

      // Append form data fields for the template
      formData.append("name", this.newTemplate.templateName);
      formData.append("unit_type", this.newTemplate.templateType);
      formData.append("description", this.newTemplate.templateDescription);
      formData.append("price", this.newTemplate.templatePrice);
      formData.append("lot_area", this.newTemplate.templateLotArea);
      formData.append("floor_area", this.newTemplate.templateFloorArea);
      // Add fields from your template form here.

      // If there are selected images, append them
      if (this.selectedImages && this.selectedImages.length) {
        console.log("Selected images:", this.selectedImages);
        this.selectedImages.forEach((file) => {
          formData.append("images", file); // Use a simple name
        });
      } else {
        console.log("No images selected.");
      }

      // Log FormData content for debugging
      console.log("FormData contents before sending to backend:");
      for (let pair of formData.entries()) {
        console.log(pair[0], pair[1]);
      }

      try {
        // Send the FormData to the backend
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

        // Check the response status
        if (response.status === 201) {
          // Assuming this.templates is an array that holds all the created templates
          this.templates.push(response.data.data); // Push the new template data into the templates array
          this.closeCreateModal(); // Close the modal after success
          alert("Template created successfully!");
        }
      } catch (error) {
        console.error("Error creating template:", error);
        alert("Failed to create template. Please try again.");
      }
    },

    async saveTemplateChanges() {
      if (!this.selectedTemplate) return;

      const formData = new FormData();

      // Log the selected template object for debugging
      console.log("Selected template: ", this.selectedTemplate);
      // Make sure the keys match
      formData.append("name", this.selectedTemplate.name); // Ensure 'name' matches the v-model in the template
      formData.append("unit_type", this.selectedTemplate.unit_type); // Ensure 'unit_type' matches the v-model in the template
      formData.append("description", this.selectedTemplate.description); // Ensure 'description' matches the v-model in the template
      formData.append("price", this.selectedTemplate.price); // Ensure 'price' matches the v-model in the template
      formData.append("lot_area", this.selectedTemplate.lot_area); // Ensure 'lot_area' matches the v-model in the template
      formData.append("floor_area", this.selectedTemplate.floor_area); // Ensure 'floor_area' matches the v-model in the template

      if (this.selectedImages && this.selectedImages.length) {
        this.selectedImages.forEach((file) => {
          formData.append("images", file);
        });
      }

      // Log formData to verify the content being sent
      console.log("FormData being sent: ", formData);

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
        console.error(
          "Error saving template changes:",
          error.response ? error.response.data : error
        );
        alert("Failed to update template.");
      }
    },
    // Archive a template
    async archiveTemplate(templateId) {
      if (confirm("Are you sure you want to archive this template?")) {
        try {
          console.log(`Archiving template with ID: ${templateId}`);
          const response = await axios.put(
            `http://localhost:8000/developer/units/templates/${templateId}/`,
            { is_archived: true }, // Set to true to archive
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                "Content-Type": "application/json",
              },
            }
          );
          console.log("Template archived successfully:", response.data);
          alert("Template archived successfully!");

          // Re-fetch the templates to ensure the UI is up-to-date
          this.fetchTemplates();
        } catch (error) {
          console.error("Error archiving template:", error.response || error);
          alert("Failed to archive template. Please try again.");
        }
      }
    },

    // Unarchive a template
    async unarchiveTemplate(templateId) {
      if (confirm("Are you sure you want to unarchive this template?")) {
        try {
          console.log(`Unarchiving template with ID: ${templateId}`);
          const response = await axios.put(
            `http://localhost:8000/developer/units/templates/${templateId}/`,
            { is_archived: false }, // Set to false to unarchive
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                "Content-Type": "application/json",
              },
            }
          );
          console.log("Template unarchived successfully:", response.data);
          alert("Template unarchived successfully!");

          // Re-fetch the templates to ensure the UI is up-to-date
          this.fetchTemplates();
        } catch (error) {
          console.error("Error unarchiving template:", error.response || error);
          alert("Failed to unarchive template. Please try again.");
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
      } catch (error) {
        this.errorMessage = "Failed to load templates.";
      } finally {
        this.isLoading = false;
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

.dropdown {
  appearance: none;
  padding: 8px 12px;
  height: 38px;
  /* Explicitly set height */
  border: 1px solid #ccc;
  border-radius: 3px;
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
  width: 5%;
}

.template-table th:nth-child(2),
.template-table td:nth-child(2) {
  width: 20%;
}

.template-table th:nth-child(3),
.template-table td:nth-child(3) {
  width: 15%;
}

.template-table th:nth-child(4),
.template-table td:nth-child(4) {
  width: 15%;
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
  width: 15%;
}

.template-table th:nth-child(8),
.template-table td:nth-child(8) {
  width: 6%;
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
  grid-template-columns: 5% 20% 15% 15% 12% 12% 15% 6%;
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
</style>
