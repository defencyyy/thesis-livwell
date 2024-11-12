<template>
  <div class="developer-brokers-page">
    <SideNav />
    <div class="content">
      <h1>Total Brokers: {{ filteredBrokers.length }}</h1>

      <!-- JWT Token Display -->
      <div>
        <p><strong>JWT Token:</strong> {{ token }}</p>
      </div>

      <!-- Add Broker Button -->
      <button @click="showModal = true">Add Broker</button>

      <!-- Search Bar -->
      <div>
        <input v-model="searchQuery" placeholder="Search Brokers" />
      </div>

      <!-- Broker Table -->
      <table v-if="filteredBrokers.length" class="table">
        <thead>
          <tr>
            <th>Email</th>
            <th>Username</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Contact Number</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="broker in filteredBrokers" :key="broker.id">
            <td>{{ broker.email }}</td>
            <td>{{ broker.username }}</td>
            <td>{{ broker.first_name }}</td>
            <td>{{ broker.last_name }}</td>
            <td>{{ broker.contact_number }}</td>
          </tr>
        </tbody>
      </table>
      <p v-if="!filteredBrokers.length">No brokers found for this company.</p>

      <!-- Modal for Adding Broker -->
      <b-modal v-model="showModal" title="Add Broker" hide-footer>
        <form @submit.prevent="addBroker">
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
            <label for="lastName">Last Name:</label>
            <input type="text" v-model="lastName" id="lastName" required />
          </div>

          <div>
            <label for="firstName">First Name:</label>
            <input type="text" v-model="firstName" id="firstName" required />
          </div>

          <div>
            <label for="password">Password:</label>
            <input type="password" v-model="password" id="password" required />
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
  name: "DevFuncBroker",
  components: {
    SideNav,
    BModal,
  },
  data() {
    return {
      token: localStorage.getItem("authToken"), // Get token to display
      showModal: false,
      email: "",
      contactNumber: "",
      lastName: "",
      firstName: "",
      password: "12345", // Default password can be pre-filled
      error: null,
      successMessage: null,
      brokers: [],
      searchQuery: "", // For searching brokers
    };
  },
  computed: {
    filteredBrokers() {
      return this.brokers.filter(
        (broker) =>
          broker.first_name
            .toLowerCase()
            .includes(this.searchQuery.toLowerCase()) ||
          broker.last_name
            .toLowerCase()
            .includes(this.searchQuery.toLowerCase()) ||
          broker.email.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  mounted() {
    this.fetchBrokers();
  },
  methods: {
    async fetchBrokers() {
      const companyId = localStorage.getItem("company_id");
      const token = localStorage.getItem("authToken");
      console.log(localStorage.getItem("authToken")); // Log to confirm token

      try {
        const response = await fetch(
          "http://localhost:8000/developer/brokers/",
          {
            headers: {
              Authorization: `Bearer ${token}`, // Ensure the token is prefixed with 'Bearer'
              "Company-ID": companyId, // Pass the company ID in the headers
            },
          }
        );
        if (response.ok) {
          const data = await response.json();
          this.brokers = data.brokers;
        } else {
          const errorData = await response.json();
          this.error = errorData.message || "Failed to fetch brokers data.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching brokers data.";
      }
    },
    async addBroker() {
      const companyId = localStorage.getItem("company_id");
      const token = localStorage.getItem("authToken");

      try {
        const response = await fetch(
          "http://localhost:8000/developer/broker/create/",
          {
            method: "POST",
            headers: {
              Authorization: `Token ${token}`, // Pass the token in the Authorization header
              "Content-Type": "application/json",
              "Company-ID": companyId, // Pass the company ID in the headers
            },
            body: JSON.stringify({
              email: this.email,
              contact_number: this.contactNumber,
              last_name: this.lastName,
              first_name: this.firstName,
              password: this.password,
            }),
          }
        );

        if (response.ok) {
          this.successMessage = "Broker added successfully!";
          this.error = null;
          this.resetForm();
          this.showModal = false;
          this.fetchBrokers(); // Refresh the brokers list
        } else {
          const errorData = await response.json();
          this.error = errorData.message || "Failed to add broker.";
        }
      } catch (error) {
        this.error = "An error occurred while adding the broker.";
      }
    },

    resetForm() {
      this.email = "";
      this.contactNumber = "";
      this.lastName = "";
      this.firstName = "";
      this.password = "";
    },
  },
};
</script>
