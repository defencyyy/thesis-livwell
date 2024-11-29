<template>
  <div class="developer-documents-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="container mt-5">
        <!-- Document Types Section -->
        <div class="title-wrapper">
          <div class="title-icon"></div>
          <div class="edit-title">Document Types</div>
        </div>
        <div
          class="card shadow-lg border-0 rounded-3 mx-auto"
          style="max-width: 900px"
        >
          <div class="card-body">
            <!-- Document Types Table -->
            <table class="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Description</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="docType in documentTypes" :key="docType.id">
                  <td>{{ docType.name }}</td>
                  <td>{{ docType.description || "N/A" }}</td>
                  <td>
                    <button
                      @click="editDocumentType(docType)"
                      class="btn btn-warning btn-sm"
                    >
                      Edit
                    </button>
                    <button
                      @click="deleteDocumentType(docType.id)"
                      class="btn btn-danger btn-sm"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <!-- Add Document Type Button -->
            <div class="d-flex justify-content-end mt-3">
              <button @click="showAddForm = true" class="btn btn-primary">
                Add Document Type
              </button>
            </div>
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
/* Add these styles to match devbrokers style for the table and layout */

.developer-documents-page {
  display: flex;
  height: 100vh;
}

.main-content {
  display: flex;
  flex-direction: column;
  margin-top: 30px;
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

.card-body {
  padding: 2.5rem;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  vertical-align: middle;
}

.table th {
  background-color: #f8f9fa;
  font-weight: bold;
}

.table td {
  background-color: #ffffff;
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
  background-color: #6c757d;
  border-radius: 5px;
  margin-right: 10px;
}

.edit-title {
  color: #000000;
  text-align: left;
}

.d-flex {
  display: flex;
  justify-content: end;
}

.mt-3 {
  margin-top: 1rem;
}

/* Adjust button layout */
.table td button {
  padding: 4px 8px;
  margin-right: 5px;
  font-size: 12px;
}

.card-body {
  padding: 2.5rem;
}
</style>
