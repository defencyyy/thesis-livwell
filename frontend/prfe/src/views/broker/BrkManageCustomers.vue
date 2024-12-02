<template>
  <header>
    <AppHeaderLivwell />
  </header>
  <div class = "main-page">
    <SideNav/>
    <div class = "main-content">
      <div class = "content">
        <div class = "title-wrapper">
          <div class = "title-left">
            <div class = "title-icon"></div>
            <div class = "edit-title">Manage Customers</div>
          </div>
        </div>
        <div class="card border-0 rounded-1 mx-auto" style="max-width: 1100px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)">
          <div class="card-body">
            <div class="row">
              <!-- Toolbar -->
              <div class="toolbar">
                <div class="left-section">
                  <!-- Search Bar -->
                  <div class="search-bar-container">
                    <input
                      type="text"
                      v-model="searchQuery"
                      placeholder="Search by Name or Customer Code"
                      class="search-bar"
                      @input="filterCustomers"
                    />
                    <i class="fa fa-search search-icon"></i>
                  </div>

                  <!-- Sort Dropdown -->
                  <select v-model="sortBy" @change="sortCustomers" class="dropdown">
                    <option value="name_asc">Name (A-Z)</option>
                    <option value="name_desc">Name (Z-A)</option>
                    <option value="site_asc">Site (A-Z)</option>
                    <option value="site_desc">Site (Z-A)</option>
                    <option value="status_asc">Document Status (Complete)</option>
                    <option value="status_desc">Document Status (Pending)</option>
                  </select>
                </div>

                <div class="right-section">
                  <!-- Add Site Button -->
                  <button @click="showModal=true" class="btn-primary add-button">
                    Add Customer
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Customer Table -->
        <div>
          <!-- Headers outside the card -->
          <div class="outside-headers">
            <span class="header-item">Code</span>
            <span class="header-item">Customer Name</span>
            <span class="header-item">Site</span>
            <span class="header-item">Unit</span>
            <span class="header-item">Contact</span>
            <span class="header-item">Document Status</span>
            <span class="header-item">Actions</span>
          </div>

          <!-- Conditional Rendering -->
          <div
            v-if="customers.length === 0"
            class="no-customers-message"
          >
            No customers found.
          </div>

          <div
            v-else
            v-for="(customer, index) in filteredCustomers"
            :key="index"
            class="card border-0 rounded-1 mx-auto my-2"
            style="
              max-width: 1100px;
              box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <div class="card-body">
              <table class="customer-table">
                <tbody>
                  <tr>
                    <td>
                      <span class="customer-code">
                        {{ customer.customer_code }}
                      </span>
                    </td>
                    <td>
                      <span class="customer-name">
                        {{ customer.customer_name }}
                      </span>
                    </td>
                    <td>
                      <span class="customer-site">
                        {{ customer.site }}
                      </span>
                    </td>
                    <td>
                      <span class="customer-unit">
                        {{ customer.unit }}
                      </span>
                    </td>
                    <td>
                      <span class="customer-contact">
                        {{ customer.contact_number }}
                      </span>
                    </td>
                    <td>
                      <span class="customer-document">
                        {{ customer.document_status }}
                      </span>
                    </td>
                    <td>
                      <div class="broker-actions d-flex gap-2">
                        <button
                          @click="openDocumentModal(customer)"
                          style="
                            border: none;
                            background-color: transparent;
                            color: #343a40;
                            cursor: pointer;
                            font-size: 18px;
                          "
                        >
                          <i class="fas fa-file"></i>
                        </button>
                        <button
                          @click="openEditModal(customer)"
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
                          @click="archiveCustomer(customer)"
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
        <!-- Modal for Adding Customer -->
        <b-modal v-model="showModal" hide-header hide-footer centered>
          <div class="modal-title p-3">
            <h5 class="mb-0">Add Customer</h5>
          </div>

          <div class="p-3">
            <form @submit.prevent="addCustomer">
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="firstName" class="form-label">First Name:</label>
                  <input
                    type="text"
                    v-model="firstName"
                    id="firstName"
                    class="form-control"
                    required
                  />
                </div>

                <div class="col-md-6">
                  <label for="lastName" class="form-label">Last Name:</label>
                  <input
                    type="text"
                    v-model="lastName"
                    id="lastName"
                    class="form-control"
                    required
                  />
                </div>
              </div>

              <div class="form-group mb-3">
                <label for="email" class="form-label">Email:</label>
                <input
                  type="email"
                  v-model="email"
                  id="email"
                  class="form-control"
                  required
                />
              </div>

              <div class="form-group mb-3">
                <label for="contactNumber" class="form-label"
                  >Contact Number:</label
                >
                <input
                  type="text"
                  v-model="contactNumber"
                  id="contactNumber"
                  class="form-control"
                  required
                />
              </div>

              <!-- Submit & Cancel Buttons -->
              <div
                class="d-flex justify-content-end gap-2 mt-30"
                style="padding-top: 15px"
              >
                <button type="submit" class="btn-add" style="width: 150px">
                  Add New Broker
                </button>
                <button
                  type="button"
                  @click="showModal = false"
                  class="btn-cancel"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import AppHeaderLivwell from "@/components/Header.vue";
import SideNav from "@/components/SideNav.vue";
import { BModal } from "bootstrap-vue-3";
import { mapState } from "vuex";

export default {
  name: "ManageCustomers",
  components: {
    SideNav,
    BModal,
    AppHeaderLivwell,
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
      showStatusMessage:false,
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
      searchQuery: "", // New property for search input
      filteredCustomers: [], // Holds the filtered list based on search query
    };
  },
  mounted() {
    this.fetchCustomers();
    this.fetchDocumentTypes(); // New function to fetch document types
  },
  methods: {
     filterCustomers() {
    const query = this.searchQuery.toLowerCase(); // Convert search query to lowercase for case-insensitive comparison
    
    if (!query) {
      // If there's no search query, show all customers
      this.filteredCustomers = this.customers;
    } else {
      // Filter customers by name or customer code
      this.filteredCustomers = this.customers.filter((customer) => {
        const customerName = customer.customer_name.toLowerCase();
        const customerCode = customer.customer_code ? customer.customer_code.toLowerCase() : ""; // Assuming customer code is in customer_code field
        return customerName.includes(query) || customerCode.includes(query);
      });
    }
  },
    
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
            console.log(this.customers);
            this.filteredCustomers = this.customers; // Initialize filteredCustomers with all customers

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
        case "status_asc": // New case for sorting by document status A-Z
      this.customers.sort((a, b) =>
        a.document_status.localeCompare(b.document_status)
      );
      break;
    case "status_desc": // New case for sorting by document status Z-A
      this.customers.sort((a, b) =>
        b.document_status.localeCompare(a.document_status)
      );
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
      if (this.selectedCustomer.status != "Reserved") {
        this.showStatusMessage = true; // Show the message to create sales first
      }
      else {
        this.showStatusMessage = false; // Show the message to create sales first
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
  background-color: #f6f6f6;
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

.AppHeaderLivWell {
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

.title-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1100px;
  margin: 20px auto;
  /* Center the wrapper */
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

.toggle-button {
  margin-left: 10px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  color: #333;
  padding: 5px 10px;
  cursor: pointer;
}

.toggle-button:hover {
  background-color: #e0e0e0;
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

.dropdown {
  padding: 8px 12px;
  height: 38px;
  /* Explicitly set height */
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  width: 80%;
  max-width: 150px;
  background-color: white;
  color: #333;
}

/* Button Styles */
.btn-primary.add-button {
  padding: 8px 12px;
  border: 1px solid #42b983;
  border-radius: 3px;
  font-size: 14px;
  background-color: #42b983;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary.add-button:hover {
  background-color: #0056b3;
}

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  margin-top: 0;
  max-width: 1100px;
  /* Ensures the card and grid align */
  margin-left: auto;
  /* Centers the card */
  margin-right: auto;
}

.customer-name {
  font-size: 15px;
  font-weight: bold;
  margin-top: 10px;
}

.customer-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background: #fff;
}

.customer-table th,
.customer-table td {
  padding-bottom: 5px;
  text-align: left;
  vertical-align: middle;
  border: none;
  /* Remove borders from all cells */
}

.customer-table th {
  background-color: #f9f9f9;
  font-weight: bold;
}

.customer-table th:nth-child(2),
.customer-table td:nth-child(2) {
  /* Location column */
  width: 10%;
}

.customer-table th:nth-child(3),
.customer-table td:nth-child(3) {
  /* Status column */
  width: 25%;
}

.customer-table th:nth-child(4),
.customer-table td:nth-child(4) {
  /* Actions column */
  width: 20%;
}

.customer-table th:nth-child(5),
.customer-table td:nth-child(5) {
  /* Actions column */
  width: 15%;
}

.customer-table th:nth-child(6),
.customer-table td:nth-child(6) {
  /* Actions column */
  width: 10%;
}

.customer-table th:nth-child(7),
.customer-table td:nth-child(7) {
  /* Actions column */
  width: 15%;
}

.outside-headers {
  display: grid;
  /* Change to grid layout */
  grid-template-columns: 10% 10% 25% 20% 15% 10% 15%;
  /* Match the column widths */
  padding: 0px 18px;
  margin: 20px auto 10px;
  max-width: 1100px;
}

.header-item {
  flex: 1;
  text-align: left;
  font-size: 15px;
  color: #333;
  font-weight: bold;
}

.btn-add {
  background-color: #42b983;
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
