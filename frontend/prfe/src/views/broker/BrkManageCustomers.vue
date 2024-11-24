<template>
  <div class="manage-customers-page">
    <SideNav />
    <div class="content">
      <h1>Manage Customers</h1>
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

      <button @click="showModal = true">Add Customer</button>

      <!-- Add Customer Modal -->
      <b-modal v-model="showModal" title="Add Customer" hide-footer>
        <form @submit.prevent="addCustomer">
          <div>
            <label for="email">Email:</label>
            <input type="email" v-model="email" id="email" required />
          </div>

          <div>
            <label for="contactNumber">Contact Number:</label>
            <input type="text" v-model="contactNumber" id="contactNumber" required />
          </div>

          <div>
            <label for="affiliatedLink">Affiliated Link:</label>
            <input type="url" v-model="affiliatedLink" id="affiliatedLink" />
          </div>

          <div>
            <label for="lastName">Last Name:</label>
            <input type="text" v-model="lastName" id="lastName" required />
          </div>

          <div>
            <label for="firstName">First Name:</label>
            <input type="text" v-model="firstName" id="firstName" required />
          </div>

          <button type="submit">Submit</button>
          <button type="button" @click="showModal = false">Cancel</button>
        </form>

        <p v-if="error" class="text-danger">{{ error }}</p>
      </b-modal>

      <!-- Multiple Document Upload Modal -->
      <!-- Multiple Document Upload Modal -->
<b-modal v-model="showDocumentModal" title="Upload Customer Documents" hide-footer>
  <template v-if="showSalesMessage">
    <p>Please create sales first before uploading documents.</p>
    <button type="button" @click="showDocumentModal = false">Close</button>
  </template>

  <template v-else>
    <form @submit.prevent="uploadDocuments">
      <div class="document-upload-form">
        <div v-for="(docType, index) in documentTypes" :key="index" class="document-upload-section">
          <label :for="'documentType' + docType.id" class="document-type-label">
            Select {{ docType.name }}:
          </label>
          <div class="file-input-wrapper">
            <input type="file" :id="'documentType' + docType.id" @change="handleFileUpload($event, docType.id)" class="file-input" />
            <span v-if="!filePreviews[docType.id]" class="no-file-chosen">No file chosen</span>
            <span v-if="filePreviews[docType.id]" class="file-name">{{ filePreviews[docType.id].name }}</span>
          </div>
          <button type="button" v-if="filePreviews[docType.id]" @click="removeFile(docType.id)" class="remove-file-btn">Remove</button>
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" class="submit-btn">Upload Documents</button>
        <button type="button" @click="showDocumentModal = false" class="cancel-btn">Cancel</button>
      </div>
    </form>
  </template>
</b-modal>


      <!-- Table to display the customers -->
      <table v-if="customers.length" class="table">
        <thead>
          <tr>
            <th>Customer Name</th>
            <th>Site</th>
            <th>Unit</th>
            <th>Contact</th>
            <th>Document Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(customer, index) in customers" :key="index" @click="openDocumentModal(customer)">
            <td>{{ customer.customer_name }}</td>
            <td>{{ customer.site }}</td>
            <td>{{ customer.unit }}</td>
            <td>{{ customer.contact_number }}</td>
            <td>{{ customer.document_status }}</td>
          </tr>
        </tbody>
      </table>
      <p v-if="!customers.length">No customers found for this broker.</p>

      <!-- Notification Pop-up (Success/Failure) -->
      <b-modal v-model="showNotification" :title="notificationTitle" hide-footer>
        <p>{{ notificationMessage }}</p>
        <button type="button" @click="showNotification = false">Close</button>
      </b-modal>
    </div>
  </div>
</template>




<script>
import SideNav from "@/components/SideNav.vue";
import { BModal } from "bootstrap-vue-3";

export default {
  name: "ManageCustomers",
  components: {
    SideNav,
    BModal,
  },
  data() {
    return {
      showModal: false, // Controls the visibility of the Add Customer modal
      showDocumentModal: false, // Controls the visibility of the Document Upload modal
      showSalesMessage: false,  // Controls the visibility of the "create sales first" message
      showNotification: false, // Controls the visibility of the notification modal
      email: '',
      contactNumber: '',
      affiliatedLink: '',
      lastName: '',
      firstName: '',
      customers: [],  // This will hold the list of customers
      selectedCustomer: null, // To hold the currently selected customer
      error: null, // Error message for form submission
      notificationTitle: '', // Title for the notification modal (Success/Failure)
      notificationMessage: '', // Message for the notification modal
      sortBy: 'name_asc', // Selected sorting option (default is "Name (A-Z)")
      filePreviews: {},  // Object to store file previews for each document type
      documentFiles: {}, 
    };
  },
  mounted() {
    this.fetchCustomers();
    this.fetchDocumentTypes();  // New function to fetch document types

  },
  methods: {
    // Fetch customer data from API
    async fetchCustomers() {
      const brokerId = localStorage.getItem("broker_id");
      if (!brokerId) {
        this.error = "Broker ID not found. Please log in again.";
        return;
      }

      try {
        const response = await fetch(`http://localhost:8000/customers/broker/${brokerId}/?include_sales=true`);
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            this.customers = data.customers;
            this.sortCustomers(); // Apply the initial sorting
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
        case 'name_asc':
          this.customers.sort((a, b) => a.customer_name.localeCompare(b.customer_name));
          break;
        case 'name_desc':
          this.customers.sort((a, b) => b.customer_name.localeCompare(a.customer_name));
          break;
        case 'site_asc':
          this.customers.sort((a, b) => a.site.localeCompare(b.site));
          break;
        case 'site_desc':
          this.customers.sort((a, b) => b.site.localeCompare(a.site));
          break;
      }
    },

    // Opens the document upload modal for the selected customer
    openDocumentModal(customer) {
      this.selectedCustomer = customer; // Set the selected customer
       if (this.selectedCustomer.site === "To be followed" || this.selectedCustomer.unit === "To be followed") {
      this.showSalesMessage = true; // Show the message to create sales first
    } else {
      this.showSalesMessage = false; // Show the document upload form
    }
      this.showDocumentModal = true; // Open the document upload modal
    },
    // Add a new customer
    async addCustomer() {
      const brokerId = localStorage.getItem("broker_id");
      if (!brokerId) {
        this.error = "Broker ID not found. Please log in again.";
        return;
      }


      const customerData = {
        broker: brokerId,
        email: this.email,
        contact_number: this.contactNumber,
        affiliated_link: this.affiliatedLink || '',
        last_name: this.lastName,
        first_name: this.firstName,
        // Fix this
        company_id: 1, // Replace with the actual company_id if available
      };

      try {
        const response = await fetch('http://localhost:8000/customers/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken') // Add CSRF token if needed
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
        } else {
          this.notificationTitle = "Error!";
          this.notificationMessage = data.message || "Failed to add customer.";
          this.showNotification = true; // Show the notification modal
        }
      } catch (error) {
        this.notificationTitle = "Error!";
        this.notificationMessage = "An error occurred while adding the customer.";
        this.showNotification = true; // Show the notification modal
      }
    },
   // Fetch document types from the API
    async fetchDocumentTypes() {
      try {
        const response = await fetch('http://localhost:8000/document-types/');
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
    
    // Optionally append default values for object_id and content_id if needed
    formData.append("object_id", 1);  // Default value of 1 for object_id
    formData.append("content_id", 1); // Default value of 1 for content_id
  }

  // Append customer and company information
  formData.append("customer", this.selectedCustomer.id);
  formData.append("company", this.selectedCustomer.company_id);
  
  try {
    const response = await fetch('http://localhost:8000/upload-document/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': this.getCookie('csrftoken'),
      },
    });

    const data = await response.json();
    if (response.ok && data.success) {
      this.notificationTitle = "Success!";
      this.notificationMessage = "Documents uploaded successfully!";
      this.showNotification = true;
      this.showDocumentModal = false;
      this.fetchCustomers(); // Refresh customer list
    } else {
      this.notificationTitle = "Error!";
      this.notificationMessage = data.message || "Failed to upload documents.";
      this.showNotification = true;
    }
  } catch (error) {
    this.notificationTitle = "Error!";
    this.notificationMessage = "An error occurred while uploading documents.";
    this.showNotification = true;
  }
},
    // Reset the form when the modal is closed
    resetForm() {
      this.email = '';
      this.contactNumber = '';
      this.affiliatedLink = '';
      this.lastName = '';
      this.firstName = '';
    },

    // Get the CSRF token (if necessary)
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
  background-color: #4CAF50;
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

</style>

