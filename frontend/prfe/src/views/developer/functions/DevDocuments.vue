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

        <div style="width: 100%; max-width: 900px;" >
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
            style="
             
              box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <div class="card-body">
              <table class="document-table">
                <tbody>
                  <tr>
                    <td>
                      <span class="document-name">
                        <td>{{ docType.name }}</td>
                      </span>
                    </td>
                    <td>
                      <span class="document-description"><td>{{ docType.description || "N/A" }}</td></span>
                    </td>
                    <td>
                    <button
                      @click="editDocumentType(docType)"
                      class="btn btn-warning btn-sm"
                    >
                      Edit
                    </button>
                    <!-- <button
                      @click="deleteDocumentType(docType.id)"
                      class="btn btn-danger btn-sm"
                    >
                      Delete
                    </button> -->
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
        <div v-if="showAddForm" class="modal show d-block" tabindex="-1">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Add New Document Type</h5>
                <button
                  type="button"
                  class="btn-close"
                  @click="closeForm"
                ></button>
              </div>
              <div class="modal-body">
                <div class="mb-3">
                  <label for="documentTypeName" class="form-label">Name</label>
                  <input
                    type="text"
                    class="form-control"
                    id="documentTypeName"
                    v-model="newDocumentType.name"
                    placeholder="Enter document type name"
                  />
                </div>
                <div class="mb-3">
                  <label for="documentTypeDescription" class="form-label"
                    >Description</label
                  >
                  <textarea
                    class="form-control"
                    id="documentTypeDescription"
                    v-model="newDocumentType.description"
                    rows="4"
                    placeholder="Enter description"
                  ></textarea>
                </div>
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click="closeForm"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  class="btn btn-primary"
                  @click="saveDocumentType"
                >
                  Save
                </button>
              </div>
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
  name: "DevDocuments",
  components: { SideNav, AppHeader },
  data() {
    return {
      documentTypes: [], // List of document types
      showAddForm: false, // Controls visibility of Add/Edit form modal
      newDocumentType: { name: "", description: "" }, // Holds the document type data for add/edit
    };
  },
  mounted() {
    this.fetchDocumentTypes();
  },
  methods: {
    // Axios instance with interceptor for refreshing tokens
    getAxiosInstance() {
      const instance = axios.create({
        baseURL: "http://localhost:8000/developer/",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          "Content-Type": "application/json",
        },
      });

      // Add response interceptor
      instance.interceptors.response.use(
        (response) => response,
        async (error) => {
          if (error.response && error.response.status === 401) {
            // Token expired, attempt to refresh
            try {
              const refreshResponse = await axios.post(
                "http://localhost:8000/auth/refresh/",
                {
                  refresh: localStorage.getItem("refreshToken"),
                }
              );

              if (refreshResponse.status === 200) {
                // Save new tokens
                localStorage.setItem(
                  "accessToken",
                  refreshResponse.data.access
                );

                // Retry original request with new access token
                error.config.headers.Authorization = `Bearer ${refreshResponse.data.access}`;
                return axios(error.config);
              }
            } catch (refreshError) {
              console.error("Error refreshing token:", refreshError);
              // Redirect to login if refresh fails
              this.$router.push({ name: "Login" });
            }
          }
          return Promise.reject(error);
        }
      );

      return instance;
    },

    // Fetch all document types from the backend
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

    // Save (create/update) a document type
    async saveDocumentType() {
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
          this.fetchDocumentTypes(); // Refresh the list
          this.closeForm(); // Close the modal
        }
      } catch (error) {
        console.error("Error saving document type:", error);
      }
    },

    // Prepare the form for editing a document type
    editDocumentType(docType) {
      this.newDocumentType = { ...docType }; // Load the existing data into the form
      this.showAddForm = true;
    },

    // Delete a document type
    async deleteDocumentType(id) {
      const axiosInstance = this.getAxiosInstance();
      if (confirm("Are you sure you want to delete this document type?")) {
        try {
          await axiosInstance.delete(`documents/document-types/${id}/`);
          this.fetchDocumentTypes(); // Refresh the list
        } catch (error) {
          console.error("Error deleting document type:", error);
        }
      }
    },

    // Close the Add/Edit form modal
    closeForm() {
      this.showAddForm = false;
      this.newDocumentType = { name: "", description: "" };
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

</style>
