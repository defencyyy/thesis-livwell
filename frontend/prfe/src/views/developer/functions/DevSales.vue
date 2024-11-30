<template>
  <div class="sales-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="sales-table-container">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Unit</th>
                <th>Customer</th>
                <th>Status</th>
                <th>Date Sold</th>
                <th>Reservation Fee</th>
                <th>Payment Method</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="sale in sales"
                :key="sale.id"
                @click="viewSaleDetails(sale.id)"
              >
                <td>{{ sale.id }}</td>
                <td>{{ sale.unit.unit_title }}</td>
                <td>
                  {{ sale.customer.first_name }} {{ sale.customer.last_name }}
                </td>
                <td>{{ sale.status }}</td>
                <td>{{ sale.date_sold }}</td>
                <td>{{ sale.reservation_fee }}</td>
                <td>{{ sale.payment_method }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Sale Details Modal (show on click) -->
        <div v-if="selectedSale" class="modal">
          <div class="modal-content">
            <h4>Sale Details</h4>
            <p><strong>ID:</strong> {{ selectedSale.id }}</p>
            <p><strong>Unit:</strong> {{ selectedSale.unit.unit_title }}</p>
            <p>
              <strong>Customer:</strong> {{ selectedSale.customer.first_name }}
              {{ selectedSale.customer.last_name }}
            </p>
            <p><strong>Status:</strong> {{ selectedSale.status }}</p>
            <p>
              <strong>Reservation Fee:</strong>
              {{ selectedSale.reservation_fee }}
            </p>
            <p>
              <strong>Payment Method:</strong> {{ selectedSale.payment_method }}
            </p>
            <p>
              <strong>Reservation File:</strong>
              <a :href="selectedSale.reservation_file" target="_blank">View</a>
            </p>
            <button @click="closeSaleDetails">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SideNav from "./SideNav.vue";
import AppHeader from "./AppHeader.vue";

export default {
  components: {
    SideNav,
    AppHeader,
  },
  data() {
    return {
      sales: [], // To hold the list of sales
      selectedSale: null, // To hold the selected sale details
    };
  },
  mounted() {
    this.fetchSales();
  },
  methods: {
    async fetchSales() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/sales/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.sales = response.data.data;
      } catch (error) {
        console.error("Error fetching sales:", error);
      }
    },
    async viewSaleDetails(saleId) {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/sales/${saleId}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.selectedSale = response.data.data;
      } catch (error) {
        console.error("Error fetching sale details:", error);
      }
    },
    closeSaleDetails() {
      this.selectedSale = null;
    },
  },
};
</script>

<style scoped>
.sales-table-container {
  margin-top: 20px;
}

.sales-table-container table {
  width: 100%;
  margin-bottom: 20px;
}

.sales-table-container th,
.sales-table-container td {
  padding: 10px;
  text-align: left;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 60%;
}

button {
  margin-top: 10px;
}
</style>
