<template>
  <div class="container">
    <!-- Sidebar -->
    <div class="sidebar">
      <nav>
        <ul>
          <li :class="{ active: activeTab === 'document-status' }">
            <a href="#" @click.prevent="setActiveTab('document-status')">
              Document Status
            </a>
          </li>
          <li :class="{ active: activeTab === 'payment-schedule' }">
            <a href="#" @click.prevent="setActiveTab('payment-schedule')">
              Payment Schedule
            </a>
          </li>
        </ul>
      </nav>
    </div>

    <!-- Main Content -->
    <div class="content">
      <!-- Document Status Content -->
      <div v-if="activeTab === 'document-status'" class="tab-content">
        <div v-if="salesDetail" class="details-card">
          <h2>Sales Agreement Details</h2>
          <div class="details-group">
            <p><strong>Customer Name:</strong> {{ salesDetail.customer_name }}</p>
            <p><strong>Site Name:</strong> {{ salesDetail.site_name }}</p>
            <p><strong>Unit Name:</strong> {{ salesDetail.unit_name }}</p>
            <p><strong>Broker Name:</strong> {{ salesDetail.broker_name }}</p>
            <p><strong>Payment Plan:</strong> {{ salesDetail.payment_plan }}</p>
            <p><strong>Unit Price:</strong> ₱{{ salesDetail.unit_price }}</p>
          </div>
          <div class="details-group">
            <p>
              <strong>Spot Discount Percentage:</strong>
              {{ salesDetail.spot_discount_percent }}%
            </p>
            <p><strong>Spot Discount:</strong> ₱{{ spotDiscount }}</p>
            <p>
              <strong>Unit Price after Spot Discount:</strong> ₱{{
                unitPriceAfterSpotDiscount
              }}
            </p>
            <p>
              <strong>TLP Discount Percentage:</strong>
              {{ salesDetail.tlp_discount_percent }}%
            </p>
            <p><strong>TLP Discount:</strong> ₱{{ tlpDiscountAmount }}</p>
            <p><strong>Net Unit Price:</strong> ₱{{ netUnitPrice }}</p>
          </div>
          <div class="details-group">
            <p>
              <strong>Other Charges Percentage:</strong>
              {{ salesDetail.other_charges_percent }}%
            </p>
            <p><strong>Other Charges:</strong> ₱{{ otherCharges }}</p>
            <p v-if="netUnitPrice > 3600000">
              <strong>VAT (12%):</strong> ₱{{ vatAmount }}
            </p>
            <p><strong>Total Amount Payable:</strong> ₱{{ totalAmountPayable }}</p>
          </div>
          <div class="details-group">
            <p v-if="salesDetail.payment_plan === 'Deffered Payment'">
              <strong>Spot Downpayment Percentage:</strong>
              {{ salesDetail.spot_downpayment_percent }}%
            </p>
            <p v-if="salesDetail.payment_plan === 'Deffered Payment'">
              <strong>Spot Downpayment:</strong> ₱{{ spotDownpayment }}
            </p>
            <p><strong>Reservation Fee:</strong> ₱{{ salesDetail.reservation_fee }}</p>
            <p v-if="salesDetail.payment_plan === 'Spot Cash'">
              <strong>Net Full Payment:</strong> ₱{{ netFullPayment }}
            </p>
            <p v-if="salesDetail.payment_plan === 'Deffered Payment'">
              <strong>Net Downpayment:</strong> ₱{{ netDownpayment }}
            </p>
          </div>
          <div class="download-button" v-if="salesDetail.reservation_agreement_url">
            <a
              :href="`http://localhost:8000/download_reservation_agreement/${salesDetail.id}`"
              download
            >
              <button>Download Reservation Agreement</button>
            </a>
          </div>
        </div>
      </div>

      <!-- Payment Schedule Content -->
      <div v-if="activeTab === 'payment-schedule'" class="tab-content">
        <div v-if="salesDetail.payment_plan === 'Deffered Payment'">
          <div class="detailed-schedule">
            <h3>Payment Schedule</h3>
            <table>
              <thead>
                <tr>
                  <th>Payment Type</th>
                  <th>Amount (₱)</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Spot Downpayment</td>
                  <td>₱{{ spotDownpayment.toFixed(2) }}</td>
                </tr>
                <tr>
                  <td>Spread Downpayment</td>
                  <td>₱{{ spreadDownpayment.toFixed(2) }}</td>
                </tr>
                <tr v-for="month in salesDetail.payable_months" :key="month">
                  <td>Month {{ month }} Payment</td>
                  <td>₱{{ payablePerMonth.toFixed(2) }}</td>
                </tr>
                <tr>
                  <td>Balance Upon Turnover</td>
                  <td>₱{{ balanceUponTurnover.toFixed(2) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div>
          <h3>Required Documents</h3>
          <ul v-if="documentTypes.length" class="documents-list">
            <li v-for="doc in documentTypes" :key="doc.id">
              <strong>{{ doc.name }}</strong>
            </li>
          </ul>
          <p v-else>No document types available.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SalesDetails",
  data() {
    return {
      activeTab: "document-status", // Default active tab
      salesDetail: null, // Store the sales details
      spotDiscount: 0,
      unitPriceAfterSpotDiscount: 0,
      tlpDiscountAmount: 0,
      netUnitPrice: 0,
      otherCharges: 0,
      totalAmountPayable: 0,
      reservationFee: 0, // Fixed reservation fee as per your example
      netFullPayment: 0,
      spotDownpayment: 0,
      spreadDownpayment: 0,
      payablePerMonth: 0,
      balanceUponTurnover: 0,
      showDetailedSchedule: false, // To toggle the detailed schedule
      documentTypes: [], // Store the document types fetched from the API
    };
  },
  created() {
    const salesDetailUuid = this.$route.params.id; // Get the UUID from the URL
    this.fetchSalesDetail(salesDetailUuid);
    this.fetchDocumentTypes(); // Fetch the document types on component creation
  },
  methods: {
    setActiveTab(tab) {
      this.activeTab = tab;
    },
    async fetchSalesDetail(salesDetailUuid) {
      try {
        const response = await fetch(
          `http://localhost:8000/sales-detail/${salesDetailUuid}/`
        ); // Update the URL with UUID
        const data = await response.json();
        if (data.success === false) {
          alert("Sales details not found");
        } else {
          this.salesDetail = data; // Store the sales details in data
          this.applySpotCashDiscount(); // Call the function after the data is fetched
          this.applyTLPDiscount();
          this.updateNetUnitPrice();
          this.applyOtherCharges();
          this.calculateVAT();
          this.calculateFinancingDetails();
        }
      } catch (error) {
        console.error("Error fetching sales details:", error);
      }
    },

    // Method to apply spot discount
    applySpotCashDiscount() {
      const discountPercentage = parseFloat(
        this.salesDetail.spot_discount_percent
      );
      this.spotDiscount =
        (this.salesDetail.unit_price * discountPercentage) / 100;
      this.unitPriceAfterSpotDiscount =
        this.salesDetail.unit_price - this.spotDiscount;
      this.updateNetUnitPrice();
    },

    // Method to apply TLP discount
    applyTLPDiscount() {
      const discountPercentage = parseFloat(
        this.salesDetail.tlp_discount_percent
      );
      this.tlpDiscountAmount =
        (this.unitPriceAfterSpotDiscount * discountPercentage) / 100;
      this.updateNetUnitPrice();
    },

    // Update net unit price after discounts
    updateNetUnitPrice() {
      this.netUnitPrice =
        this.unitPriceAfterSpotDiscount - this.tlpDiscountAmount;
      this.applyOtherCharges();
    },

    // Apply other charges
    applyOtherCharges() {
      const otherChargesPercentage = parseFloat(
        this.salesDetail.other_charges_percent
      );
      this.otherCharges = (this.netUnitPrice * otherChargesPercentage) / 100;
      this.totalAmountPayable = this.netUnitPrice + this.otherCharges;
      this.netFullPayment = this.totalAmountPayable - this.reservationFee;
      this.calculateFinancingDetails();
    },

    // Calculate VAT if applicable
    calculateVAT() {
      if (this.netUnitPrice > 3600000) {
        this.vatAmount = this.netUnitPrice * 0.12;
        this.totalAmountPayable += this.vatAmount;
      }
    },

    // Calculate financing details like downpayment, payable per month, and balance upon turnover
    calculateFinancingDetails() {
      const spotDownpaymentPercentage = parseFloat(
        this.salesDetail.spot_downpayment_percent
      );
      const spreadDownpaymentPercentage = parseFloat(
        this.salesDetail.spread_downpayment_percent
      );
      this.spotDownpayment =
        this.totalAmountPayable * (spotDownpaymentPercentage / 100);
      this.spreadDownpayment =
        this.totalAmountPayable * (spreadDownpaymentPercentage / 100);
      this.reservationFee = this.salesDetail.reservation_fee;
      if (spotDownpaymentPercentage === 0) {
        this.netDownpayment = this.spreadDownpayment - this.reservationFee;
        this.payablePerMonth =
          this.netDownpayment / this.salesDetail.payable_months;
      } else {
        this.netDownpayment = this.spotDownpayment - this.reservationFee;
        this.payablePerMonth =
          this.spreadDownpayment / this.salesDetail.payable_months;
      }

      this.balanceUponTurnover =
        ((100 - (spotDownpaymentPercentage + spreadDownpaymentPercentage)) /
          100) *
        this.totalAmountPayable;
    },
    // Fetch Document Types
    async fetchDocumentTypes() {
      try {
        const response = await fetch("http://localhost:8000/document-types/");
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            this.documentTypes = data.documentTypes;
          } else {
            this.error = data.message || "Failed to fetch document types.";
          }
        }
      } catch (error) {
        this.error = "An error occurred while fetching document types.";
      }
    },

    // Toggle the visibility of the detailed schedule
    toggleDetailedSchedule() {
      this.showDetailedSchedule = !this.showDetailedSchedule;
    },
  },
};
</script>

<style scoped>
h2 {
  font-size: 24px;
  margin-bottom: 20px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  font-size: 16px;
  margin-bottom: 8px;
}
button.toggle-button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
}
button.toggle-button:hover {
  background-color: #45a049;
}
.detailed-schedule {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th,
td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}
th {
  background-color: #f2f2f2;
}.container {
  display: flex;
}

.sidebar {
  width: 200px;
  background-color: #f8f9fa;
  padding: 20px;
  position: fixed; /* Keeps sidebar fixed on the left */
  height: 100vh; /* Full screen height */
  top: 0;
  left: 0;
}

.sidebar nav ul {
  list-style: none;
  padding: 0;
}

.sidebar nav ul li {
  margin-bottom: 10px;
}

.sidebar nav ul li a {
  text-decoration: none;
  color: #333;
  display: block;
  padding: 10px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.sidebar nav ul li a:hover {
  background-color: #e9ecef;
}

.sidebar nav ul li.active a {
  background-color: #007bff;
  color: #fff;
}

.content {
  margin-left: 220px; /* Add space for sidebar */
  padding: 20px;
  width: calc(100% - 220px); /* Ensure content takes up remaining space */
}

.tab-content {
  margin-bottom: 20px;
}

.details-group {
  margin-bottom: 15px;
}

/* Style for the content elements */
h2, h3 {
  margin-bottom: 20px;
}
</style>
