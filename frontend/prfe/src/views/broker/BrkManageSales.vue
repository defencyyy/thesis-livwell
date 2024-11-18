<template>
  <div class="manage-sales-page">
    <SideNav />
    <div class="content">
      <h1>Welcome to the Manage Sales Page</h1>
      <p>This is where you can manage sales data for brokers and developers.</p>

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
          <tr
            v-for="sale in sales"
            :key="sale.id"
            @click="openSalesAgreementModal(sale)"
            style="cursor: pointer;"
          >
            <td>{{ sale.customer_name }}</td>
            <td>{{ sale.site_name }}</td>
            <td>{{ sale.unit_title }}</td>
            <td>{{ sale.status }}</td>
          </tr>
        </tbody>
      </table>

      <!-- No customers found message -->
      <p v-if="!sales.length">No sales found.</p>

      <!-- Sales Agreement Modal -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <h2>Sales Agreement</h2>
          <p><strong>Customer:</strong> {{ selectedSale.customer_name }}</p>
          <p><strong>Unit:</strong> {{ selectedSale.unit_title }}</p>
          <p><strong>Site:</strong> {{ selectedSale.site_name }}</p>

          <form @submit.prevent="submitSalesAgreement">
            <div>
              <label for="payment-plan">Payment Plan</label>
              <select id="payment-plan" v-model="salesAgreement.payment_plan" required>
                <option value="spot_cash">Spot Cash</option>
                <option value="bank_financing">Bank Financing</option>
                <option value="in_house_financing">In-House Financing</option>
              </select>
            </div>

            <div>
              <label for="down-payment">Down Payment Amount</label>
              <input
                type="number"
                id="down-payment"
                v-model="salesAgreement.down_payment"
                placeholder="Enter amount"
                required
              />
            </div>

            <div>
              <label for="installment-term">Installment Term (months)</label>
              <input
                type="number"
                id="installment-term"
                v-model="salesAgreement.installment_term"
                placeholder="Enter term"
                required
              />
            </div>

            <div>
              <label for="special-terms">Special Terms</label>
              <textarea
                id="special-terms"
                v-model="salesAgreement.special_terms"
                placeholder="Any special conditions or terms?"
              ></textarea>
            </div>

            <button type="submit">Save Sales Agreement</button>
            <button type="button" @click="closeModal">Cancel</button>
          </form>
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
      sales: [], // List of sales data
      showModal: false,
      selectedSale: null, // Currently selected sale row
      salesAgreement: {
        payment_plan: "",
        down_payment: "",
        installment_term: "",
        special_terms: "",
      },
    };
  },
  methods: {
    // Fetch sales data from the backend
    async fetchSales() {
      try {
        const response = await fetch("http://localhost:8000/sales/");
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            this.sales = data.sales; // This should now have customer name, site name, and unit title
          } else {
            console.error(data.message || "Failed to fetch sales data.");
          }
        } else {
          console.error("Failed to fetch sales data.");
        }
      } catch (error) {
        console.error("An error occurred while fetching sales data.");
      }
    },

    // Open the sales agreement modal
    openSalesAgreementModal(sale) {
      this.selectedSale = sale;
      this.showModal = true;
    },

    // Close the modal
    closeModal() {
      this.showModal = false;
      this.salesAgreement = {
        payment_plan: "",
        down_payment: "",
        installment_term: "",
        special_terms: "",
      };
    },

    // Submit the sales agreement
    submitSalesAgreement() {
      // Placeholder for handling form submission
      console.log("Sales Agreement Data:", this.salesAgreement);
      this.closeModal();
    },
  },
  mounted() {
    this.fetchSales(); // Fetch sales data when the page loads
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
