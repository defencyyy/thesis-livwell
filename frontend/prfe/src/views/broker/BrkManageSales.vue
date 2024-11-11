<template>
  <div class="manage-sales-page">
    <SideNav />
    <div class="content">
        <h1>Welcome to the Manage Sales Page</h1>
        <p>This is where you can manage sales data for brokers and developers.</p>

        <!-- Add Sale Button -->
        <button @click="openModal">Add Sale</button>

        <!-- Modal -->
        <div v-if="modalOpen" class="modal">
          <div class="modal-content">
            <h2>Add Sale</h2>

            <!-- Form to collect sales data -->
            <form @submit.prevent="submitSale">
              <!-- Customer Dropdown -->
              <label for="customer">Customer:</label>
              <select v-model="selectedCustomer" id="customer" required>
                <option value="" disabled>Select a customer</option>
                <option v-for="customer in customers" :key="customer.id" :value="customer.id">
                  {{ customer.customer_name }}
                </option>
              </select>

              <!-- Unit Dropdown -->
              <label for="unit">Unit:</label>
              

              <!-- Submit Button -->
              <button type="submit">Submit</button>
            </form>

            <button @click="closeModal">Close</button>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import axios from "axios"; 

export default {
  name: "ManageSales",
  components: {
    SideNav,
  },
  data() {
    return {
      modalOpen: false,  // To toggle modal visibility
      customers: [],     // List of customers for the dropdown
      units: [],         // List of available units for the dropdown
      selectedCustomer: "", // Selected customer ID

    };
  },
  methods: {
    openModal() {
      this.modalOpen = true;
      this.fetchCustomers(); 
    },
    closeModal() {
      this.modalOpen = false;
    },
    async fetchCustomers() {
      const brokerId = localStorage.getItem("broker_id");
      try {
        const response = await fetch(`http://localhost:8000/customers/broker/${brokerId}/`);
        if (response.ok) {
          const data = await response.json();
          this.customers = data.customers;
        } else {
          const errorData = await response.json();
          this.error = errorData.message || "Failed to fetch customer data.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching customer data.";
      }
    },

   

    async submitSale() {
      const saleData = {
        broker_id: this.$store.state.brokerId,  // Assuming broker ID is stored in Vuex
        customer_id: this.selectedCustomer,
        unit_id: this.selectedUnit,
        date_sold: new Date().toISOString(), // You can adjust this based on the actual format
        status: 'pending', // Set the initial status as 'pending'
      };

      try {
        const response = await axios.post("/sales/add", saleData); // Send data to the backend
        if (response.data.success) {
          alert("Sale added successfully!");
          this.closeModal(); // Close the modal after successful submission
        } else {
          alert("Error adding sale.");
        }
      } catch (error) {
        console.error("Error submitting sale:", error);
      }
    }
  }
};
</script>

<style scoped>
.manage-sales-page {
  display: flex;
  height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}

/* Modal styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  width: 300px;
}
</style>
