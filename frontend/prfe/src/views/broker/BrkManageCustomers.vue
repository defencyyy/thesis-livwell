<template>
  <div class="manage-customers-page">
    <SideNav />
    <div class="content">
      <h1>Manage Customers</h1>
      <p>Here you can view and manage your customers.</p>

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

        <button type="submit">Add Customer</button>
      </form>

      <p v-if="error" class="text-danger">{{ error }}</p>
      <p v-if="successMessage">{{ successMessage }}</p>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";

export default {
  name: "ManageCustomers",
  components: {
    SideNav,
  },
  data() {
    return {
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
      // Get the currently logged broker's ID (you'll need to implement this logic)
      const brokerId = localStorage.getItem("broker_id");

      // Add customer logic
      try {
        const response = await fetch('http://localhost:8000/customers/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            broker: brokerId,
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
    async getCurrentBrokerId() {
      // Replace with actual logic to retrieve the logged-in broker's ID
      // For example, you might fetch it from the store or an API endpoint
      const response = await fetch('http://localhost:8000/current-broker/');
      const data = await response.json();
      return data.id; // Assuming the response contains the broker ID
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
