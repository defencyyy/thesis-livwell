<template>
  <div>
    <AppHeader />
    <div class="main-page">
      <SideNav />
      <div class="main-content">
        <div class="content">
          <div class="title-wrapper">
            <div class="title-left">
              <div class="title-icon"></div>
              <div class="edit-title"><strong>Manage Customers</strong></div>
            </div>
          </div>

          <div
            class="card border-0 rounded-1 mx-auto"
            style="
              max-width: 1100px;
              box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
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
                    <select
                      v-model="sortBy"
                      @change="sortCustomers"
                      class="dropdown"
                    >
                      <option value="name_asc">Name (A-Z)</option>
                      <option value="name_desc">Name (Z-A)</option>
                      <option value="customer_code_asc">
                        Customer Code (A-Z)
                      </option>
                      <option value="customer_code_desc">
                        Customer Code (Z-A)
                      </option>
                      <!-- New sorting option -->
                    </select>
                  </div>

                  <div class="right-section">
                    <!-- Add Site Button -->
                    <button
                      @click="showModal = true"
                      class="btn-primary add-button"
                    >
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
              <span class="header-item">Name</span>
              <span class="header-item">Contact</span>
              <span class="header-item">Actions</span>
            </div>

            <!-- Conditional Rendering -->
            <div v-if="customers.length === 0" class="no-customers-message">
              No customers found.
            </div>

            <div
              v-else
              v-for="(customer, index) in paginatedCustomers"
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
                        <span class="customer-contact">
                          {{ customer.contact_number }}
                        </span>
                      </td>
                      <td>
                        <div class="broker-actions d-flex gap-2">
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
                            @click="DeleteSaleModal(customer)"
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
              <li :class="['page-item', { disabled: currentPage === totalPages }]">
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

          <!-- Modal for Adding Customer -->
          <b-modal v-model="showModal" hide-header hide-footer centered>
            <div class="modal-title p-3">
              <h5 class="mb-0">Add Customer</h5>
            </div>

            <div class="p-3">
              <form @submit.prevent="addCustomer">
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="firstName" class="form-label"
                      >First Name:</label
                    >
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
                  <button type="submit" class="btn-add">Submit</button>
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

          <!-- Edit Customer Modal -->
          <b-modal v-model="showEditModal" hide-header hide-footer centered>
            <div class="modal-title p-3">
              <h5 class="mb-0">Update Details</h5>
            </div>

            <div class="p-3">
              <form @submit.prevent="updateCustomer">
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="firstName" class="form-label"
                      >First Name:</label
                    >
                    <input
                      type="text"
                      v-model="editFirstName"
                      id="editFirstName"
                      class="form-control"
                      required
                    />
                  </div>

                  <div class="col-md-6">
                    <label for="lastName" class="form-label">Last Name:</label>
                    <input
                      type="text"
                      v-model="editLastName"
                      id="editLastName"
                      class="form-control"
                      required
                    />
                  </div>
                </div>

                <div class="form-group mb-3">
                  <label for="email" class="form-label">Email:</label>
                  <input
                    type="email"
                    v-model="editEmail"
                    id="editEmail"
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
                    v-model="editContactNumber"
                    id="editContactNumber"
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
                    Update
                  </button>
                  <button
                    type="button"
                    @click="showEditModal = false"
                    class="btn-cancel"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </b-modal>

          <!-- Documents -->
          <b-modal v-model="showDocumentModal" hide-header hide-footer centered>
            <div class="modal-title p-3">
              <h5 class="mb-0">Customer Documents</h5>
            </div>

            <div class="p-3">
              <div v-if="showStatusMessage">
                <p>Waiting for Developer to confirm Reservation</p>
                <div class="button-container">
                  <button
                    type="button"
                    @click="showDocumentModal = false"
                    class="btn-cancel-right"
                  >
                    Close
                  </button>
                </div>
              </div>
              <div v-else>
                <form @submit.prevent="uploadDocuments">
                  <div class="document-upload-form">
                    <div
                      v-for="(docType, index) in documentTypes"
                      :key="index"
                      class="document-upload-section mb-3"
                    >
                      <label
                        :for="'documentType' + docType.id"
                        class="form-label"
                      >
                        <b> Upload {{ docType.name }} </b>
                      </label>

                      <div
                        class="file-input-wrapper d-flex align-items-center gap-2"
                      >
                        <!-- Show the file input if no file has been selected -->
                        <input
                          type="file"
                          :id="'documentType' + docType.id"
                          @change="handleFileUpload($event, docType.id)"
                          class="form-control"
                          v-if="!filePreviews[docType.id]"
                        />

                        <!-- Show the file name after file has been selected -->
                        <div
                          v-if="filePreviews[docType.id]"
                          class="d-flex align-items-center gap-2"
                        >
                          <span class="file-name">
                            {{ filePreviews[docType.id].name }}
                          </span>

                          <button
                            type="button"
                            @click="removeFile(docType.id)"
                            class="btn btn-danger btn-sm"
                          >
                            <i class="fas fa-trash"></i>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="form-actions">
                    <div
                      class="d-flex justify-content-end gap-2 mt-30"
                      style="padding-top: 15px"
                    >
                      <button
                        type="submit"
                        class="btn-add"
                        style="width: 150px"
                      >
                        Upload Document
                      </button>
                      <button
                        type="button"
                        @click="showDocumentModal = false"
                        class="btn-cancel"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </b-modal>

          <!-- Delete -->
          <b-modal
            v-model="showDeleteModal"
            title="Delete Confirmation"
            hide-footer
            centered
          >
            <p>Are you sure you want to delete this this customer?</p>

            <div
              class="d-flex justify-content-end gap-2 mt-30"
              style="padding-top: 15px"
            >
              <button
                type="button"
                @click="deleteSaleFromBackend(selectedCustomer.id)"
                class="btn-add"
              >
                Yes
              </button>
              <button
                type="button"
                @click="showDeleteModal = false"
                class="btn-cancel"
              >
                Cancel
              </button>
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
        </div>
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
    sortedAndFilteredCustomers() {
      let filtered = this.searchQuery
        ? this.customers.filter((customer) => {
            const customerName = customer.customer_name.toLowerCase();
            const customerCode = customer.customer_code
              ? customer.customer_code.toLowerCase()
              : "";
            return (
              customerName.includes(this.searchQuery.toLowerCase()) ||
              customerCode.includes(this.searchQuery.toLowerCase())
            );
          })
        : this.customers;

      switch (this.sortBy) {
        case "name_asc":
          return filtered.sort((a, b) =>
            a.customer_name.localeCompare(b.customer_name)
          );
        case "name_desc":
          return filtered.sort((a, b) =>
            b.customer_name.localeCompare(a.customer_name)
          );
        case "customer_code_asc":
          return filtered.sort((a, b) =>
            a.customer_code.localeCompare(b.customer_code)
          );
        case "customer_code_desc":
          return filtered.sort((a, b) =>
            b.customer_code.localeCompare(a.customer_code)
          );
        default:
          return filtered;
      }
    },
    paginatedCustomers() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.sortedAndFilteredCustomers.slice(startIndex, endIndex);
    },
    totalPages() {
      return Math.ceil(
        this.sortedAndFilteredCustomers.length / this.itemsPerPage
      );
    },
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
      showEditModal: false, // Edit customer modal visibility
      showDeleteModal: false, // To toggle the delete modal visibility
      showSalesMessage: false, // Controls the visibility of the "create sales first" message
      showStatusMessage: false,
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
      searchQuery: "", // New property for search input
      filteredCustomers: [], // Holds the filtered list based on search query
      currentPage: 1, // Current page number
      itemsPerPage: 15, // Number of customers per page
    };
  },
  mounted() {
    this.fetchCustomers();
  },
  methods: {
    goToPage(pageNumber) {
      if (pageNumber > 0 && pageNumber <= this.totalPages) {
        this.currentPage = pageNumber;
      }
    },

    async fetchCustomers() {
      if (!this.userId) {
        this.error = "Broker ID not found. Please log in again.";
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:8000/customers/broker/${this.userId}/?include_sales=false`
        );
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            this.customers = data.customers;
            this.filteredCustomers = this.customers; // Initialize filteredCustomers with all customers
            this.sortCustomers(); // Call the sorting function here
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

    DeleteSaleModal(customer) {
      this.selectedCustomer = customer; // Set the selected customer
      if (
        this.selectedCustomer.site === "To be followed" ||
        this.selectedCustomer.unit === "To be followed"
      ) {
        this.showSalesMessage = true; // Show the message to create sales first
      } else {
        this.showSalesMessage = false; // Show the document upload form
      }
      this.showDeleteModal = true; // Show the modal
    },
    async deleteSaleFromBackend(customer_id) {
      try {
        // Send a POST request with DELETE override if CSRF protection is enabled
        const response = await fetch(
          `http://localhost:8000/delete_customer/${customer_id}/`,
          {
            method: "POST", // Use POST with _method override
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": this.getCookie("csrftoken"),
            },
            body: JSON.stringify({ _method: "DELETE" }), // Overriding method to DELETE
          }
        );

        if (response.ok) {
          this.notificationTitle = "Success!";
          this.notificationMessage = this.showSalesMessage
            ? "Customer Removed Successfully!"
            : "Customer Sale Removed Successfully!";
          this.showNotification = true;
          this.showDeleteModal = false; // Close the modal
          this.fetchCustomers(); // Refresh customers list after deletion
        } else {
          this.notificationTitle = "Error!";
          this.notificationMessage = this.showSalesMessage
            ? "Customer Removal Failed!"
            : "Customer Sale Removal Failed!";
          this.showNotification = true;
          this.showDeleteModal = false; // Close the modal
          this.fetchCustomers(); // Refresh customers list even if there's an error
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while deleting the sale or customer");
      }
    },
    // Add a new customer
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
        this.showNotification = true; // Show the notification modal
      }
    },
    // Fetch existing documents for the selected customer
    async fetchCustomerDocuments(customerId, salesId) {
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
      resetForm() {
      this.email = '';
      this.contactNumber = '';
      this.lastName = '';
      this.firstName = '';
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
  padding-right: 20px;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-bar-container {
  position: relative;
  width: 100%;
  max-width: 400px;
}

.search-bar {
  width: 400px;
  padding: 8px 12px 8px 40px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.search-icon {
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
  color: #777;
  font-size: 16px;
  pointer-events: none;
}

.dropdown {
  padding: 8px 12px;
  height: 38px;
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

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  margin-top: 0;
  max-width: 1100px;
  margin-left: auto;
  margin-right: auto;
}

.customer-name {
  font-size: 14px;
  font-weight: bold;
  margin-top: 10px;
}

.outside-headers {
  display: grid;
  grid-template-columns: 25% 35% 30% 10%;
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
  white-space: nowrap;
}

.customer-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  text-align: left; /* Consistent with headers */
}

.customer-table td {
  padding: 10px 0; /* Matches outside-headers padding */
}

.customer-table td:nth-child(1),
.outside-headers .header-item:nth-child(1) {
  width: 25%;
}

.customer-table td:nth-child(2),
.outside-headers .header-item:nth-child(2) {
  width: 35%;
}

.customer-table td:nth-child(3),
.outside-headers .header-item:nth-child(3) {
  width: 30%;
}

.customer-table td:nth-child(4),
.outside-headers .header-item:nth-child(4) {
  width: 10%;
}

.btn-add {
  background-color: #0560fd;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 10px;
}

.btn-cancel {
  background-color: #343a40;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 10px;
}

.button-container {
  display: flex;
  justify-content: flex-end;
}

.btn-cancel-right {
  background-color: #343a40;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 10px;
  cursor: pointer;
}

input[type="file"] {
  border: 1px solid #ccc;
  border-radius: 8px;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: -15px; /* Reduce margin */
  padding-right: 40px; /* Reduce padding */
  font-size: 14px; /* Smaller font size */
  line-height: 1.2; /* Adjust line height for compactness */
}

.page-item {
  margin: 0 2px; /* Reduce spacing between buttons */
}

.page-link {
  padding: 4px 8px; /* Smaller button padding */
  font-size: 14px; /* Match font size for consistency */
}

/* General Styles for Small Screens */
@media (max-width: 768px) {
  .main-page {
    flex-direction: column;
  }

  .SideNav {
    width: 100%;
    position: relative;
    height: auto;
  }

  .main-content {
    margin-left: 0;
    margin-top: 0;
  }

  .content {
    padding: 10px;
  }

  .title-wrapper {
    flex-direction: column;
    align-items: flex-start;
  }

  .toolbar {
    flex-direction: column;
    gap: 10px;
  }

  .search-bar-container {
    width: 100%;
  }

  .search-bar {
    width: 100%;
  }

  .dropdown {
    width: 100%;
    margin-left: 0;
  }

  .right-section .add-button {
    width: 100%;
    text-align: center;
  }

  .customer-table td {
    font-size: 0.875rem;
  }

  .pagination-controls {
    flex-wrap: wrap;
    gap: 5px;
  }

  .page-button {
    padding: 8px 16px;
  }
}

/* Styles for Extra Small Screens */
@media (max-width: 480px) {
  .title-left {
    flex-direction: column;
    align-items: flex-start;
  }

  .edit-title {
    font-size: 1.25rem;
  }

  .search-bar {
    padding: 8px;
  }

  .customer-table td {
    padding: 8px;
  }

  .btn-add,
  .btn-cancel {
    width: 100%;
    padding: 8px;
  }

  .btn-cancel-right {
    width: 100%;
    padding: 8px;
  }
}
</style>
