<template>
  <header>
    <HeaderLivwell />
  </header>
  <div class="manage-sales-page">
    <SideNav />
    <div class="content">
      <h1>Welcome to the Manage Sales Page</h1>
      <p>This is where you can manage sales data for brokers and developers.</p>

      <!-- Add Sale Button -->
      <button @click="openModal">Add Sale</button>

      <div v-if="loading" class="loading-spinner">Loading...</div>

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
            <select
              v-model="selectedCustomer"
              id="customer"
              required
              v-if="customers.length > 0"
            >
              <option value="" disabled>Select a customer</option>
              <option
                v-for="customer in customers"
                :key="customer.id"
                :value="customer.id"
              >
                {{ customer.name }}
              </option>
            </select>
            <!-- Fallback message if no customers -->
            <p v-else>No customers available</p>

            <!-- Site Dropdown -->
            <label for="site">Site:</label>
            <select
              v-model="selectedSite"
              id="site"
              required
              @change="fetchUnits"
            >
              <option value="" disabled>Select a site</option>
              <option v-for="site in sites" :key="site.id" :value="site.id">
                {{ site.name }}
              </option>
            </select>

            <!-- Unit Dropdown -->
            <label for="unit">Unit:</label>
            <select v-model="selectedUnit" id="unit" required>
              <option value="" disabled>Select a unit</option>
              <option
                v-for="unit in availableUnits"
                :key="unit.id"
                :value="unit.id"
              >
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
import { mapGetters, mapActions } from "vuex";

export default {
  name: "ManageSales",
  components: {
    SideNav,
    HeaderLivwell,
  },
  data() {
    return {
      modalOpen: false,
      sites: [],
      availableUnits: [],
      customers: [],
      selectedSite: "",
      selectedUnit: "",
      selectedCustomer: "",
      companyId: "",
      error: null,
      sales: [],
      loading: false,
    };
  },
  computed: {
    ...mapGetters(["getUserId"]), // Use Vuex getter to access userId (broker ID)
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    ...mapActions(["fetchUserId"]), // Map Vuex actions (if necessary)

    openModal() {
      this.modalOpen = true;
    },
    closeModal() {
      this.modalOpen = false;
    },

    async fetchSales() {
      try {
        const response = await fetch("http://localhost:8000/sales/");
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            this.sales = data.sales;
          } else {
            this.error = data.message || "Failed to fetch sales data.";
          }
        } else {
          this.error = "Failed to fetch sales data.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching sales data.";
      } finally {
        this.loading = false;
      }
    },

    async fetchData() {
      await Promise.all([this.fetchSites(), this.getBrokerData()]);
      this.fetchSales();
    },

    async fetchSites() {
      try {
        const response = await fetch(`http://localhost:8000/sites/`);
        if (response.ok) {
          const data = await response.json();
          this.sites = data.sites.filter((site) => site.units.length > 0);
        } else {
          this.error = "Failed to fetch sites.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching sites.";
      }
    },

    async fetchUnits() {
      if (!this.selectedSite) return;

      try {
        const response = await fetch(
          `http://localhost:8000/units/site/${this.selectedSite}`
        );
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

    async getBrokerData() {
      const brokerId = this.getUserId; // Fetch brokerId from Vuex

      try {
        const response = await fetch(
          `http://localhost:8000/brokers/${brokerId}/`
        );
        if (response.ok) {
          const brokerData = await response.json();
          this.companyId = brokerData.company_id;
          this.fetchCustomers();
        } else {
          this.error = "Failed to fetch broker data.";
        }
      } catch (error) {
        this.error = "An error occurred while fetching broker data.";
      }
    },

    async fetchCustomers() {
      const brokerId = this.getUserId;
      const authToken = this.$store.getters.getAuthToken;

      if (!brokerId) {
        this.error = "Broker ID not found. Please log in again.";
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:8000/customers/broker/${brokerId}/?include_sales=true`,
          {
            headers: {
              Authorization: `Bearer ${authToken}`,
            },
          }
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

    async submitSale() {
      const saleData = {
        site: this.selectedSite,
        unit: this.selectedUnit,
        customer: this.selectedCustomer,
        broker: this.getUserId, // Using Vuex's brokerId
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
          alert(data.message);
          this.closeModal();
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
