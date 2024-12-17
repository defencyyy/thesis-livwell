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
                    <select v-model="sortBy" class="dropdown">
                      <option value="id">Sort: ID</option>
                      <option value="name">Sort: Name</option>
                    </select>

                    <!-- Sort Order Dropdown -->
                    <select v-model="sortOrder" class="dropdown">
                      <option value="asc">Ascending</option>
                      <option value="desc">Descending</option>
                    </select>
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
                v-for="template in paginatedTemplates"
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
                            {{ template.relative_id || "N/A" }}
                          </span>
                        </td>

                        <!-- Template Name -->
                        <td>
                          <strong
                            ><span>{{ template.name }}</span></strong
                          >
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
                          <div class="broker-actions d-flex">
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
                    <a
                      class="page-link"
                      href="#"
                      @click.prevent="goToPage(page)"
                    >
                      {{ page }}
                    </a>
                  </li>
                  <li
                    :class="[
                      'page-item',
                      { disabled: currentPage === totalPages },
                    ]"
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
                  v-model="newTemplate.name"
                  class="form-control"
                  required
                />
              </div>

              <!-- Description Field -->
              <div class="form-group mb-3">
                <label for="templateDescription">Description</label>
                <textarea
                  v-model="newTemplate.description"
                  class="form-control"
                  rows="3"
                ></textarea>
              </div>

              <!-- Unit Type Dropdown -->
              <div class="form-group mb-3">
                <label for="templateType">Unit Type</label>
                <b-form-select
                  v-model="newTemplate.unit_type"
                  :options="selectUnitTypeOptions"
                  required
                />
              </div>

              <!-- Price Field -->
              <div class="form-group mb-3">
                <label for="templatePrice">Price</label>
                <input
                  type="number"
                  v-model="newTemplate.price"
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
                      v-model="newTemplate.bedroom"
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
                      v-model="newTemplate.bathroom"
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
                      v-model="newTemplate.floor_area"
                      class="form-control"
                    />
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-group mb-3">
                    <label for="templateLotArea">Lot Area</label>
                    <input
                      type="number"
                      v-model="newTemplate.lot_area"
                      class="form-control"
                    />
                  </div>
                </div>
              </div>

              <!-- Image Upload -->
              <div class="form-group mb-3">
                <label for="image">Upload Images (Max:5)</label>
                <input
                  type="file"
                  @change="handleFileChange"
                  class="form-control"
                  accept="image/*"
                  multiple
                />
              </div>

              <!-- Image Preview -->
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
      hide-header
      centered
      size="lg"
    >
      <div class="modal-title p-3">
        <h5 class="mb-0">Edit Unit Template</h5>
      </div>

      <div class="p-3">
        <form
          @submit.prevent="saveTemplateChanges"
          enctype="multipart/form-data"
        >
          <div class="row">
            <!-- Left Section -->
            <div class="col-md-6">
              <div v-if="selectedTemplate" class="form-group mb-3">
                <label for="templateName">Name</label>
                <input
                  type="text"
                  v-model="selectedTemplate.name"
                  class="form-control"
                  disabled
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
                  disabled
                  required
                />
              </div>
            </div>

            <div class="col-md-6">
              <!-- Bedrooms and Bathrooms Fields -->
              <div class="row">
                <div class="col-md-6">
                  <div v-if="selectedTemplate" class="form-group mb-3">
                    <label for="templateBedrooms">Bedrooms</label>
                    <input
                      type="number"
                      v-model="selectedTemplate.bedroom"
                      class="form-control"
                      disabled
                      required
                    />
                  </div>
                </div>
                <div class="col-md-6">
                  <!-- Bathrooms Field -->
                  <div v-if="selectedTemplate" class="form-group mb-3">
                    <label for="templateBathrooms">Bathrooms</label>
                    <input
                      type="number"
                      v-model="selectedTemplate.bathroom"
                      class="form-control"
                      disabled
                      required
                    />
                  </div>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6">
                  <!-- Floor Area Field -->
                  <div v-if="selectedTemplate" class="form-group mb-3">
                    <label for="templateFloorArea">Floor Area</label>
                    <input
                      type="number"
                      v-model="selectedTemplate.floor_area"
                      disabled
                      class="form-control"
                    />
                  </div>
                </div>
                <div class="col-md-6">
                  <!-- Lot Area Field -->
                  <div v-if="selectedTemplate" class="form-group mb-3">
                    <label for="templateLotArea">Lot Area</label>
                    <input
                      type="number"
                      v-model="selectedTemplate.lot_area"
                      disabled
                      class="form-control"
                    />
                  </div>
                </div>
              </div>

              <!-- Price Field -->
              <div v-if="selectedTemplate" class="form-group mb-3">
                <label for="templatePrice">Price</label>
                <input
                  type="number"
                  v-model="selectedTemplate.price"
                  class="form-control"
                  disabled
                  required
                />
              </div>

              <!-- Image Previews -->
              <div
                v-if="
                  selectedTemplate &&
                  selectedTemplate.images &&
                  selectedTemplate.images.length > 0
                "
                class="form-group mb-3"
              >
                <label for="existingImages">Existing Images</label>
                <div class="d-flex gap-2">
                  <img
                    v-for="(image, index) in selectedTemplate.images"
                    :key="index"
                    :src="getPictureUrl(image.image)"
                    class="img-thumbnail"
                    style="width: 100px; height: 100px"
                  />
                </div>
              </div>
            </div>
          </div>

          <div
            class="d-flex justify-content-end gap-2 mt-30"
            style="padding-top: 15px"
          >
            <button type="submit" class="btn-add" style="width: 150px">
              Save Changes
            </button>
            <button
              type="button"
              @click="isEditModalOpen = false"
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
      <div class="button-container">
        <!-- Confirm Button -->
        <button type="button" @click="confirmAction" class="btn btn-primary">
          Confirm
        </button>
        <!-- Cancel Button -->
        <button type="button" @click="cancelAction" class="btn btn-secondary">
          Cancel
        </button>
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
      unitTypes: [],
      isLoading: false,
      errorMessage: null,
      searchQuery: "",
      selectedTemplate: null,
      selectedImages: [],
      imagePreviews: [],
      showArchived: false,
      viewFilter: "active",
      sortBy: "id", // Default sort by name
      sortOrder: "asc", // Default sort order ascending

      // Modal States
      isCreateModalOpen: false,
      isEditModalOpen: false,
      showConfirmModal: false,

      // New Template
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

      // Notifications
      showNotification: false,
      notificationTitle: "",
      notificationMessage: "",

      // Confirmation Modal
      confirmMessage: "",
      actionToConfirm: null,
      confirmParams: [],
      currentPage: 1,
      itemsPerPage: 10,
    };
  },

  computed: {
    ...mapState({
      companyId: (state) => state.companyId,
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

    selectUnitTypeOptions() {
      return [
        { value: null, text: "Select" },
        ...this.unitTypes
          .filter((type) => !type.is_archived) // Exclude archived types
          .map((type) => ({
            value: type.id,
            text: type.name,
          })),
      ];
    },

    filteredTemplates() {
      const filtered = this.templates.filter((template) => {
        const matchesSearch = template.name
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase());

        // Filtering by Active/Archived
        const isArchived =
          this.viewFilter === "archived"
            ? template.is_archived
            : this.viewFilter === "active"
            ? !template.is_archived
            : true;

        return matchesSearch && isArchived;
      });

      // Sorting by ID or Name, with default (is_custom: false) coming first
      return filtered.sort((a, b) => {
        // Handle is_custom prioritization before sorting by ID or Name
        if (this.sortOrder === "asc") {
          // Ascending: default (is_custom: false) comes first
          if (a.is_custom === false && b.is_custom === true) {
            return -1; // a (default) comes first
          }
          if (a.is_custom === true && b.is_custom === false) {
            return 1; // b (default) comes first
          }
        } else if (this.sortOrder === "desc") {
          // Descending: non-default (is_custom: true) comes first
          if (a.is_custom === false && b.is_custom === true) {
            return 1; // b (non-default) comes first
          }
          if (a.is_custom === true && b.is_custom === false) {
            return -1; // a (non-default) comes first
          }
        }

        // Sorting by ID if no is_custom difference
        if (this.sortBy === "id") {
          return this.sortOrder === "asc" ? a.id - b.id : b.id - a.id;
        }

        // Sorting by Name if no is_custom difference
        if (this.sortBy === "name") {
          const nameA = a.name.toLowerCase();
          const nameB = b.name.toLowerCase();
          return this.sortOrder === "asc"
            ? nameA.localeCompare(nameB)
            : nameB.localeCompare(nameA);
        }
      });
    },
    archivedTemplates() {
      return this.templates.filter((template) => template.is_archived);
    },

    activeTemplates() {
      return this.templates.filter((template) => !template.is_archived);
    },
    paginatedTemplates() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredTemplates.slice(
        startIndex,
        startIndex + this.itemsPerPage
      );
    },

    totalPages() {
      return Math.ceil(this.filteredTemplates.length / this.itemsPerPage);
    },
  },
  methods: {
    getPictureUrl(picture) {
      const url = `http://localhost:8000${picture}`;
      console.log(url); // Check the URL being generated
      return url;
    },
    goToPage(pageNumber) {
      if (pageNumber > 0 && pageNumber <= this.totalPages) {
        this.currentPage = pageNumber;
      }
    },
    toggleView(viewType) {
      this.viewFilter = viewType;
      if (this.viewFilter === "active") {
        this.showArchived = false; // Hides archived templates
      } else if (this.viewFilter === "archived") {
        this.showArchived = true; // Shows archived templates
      }
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

    handleFileChange(event) {
      const files = event.target.files;
      if (files && files.length > 0) {
        this.selectedImages = Array.from(files); // Store files
        this.imagePreviews = this.selectedImages.map(
          (file) => URL.createObjectURL(file) // Generate image previews
        );
      }
    },

    // Create template with image files
    async createTemplate() {
      try {
        // Validate form fields
        if (
          !this.newTemplate.name ||
          !this.newTemplate.unit_type ||
          !this.newTemplate.price
        ) {
          alert("Please fill in all the required fields.");
          return;
        }

        // Create a FormData object to send both template data and images
        const formData = new FormData();

        // Append template data fields
        formData.append("name", this.newTemplate.name);
        formData.append("unit_type", this.newTemplate.unit_type);
        formData.append("description", this.newTemplate.description);
        formData.append("bathroom", this.newTemplate.bathroom);
        formData.append("bedroom", this.newTemplate.bedroom);
        formData.append("price", this.newTemplate.price);
        formData.append("lot_area", this.newTemplate.lot_area);
        formData.append("floor_area", this.newTemplate.floor_area);

        // Append selected images
        if (this.selectedImages.length > 0) {
          // Append images without using index notation
          this.selectedImages.forEach((file) => {
            console.log(file); // Check the file object before appending
            formData.append("images", file);
            formData.append("image_types", "unit_template");
            formData.append("primaries", false);
          });
        } else {
          console.log("No images selected.");
        }

        // Log FormData contents (for debugging)
        console.log("FormData contents before sending to backend:");
        for (let pair of formData.entries()) {
          console.log(pair[0], pair[1]);
        }

        // Send the form data to the backend
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

        // Handle the response (template created successfully)
        this.templates.push(response.data.data);
        this.closeCreateModal();

        this.notificationTitle = "Success";
        this.notificationMessage = "Template created successfully!";
        this.showNotification = true;
      } catch (error) {
        console.error("Error creating template:", error);
        this.notificationTitle = "Error";
        this.notificationMessage =
          "Failed to create template. Please try again.";
        this.showNotification = true;
      }
    },

    // Modify the save template method to handle images the same way
    async saveTemplateChanges() {
      this.showConfirmation(
        "Are you sure you want to save these changes?",
        async () => {
          try {
            const formData = new FormData();
            formData.append("name", this.selectedTemplate.name);
            formData.append("unit_type", this.selectedTemplate.unit_type);
            formData.append("description", this.selectedTemplate.description);
            formData.append("price", this.selectedTemplate.price);
            formData.append("lot_area", this.selectedTemplate.lot_area);
            formData.append("floor_area", this.selectedTemplate.floor_area);

            // Append selected images to form data for updating template
            if (this.selectedImages.length) {
              this.selectedImages.forEach((file) => {
                formData.append("images", file); // Append each image
              });
            }

            const response = await axios.put(
              `http://localhost:8000/developer/units/templates/${this.selectedTemplate.id}/`,
              formData,
              {
                headers: {
                  Authorization: `Bearer ${localStorage.getItem(
                    "accessToken"
                  )}`,
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

            this.notificationTitle = "Success";
            this.notificationMessage = "Template updated successfully!";
            this.showNotification = true;
          } catch (error) {
            console.error("Error updating template:", error);
            this.notificationTitle = "Error";
            this.notificationMessage =
              "Failed to update template. Please try again.";
            this.showNotification = true;
          }
        },
        []
      );
    },
    async archiveTemplate(templateId) {
      this.showConfirmation(
        "Are you sure you want to archive this template?",
        this.performArchiveTemplate,
        [templateId]
      );
    },

    async performArchiveTemplate(templateId) {
      try {
        await axios.put(
          `http://localhost:8000/developer/units/templates/${templateId}/`,
          { is_archived: true },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.fetchTemplates();

        this.notificationTitle = "Success";
        this.notificationMessage = "Template archived successfully!";
        this.showNotification = true;
      } catch (error) {
        console.error("Error archiving template:", error);
        this.notificationTitle = "Error";
        this.notificationMessage =
          "Failed to archive template. Please try again.";
        this.showNotification = true;
      }
    },

    async unarchiveTemplate(templateId) {
      this.showConfirmation(
        "Are you sure you want to unarchive this template?",
        this.performUnarchiveTemplate,
        [templateId]
      );
    },

    async performUnarchiveTemplate(templateId) {
      try {
        await axios.put(
          `http://localhost:8000/developer/units/templates/${templateId}/`,
          { is_archived: false },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.fetchTemplates();

        this.notificationTitle = "Success";
        this.notificationMessage = "Template unarchived successfully!";
        this.showNotification = true;
      } catch (error) {
        console.error("Error unarchiving template:", error);
        this.notificationTitle = "Error";
        this.notificationMessage =
          "Failed to unarchive template. Please try again.";
        this.showNotification = true;
      }
    },
    showConfirmation(message, action, params) {
      this.confirmMessage = message;
      this.actionToConfirm = action; // Use the renamed key here
      this.confirmParams = params;
      this.showConfirmModal = true;
    },

    cancelAction() {
      this.showConfirmModal = false; // Close modal on cancel
    },

    async confirmAction() {
      try {
        // Dynamically call the function stored in actionToConfirm with the provided params
        await this.actionToConfirm(...this.confirmParams);
        this.showConfirmModal = false; // Close modal after confirmation
      } catch (error) {
        this.showConfirmModal = false; // Close modal on error
        this.notificationTitle = "Error";
        this.notificationMessage = "An error occurred during the action.";
        this.showNotification = true;
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
  font-size: 14px;
}

.template-table th,
.template-table td {
  padding-bottom: 5px;
  text-align: left;
  vertical-align: middle;
  border: none;
  padding: 7px;
  /* Remove borders from all cells */
}

.template-table th {
  background-color: #f9f9f9;
  font-weight: bold;
}

.template-table th:nth-child(1),
.template-table td:nth-child(1) {
  width: 6%;
}

.template-table th:nth-child(2),
.template-table td:nth-child(2) {
  width: 22%;
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
  width: 10%;
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
  grid-template-columns: 6% 22% 15% 15% 12% 12% 10% 6%;
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
.pagination {
  display: flex;
  justify-content: flex-end;
  max-width: 1100px;
  width: 100%;
  /* Reduce padding */
  font-size: 12px;
  /* Smaller font size */
  line-height: 1;
  margin: 0;

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
</style>
