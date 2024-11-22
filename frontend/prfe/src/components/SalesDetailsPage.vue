<template>
  <div v-if="salesDetail">
    <h2>Sales Agreement Details</h2>

    <p><strong>Customer ID:</strong> {{ salesDetail.customer_name }}</p>
    <p><strong>Site ID:</strong> {{ salesDetail.site_name }}</p>
    <p><strong>Unit ID:</strong> {{ salesDetail.unit_name }}</p>
    <p><strong>Broker ID:</strong> {{ salesDetail.broker_name }}</p>
    <p><strong>Payment Plan:</strong> {{ salesDetail.payment_plan }}</p>
    <p><strong>Unit Price:</strong> ₱{{ salesDetail.unit_price }}</p>
    <p><strong>Spot Discount Percentage:</strong> {{ salesDetail.spot_discount_percent }}%</p>
    <p><strong>Spot Discount:</strong> ₱{{ spotDiscount }}</p>
    <p><strong>Unit Price after Spot Discount:</strong> ₱{{ unitPriceAfterSpotDiscount }}</p>
    <p><strong>TLP Discount Percentage:</strong> {{ salesDetail.tlp_discount_percent }}%</p>
    <p><strong>TLP Discount:</strong> ₱{{ tlpDiscountAmount }}</p>
    <p><strong>Net Unit Price:</strong> ₱{{ netUnitPrice }}</p>
    <p><strong>Other Charges Percentage:</strong> {{ salesDetail.other_charges_percent }}%</p>
    <p><strong>Other Charges:</strong> ₱{{ otherCharges }}</p>
    <p v-if="netUnitPrice > 3600000"><strong>VAT (12%):</strong> ₱{{ vatAmount }}</p>
    <p ><strong>Total Amount Payable:</strong> ₱{{ totalAmountPayable }}</p>
    <p v-if="salesDetail.payment_plan === 'Deffered Payment'"><strong>Spot Downpayment Percentage:</strong> {{ salesDetail.spot_downpayment_percent }}%</p>
    <p v-if="salesDetail.payment_plan === 'Deffered Payment'"><strong>Spot Downpayment:</strong> ₱{{ spotDownpayment }}</p>
    <p><strong>Reservation Fee:</strong> ₱{{ salesDetail.reservation_fee }}</p>
    <p v-if="salesDetail.payment_plan === 'Spot Cash'"><strong>Net Full Payment:</strong> ₱{{ netFullPayment }}</p>
    <p v-if="salesDetail.payment_plan === 'Deffered Payment'"><strong>Net Downpayment:</strong> ₱{{ netDownpayment }}</p>
    <p v-if="salesDetail.payment_plan === 'Deffered Payment'"><strong>Spread Downpayment Percentage:</strong> {{ salesDetail.spread_downpayment_percent }}%</p>
    <p v-if="salesDetail.payment_plan === 'Deffered Payment'"><strong>Spread Downpayment:</strong> ₱{{ spreadDownpayment }}</p>
    <p v-if="salesDetail.payment_plan === 'Deffered Payment'"><strong>Payable Months:</strong> {{ salesDetail.payable_months }}</p>
    <p v-if="salesDetail.payment_plan === 'Deffered Payment'"><strong>Payable Per Month:</strong> ₱{{ payablePerMonth }}</p>
    <p v-if="salesDetail.payment_plan === 'Deffered Payment'"><strong>Balance Upon Turnover:</strong> ₱{{ balanceUponTurnover }}</p>

    <!-- Collapsible Table Section - Only for Deferred Payment -->
    <div v-if="salesDetail.payment_plan === 'Deffered Payment'">
      <button @click="toggleDetailedSchedule" class="toggle-button">
        {{ showDetailedSchedule ? 'Hide Detailed Schedule' : 'Show Detailed Schedule' }}
      </button>

      <!-- Detailed Monthly Schedule (Visible when expanded) -->
      <div v-if="showDetailedSchedule" class="detailed-schedule">
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
            <!-- Loop through the months to display monthly payments -->
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

  </div>
</template>

<script>
export default {
  name: "SalesDetails",
  data() {
    return {
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
    };
  },
  created() {
    const salesDetailId = this.$route.params.id; // Get the ID from the URL
    this.fetchSalesDetail(salesDetailId);
  },
  methods: {
    async fetchSalesDetail(salesDetailId) {
      try {
        const response = await fetch(`http://localhost:8000/sales-detail/${salesDetailId}/`);
        const data = await response.json();
        if (data.success === false) {
          alert('Sales details not found');
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
        console.error('Error fetching sales details:', error);
      }
    },

    // Method to apply spot discount
    applySpotCashDiscount() {
      const discountPercentage = parseFloat(this.salesDetail.spot_discount_percent);
      this.spotDiscount = (this.salesDetail.unit_price * discountPercentage) / 100;
      this.unitPriceAfterSpotDiscount = this.salesDetail.unit_price - this.spotDiscount;
      this.updateNetUnitPrice();
    },

    // Method to apply TLP discount
    applyTLPDiscount() {
      const discountPercentage = parseFloat(this.salesDetail.tlp_discount_percent);
      this.tlpDiscountAmount = (this.unitPriceAfterSpotDiscount * discountPercentage) / 100;
      this.updateNetUnitPrice();
    },

    // Update net unit price after discounts
    updateNetUnitPrice() {
      this.netUnitPrice = this.unitPriceAfterSpotDiscount - this.tlpDiscountAmount;
      this.applyOtherCharges();
    },

    // Apply other charges
    applyOtherCharges() {
      const otherChargesPercentage = parseFloat(this.salesDetail.other_charges_percent);
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
      const spotDownpaymentPercentage = parseFloat(this.salesDetail.spot_downpayment_percent);
      const spreadDownpaymentPercentage = parseFloat(this.salesDetail.spread_downpayment_percent);
      this.spotDownpayment = this.totalAmountPayable * (spotDownpaymentPercentage / 100);
      this.spreadDownpayment = this.totalAmountPayable * (spreadDownpaymentPercentage / 100);
      this.reservationFee = this.salesDetail.reservation_fee;
      if (spotDownpaymentPercentage === 0) {
        this.netDownpayment = this.spreadDownpayment - this.reservationFee;
        this.payablePerMonth = this.netDownpayment / this.salesDetail.payable_months;
      } else {
        this.netDownpayment = this.spotDownpayment - this.reservationFee;
        this.payablePerMonth = this.spreadDownpayment / this.salesDetail.payable_months;
      }

      this.balanceUponTurnover = (100 - (spotDownpaymentPercentage + spreadDownpaymentPercentage)) / 100 * this.totalAmountPayable;
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
  background-color: #4CAF50;
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
th, td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}
th {
  background-color: #f2f2f2;
}
</style>
