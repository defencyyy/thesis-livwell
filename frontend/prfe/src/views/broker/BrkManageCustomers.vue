<template>
  <header>
    <HeaderLivwell />
  </header>
  <div class="manage-customers-page">
    <SideNav />
    <div class="content">
      <h1>Manage Customers</h1>
      <p>Here you can view and manage your customers.</p>

      <!-- Add Customer Button -->
      <button @click="showModal = true">Add Customer</button>

      <!-- Modal for Adding Customer -->

      <b-modal v-model="showModal" title="Add Customer" hide-footer>
        <form @submit.prevent="addCustomer">
          <div>
            <label for="email">Email:</label>
            <input type="email" v-model="email" id="email" required />
          </div>

          <div>
            <label for="contactNumber">Contact Number:</label>
            <input
              type="text"
              v-model="contactNumber"
              id="contactNumber"
              required
            />
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

      <!-- Modal for Document Upload -->
      <b-modal
        v-model="showDocumentModal"
        title="Upload Customer Documents"
        hide-footer
      >
        <form @submit.prevent="uploadDocuments">
          <div>
            <label for="validId">Valid ID:</label>
            <input type="file" id="validId" ref="validId" />
          </div>

          <div>
            <label for="proofOfIncome">Proof of Income:</label>
            <input type="file" id="proofOfIncome" ref="proofOfIncome" />
          </div>

          <div>
            <label for="proofOfBilling">Proof of Billing:</label>
            <input type="file" id="proofOfBilling" ref="proofOfBilling" />
          </div>

          <div>
            <label for="reservationAgreement">Reservation Agreement:</label>
            <input
              type="file"
              id="reservationAgreement"
              ref="reservationAgreement"
            />
          </div>

          <div>
            <label for="salesAgreement">Sales Agreement:</label>
            <input type="file" id="salesAgreement" ref="salesAgreement" />
          </div>

          <div>
            <label for="tin">TIN:</label>
            <input type="file" id="tin" ref="tin" />
          </div>

          <button type="submit">Submit Documents</button>
          <button type="button" @click="showDocumentModal = false">
            Cancel
          </button>
        </form>
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
          <tr
            v-for="(customer, index) in customers"
            :key="index"
            @click="openDocumentModal(customer)"
          >
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
      <b-modal
        v-model="showNotification"
        :title="notificationTitle"
        hide-footer
      >
        <p>{{ notificationMessage }}</p>
        <button type="button" @click="showNotification = false">Close</button>
      </b-modal>
    </div>
  </div>
</template>

<script>
import HeaderLivwell from "@/components/HeaderLivwell.vue";
import SideNav from "@/components/SideNav.vue";
import { BModal } from "bootstrap-vue-3";

export default {
  name: "ManageCustomers",
  components: {
    SideNav,
    BModal,
    HeaderLivwell,
  },
  data() {
    return {
      showModal: false, // Controls the visibility of the Add Customer modal
      showDocumentModal: false, // Controls the visibility of the Document Upload modal
      showNotification: false, // Controls the visibility of the notification modal
      email: "",
      contactNumber: "",
      affiliatedLink: "",
      lastName: "",
      firstName: "",
      customers: [], // This will hold the list of customers
      selectedCustomer: null, // To hold the currently selected customer
      error: null, // Error message for form submission
      notificationTitle: "", // Title for the notification modal (Success/Failure)
      notificationMessage: "", // Message for the notification modal
    };
  },
  mounted() {
    this.fetchCustomers();
  },
  methods: {
    async fetchCustomers() {
      const brokerId = this.$store.getters.getUserId; // Get the user_id from Vuex store
      if (!brokerId) {
        this.error = "Broker ID not found. Please log in again.";
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:8000/customers/broker/${brokerId}/?include_sales=true`
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

    // Opens the document upload modal for the selected customer
    openDocumentModal(customer) {
      this.selectedCustomer = customer; // Set the selected customer directly
      console.log("Selected customer:", this.selectedCustomer); // Directly log the selected customer data
      this.showDocumentModal = true; // Open the document upload modal
    },
    async uploadDocuments() {
      const customer = this.selectedCustomer; // Directly use selectedCustomer
      console.log("Selected customer data:", customer); // Log the actual customer data

      if (!customer || !customer.id) {
        this.notificationTitle = "Error!";
        this.notificationMessage =
          "No customer selected or invalid customer data.";
        this.showNotification = true; // Show the notification modal
        return; // Exit the function if no customer is selected or invalid
      }

      const formData = new FormData();
      formData.append("valid_id", this.$refs.validId.files[0]);
      formData.append("proof_of_income", this.$refs.proofOfIncome.files[0]);
      formData.append("proof_of_billing", this.$refs.proofOfBilling.files[0]);
      formData.append(
        "reservation_agreement",
        this.$refs.reservationAgreement.files[0]
      );
      formData.append("sales_agreement", this.$refs.salesAgreement.files[0]);
      formData.append("tin", this.$refs.tin.files[0]);

      try {
        const response = await fetch(
          `http://localhost:8000/customers/${customer.id}/upload-documents`, // Use customer.id
          {
            method: "POST",
            body: formData,
          }
        );

        if (response.ok) {
          this.notificationTitle = "Success!";
          this.notificationMessage = "Documents uploaded successfully!";
          this.showNotification = true; // Show the notification modal
          this.showDocumentModal = false; // Close the document upload modal
        } else {
          const errorData = await response.json();
          this.notificationTitle = "Error!";
          this.notificationMessage =
            errorData.message || "Failed to upload documents.";
          this.showNotification = true; // Show the notification modal
        }
      } catch (error) {
        this.notificationTitle = "Error!";
        this.notificationMessage =
          "An error occurred while uploading documents.";
        this.showNotification = true; // Show the notification modal
      }
    },
    // Add a new customer
    async addCustomer() {
      const brokerId = this.$store.getters.getUserId;
      if (!brokerId) {
        this.error = "Broker ID not found. Please log in again.";
        return;
      }

      const customerData = {
        broker: brokerId,
        email: this.email,
        contact_number: this.contactNumber,
        affiliated_link: this.affiliatedLink || "",
        last_name: this.lastName,
        first_name: this.firstName,
        company_id: 1, // Replace with the actual company_id if available
      };

      try {
        const response = await fetch("http://localhost:8000/customers/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.getCookie("csrftoken"), // Add CSRF token if needed
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
        this.notificationMessage =
          "An error occurred while adding the customer.";
        this.showNotification = true; // Show the notification modal
      }
    },

    // Reset the form when the modal is closed
    resetForm() {
      this.email = "";
      this.contactNumber = "";
      this.affiliatedLink = "";
      this.lastName = "";
      this.firstName = "";
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
</style>
