<template>
  <div class="developer-brokers-page">
    <SideNav />
    <div class="content">
      <h1>Total Brokers: {{ brokers.length }}</h1>

      <button @click="showModal = true">Add Broker</button>

      <!-- Search Bar -->
      <div>
        <input v-model="searchQuery" placeholder="Search Brokers" />
      </div>

      <!-- Broker Table -->
      <table>
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

      <!-- Modal -->
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
import { mapGetters } from "vuex";
import axios from "axios";

export default {
  name: "DevFuncBroker",
  components: {
    SideNav,
    BModal,
  },
  data() {
    return {
      showModal: false,
      email: "",
      contactNumber: "",
      lastName: "",
      firstName: "",
      password: "",
      error: null,
      successMessage: null,
      brokers: [],
      searchQuery: "", // For searching brokers
    };
  },
  computed: {
    ...mapGetters(["getCompanyId", "getUserId"]),
    companyId() {
      return this.getCompanyId; // Automatically use the company ID from Vuex
    },
    userId() {
      return this.getUserId; // Automatically use the user ID from Vuex if needed
    },
    // Filter brokers based on the search query
    filteredBrokers() {
      return this.brokers.filter((broker) =>
        Object.values(broker).some((value) =>
          String(value).toLowerCase().includes(this.searchQuery.toLowerCase())
        )
      );
    },
  },
  mounted() {
    this.fetchBrokers();
  },
  methods: {
    async fetchBrokers() {
      if (!this.userId || !this.companyId) {
        alert("Developer or Company ID not found. Please log in.");
        return;
      }

      try {
        const response = await axios.get(
          "http://localhost:8000/developer/brokers/",
          {
            headers: {
              "Developer-ID": this.userId,
              "Company-ID": this.companyId,
            },
          }
        );

        if (response.status === 200) {
          this.brokers = response.data;
        } else {
          this.error = "Error fetching brokers.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching brokers.";
      }
    },
    async addBroker() {
      try {
        const response = await axios.post(
          "http://localhost:8000/developer/brokers/",
          {
            email: this.email,
            contact_number: this.contactNumber,
            last_name: this.lastName,
            first_name: this.firstName,
            password: this.password,
          },
          {
            headers: {
              "Developer-ID": this.userId,
              "Company-ID": this.companyId,
            },
          }
        );

        if (response.status === 201) {
          this.successMessage = "Broker created successfully!";
          this.error = null;
          this.resetForm();
          this.fetchBrokers(); // Refresh the broker list after creation
          this.showModal = false;
        } else {
          this.error = "Failed to create broker.";
        }
      } catch (error) {
        this.error = "An error occurred while creating the broker.";
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
