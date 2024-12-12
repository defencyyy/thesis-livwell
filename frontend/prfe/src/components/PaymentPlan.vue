<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <router-link class="text-start text" to="/broker/affiliated-units">
          <div class = "back-container">
            <i class="fas fa-arrow-left"></i> Back to Units
          </div>
        </router-link>

        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title"><strong>Payment Plan for Unit {{ unitDetails ? unitDetails.unit_title : unitId }}</strong></div>
          </div>
        </div>

        <div class="payment-plan-container">
          <div class="row mb-3 ps-5">
            <div class="col-12 d-flex justify-content-around align-items-center">
              <!-- Left Section: Property Price -->
              <div class="text-center">
                <h5 class="price-header">Property Price</h5>
                <p class="property-price"><strong>₱ {{ selectedUnit.price }}</strong></p>
              </div>
              <!-- Right Section: Payment Plan -->
              <div class="text-center">
                <h5 class="price-header">Payment Plan</h5>
                <select v-model="selectedPaymentPlan" id="paymentPlan" class="form-select mt-2" required>
                  <option value="Spot Cash">Spot Cash</option>
                  <option value="Deferred Payment">Deferred Payment</option>
                </select>
              </div>
            </div>
          </div>

          <div class="card shadow-lg border-0 rounded-1 mx-auto" style="max-width: 900px;">
            <div class="card-body">
              <form>
                <div class="row">
                  <div class="col-md-6">
                    <!-- Spot Discount -->
                    <div class="mb-3">
                      <label for="spotDiscount" class="form-label text-start">Spot Discount</label>
                      <input
                        type="number"
                        id="spotDiscount"
                        v-model="spotCashDiscount"
                        @input="updatePaymentDetails"
                        class="form-control"
                        :min="0"
                        :max="maxSpotCashDiscount"
                      />
                      <p><strong>Spot Discount:</strong> ₱{{ spotDiscount }}</p>
                      <p><strong>Unit Price after Spot Discount:</strong> ₱{{ unitPriceAfterSpotDiscount }}</p>
                    </div>

                    <!-- Other Charges -->
                    <div class="mb-3">
                      <label for="otherChargesPercentage" class="form-label text-start">Other Charges (%)</label>
                      <input
                        type="number"
                        id="otherChargesPercentage"
                        v-model="otherChargesPercentage"
                        @input="updatePaymentDetails"
                        class="form-control"
                        min="0"
                        max="maxOtherChargesPercentage"
                        step="0.1"
                      />
                      <p><strong>Other Charges:</strong> ₱{{ otherCharges }}</p>
                      <p v-if="netUnitPrice > 3600000"><strong>VAT (12%):</strong> ₱{{ vatAmount }}</p>
                      <p><strong>Total Amount Payable:</strong> ₱{{ totalAmountPayable }}</p>
                    </div>

                    <!-- Spread Downpayment -->
                    <div v-if="selectedPaymentPlan === 'Deferred Payment'">
                      <div class="mb-3 align-fields">
                        <label for="spreadDownpayment" class="form-label text-start">Spread Downpayment</label>
                        <input
                        type="number"
                        v-model="spreadDownpaymentPercentage"
                        id="spreadDownpayment"
                        @input="updatePaymentDetails"
                        min="0"
                        max="100"
                        step="1"
                        class="form-control"
                        required
                        placeholder="Enter percentage"
                      />
                      <p><strong>Spread Downpayment:</strong> ₱{{ spreadDownpayment }}</p>
                      </div>
                    </div>
                  </div>

                  <div class="col-md-6">
                    <!-- TLP Discount -->
                    <div class="mb-3">
                      <label for="tlpDiscount" class="form-label text-start">TLP Discount (Optional)</label>
                      <input
                        type="number"
                        id="tlpDiscount"
                        v-model="tlpDiscount"
                        @input="updatePaymentDetails"
                        class="form-control"
                        min="0"
                        max="maxTlpDiscount"
                      />
                      <p><strong>TLP Discount:</strong> ₱{{ tlpDiscountAmount }}</p>
                      <p><strong>Net Unit Price:</strong> ₱{{ netUnitPrice }}</p>
                    </div>

                    <!-- Spot Downpayment -->
                    <div v-if="selectedPaymentPlan === 'Deferred Payment'" class="mb-3">
                      <label for="spotDownpayment" class="form-label text-start">Spot Downpayment</label>
                      <input
                        type="number"
                        id="spotDownpayment"
                        v-model="spotDownpaymentPercentage"
                        class="form-control"
                        @input="updatePaymentDetails"
                        min="0"
                        step="5"
                        placeholder="Enter downpayment percentage"
                        required
                      />
                      <p><strong>Spot Downpayment:</strong> ₱{{ spotDownpayment }}</p>
                      <p><strong>Reservation Fee:</strong> ₱{{ reservationFee }}</p>
                      <p v-if="selectedPaymentPlan === 'Spot Cash'"><strong>Net Full Payment:</strong> ₱{{ netFullPayment }}</p>
                      <p v-if="selectedPaymentPlan === 'Deferred Payment'"><strong>Net Downpayment:</strong> ₱{{ netDownpayment }}</p>
                      <!-- Payable in Months -->
                      <div class="mb-3">
                        <label for="months" class="form-label text-start">Months to Pay</label>
                        <input
                          type="number"
                          v-model="payableMonths"
                          id="months"
                          @input="updatePaymentDetails"
                          class="form-control"
                          min="1"
                          max="maxPayableMonths"
                          step="1"
                          required
                        />
                        <p><strong>Payable Per Month:</strong> ₱{{ payablePerMonth }}</p>
                        <p><strong>Balance Upon Turnover:</strong> ₱{{ balanceUponTurnover }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </form>
            </div>
          </div>

          </div>

          <div class="title-wrapper">
            <div class="title-left">
              <div class="title-icon"></div>
              <div class="edit-title"><strong>Payment Schedule Summary</strong></div>
            </div>
          </div>
          
          <div class="payment-container">
            <!-- Payment Summary and Additional Information -->
            <div class="summary-and-info">
              <!-- Payment Schedule Summary -->
              <div class="payment-schedule-summary">
                <div class="summary-item">
                  <span class="label">Spot Downpayment:</span>
                  <span class="value">₱0.00</span>
                </div>
                <hr class="separator">
                <div class="summary-item">
                  <span class="label">Spread Downpayment:</span>
                  <span class="value">₱N/A</span>
                </div>
                <hr class="separator">
                <div class="summary-item highlight">
                  <span class="label">Monthly Payment:</span>
                  <span class="value">₱50,000 / month for 360 months</span>
                </div>
                <hr class="separator">
                <div class="summary-item">
                  <span class="label">Balance Upon Turnover:</span>
                  <span class="value">₱3,000,000</span>
                </div>
                <button @click="toggleDetailedSchedule" class="btn btn-primary">
                  {{
                    showDetailedSchedule
                      ? "Hide Detailed Schedule"
                      : "Show Detailed Schedule"
                  }}
                </button>
              </div>

              <!-- Additional Information Box -->
              <div class="additional-box">
                <h4><center>Monthly Amortization (6.5%)</center></h4>
                <div class="summary-item">
                  <span class="label">10 years</span>
                  <span class="value">₱{{ amortization10Years.toFixed(2) }}</span>
                </div>
                <hr class="separator">
                <div class="summary-item">
                  <span class="label">15 years</span>
                  <span class="value">₱{{ amortization15Years.toFixed(2) }}</span>
                </div>
                <hr class="separator">
                <div class="summary-item">
                  <span class="label">20 years</span>
                  <span class="value">₱{{ amortization20Years.toFixed(2) }}</span>
                </div>
                <hr class="separator">
                <div class="summary-item">
                  <span class="label">25 years</span>
                  <span class="value">₱{{ amortization25Years.toFixed(2) }}</span>
                </div>
              </div>
            </div>

            <!-- Detailed Schedule -->
            <div v-if="showDetailedSchedule" class="detailed-schedule">
              <table class="payment-table">
                <thead>
                  <tr>
                    <th>Payment Type</th>
                    <th class="amount-column">Amount (₱)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Spot Downpayment</td>
                    <td class="amount-column highlight">₱{{ spotDownpayment.toFixed(2) }}</td>
                  </tr>
                  <tr>
                    <td>Spread Downpayment</td>
                    <td class="amount-column highlight">₱{{ spreadDownpayment.toFixed(2) }}</td>
                  </tr>
                  <tr v-for="month in payableMonths" :key="month">
                    <td>Month {{ month }} Payment</td>
                    <td class="amount-column">₱{{ payablePerMonth.toFixed(2) }}</td>
                  </tr>
                  <tr>
                    <td>Balance Upon Turnover</td>
                    <td class="amount-column highlight">₱{{ balanceUponTurnover.toFixed(2) }}</td>
                  </tr>
                </tbody>
              </table>
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

export default {
  components: {
    SideNav,
    AppHeader,
  },
  data() {
    return {
      unitId: this.$route.params.unitId,
      unitDetails: null,
      units: [],
      siteName: "",
      siteYear: "",
      isModalVisible: false,
      selectedUnit: {
        images: null, // Initially null
      },
      showDetailedSchedule: false, // To toggle detailed payment schedule
      customers: [],

      // Payment Scheme Data
      selectedPaymentPlan: "Spot Cash", // Default payment plan
      unitPrice: 0, // Example price of the unit
      spotCashDiscount: 0,
      maxSpotCashDiscount: 0, // Default value fetched from DB
      maxotherChargesPercentage: 0,
      maxtlpDiscount:0,
      tlpDiscount: 0,
      spotDiscount: 0,
      unitPriceAfterSpotDiscount: 0,
      tlpDiscountAmount: 0,
      netUnitPrice: 0,
      otherChargesPercentage: 0,
      otherCharges: 0,
      totalAmountPayable: 0,
      reservationFee: 0,
      netFullPayment: 0,
      spotDownpaymentPercentage: 0,
      spotDownpayment: 0,
      spreadDownpaymentPercentage: 0,
      spreadDownpayment: 0,
      payableMonths: 1,
      maxpayableMonths:0,
      payablePerMonth: 0,
      balanceUponTurnover: 0,
      vat: 0,
    };
    },
    computed:{
     amortization10Years() {
    return this.calculateAmortization(this.balanceUponTurnover, 10);
  },
  amortization15Years() {
    return this.calculateAmortization(this.balanceUponTurnover, 15);
  },
  amortization20Years() {
    return this.calculateAmortization(this.balanceUponTurnover, 20);
  },
  amortization25Years() {
    return this.calculateAmortization(this.balanceUponTurnover, 25);
  },
  },
  mounted() {
    this.fetchUnitDetails();
    this.updatePaymentDetails();

  },
methods: {
        calculateAmortization(balance, years) {
      const interestRate = 6.5 / 100; // 6.5% annual interest
      const monthlyRate = interestRate / 12; // Monthly interest rate
      const totalMonths = years * 12; // Total number of months
      return (
        balance *
        (monthlyRate * Math.pow(1 + monthlyRate, totalMonths)) /
        (Math.pow(1 + monthlyRate, totalMonths) - 1)
      );
    },
   async fetchUnitDetails() {
  try {
    const response = await axios.get(
      `http://localhost:8000/units/${this.unitId}/details`
    );
    this.unitDetails = response.data.unit; // Assuming `unit` is the key in the response
    this.selectedUnit = this.unitDetails;
    this.unitPrice = this.unitDetails.price; // Set the price of the selected unit
    this.spotCashDiscount = this.selectedUnit.spot_discount;
    this.payableMonths = this.selectedUnit.months;
    this.maxpayableMonths = this.payableMonths;
    this.maxSpotCashDiscount= this.spotCashDiscount; // Default value fetched from DB
    this.tlpDiscount = this.selectedUnit.TLP_Discount;
    this.maxtlpDiscount = this.tlpDiscount;
    this.otherChargesPercentage = this.selectedUnit.other_charges;
    this.maxotherChargesPercentage = this.otherChargesPercentage;
    this.reservationFee = this.selectedUnit.reservation_fee;
    this.vat = this.selectedUnit.vat_percent;
    this.updatePaymentDetails();
  } catch (error) {
    console.error("Error fetching unit details:", error);
  }
      },
 toggleDetailedSchedule() {
      // Toggle the visibility of the detailed payment schedule
      this.showDetailedSchedule = !this.showDetailedSchedule;
    },
    updatePaymentDetails() {
    if (this.spotCashDiscount < 0) {
        this.spotCashDiscount = 0;
      } else if (this.spotCashDiscount > this.maxSpotCashDiscount) {
        this.spotCashDiscount = this.maxSpotCashDiscount;
      }
      if (this.tlpDiscount < 0) {
        this.tlpDiscount = 0;
      } else if (this.tlpDiscount > this.maxtlpDiscount) {
        this.tlpDiscount = this.maxtlpDiscount;
      }
      if (this.otherChargesPercentage < 0) {
        this.otherChargesPercentage = 0;
      } else if (this.otherChargesPercentage > this.maxotherChargesPercentage) {
        this.otherChargesPercentage = this.maxotherChargesPercentage;
      }
      if (this.payableMonths < 0) {
        this.payableMonths = 1;
      } else if (this.payableMonths > this.maxpayableMonths) {
        this.payableMonths = this.maxpayableMonths;
      }
      this.applySpotCashDiscount();
      this.applyTLPDiscount();
      this.applyOtherCharges();
      this.calculateVAT();
      this.calculateFinancingDetails();
    },

    applySpotCashDiscount() {
    const discountPercentage = parseFloat(this.spotCashDiscount);
    this.spotDiscount = (this.unitPrice * discountPercentage) / 100;
    console.log(this.spotDiscount,this.unitPrice);
    this.unitPriceAfterSpotDiscount = this.unitPrice - this.spotDiscount;
    this.updateNetUnitPrice();
    },

    applyTLPDiscount() {
      const discountPercentage = parseFloat(this.tlpDiscount);
      this.tlpDiscountAmount =
        (this.unitPriceAfterSpotDiscount * discountPercentage) / 100;
      this.updateNetUnitPrice();
    },

    updateNetUnitPrice() {
      this.netUnitPrice =
        this.unitPriceAfterSpotDiscount - this.tlpDiscountAmount;
      this.applyOtherCharges();
    },

    applyOtherCharges() {
      const otherChargesPercentage = parseFloat(this.otherChargesPercentage);
      this.otherCharges = (this.netUnitPrice * otherChargesPercentage) / 100;
      this.totalAmountPayable = this.netUnitPrice + this.otherCharges;
      this.netFullPayment = this.totalAmountPayable - this.reservationFee;
    },
    calculateVAT() {
      if (this.netUnitPrice > 3600000) {
        this.vatAmount = this.netUnitPrice * (this.vat / 100);
        this.totalAmountPayable += this.vatAmount;
      }
    },

    calculateFinancingDetails() {
      this.spotDownpayment =
        this.totalAmountPayable * (this.spotDownpaymentPercentage / 100);
      this.spreadDownpayment =
        this.totalAmountPayable * (this.spreadDownpaymentPercentage / 100);
      if (this.spotDownpaymentPercentage == "0") {
        this.netDownpayment = this.spreadDownpayment - this.reservationFee;
        this.payablePerMonth = this.netDownpayment / this.payableMonths;
      } else {
        this.netDownpayment = this.spotDownpayment - this.reservationFee;
        this.payablePerMonth = this.spreadDownpayment / this.payableMonths;
      }
      this.balanceUponTurnover =
        ((100 -
          (Number(this.spreadDownpaymentPercentage) +
            Number(this.spotDownpaymentPercentage))) /
          100) *
        this.totalAmountPayable; // Correct sum of percentages
    },
  },
};
</script>

<style scoped>
html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.SideNav {
  width: 250px;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #343a40;
  z-index: 1;
}

.AppHeader {
  width: 100%;
  height: 60px;
  background-color: #343a40;
  display: flex;
  align-items: center;
  padding-left: 10px;
  color: #ffffff;
}

.main-page {
  display: flex;
  min-height: 100vh;
  background-color: #e8f0fa;
}

.main-content {
  display: flex;
  flex-direction: column;
  margin-top: 80px;
  margin-left: 250px;
  flex: 1;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}

.text{
  color: black;
  text-decoration: none !important;
}

.title-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1100px;
  margin: 20px auto;
  /* Center the wrapper */
}

.title-left {
  display: flex;
  align-items: center;
}

.title-icon {
  width: 15px;
  height: 5px;
  background-color: #343a40;
  border-radius: 5px;
  margin-right: 10px;
}

.edit-title {
  color: #000000;
  text-align: left;
}

.payment-plan-container {
  padding: 20px;
  border-radius: 8px;
}

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 2.5rem;
}

.form-label {
  color: #333;
}

p {
  margin: 5px 0;
  font-size: 0.9rem;
}

.row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.col-md-6 {
  flex: 1;
  min-width: 300px;
}

.align-fields{
  margin-top: 35px;
}

.property-price {
  font-size: 20px;
}

.payment-container {
  display: flex;
  flex-wrap: wrap; /* Allows wrapping for responsiveness */
  justify-content: space-between;
  gap: 20px;
  margin: 20px 0;
}

.summary-and-info {
  display: flex;
  flex-direction: column; /* Stack summary and additional box */
  gap: 20px;
  flex: 1; /* Flex item for dynamic width */
  max-width: 400px;
}

.payment-schedule-summary,
.detailed-schedule,
.additional-box {
  min-width: 300px;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  overflow-y: auto; /* Add scroll if content exceeds height */
}

.payment-schedule-summary {
  background: #f9f9f9;
  height: 300px;
  max-width: 400px;
  margin-left: 60px !important;
}

.additional-box {
  background: #f9f9f9;
  text-align: left;
  margin-top: 20px;
  max-width: 400px;
  height: 300px;
  margin-left: 60px !important;
}

.detailed-schedule {
  flex: 1; /* Flex item for dynamic width */
  height: 450px;
  min-width: 300px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-size: 16px;
}

.summary-item .label {
  color: #555;
}

.summary-item .value {
  font-weight: bold;
  color: #000;
}

.summary-item.highlight .value {
  font-weight: bold;
  color: #007bff;
}

.separator {
  border: none;
  border-top: 1px solid #ddd;
  margin: 10px 0;
}

.btn-primary {
  display: block;
  width: 100%;
  padding: 10px 20px;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.payment-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 16px;
  font-family: Arial, sans-serif;
  margin-top: 10px;
}

.payment-table th,
.payment-table td {
  border: 1px solid #ddd;
  padding: 12px;
}

.payment-table thead th {
  background-color: #007bff;
  color: white;
  text-align: center;
}

.payment-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.payment-table tbody tr:hover {
  background-color: #f1f1f1;
}

.amount-column {
  text-align: right;
}

.highlight {
  font-weight: bold;
  color: #007bff;
}

/* juju */

label {
  display: block;
  margin: 10px 0 5px;
}

input {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  box-sizing: border-box;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
