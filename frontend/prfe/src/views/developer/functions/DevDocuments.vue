<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <!-- Document Types Section -->
        <div class="title-wrapper">
          <div class="title-icon"></div>
          <div class="edit-title">Document Types</div>
        </div>

        <div style="width: 100%; max-width: 900px">
          <!-- Headers outside the card -->
          <div class="outside-headers">
            <span class="header-item">Document Name</span>
            <span class="header-item">Description</span>
            <span class="header-item">Actions</span>
          </div>

          <div
            v-for="docType in documentTypes"
            :key="docType.id"
            class="card border-0 rounded-1 mx-auto my-2"
            style="box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
          >
            <div class="card-body">
              <table class="document-table">
                <tbody>
                  <tr>
                    <td class="document-name">
                      {{ docType.name }}
                    </td>
                    <td class="document-description">
                      {{ docType.description || "N/A" }}
                    </td>
                    <td>
                      <button
                        @click="editDocumentType(docType)"
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
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="d-flex justify-content-end mt-3">
            <button @click="showAddForm = true" class="btn-add">
              Add Document
            </button>
          </div>
        </div>

        <!-- Add/Edit Document Type Modal -->
        <b-modal
          v-model="showAddForm"
          :title="
            newDocumentType.id ? 'Edit Document Type' : 'Add New Document'
          "
          hide-footer
          hide-header
          centered
          @hide="onModalHide"
        >

        <div class="modal-title p-3">
            <h5 class="mb-0"> {{ newDocumentType.id ? 'Edit Document Type' : 'Add New Document' }}</h5>
          </div>

          <div class="p-3">

          <div class="mb-3">
            <small>Name </small>
            <input
              type="text"
              class="form-control"
              id="documentTypeName"
              v-model="newDocumentType.name"
              placeholder="Enter document type name"
              :disabled="newDocumentType.id ? true : false"
              :class="{ 'is-invalid': nameError }"
            />
            <div v-if="nameError" class="invalid-feedback">
              Please enter a document name.
            </div>
          </div>

          <div class="mb-3">
            <small>Description</small>
            
            <textarea
              class="form-control"
              id="documentTypeDescription"
              v-model="newDocumentType.description"
              rows="4"
              placeholder="Enter description"
            ></textarea>
          </div>

          <!-- Modal Footer -->
          <div
            class="d-flex justify-content-end gap-2 mt-3"
            style="padding-top: 15px"
          >
            <button
              type="button"
              class="btn-add"
              @click="saveDocumentType"
            >
              {{ newDocumentType.id ? "Save Changes" : "Add Document" }}
            </button>
            <button type="button" class="btn-cancel" @click="closeForm">
              Cancel
            </button>
          </div>
          </div>
        </b-modal>

        <!-- Notification Modal -->
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

        <!-- Confirmation Modal -->
        <b-modal
          v-model="showConfirmModal"
          :title="'Confirmation'"
          hide-footer
          centered
        >
          <p>{{ confirmMessage }}</p>
          <div
            class="d-flex justify-content-end gap-2 mt-30"
            style="padding-top: 15px"
          >
            <button
              type="button"
              @click="confirmAction"
              class="btn btn-primary"
            >
              Confirm
            </button>
            <button
              type="button"
              @click="cancelAction"
              class="btn btn-secondary"
            >
              Cancel
            </button>
          </div>
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { BModal } from "bootstrap-vue-3";
import axios from "axios";

export default {
  name: "DevDocuments",
  components: { SideNav, AppHeader, BModal },
  data() {
    return {
      documentTypes: [],
      showAddForm: false,
      newDocumentType: { name: "", description: "" },
      originalDocumentType: null, // Keep track of the original document type for comparison
      nameError: false, // Validation flag for name field
      showNotification: false,
      notificationTitle: "",
      notificationMessage: "",
      showConfirmModal: false,
      confirmMessage: "",
      actionToConfirm: null,
      confirmParams: [],
    };
  },
  mounted() {
    this.fetchDocumentTypes();
  },
  methods: {
    getAxiosInstance() {
      const instance = axios.create({
        baseURL: "http://localhost:8000/developer/",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          "Content-Type": "application/json",
        },
      });

      instance.interceptors.response.use(
        (response) => response,
        async (error) => {
          if (error.response && error.response.status === 401) {
            try {
              const refreshResponse = await axios.post(
                "http://localhost:8000/auth/refresh/",
                {
                  refresh: localStorage.getItem("refreshToken"),
                }
              );

              if (refreshResponse.status === 200) {
                localStorage.setItem(
                  "accessToken",
                  refreshResponse.data.access
                );

                error.config.headers.Authorization = `Bearer ${refreshResponse.data.access}`;
                return axios(error.config);
              }
            } catch (refreshError) {
              console.error("Error refreshing token:", refreshError);
              this.$router.push({ name: "Login" });
            }
          }
          return Promise.reject(error);
        }
      );

      return instance;
    },

    async fetchDocumentTypes() {
      const axiosInstance = this.getAxiosInstance();
      try {
        const response = await axiosInstance.get("documents/document-types/");
        if (response.status === 200) {
          this.documentTypes = response.data;
        }
      } catch (error) {
        console.error("Error fetching document types:", error);
      }
    },

    async saveDocumentType() {
      // Validate name field
      if (!this.newDocumentType.name.trim()) {
        this.nameError = true;
        return;
      }

      // If we're editing, compare changes
      if (this.newDocumentType.id) {
        if (
          this.newDocumentType.name === this.originalDocumentType.name &&
          this.newDocumentType.description ===
            this.originalDocumentType.description
        ) {
          this.showNotificationWithMessage(
            "Invalid",
            "No changes were made to the document type."
          );
          this.closeForm();
          return;
        }
      }

      const message = this.newDocumentType.id
        ? "Do you want to save the changes to this document type?"
        : "'Document type names can't be changed. Proceed?";

      const action = this.newDocumentType.id
        ? this.confirmSaveDocumentType
        : this.confirmAddDocumentType;
      const params = [];

      // Show the confirmation modal before proceeding
      this.showConfirmation(message, action, params);
    },

    // Handle the confirmation for saving a document type (edit action)
    async confirmSaveDocumentType() {
      const axiosInstance = this.getAxiosInstance();
      const method = this.newDocumentType.id ? "PUT" : "POST";
      const url = this.newDocumentType.id
        ? `documents/document-types/${this.newDocumentType.id}/`
        : `documents/document-types/`;

      try {
        const response = await axiosInstance({
          method,
          url,
          data: this.newDocumentType,
        });

        if ([200, 201].includes(response.status)) {
          this.fetchDocumentTypes();
          this.closeForm();
          this.showNotificationWithMessage(
            "Success",
            "Document type saved successfully!"
          );
        }
      } catch (error) {
        console.error("Error saving document type:", error);
        this.showNotificationWithMessage(
          "Error",
          "An error occurred while saving document type."
        );
      }
    },

    // Handle the confirmation for adding a new document type
    async confirmAddDocumentType() {
      const axiosInstance = this.getAxiosInstance();
      const url = "documents/document-types/";

      try {
        const response = await axiosInstance.post(url, this.newDocumentType);

        if (response.status === 201) {
          this.fetchDocumentTypes();
          this.closeForm();
          this.showNotificationWithMessage(
            "Success",
            "Document type added successfully!"
          );
        }
      } catch (error) {
        console.error("Error adding document type:", error);
        this.showNotificationWithMessage(
          "Error",
          "An error occurred while adding document type. No duplicate names allowed."
        );
      }
    },

    // Function to show a confirmation modal
    showConfirmation(message, action, params) {
      this.confirmMessage = message;
      this.actionToConfirm = action;
      this.confirmParams = params;
      this.showConfirmModal = true;
    },

    cancelAction() {
      this.showConfirmModal = false;
    },

    // Confirm action when the user confirms the modal
    async confirmAction() {
      try {
        await this.actionToConfirm(...this.confirmParams);
        this.showConfirmModal = false;
      } catch (error) {
        this.showConfirmModal = false;
        this.showNotificationWithMessage(
          "Error",
          "An error occurred during the action."
        );
      }
    },

    // Edit Document Type (Populate fields with existing data)
    editDocumentType(docType) {
      this.originalDocumentType = { ...docType }; // Store original values to compare for changes
      this.newDocumentType = { ...docType };
      this.showAddForm = true;
    },

    // Close the form after submission
    closeForm() {
      this.showAddForm = false;
      this.newDocumentType = { name: "", description: "" };
      this.originalDocumentType = null; // Reset original document type after closing
      this.nameError = false; // Reset name error
    },

    onModalHide() {
      this.newDocumentType = { name: "", description: "" }; // Clear form data when modal is hidden
      this.nameError = false; // Clear validation error when modal is hidden
    },

    // Show Notification after action completion
    showNotificationWithMessage(title, message) {
      this.notificationTitle = title;
      this.notificationMessage = message;
      this.showNotification = true;
    },
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
  background-color: #e8f0fa;
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
  display: flex;
  /* Use flexbox to center the content */
  align-items: center;
  /* Center vertically */
  flex-direction: column;
  /* Stack the dashboard boxes and sales table vertically */
}

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
  font-size: 14px;
}

.outside-headers {
  display: grid;
  /* Change to grid layout */
  grid-template-columns: 35% 55% 10%;
  /* Match the column widths */
  padding: 0px 15px;
  margin: 20px auto 10px;
  width: 100%;
  max-width: 900px;
}

.header-item {
  flex: 1;
  text-align: left;
  font-size: 14px;
  color: #333;
  font-weight: bold;
}

.document-table th:nth-child(2),
.document-table td:nth-child(2) {
  /* Location column */
  width: 55%;
}

.document-table th:nth-child(3),
.document-table td:nth-child(3) {
  /* Status column */
  width: 10%;
}

.document-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background: #fff;
}

.document-table th,
.document-table td {
  text-align: left;
  vertical-align: middle;
  border: none;
  /* Remove borders from all cells */
}

.document-table th {
  background-color: #f9f9f9;
  font-weight: bold;
}

.btn-warning {
  background-color: #ffc107;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-primary {
  padding: 8px 12px;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  font-size: 14px;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.modal-dialog {
  max-width: 500px;
}

.modal-header {
  background-color: #f8f9fa;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  background-color: #f8f9fa;
}

.btn-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: #000;
}

.form-control {
  border-radius: 8px;
}

.title-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 900px;
  margin: 20px auto;
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
  font-weight: bold;
  /* Align the text to the left */
}

.btn-add {
  background-color: #0560fd;
  font-size: 14px;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
}

.button-container {
  display: flex;
  justify-content: flex-end;
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

.btn-cancel-right {
  background-color: #343a40;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
}
</style>
