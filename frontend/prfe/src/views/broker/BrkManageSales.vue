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
                {{ customer.name }}
              </option>
            </select>

            <!-- Site Dropdown -->
            <label for="site">Site:</label>
            <select v-model="selectedSite" id="site" required @change="fetchUnits">
              <option value="" disabled>Select a site</option>
              <option v-for="site in sites" :key="site.id" :value="site.id">
                {{ site.name }}
              </option>
            </select>

            <!-- Unit Dropdown -->
            <label for="unit">Unit:</label>
            <select v-model="selectedUnit" id="unit" required>
              <option value="" disabled>Select a unit</option>
              <option v-for="unit in availableUnits" :key="unit.id" :value="unit.id">
                {{ unit.unit_title }}
              </option>
            </select>

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

export default {
  name: "ManageSales",
  components: {
    SideNav,
  },
  data() {
    return {
      modalOpen: false,  // To toggle modal visibility
      sites: [],         // List of available sites
      availableUnits: [], // List of units available for the selected site
      customers: [],      // List of customers for the broker
      selectedSite: "",    // Selected site ID
      selectedUnit: "",    // Selected unit ID
      selectedCustomer: "", // Selected customer ID
      brokerId: "",       // Broker ID (will be retrieved from local storage)
      companyId: "",      // Company ID fetched from broker data
      error: null,        // Error message placeholder
    };
  },
  methods: {
    openModal() {
      this.modalOpen = true;
      this.fetchData(); // Fetch all necessary data when opening the modal
    },
    closeModal() {
      this.modalOpen = false;
    },

    // Fetch all data needed for the modal
    async fetchData() {
      await Promise.all([this.fetchSites(), this.getBrokerData(), this.fetchCustomers()]);
    },

    // Fetch sites that have available units
    async fetchSites() {
      try {
        const response = await fetch(`http://localhost:8000/sites/`);
        if (response.ok) {
          const data = await response.json();
          // Filter out sites that have no available units
          this.sites = data.sites.filter(site => site.units.length > 0);
        } else {
          this.error = "Failed to fetch sites.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching sites.";
      }
    },

    // Fetch available units for the selected site
    async fetchUnits() {
      if (!this.selectedSite) return;
      
      try {
        const response = await fetch(`http://localhost:8000/units/site/${this.selectedSite}`);
        if (response.ok) {
          const data = await response.json();
          this.availableUnits = data.units;
        } else {
          this.error = "Failed to fetch units.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching units.";
      }
    },

    // Fetch broker data, including company_id
    async getBrokerData() {
      this.brokerId = localStorage.getItem("broker_id");
      try {
        const response = await fetch(`http://localhost:8000/brokers/${this.brokerId}/`);
        if (response.ok) {
          const brokerData = await response.json();
          this.companyId = brokerData.company_id;
        } else {
          this.error = "Failed to fetch broker data.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching broker data.";
      }
    },

    // Fetch customers for the logged-in broker
    async fetchCustomers() {
      try {
        const response = await fetch(`http://localhost:8000/customers/broker/${this.brokerId}`);
        if (response.ok) {
          const data = await response.json();
          this.customers = data.customers;
        } else {
          this.error = "Failed to fetch customers.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching customers.";
      }
    },

    // Submit sale to the backend
    async submitSale() {
      const saleData = {
        site: this.selectedSite,
        unit: this.selectedUnit,
        customer: this.selectedCustomer,
        broker: this.brokerId,
        company: this.companyId,  // Ensure this is passed correctly
      };

      try {
        const response = await fetch(`http://localhost:8000/sales/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(saleData),
        });

        if (response.ok) {
          const data = await response.json();
          alert(data.message);  // Show success message
          this.closeModal();  // Close modal after successful submission
        } else {
          const errorData = await response.json();
          alert(errorData.message || "Error occurred during sale submission.");
        }
      } catch (error) {
        alert("An error occurred while submitting the sale.");
      }
    },
  },
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
  border-radius: 8px;
  width: 400px;
  text-align: left;
}
</style>
