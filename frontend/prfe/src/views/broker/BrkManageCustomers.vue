<template>
  <div>    
  <AppHeader />
  <div class="manage-customers-page">
    <SideNav />
    <div class="content">
      <h1 class="display-5 fw-bolder text-capitalize">Manage Customers</h1>
      <p>Here you can view and manage your customers.</p>

      <!-- Sorting and Adding Customers Section -->
      <div class="sort-options">
        <label for="sortBy">Sort by:</label>
        <select id="sortBy" v-model="sortBy" @change="sortCustomers">
          <option value="name_asc">Name (A-Z)</option>
          <option value="name_desc">Name (Z-A)</option>
          <option value="site_asc">Site (A-Z)</option>
          <option value="site_desc">Site (Z-A)</option>
        </select>
      </div>

      <button @click="showModal = true" class="btn custom-button">Add Customer</button>



      <!-- Add Customer Modal -->
      <b-modal v-model="showModal" title="Add Customer" hide-footer>
        <form @submit.prevent="addCustomer" class="form-container">
          <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" v-model="email" id="email" class="input-field" required />
          </div>

          <div class="form-group">
            <label for="contactNumber">Contact Number:</label>
            <input
              type="text"
              v-model="contactNumber"
              id="contactNumber"
              class="input-field"
              required
            />
          </div>

          <div class="form-group">
            <label for="lastName">Last Name:</label>
            <input type="text" v-model="lastName" id="lastName" class="input-field" required />
          </div>

          <div class="form-group">
            <label for="firstName">First Name:</label>
            <input type="text" v-model="firstName" id="firstName" class="input-field" required />
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-submit">Submit</button>
            <button type="button" @click="showModal = false" class="btn btn-cancel">Cancel</button>
          </div>
        </form>

        <p v-if="error" class="text-danger">{{ error }}</p>
      </b-modal>


      <!-- Multiple Document Upload Modal -->
      <b-modal
        v-model="showDocumentModal"
        title="Upload Customer Documents"
        hide-footer
      >
        <template v-if="showSalesMessage">
          <p>Please create sales first before uploading documents.</p>
          <button type="button" @click="showDocumentModal = false">
            Close
          </button>
        </template>

        <template v-else>
          <form @submit.prevent="uploadDocuments">
            <div class="document-upload-form">
              <div
                v-for="(docType, index) in documentTypes"
                :key="index"
                class="document-upload-section"
              >
                <label
                  :for="'documentType' + docType.id"
                  class="document-type-label"
                >
                  Select {{ docType.name }}:
                </label>

                <div class="file-input-wrapper">
                  <!-- Show the file input if no file has been selected -->
                  <input
                    type="file"
                    :id="'documentType' + docType.id"
                    @change="handleFileUpload($event, docType.id)"
                    class="file-input"
                    v-if="!filePreviews[docType.id]"
                  />

                  <!-- Show the file name after file has been selected -->
                  <span v-if="filePreviews[docType.id]" class="file-name">
                    {{ filePreviews[docType.id].name }}
                  </span>

                  <!-- Show "No file chosen" only if no file has been selected -->
                  <span v-else class="no-file-chosen">No file chosen</span>
                </div>

                <!-- If a file is uploaded, allow removing it -->
                <button
                  type="button"
                  v-if="filePreviews[docType.id]"
                  @click="removeFile(docType.id)"
                  class="remove-file-btn"
                >
                  Remove
                </button>
              </div>
            </div>

            <div class="form-actions">
              <button type="submit" class="submit-btn">Upload Documents</button>
              <button
                type="button"
                @click="showDocumentModal = false"
                class="cancel-btn"
              >
                Cancel
              </button>
            </div>
          </form>
        </template>
      </b-modal>

      <!-- Table to display the customers -->
      <table v-if="customers.length" class="table">
        <thead>
          <tr>
            <th>Customer Name</th>
            <th>Customer Code</th>
            <th>Site</th>
            <th>Unit</th>
            <th>Contact</th>
            <th>Document Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(customer, index) in customers"
            :key="index"
            @click="openDocumentModal(customer)"
          ></tr>

          <tr v-for="(customer, index) in customers" :key="index">
            <td>{{ customer.customer_name }}</td>
            <td>{{ customer.customer_code }}</td>
            <td>{{ customer.site }}</td>
            <td>{{ customer.unit }}</td>
            <td>{{ customer.contact_number }}</td>
            <td>{{ customer.document_status }}</td>
            <td>
              <!-- Documents Button -->
             <!-- Documents Button -->
              <button
                @click="openDocumentModal(customer)"
                class="btn btn-primary me-5"
              >
                <i class="fas fa-file-alt"></i> Documents
              </button>

              <!-- Edit Button -->
              <button
                @click="openEditModal(customer)"
                class="btn btn-warning me-5"
              >
                <i class="fas fa-edit"></i> Edit
              </button>

              <!-- Archive Button -->
              <button
                @click="archiveCustomer(customer)"
                class="btn btn-danger"
              >
                <i class="fas fa-archive"></i> Archive
              </button>

            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!customers.length">No customers found for this broker.</p>

      <!-- Notification Pop-up (Success/Failure) -->
      <b-modal
        v-model="showNotification"
        :title="notificationTitle"
        hide-footer
      >
        <p>{{ notificationMessage }}</p>
        <button type="button" @click="showNotification = false">Close</button>
      </b-modal>

      <!-- Edit Customer Modal -->
      <b-modal v-model="showEditModal" title="Edit Customer" hide-footer>
        <form @submit.prevent="updateCustomer" class="form-container">
          <div class="form-group">
            <label for="editEmail">Email:</label>
            <input type="email" v-model="editEmail" id="editEmail" class="input-field" required />
          </div>

          <div class="form-group">
            <label for="editContactNumber">Contact Number:</label>
            <input
              type="text"
              v-model="editContactNumber"
              id="editContactNumber"
              class="input-field"
              required
            />
          </div>

          <div class="form-group">
            <label for="editLastName">Last Name:</label>
            <input
              type="text"
              v-model="editLastName"
              id="editLastName"
              class="input-field"
              required
            />
          </div>

          <div class="form-group">
            <label for="editFirstName">First Name:</label>
            <input
              type="text"
              v-model="editFirstName"
              id="editFirstName"
              class="input-field"
              required
            />
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-submit">Update Customer</button>
            <button
              type="button"
              @click="showEditModal = false"
              class="btn btn-cancel"
            >
              Cancel
            </button>
          </div>
        </form>

      </b-modal>
    </div>
  </div>
  </div>
</template>

<script>
import AppHeader from "@/components/Header.vue";
import SideNav from "@/components/SideNav.vue";
import { BModal } from "bootstrap-vue-3";
import { mapState } from "vuex";

export default {
  name: "ManageCustomers",
  components: {
    SideNav,
    BModal,
    AppHeader,
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId,
      userType: (state) => state.userType,
      companyId: (state) => state.companyId,
    }),
  },
  vuexUserId() {
    return this.userId;
  },
  vuexCompanyId() {
    return this.companyId;
  },
  data() {
    return {
      showModal: false, // Controls the visibility of the Add Customer modal
      showDocumentModal: false, // Controls the visibility of the Document Upload modal
      showEditModal: false, // Edit customer modal visibility
      showSalesMessage: false, // Controls the visibility of the "create sales first" message
      showNotification: false, // Controls the visibility of the notification modal
      email: "",
      contactNumber: "",
      lastName: "",
      firstName: "",
      customers: [], // This will hold the list of customers
      selectedCustomer: null, // To hold the currently selected customer
      error: null, // Error message for form submission
      notificationTitle: "", // Title for the notification modal (Success/Failure)
      notificationMessage: "", // Message for the notification modal
      sortBy: "name_asc", // Selected sorting option (default is "Name (A-Z)")
      filePreviews: {}, // Object to store file previews for each document type
      document_status: "Pending",
      documentFiles: {},
    };
  },
  mounted() {
    this.fetchCustomers();
    this.fetchDocumentTypes(); // New function to fetch document types
  },
  methods: {
    async fetchCustomers() {
      if (!this.userId) {
        this.error = "Broker ID not found. Please log in again.";
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:8000/customers/broker/${this.userId}/?include_sales=true`
        );
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            this.customers = data.customers;
          } else {
            this.error = data.message || "Failed to fetch customer data.";
          }
        } else {
          const errorData = await response.json();
          this.error = errorData.message || "Failed to fetch customer data.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching customer data.";
      }
    },

    // Sort customers based on selected option
    sortCustomers() {
      switch (this.sortBy) {
        case "name_asc":
          this.customers.sort((a, b) =>
            a.customer_name.localeCompare(b.customer_name)
          );
          break;
        case "name_desc":
          this.customers.sort((a, b) =>
            b.customer_name.localeCompare(a.customer_name)
          );
          break;
        case "site_asc":
          this.customers.sort((a, b) => a.site.localeCompare(b.site));
          break;
        case "site_desc":
          this.customers.sort((a, b) => b.site.localeCompare(a.site));
          break;
      }
    },
    openEditModal(customer) {
      this.selectedCustomer = customer; // Set the selected customer
      this.editEmail = customer.email;
      this.editContactNumber = customer.contact_number;
      this.editLastName = customer.l_name;
      this.editFirstName = customer.f_name;
      this.showEditModal = true; // Show the edit modal
    },

    // Update customer data
    async updateCustomer() {
      const updatedData = {
        email: this.editEmail,
        contact_number: this.editContactNumber,
        last_name: this.editLastName,
        first_name: this.editFirstName,
      };

      try {
        const response = await fetch(
          `http://localhost:8000/customers/${this.selectedCustomer.id}/`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": this.getCookie("csrftoken"),
            },
            body: JSON.stringify(updatedData),
          }
        );

        const data = await response.json();
        if (response.ok && data.success) {
          this.notificationTitle = "Success!";
          this.notificationMessage = "Customer updated successfully!";
          this.showNotification = true;
          this.showEditModal = false; // Close the modal
          this.fetchCustomers(); // Refresh the customer list
        } else {
          this.notificationTitle = "Error!";
          this.notificationMessage =
            data.message || "Failed to update customer.";
          this.showNotification = true;
        }
      } catch (error) {
        this.notificationTitle = "Error!";
        this.notificationMessage = "An error occurred while updating customer.";
        this.showNotification = true;
      }
    },

    // Opens the document upload modal for the selected customer
    openDocumentModal(customer) {
      this.selectedCustomer = customer; // Set the selected customer
      if (
        this.selectedCustomer.site === "To be followed" ||
        this.selectedCustomer.unit === "To be followed"
      ) {
        this.showSalesMessage = true; // Show the message to create sales first
      } else {
        this.showSalesMessage = false; // Show the document upload form
      }
      this.fetchCustomerDocuments(this.selectedCustomer.id, this.selectedCustomer.sales_id);

      this.showDocumentModal = true; // Open the document upload modal
    },
    // Add a new customer
    async addCustomer() {
      const companyId = this.companyId; // Directly access the mapped state
      if (!this.userId) {
        this.error = "Broker ID not found. Please log in again.";
        return;
      }

      const customerData = {
        broker: this.userId,
        email: this.email,
        contact_number: this.contactNumber,
        last_name: this.lastName,
        first_name: this.firstName,
        company_id: companyId,
      };

      try {
        const response = await fetch("http://localhost:8000/customers/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(customerData),
        });

        const data = await response.json();

        if (response.ok && data.success) {
          this.notificationTitle = "Success!";
          this.notificationMessage = "Customer added successfully!";
          this.showNotification = true; // Show the notification modal
          this.showModal = false; // Close the modal
          this.fetchCustomers(); // Refresh customer list
          this.resetForm();
        } else {
          this.notificationTitle = "Error!";
          this.notificationMessage = data.message || "Failed to add customer.";
          this.showNotification = true; // Show the notification modal
        }
      } catch (error) {
        this.notificationTitle = "Error!";
        this.notificationMessage =
          "An error occurred while adding the customer.";
        this.showNotification = true; // Show the notification modal
      }
    },
    // Fetch existing documents for the selected customer
    async fetchCustomerDocuments(customerId,salesId) {
      try {
        const response = await fetch(
          `http://localhost:8000/documents/customer/${customerId}/${salesId}/`
        );
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            // Store the documents in the component's data
            this.customerDocuments = data.documents; // An array of the customer's documents
            this.updateDocumentPreviews(); // Update the file previews based on existing documents
          } else {
            this.error = data.message || "Failed to fetch customer documents.";
          }
        }
      } catch (error) {
        this.error = "An error occurred while fetching customer documents.";
      }
    },
    // Update file previews based on existing documents
    updateDocumentPreviews() {
      // Initialize filePreviews as an empty object
      this.filePreviews = {};

      // Loop through each document type and check if it's already uploaded
      this.documentTypes.forEach((docType) => {
        const existingDoc = this.customerDocuments.find(
          (doc) => doc.document_type_id === docType.id
        );

        if (existingDoc) {
          // If a document exists for this document type, set the preview
          this.filePreviews[docType.id] = {
            name: existingDoc.file_name, // Use the file name from the database
            url: existingDoc.file_url, // Optionally, you could store the file URL for further use
          };
        }
      });
    },

    // Fetch document types from the API
    async fetchDocumentTypes() {
      try {
        const response = await fetch("http://localhost:8000/document-types/");
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            this.documentTypes = data.documentTypes;
          } else {
            this.error = data.message || "Failed to fetch document types.";
          }
        }
      } catch (error) {
        this.error = "An error occurred while fetching document types.";
      }
    },

    // Handle file selection for multiple document types
    handleFileUpload(event, docTypeId) {
      const file = event.target.files[0];
      if (file) {
        if (this.filePreviews[docTypeId]) {
          this.removeFile(docTypeId); // This will remove the old file
        }
        this.filePreviews[docTypeId] = file; // Store the file preview
        this.documentFiles[docTypeId] = file; // Store the actual file
      }
    },

    // Remove file preview and file data for a document type
    removeFile(docTypeId) {
      delete this.filePreviews[docTypeId];
      delete this.documentFiles[docTypeId];
    },

    // Upload multiple documents
    async uploadDocuments() {
      const formData = new FormData();

      // Loop through the documentFiles object to process each file and its document type
      for (const docTypeId in this.documentFiles) {
        const file = this.documentFiles[docTypeId];

        // Append the file and the associated document type to formData
        formData.append("files[]", file); // Append the file under "files[]"
        formData.append("document_types[]", docTypeId); // Append the document type ID under "document_types[]"
        formData.append("sales_id", this.selectedCustomer.sales_id);

      }

      // Append customer and company information
      formData.append("customer", this.selectedCustomer.id);
      formData.append("company", this.selectedCustomer.company_id);
       // Log the formData for debugging
      try {
        const response = await fetch("http://localhost:8000/upload-document/", {
          method: "POST",
          body: formData,
          headers: {
            "X-CSRFToken": this.getCookie("csrftoken"),
          },
        });

        const data = await response.json();
        if (response.ok && data.success) {
          this.notificationTitle = "Success!";
          this.notificationMessage = "Documents uploaded successfully!";
          this.showNotification = true;
          this.showDocumentModal = false;
          this.resetForm();

          this.fetchCustomers(); // Refresh customer list
        } else {
          this.notificationTitle = "Error!";
          this.notificationMessage =
            data.message || "Failed to upload documents.";
          this.showNotification = true;
        }
      } catch (error) {
        this.notificationTitle = "Error!";
        this.notificationMessage =
          "An error occurred while uploading documents.";
        this.showNotification = true;
      }
    },
    // Reset the form when the modal is closed
    resetForm() {
      this.email = "";
      this.contactNumber = "";
      this.lastName = "";
      this.firstName = "";
      this.documentFiles = {}; // Clear the actual files
  // Optionally, clear any other form-related fields
  this.selectedCustomer = null; // Clear selected customer
    },
    getCookie(name) {
      let value = "; " + document.cookie;
      let parts = value.split("; " + name + "=");
      if (parts.length === 2) return parts.pop().split(";").shift();
    },
    },
};
</script>

<style scoped>
.manage-customers-page {
  display: flex;
  height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}

/* Add some space for the sorting options */
.sort-options {
  margin-bottom: 20px;
}

.sort-options select {
  margin-left: 10px;
}

/* Table Hover Effect */


.table tbody tr:hover {
  cursor: pointer;
  background-color: #f1f1f1;
}

.table tbody tr.active {
  background-color: #d3d3d3;
}

.document-upload-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.document-type-label {
  font-weight: bold;
  margin-bottom: 6px;
  font-size: 1.1em;
}

.file-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.file-input {
  padding: 8px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

.no-file-chosen {
  color: #888;
  font-style: italic;
  padding-left: 8px;
}

.file-name {
  color: #333;
  padding-left: 8px;
}

.remove-file-btn {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 6px;
  font-size: 0.9em;
}

.remove-file-btn:hover {
  background-color: #ff1a1a;
}

.submit-btn {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 1.1em;
  cursor: pointer;
  width: 100%;
}

.submit-btn:hover {
  background-color: #45a049;
}

.cancel-btn {
  background-color: #f44336;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 1.1em;
  cursor: pointer;
  width: 100%;
  margin-top: 10px;
}

.cancel-btn:hover {
  background-color: #e53935;
}
.btn {
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-warning {
  background-color: #ffc107;
  color: black;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn:hover {
  opacity: 0.8;
}





/* dropdown in sort */
/* Sort Options Styling */
.sort-options {
  margin-bottom: 20px;
}

.sort-options label {
  font-size: 14px;
  margin-right: 10px;
  color: #333; /* Text color for the label */
}

/* Dropdown Styling */
.sort-options select {
  background-color: #ffffff; /* White background */
  color: #000000; /* Black text */
  border: 1px solid #ccc; /* Light border */
  border-radius: 8px; /* Rounded corners */
  padding: 8px 12px; /* Padding for better appearance */
  font-size: 14px;
  outline: none;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* Dropdown Option Hover Effect */
.sort-options select option {
  background-color: #ffffff; /* White background */
  color: #000000; /* Black text */
}

/* Hover Effect for Dropdown */
.sort-options select:hover {
  background-color: #007bff; /* Blue background */
  color: white; /* White text */
}

/* Focus Effect for Dropdown */
.sort-options select:focus {
  border-color: #007bff; /* Blue border on focus */
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.8); /* Focus shadow */
}


/* button in add customer  */
.custom-button {
  background-color: #007bff; /* Bootstrap blue */
  color: white; /* White text */
  border-radius: 8px; /* Rounded corners */
  margin: 10px; /* Add some space around the button */
  padding: 10px 20px; /* Adjust padding for better appearance */
  border: none; /* Remove default border */
  font-size: 14px; /* Adjust font size */
  cursor: pointer; /* Pointer cursor for better UX */
  transition: background-color 0.3s ease; /* Smooth transition */
}

.custom-button:hover {
  background-color: #b1b1b1; /* Darker blue on hover */
}





.form-container {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

/* Form Group */
.form-group {
  margin-bottom: 15px;
}

/* Labels */
.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

/* Input Fields */
.input-field {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
  background-color: #fff;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.input-field:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.4);
  outline: none;
}

.form-actions {
  
  justify-content: space-between;
  margin-top: 20px;
}


/* Buttons */
.btn {
  padding: 15px 15px;
  font-size: 14px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, box-shadow 0.3s;
 
}

.btn-submit {
  background-color: #007bff;
  color: white;
}

.btn-submit:hover {
  background-color: #0056b3;
}

.btn-cancel {
  background-color: #ff4d4d;
  color: white;
}

.btn-cancel:hover {
  background-color: #cc0000;
}
</style>
