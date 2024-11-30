<template>
  <div class="developer-sales-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <h1>Manage Sales</h1>
        <p>View and manage sales details for your company.</p>

        <!-- Sales Table -->
        <table v-if="sales.length > 0" class="sales-table">
          <thead>
            <tr>
              <th>Customer Name</th>
              <th>Unit Title</th>
              <th>Site Name</th>
              <th>Status</th>
              <th>Reservation Fee</th>
              <th>Payment Method</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="sale in sales"
              :key="sale.id"
              @click="openSalesDetailModal(sale)"
              style="cursor: pointer"
            >
              <td>
                {{ sale.customer.first_name }} {{ sale.customer.last_name }}({{
                  sale.customer.code
                }})
              </td>
              <td>{{ sale.unit.unit_title }}</td>
              <td>{{ sale.site.name || "N/A" }}</td>
              <td>{{ sale.status }}</td>
              <td>{{ formatCurrency(sale.reservation_fee) }}</td>
              <!-- Updated this line -->
              <td>{{ sale.payment_method }}</td>
              <td>
                <button
                  @click="updateSaleStatus(sale.id)"
                  class="btn btn-primary"
                >
                  Change Status
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- No sales found message -->
        <p v-if="!sales.length">No sales found.</p>

        <!-- Sales Detail Modal -->
        <div v-if="showModal" class="modal">
          <div class="modal-content">
            <h2>Sales Agreement</h2>
            <p>
              <strong>Customer:</strong> {{ selectedSale.customer.first_name }}
              {{ selectedSale.customer.last_name }}
            </p>
            <p><strong>Unit:</strong> {{ selectedSale.unit.unit_title }}</p>
            <p><strong>Site:</strong> {{ selectedSale.site.name || "N/A" }}</p>
            <p><strong>Status:</strong> {{ selectedSale.status }}</p>
            <p>
              <strong>Reservation Fee:</strong>
              {{ formatCurrency(selectedSale.reservation_fee) }}
              <!-- Updated this line -->
            </p>
            <p>
              <strong>Payment Method:</strong> {{ selectedSale.payment_method }}
            </p>

            <div v-if="selectedSale.reservation_file">
              <p>
                <strong>Reservation File:</strong>
                <a
                  :href="getFileUrl(selectedSale.reservation_file)"
                  target="_blank"
                  >View File</a
                >
              </p>
            </div>

            <div>
              <button @click="closeModal" class="btn btn-secondary">
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";
import { mapState } from "vuex";

export default {
  name: "DevSales",
  components: { SideNav, AppHeader },
  data() {
    return {
      sales: [], // List of sales data
      showModal: false,
      selectedSale: null, // Currently selected sale
      errorMessage: "", // Error message for API requests
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId,
      companyId: (state) => state.companyId,
      loggedIn: (state) => state.loggedIn,
    }),
  },
  mounted() {
    if (!this.loggedIn || !this.companyId) {
      this.redirectToLogin();
    } else {
      this.fetchSales(); // Fetch sales data on page load
    }
  },
  methods: {
    async fetchSales() {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/sales/?company_id=${this.companyId}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.sales = response.data.sales || []; // Ensure the sales data is an array
      } catch (error) {
        console.error("Error fetching sales data:", error);
        this.errorMessage = "Failed to load sales data.";
      }
    },
    async updateSaleStatus(saleId) {
      try {
        const response = await axios.put(
          `http://localhost:8000/developer/sales/${saleId}/update-status/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          alert("Sale status updated successfully!");
          this.fetchSales(); // Refresh the sales data
        } else {
          alert("Error updating sale status.");
        }
      } catch (error) {
        console.error("Error updating sale status:", error);
        alert("Failed to update sale status.");
      }
    },
    openSalesDetailModal(sale) {
      this.selectedSale = sale;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedSale = null;
    },
    getFileUrl(filePath) {
      return `http://localhost:8000${filePath}`;
    },
    redirectToLogin() {
      this.$router.push({ name: "DevLogin" });
    },
    // Method to format currency (replace the filter)
    formatCurrency(amount) {
      return new Intl.NumberFormat().format(amount);
    },
  },
};
</script>

<style scoped>
.main-content {
  display: flex;
  flex-direction: column;
  margin-top: 80px; /* Ensure there's enough space for the header */
  margin-left: 250px; /* Offset for sidebar */
  flex: 1;
  padding: 20px; /* Add some padding around the content */
}

.sales-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.sales-table th,
.sales-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.sales-table th {
  background-color: #f8f9fa;
  font-weight: bold;
}

.sales-table td {
  background-color: #ffffff;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.modal-content {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-content h2 {
  margin-bottom: 20px;
}

.modal-content p {
  margin-bottom: 10px;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
