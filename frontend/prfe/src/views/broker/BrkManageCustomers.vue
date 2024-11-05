<template>
  <div class="manage-customers-page">
    <SideNav />
    <div class="content">
      <h1>Manage Customers</h1>
      <p>Here you can view and manage your customers.</p>

      <!-- Add Customer Button -->
      <button @click="showModal = true">Add Customer</button>

      <!-- Modal -->
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
        <p v-if="successMessage">{{ successMessage }}</p>
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
      showModal: false, // Controls the visibility of the modal
      email: '',
      contactNumber: '',
      affiliatedLink: '',
      lastName: '',
      firstName: '',
      error: null,
      successMessage: null,
    };
  },
  methods: {
    async addCustomer() {
      const brokerId = localStorage.getItem("broker_id");
      const phonePattern = /^(?:\(\d{3}\)|\d{3}-)?\d{3}-\d{4}$/;

      if (!phonePattern.test(this.contactNumber)) {
        this.error = "Please enter a valid phone number format (e.g., 123-456-7890).";
        this.successMessage = null;
        return;
      }

      try {
        const brokerResponse = await fetch(`http://localhost:8000/brokers/${brokerId}/`);
        if (!brokerResponse.ok) {
          const errorData = await brokerResponse.json();
          this.error = errorData.message || "Failed to fetch broker data.";
          this.successMessage = null;
          return;
        }
        const brokerData = await brokerResponse.json();
        const companyId = brokerData.company_id;

        const response = await fetch('http://localhost:8000/customers/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            broker: brokerId,
            company_id: companyId,
            email: this.email,
            contact_number: this.contactNumber,
            affiliated_link: this.affiliatedLink,
            last_name: this.lastName,
            first_name: this.firstName,
          }),
        });

        if (response.ok) {
          this.successMessage = "Customer added successfully!";
          this.error = null;
          this.resetForm();
          this.showModal = false; // Close the modal after submission
        } else {
          const errorData = await response.json();
          this.error = errorData.message || "Failed to add customer.";
          this.successMessage = null;
        }
      } catch (error) {
        this.error = "An error occurred while adding the customer.";
        this.successMessage = null;
      }
    },
    resetForm() {
      this.email = '';
      this.contactNumber = '';
      this.affiliatedLink = '';
      this.lastName = '';
      this.firstName = '';
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
