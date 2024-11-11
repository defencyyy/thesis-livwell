<template>
  <header>
    <HeaderLivwell/>
  </header>
  <div class="manage-sales-page">
    <SideNav />
    <div class="content">
      <h1>Welcome to the Manage Sales Page</h1>
      <p>This is where you can manage sales data for brokers and developers.</p>

      <!-- Add Sale Button -->
      <button @click="openModal">Add Sale</button>

      <!-- Sales Table -->
      <table v-if="sales.length > 0" class="sales-table">
        <thead>
          <tr>
            <th>Customer Name</th>
            <th>Site Name</th>
            <th>Unit Title</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sale in sales" :key="sale.id">
            <td>{{ sale.customer_name }}</td>
            <td>{{ sale.site_name }}</td>
            <td>{{ sale.unit_title }}</td>
            <td>{{ sale.status }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Modal -->
      <div v-if="modalOpen" class="modal">
        <div class="modal-content">
          <h2>Add Sale</h2>

          <!-- Form to collect sales data -->
          <form @submit.prevent="submitSale">
           <!-- Customer Dropdown -->
          <label for="customer">Customer:</label>
          <select v-model="selectedCustomer" id="customer" required v-if="customers.length > 0">
            <option value="" disabled>Select a customer</option>
            <option v-for="customer in customers" :key="customer.id" :value="customer.id">
              {{ customer.name }}
            </option>
          </select>
          <!-- Fallback message if no customers -->
          <p v-else>No customers available</p>

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
import HeaderLivwell from "@/components/HeaderLivwell.vue";
import SideNav from "@/components/SideNav.vue";

export default {
  name: "ManageSales",
  components: {
    SideNav,
    name: "ManageSales",
    components: {
    SideNav, HeaderLivwell
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
      sales: [],          // List of sales data
    };
  },
  mounted() {
    // Call fetchSales immediately after the component is mounted
    this.fetchData(); // Fetch all necessary data when the page loads
  },
  methods: {
    openModal() {
      this.modalOpen = true;
    },
    closeModal() {
      this.modalOpen = false;
    },

    // Fetch sales data from the backend
    async fetchSales() {
      try {
        const response = await fetch("http://localhost:8000/sales/");
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            this.sales = data.sales;  // This should now have customer name, site name, and unit title
          } else {
            this.error = data.message || "Failed to fetch sales data.";
          }
        } else {
          this.error = "Failed to fetch sales data.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching sales data.";
      }
    },

    // Fetch all data needed for the modal (sites, broker data, etc.)
    async fetchData() {
      await Promise.all([this.fetchSites(), this.getBrokerData()]);
      this.fetchSales();  // Fetch sales data after loading sites and broker data
    },

    // Fetch sites that have available units
    async fetchSites() {
      try {
        const response = await fetch(`http://localhost:8000/sites/`);
        if (response.ok) {
          const data = await response.json();
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
          this.fetchCustomers();  // Fetch customers after getting broker data
        } else {
          this.error = "Failed to fetch broker data.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching broker data.";
      }
    },

    // Fetch customers for the logged-in broker
    async fetchCustomers() {
  const brokerId = localStorage.getItem("broker_id");
  
  if (!brokerId) {
    this.error = "Broker ID not found. Please log in again.";
    return;
  }

  try {
    const response = await fetch(`http://localhost:8000/customers/broker/${brokerId}/?include_sales=false`);
    if (response.ok) {
      const data = await response.json();
      if (data.success) {
        this.customers = data.customers; // This will exclude sales data
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

    // Submit sale to the backend
    async submitSale() {
      const saleData = {
        site: this.selectedSite,
        unit: this.selectedUnit,
        customer: this.selectedCustomer,
        broker: this.brokerId,
        company: this.companyId,
      };

      try {
        const response = await fetch("http://localhost:8000/sales/create/", {
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
}
}
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
.sales-table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

.sales-table th,
.sales-table td {
  padding: 8px;
  border: 1px solid #ccc;
}

.sales-table th {
  background-color: #f4f4f4;
}
</style>