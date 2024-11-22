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
          <p><strong>Site:</strong> {{ selectedSale.site_name }}</p>
          <p><strong>Unit:</strong> {{ selectedSale.unit_title }}</p>
          <!-- Payment Plan Section -->
          <div class="form-group">
            <label for="paymentPlan">Payment Plan</label>
            <select v-model="selectedPaymentPlan" id="paymentPlan" required>
              <option value="Spot Cash">Spot Cash</option>
              <option value="Deffered Payment">Deffered Payment</option>
            </select>
          </div>

        
          <!-- In-House Financing Plan -->
            <p><strong>Unit Price:</strong> ₱{{ unitPrice }}</p>

            <!-- Spot Discount -->
            <div class="form-group">
              <label for="spotDiscount">Spot Discount</label>
              <select v-model="spotCashDiscount" id="spotDiscount" @change="updatePaymentDetails" required>
                <option value="0">0%</option>
                <option value="1">1%</option>
                <option value="5">5%</option>
                <option value="10">10%</option>
                <option value="15">15%</option>
              </select>
            </div>
            <p><strong>Spot Discount:</strong> ₱{{ spotDiscount }}</p>

            <!-- Unit Price after Spot Discount -->
            <p><strong>Unit Price after Spot Discount:</strong> ₱{{ unitPriceAfterSpotDiscount }}</p>

            <!-- TLP Discount -->
            <div class="form-group">
              <label for="tlpDiscount">TLP Discount</label>
              <select v-model="tlpDiscount" id="tlpDiscount" @change="updatePaymentDetails" required>
                <option value="0">None</option>
                <option value="5">5%</option>
                <option value="10">10%</option>
                <option value="15">15%</option>
              </select>
            </div>
            <p><strong>TLP Discount:</strong> ₱{{ tlpDiscountAmount }}</p>

            <!-- Net Unit Price -->
            <p><strong>Net Unit Price:</strong> ₱{{ netUnitPrice }}</p>

            <!-- Other Charges -->
            <div class="form-group">
              <label for="otherCharges">Other Charges</label>
              <select v-model="otherChargesPercentage" id="otherCharges" @change="updatePaymentDetails" required>
                <option value="8.5">8.5%</option>
                <option value="10">10%</option>
                <option value="15">15%</option>
              </select>
            </div>
            <p><strong>Other Charges:</strong> ₱{{ otherCharges }}</p>

            <!-- VAT Calculation -->
            <p v-if="netUnitPrice > 3600000"><strong>VAT (12%):</strong> ₱{{ vatAmount }}</p>

            <!-- Total Amount Payable -->
            <p><strong>Total Amount Payable:</strong> ₱{{ totalAmountPayable }}</p>
            <!-- Spot Downpayment -->
            <div v-if="selectedPaymentPlan === 'Deffered Payment'" class="form-group">
            <label for="spotDownpayment">Spot Downpayment</label>
            <input 
              type="number" 
              id="spotDownpayment" 
              v-model="spotDownpaymentPercentage" 
              @input="updatePaymentDetails"
              min="0"
              step="5"
              placeholder="Enter downpayment percentage"
              required
            />
          </div>

            <p v-if="selectedPaymentPlan === 'Deffered Payment'"><strong>Spot Downpayment:</strong> ₱{{ spotDownpayment }}</p>

            <!-- Reservation Fee -->
            <p><strong>Reservation Fee:</strong> ₱{{ reservationFee }}</p>
            <p v-if="selectedPaymentPlan === 'Spot Cash'"><strong>Net Full Payment:</strong> ₱{{ netFullPayment }}</p>


            <!-- Net Downpayment -->
            <p v-if="selectedPaymentPlan === 'Deffered Payment'"><strong>Net Downpayment:</strong> ₱{{ netDownpayment }}</p>
            
            <div v-if="selectedPaymentPlan === 'Deffered Payment'">
            <!-- Spread Downpayment -->
            <div class="form-group">
              <label for="spreadDownpayment">Spread Downpayment</label>
              <select v-model="spreadDownpaymentPercentage" id="spreadDownpayment" @change="updatePaymentDetails" required>
                <option value="0">0%</option>
                <option value="5">5%</option>
                <option value="10">10%</option>
                <option value="15">15%</option>
              </select>
            </div>
            <p><strong>Spread Downpayment:</strong> ₱{{ spreadDownpayment }}</p>

            <!-- Payable in Months -->
            <div class="form-group">
              <label for="months">Months to Pay</label>
              <input type="number" v-model="payableMonths" id="months" @input="updatePaymentDetails" min="1" step="1"  required />
            </div>
            <p><strong>Payable Per Month:</strong> ₱{{ payablePerMonth }}</p>
            <!-- Balance Upon Turnover -->
            <p><strong>Balance Upon Turnover:</strong> ₱{{ balanceUponTurnover }}</p>
            <h3>Payment Schedule Summary</h3>

    <!-- Payment Summary -->
    <div class="payment-summary">
      <p><strong>Spot Downpayment:</strong> ₱{{ spotDownpayment.toFixed(2) }}</p>
      <p><strong>Spread Downpayment:</strong> ₱{{ spreadDownpayment.toFixed(2) }}</p>
      <p><strong>Monthly Payment:</strong> ₱{{ payablePerMonth.toFixed(2) }} / month for {{ payableMonths }} months</p>
      <p><strong>Balance Upon Turnover:</strong> ₱{{ balanceUponTurnover.toFixed(2) }}</p>
    </div>

    <!-- Expandable Detailed Schedule Section -->
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
          <tr v-for="month in payableMonths" :key="month">
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
          <!-- Required Documents Section (Always Displayed) -->
          <div class="form-group">
            <h3>Required Documents</h3>
            <ul>
              <li><strong>Reservation Agreement:</strong>
                <input type="file"  @change="handleFileChange" id="reservationAgreement" required />
              </li>
              <li><strong>Valid ID (Front and Back):</strong> A clear copy of a government-issued ID with a signature.</li>
              <li><strong>Proof of Billing:</strong> A recent utility bill or bank statement showing the customer's name and address.</li>
              <li><strong>Proof of Income:</strong> A recent payslip or income tax return (ITR).</li>
               <li><strong>Sales Agreement:</strong> To be followed (after the contract is signed).</li>
              <li><strong>TIN:</strong> A clear copy of the customer's Taxpayer Identification Number (TIN) certificate.</li>
              </ul>
          </div>
        <button @click="submitToCustomer">Submit to Customer</button>
        <button @click="closeModal">Close</button>
        <!-- Loading Indicator -->
        <div v-if="loading" class="loading-overlay">
          <div class="loading-spinner">
            <div class="spinner"></div>
            <p>Submitting...</p>
          </div>
        </div>


        </div>
        </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import axios from 'axios';

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
      // Payment Scheme Data
      selectedPaymentPlan: 'Spot Cash', // Default payment plan
      unitPrice: 0, // Example price of the unit
      spotCashDiscount: 0,
      tlpDiscount: 0,
      spotDiscount: 0, 
      unitPriceAfterSpotDiscount: 0,
      tlpDiscountAmount: 0,
      netUnitPrice: 0,
      otherChargesPercentage: 8.5,
      otherCharges: 0,
      totalAmountPayable: 0,
      reservationFee: 0,
      netFullPayment: 0,
      spotDownpaymentPercentage: 0,
      spotDownpayment: 0,
      spreadDownpaymentPercentage: 0,
      spreadDownpayment: 0,
      payableMonths: 40,
      payablePerMonth: 0,
      balanceUponTurnover: 0,
      file: null,

      showDetailedSchedule: false, // To toggle detailed payment schedule
      loading: false, // Track loading state

    };
  },
  methods: {
    toggleDetailedSchedule() {
      // Toggle the visibility of the detailed payment schedule
      this.showDetailedSchedule = !this.showDetailedSchedule;
    },
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
      this.unitPrice = sale.price;  // Set unitPrice to the selected sale's unit price
      this.showModal = true;
      this.updatePaymentDetails();

    },
    updatePaymentDetails() {
      if (this.selectedPaymentPlan === 'Spot Cash') {
        this.applySpotCashDiscount();
        this.applyTLPDiscount();
        this.applyOtherCharges();
        this.calculateVAT();

      }
       else if (this.selectedPaymentPlan === 'Deffered Payment') {
        this.applySpotCashDiscount();
        this.applyTLPDiscount();
        this.applyOtherCharges();
        this.calculateVAT();
        this.calculateFinancingDetails();
      }
    },

    applySpotCashDiscount() {
      const discountPercentage = parseFloat(this.spotCashDiscount);
      this.spotDiscount = (this.unitPrice * discountPercentage) / 100;
      this.unitPriceAfterSpotDiscount = this.unitPrice - this.spotDiscount;
      this.updateNetUnitPrice();
    },
    

    applyTLPDiscount() {
      const discountPercentage = parseFloat(this.tlpDiscount);
      this.tlpDiscountAmount = (this.unitPriceAfterSpotDiscount * discountPercentage) / 100;
      this.updateNetUnitPrice();
    },

    updateNetUnitPrice() {
      this.netUnitPrice = this.unitPriceAfterSpotDiscount - this.tlpDiscountAmount;
      this.applyOtherCharges();
    },

    applyOtherCharges() {
      const otherChargesPercentage = parseFloat(this.otherChargesPercentage);
      this.otherCharges = (this.netUnitPrice * otherChargesPercentage) / 100;
      this.totalAmountPayable = this.netUnitPrice + this.otherCharges;
      this.reservationFee = "30000" // 10% reservation fee
      this.netFullPayment = this.totalAmountPayable - this.reservationFee;
    },
    calculateVAT() {
      if (this.netUnitPrice > 3600000) {
        this.vatAmount = this.netUnitPrice * 0.12;
        this.totalAmountPayable += this.vatAmount;
      }

    },

    calculateFinancingDetails() {
      this.spotDownpayment = this.totalAmountPayable * (this.spotDownpaymentPercentage / 100);
      this.spreadDownpayment = this.totalAmountPayable * (this.spreadDownpaymentPercentage / 100);
      if (this.spotDownpaymentPercentage == '0') {
        this.netDownpayment = this.spreadDownpayment - this.reservationFee;
        this.payablePerMonth = this.netDownpayment / this.payableMonths;
      }
      else {
        this.netDownpayment = this.spotDownpayment - this.reservationFee;
        this.payablePerMonth = this.spreadDownpayment / this.payableMonths; 
      }
      this.balanceUponTurnover =(100-(Number(this.spreadDownpaymentPercentage) + Number(this.spotDownpaymentPercentage)))/100*this.totalAmountPayable;  // Correct sum of percentages
    },
    handleFileChange(event) {
      const fileInput = event.target.files[0];
      if (fileInput) {
        this.file = fileInput;
      }
    },
  
    async submitToCustomer() {
    this.loading = true;
    // Collect data to send to the backend
    const data = {
      customer_id: this.selectedSale.customer_id,
      site_id: this.selectedSale.site_id,
      unit_id: this.selectedSale.unit_id,
      broker_id: this.selectedSale.broker_id,
      payment_plan: this.selectedPaymentPlan,
      spot_discount_percent: this.spotCashDiscount,
      tlp_discount_percent: this.tlpDiscount,
      other_charges_percent: this.otherChargesPercentage,
      spot_downpayment_percent: this.spotDownpaymentPercentage,
      reservation_fee: this.reservationFee,
      spread_downpayment_percent: this.spreadDownpaymentPercentage,
      payable_months: this.payableMonths,
      payable_per_month: this.payablePerMonth,
      balance_upon_turnover: this.balanceUponTurnover,
      net_unit_price: this.netUnitPrice,
      total_amount_payable: this.totalAmountPayable,
      net_full_payment: this.netFullPayment,
      customer_email: this.selectedSale.email,  // Include the customer email
      reservation_agreement: this.file,  // Add reservation_agreement here
      };

  try {
    const response = await axios.post('http://localhost:8000/submit-sales/', data, {
      headers: {
        'Content-Type': 'application/json',  // Sending JSON data
      }
    });

    // Axios automatically parses the JSON response, so you can directly use response.data
    if (response.data.success) {
      alert("Sales agreement submitted successfully!");
      this.closeModal(); // Close the modal after submission
    } else {
      alert("Error: " + response.data.message);
    }
  } catch (error) {
    // Handle any errors that occur
    if (error.response) {
      // Server responded with a status code outside 2xx range
      console.error("Response error:", error.response.data);
      alert("Error: " + (error.response.data.message || "Failed to submit sales agreement."));
    } else if (error.request) {
      // Request was made but no response received
      console.error("Request error:", error.request);
      alert("No response from server. Please try again later.");
    } else {
      // Something else caused the error
      console.error("Error:", error.message);
      alert("An error occurred while submitting the sales agreement: " + error.message);
    }
      }
  finally {
    // Stop loading after the request completes
    this.loading = false;
  }
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
  overflow: hidden; /* Hide any overflowed content */
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-height: 90%; /* Ensure the modal doesn't exceed 90% of the viewport height */
  overflow-y: auto; /* Make the content scrollable if it overflows */
}

.payment-summary {
  margin-bottom: 20px;
}

.detailed-schedule {
  margin-top: 20px;
  border-top: 1px solid #ccc;
  padding-top: 10px;
}

.toggle-button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  margin-bottom: 20px;
}

.toggle-button:hover {
  background-color: #0056b3;
}

table {
  width: 100%;
  border-collapse: collapse;
}

table, th, td {
  border: 1px solid #ddd;
}

th, td {
  padding: 10px;
  text-align: left;
}

th {
  background-color: #f4f4f4;
}

td {
  text-align: right;
}
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* Ensure it's on top of other content */
}

.loading-spinner {
  text-align: center;
  color: #fff;
}

.spinner {
  border: 4px solid #f3f3f3; /* Light grey background */
  border-top: 4px solid #3498db; /* Blue color for the spinning part */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

</style>
