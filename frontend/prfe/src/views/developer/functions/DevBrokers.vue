<template>
  <div class="developer-brokers-page">
    <SideNav />
    <div class="content">
      <!-- Header Section -->
      <div class="header">
        <h1>Total Brokers: {{ filteredBrokers.length }}</h1>
        <button @click="showModal = true">Add Broker</button>
      </div>

      <!-- Search & Filter -->
      <div class="filter-section">
        <input
          v-model="searchQuery"
          placeholder="Search Brokers"
          class="search-bar"
        />
        <select v-model="brokersPerPage" class="page-limit-selector">
          <option v-for="limit in [5, 10, 15, 20]" :key="limit" :value="limit">
            Show {{ limit }} per page
          </option>
        </select>
      </div>

      <!-- Broker Table -->
      <table v-if="currentBrokers.length" class="table">
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
          <tr v-for="broker in currentBrokers" :key="broker.id">
            <td>{{ broker.email }}</td>
            <td>{{ broker.username }}</td>
            <td>{{ broker.first_name }}</td>
            <td>{{ broker.last_name }}</td>
            <td>{{ broker.contact_number }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No brokers found for this company.</p>

      <!-- Pagination -->
      <div class="pagination" v-if="filteredBrokers.length > brokersPerPage">
        <button
          v-for="page in totalPages"
          :key="page"
          @click="currentPage = page"
          :class="{ active: currentPage === page }"
        >
          {{ page }}
        </button>
      </div>

      <!-- Modal for Adding Broker -->
      <b-modal v-model="showModal" title="Add Broker" hide-footer>
        <form @submit.prevent="addBroker">
          <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" v-model="email" id="email" required />
          </div>

          <div class="form-group">
            <label for="contactNumber">Contact Number:</label>
            <input
              type="text"
              v-model="contactNumber"
              id="contactNumber"
              required
            />
          </div>

          <div class="form-group">
            <label for="lastName">Last Name:</label>
            <input type="text" v-model="lastName" id="lastName" required />
          </div>

          <div class="form-group">
            <label for="firstName">First Name:</label>
            <input type="text" v-model="firstName" id="firstName" required />
          </div>

          <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" v-model="password" id="password" required />
          </div>

          <button type="submit">Submit</button>
          <button type="button" @click="showModal = false">Cancel</button>
        </form>

        <p v-if="error" class="text-danger">{{ error }}</p>
        <p v-if="successMessage" class="text-success">{{ successMessage }}</p>
      </b-modal>
    </div>
  </div>
</template>

--- ### Script: ```javascript
<script>
import SideNav from "@/components/SideNav.vue";
import { BModal } from "bootstrap-vue-3";

export default {
  name: "DeveloperBrokers",
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
      brokers: [], // Replace this with actual data from the API later
      searchQuery: "",
      brokersPerPage: 15,
      currentPage: 1,
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
    totalPages() {
      return Math.ceil(this.filteredBrokers.length / this.brokersPerPage);
    },
    currentBrokers() {
      const start = (this.currentPage - 1) * this.brokersPerPage;
      const end = start + this.brokersPerPage;
      return this.filteredBrokers.slice(start, end);
    },
  },
  methods: {
    fetchMockBrokers() {
      // Mock brokers data for now
      this.brokers = [
        {
          id: 1,
          email: "broker1@example.com",
          username: "broker1",
          first_name: "John",
          last_name: "Doe",
          contact_number: "123456789",
        },
        // Add more brokers as needed
      ];
    },
    addBroker() {
      // For now, add a mock broker to the brokers list
      const newBroker = {
        id: Date.now(),
        email: this.email,
        username: this.email.split("@")[0],
        first_name: this.firstName,
        last_name: this.lastName,
        contact_number: this.contactNumber,
      };

      this.brokers.push(newBroker);
      this.resetForm();
      this.successMessage = "Broker added successfully!";
      this.showModal = false;
    },
    resetForm() {
      this.email = "";
      this.contactNumber = "";
      this.lastName = "";
      this.firstName = "";
      this.password = "";
    },
  },
  mounted() {
    this.fetchMockBrokers(); // Load mock data or replace with an API call later
  },
};
</script>

<style scoped>
.developer-brokers-page {
  display: flex;
}

.content {
  flex: 1;
  padding: 20px;
}

.filter-section {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
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
}

.pagination {
  display: flex;
  gap: 5px;
  margin-top: 20px;
}

.pagination .active {
  font-weight: bold;
}
</style>
