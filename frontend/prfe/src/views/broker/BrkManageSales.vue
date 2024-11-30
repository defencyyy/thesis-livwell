<template>
  <div>
    <AppHeader/>
 
  <div class="manage-sales-page">

    <SideNav />
    <div class="content">
      <h1 class="display-5 fw-bolder text-capitalize">Welcome to the Manage Sales Page</h1>
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
            style="cursor: pointer"
           
          > 
            <td class="text-uppercase">{{ sale.customer_name}}({{ sale.customer_code }})</td>
            <td class="text-uppercase">{{ sale.site_name }}</td>
            <td class="text-uppercase">{{ sale.unit_title }}</td>
            <td class="text-uppercase">{{ sale.status }}</td>
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
        <div v-if="salesDetailsExists">
        <p><strong>Payment Plan:</strong> {{ salesDetails.payment_plan }}</p>
        <p><strong>Unit Price:</strong> ₱{{ salesDetails.unit_price }}</p>
        <p><strong>Spot Discount Percentage:</strong> {{ salesDetails.spot_discount }}%</p>
        <p><strong>Spot Discount:</strong> ₱{{ this.spotDiscount }}</p>
        <p><strong>Unit Price after Spot Discount:</strong> ₱{{ this.unitPriceAfterSpotDiscount }}</p>
        <p><strong>TLP Discount Percentage:</strong> {{ salesDetails.tlp_discount }}%</p>
        <p><strong>TLP Discount:</strong> ₱{{ this.tlpDiscountAmount }}</p>
        <p><strong>Net Unit Price:</strong> ₱{{ netUnitPrice }}</p>
        <p><strong>Other Charges Percentage:</strong> {{ salesDetails.other_charges_percent }}%</p>
        <p><strong>Other Charges:</strong> ₱{{ otherCharges }}</p>
        <p v-if="netUnitPrice > 3600000"><strong>VAT (12%):</strong> ₱{{ vatAmount }}</p>
        <p ><strong>Total Amount Payable:</strong> ₱{{ totalAmountPayable }}</p>
        <p v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Spot Downpayment Percentage:</strong> {{ salesDetails.spot_downpayment_percent }}%</p>
        <p v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Spot Downpayment:</strong> ₱{{ spotDownpayment }}</p>
        <p><strong>Reservation Fee:</strong> ₱{{ salesDetails.reservation_fee }}</p>
        <p v-if="salesDetails.payment_plan === 'Spot Cash'"><strong>Net Full Payment:</strong> ₱{{ netFullPayment }}</p>
        <p v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Net Downpayment:</strong> ₱{{ netDownpayment }}</p>
        <p v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Spread Downpayment Percentage:</strong> {{ salesDetails.spread_downpayment_percent }}%</p>
        <p v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Spread Downpayment:</strong> ₱{{ spreadDownpayment }}</p>
        <p v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Payable Months:</strong> {{ salesDetails.payable_months }}</p>
        <p v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Payable Per Month:</strong> ₱{{ payablePerMonth }}</p>
        <p v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Balance Upon Turnover:</strong> ₱{{ balanceUponTurnover }}</p>
        <button v-if="selectedSale.status !== 'Pending Sold' && selectedSale.status !== 'Sold'" @click="markUnitAsSold">Mark Unit as Sold </button>
        <button @click="closeModal">Close</button>

            <!-- Add other fields you want to display here -->
          </div>

          <!-- Payment Plan Section -->
          <div v-if="!salesDetailsExists">
            <div class="form-group">
            <label for="paymentPlan"><b>Payment Plan: </b></label>
            <select v-model="selectedPaymentPlan" id="paymentPlan" required>
              <option value="Spot Cash">Spot Cash</option>
              <option value="Deffered Payment">Deffered Payment</option>
            </select>
          </div>


          <!-- In-House Financing Plan -->
            <p><strong>Unit Price:</strong> ₱{{ unitPrice }}</p>

            <!-- Spot Discount -->
            <div class="form-group">
              <label for="spotDiscount">Spot Discount: </label>
              <select v-model="spotCashDiscount" id="spotDiscount" @change="updatePaymentDetails" required>
                <option value="0">0%</option>
                <option value="1">1%</option>
                <option value="5">5%</option>
                <option value="10">10%</option>
                <option value="15">15%</option>
              </select>
            </div>
            <p><strong>Spot Discount:</strong> ₱{{ spotDiscount }}</p>

            <p><strong>Unit Price after Spot Discount:</strong> ₱{{ unitPriceAfterSpotDiscount }}</p>


             <!-- TLP Discount -->
            <div class="form-group">
              <label for="tlpDiscount">TLP Discount: </label>
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
              <label for="otherCharges">Other Charges: </label>
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
            <p>
              <strong>Total Amount Payable:</strong> ₱{{ totalAmountPayable }}
            </p>
            <!-- Spot Downpayment -->
            <div
              v-if="selectedPaymentPlan === 'Deffered Payment'"
              class="form-group"
            >
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
        <!-- Display error message if there's an error -->
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        </div>
        </div>
        </div>
    </div>
  </div>

</div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue"
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "ManageSales",
  components: {
    SideNav,
    AppHeader,
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId || null,
      userType: (state) => state.userType || null,
      companyId: (state) => state.companyId || null,
      loggedIn: (state) => state.loggedIn, // Use Vuex loggedIn state
    }),
    localStorageUserId() {
      return localStorage.getItem("user_id");
    },
    localStorageCompanyId() {
      return localStorage.getItem("company_id");
    },
  },
  data() {
    return {
      sales: [], // List of sales data
      showModal: false,
      selectedSale: null, // Currently selected sale row
      salesDetailsExists: false, // Flag to check if sales details already exist
      salesDetails: null, // S
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
      errorMessage: '',    // Error message
      showDetailedSchedule: false, // To toggle detailed payment schedule
      loading: false, // Track loading state
    };
  },
  mounted() {
    this.fetchSales(); // Fetch sales when the component is mounted

    if (!this.loggedIn || this.userType !== "broker" || !this.companyId) {
      this.redirectToLogin();
    }
  },
  watch: {
    loggedIn(newVal) {
      if (!newVal || this.userType !== "broker" || !this.companyId) {
        this.redirectToLogin();
      }
    },
    userType(newVal) {
      if (newVal !== "broker" || !this.companyId) {
        this.redirectToLogin();
      }
    },
    companyId(newVal) {
      if (!newVal || this.userType !== "broker") {
        this.redirectToLogin();
      }
    },
  },
  methods: {
    toggleDetailedSchedule() {
      // Toggle the visibility of the detailed payment schedule
      this.showDetailedSchedule = !this.showDetailedSchedule;
    },
    async checkSalesDetails() {
      if (!this.selectedSale) {
        console.error("No sale selected!");
        return;
      }

      try {
        const response = await axios.get(
          `http://localhost:8000/salesdetails/check/${this.selectedSale.customer_id}/${this.selectedSale.site_id}/${this.selectedSale.unit_id}`
        );
        if (response.data.exists) {
          this.salesDetailsExists = true;
          this.salesDetails = response.data.details;
          this.updatePaymentDetails();
        } else {
          this.salesDetailsExists = false;
          this.updatePaymentDetails();
        }
      } catch (error) {
        console.error("Error checking sales details:", error);
      }
    },

    async fetchSales() {
      const brokerId = this.userId; // Use Vuex userId instead of localStorage
      try {
        const response = await fetch(
          `http://localhost:8000/sales/?broker_id=${brokerId}`
        );
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
      this.unitPrice = sale.price; // Set unitPrice to the selected sale's unit price
      this.showModal = true;

     
      // Check if the sales details already exist for this customer and unit
      this.checkSalesDetails();
      this.updatePaymentDetails();
    },
    updatePaymentDetails() {
      if (this.salesDetailsExists) {
        // Use salesDetails to update payment details
        this.updateSalesDetailsPaymentDetails();
      } else {
        // Use manual input values to calculate details
        this.applySpotCashDiscount();
        this.applyTLPDiscount();
        this.applyOtherCharges();
        this.calculateVAT();
        this.calculateFinancingDetails();
      }
    },
    updateSalesDetailsPaymentDetails() {
    // Extract values from salesDetails for calculation
    const sales = this.salesDetails;

      this.unitPrice = sales.unit_price;
    this.spotCashDiscount = sales.spot_discount;
    this.tlpDiscount = sales.tlp_discount;
    this.otherChargesPercentage = sales.other_charges_percent;
    this.spotDownpaymentPercentage = sales.spot_downpayment_percent;
    this.spreadDownpaymentPercentage = sales.spread_downpayment_percent;
    this.payableMonths = sales.payable_months;
    this.reservationFee = sales.reservation_fee;

    // Now, perform calculations based on these values
    this.applySpotCashDiscount();
    this.applyTLPDiscount();
    this.applyOtherCharges();
    this.calculateVAT();
    this.calculateFinancingDetails();
  },
  applySpotCashDiscount() {
    const discountPercentage = parseFloat(this.spotCashDiscount);
    this.spotDiscount = (this.unitPrice * discountPercentage) / 100;
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
    this.reservationFee = "30000"; // 10% reservation fee
    this.netFullPayment = this.totalAmountPayable - this.reservationFee;
  },
  calculateVAT() {
    if (this.netUnitPrice > 3600000) {
      this.vatAmount = this.netUnitPrice * 0.12;
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
    this.balanceUponTurnover =((100 -(Number(this.spreadDownpaymentPercentage) +Number(this.spotDownpaymentPercentage))) /100) *this.totalAmountPayable; // Correct sum of percentages
  },

  handleFileChange(event) {
    const fileInput = event.target.files[0];
    if (fileInput) {
      this.file = fileInput;
    }
  },

  async submitToCustomer() {
    this.loading = true;
    this.updatePaymentDetails();

    // Check if the selected payment plan is "Spot Cash" and validate required fields
    if (!this.file) {
      this.errorMessage ="All fields are required except the payment reference.";
      this.loading = false;
      return; // Stop further processing if validation fails
    }
    if (
      this.selectedPaymentPlan === "Deffered Payment" &&this.netDownpayment < 0) {
      this.errorMessage = "Select Down Payment Percent";
      this.loading = false;
      return; // Stop further processing if validation fails
    }
    const formData = new FormData();
    // Add sales details
    formData.append("customer_id", this.selectedSale.customer_id);
    formData.append("site_id", this.selectedSale.site_id);
    formData.append("unit_id", this.selectedSale.unit_id);
    formData.append("broker_id", this.selectedSale.broker_id);
    formData.append("payment_plan", this.selectedPaymentPlan);
    formData.append("spot_discount_percent", this.spotCashDiscount);
    formData.append("tlp_discount_percent", this.tlpDiscount);
    formData.append("other_charges_percent", this.otherChargesPercentage);
    formData.append("spot_downpayment_percent", this.spotDownpaymentPercentage);
    formData.append("reservation_fee", this.reservationFee);
    formData.append("spread_downpayment_percent",this.spreadDownpaymentPercentage);
    formData.append("payable_months", this.payableMonths);
    formData.append("payable_per_month", this.payablePerMonth);
    formData.append("balance_upon_turnover", this.balanceUponTurnover);
    formData.append("net_unit_price", this.netUnitPrice);
    formData.append("total_amount_payable", this.totalAmountPayable);
    formData.append("net_full_payment", this.netFullPayment);
    formData.append("customer_email", this.selectedSale.email);

    // Add the reservation agreement file
    if (this.file) {
      formData.append("reservation_agreement", this.file);
    }

    try {
      const response = await axios.post(
        "http://localhost:8000/submit-sales/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data", // Use multipart/form-data for file uploads
          },
        }
      );

      if (response.data.success) {
        alert("Sales agreement submitted successfully!");
        this.closeModal(); // Close the modal after submission
      } else {
        alert("Error: " + response.data.message);
      }
    } catch (error) {
      console.error("Error during submission:", error);
      alert(
        "Error: " +
          (error.response ? error.response.data.message : error.message)
      );
    } finally {
      this.loading = false;
    }
    },
  async markUnitAsSold() {
        try {      

            // Make an API request to mark the unit as sold
          const response = await axios.post(`http://localhost:8000/mark/${this.selectedSale.customer_id}/${this.selectedSale.sale_id}/`);

            
            if (response.data.success) {
                // Successfully marked as sold
                alert('Unit successfully marked as sold!');
                // Optionally, update the UI to reflect this change (e.g., mark the unit in the list as sold)
            } else {
                // Handle failure (e.g., customer has not submitted all required documents)
                alert(response.data.message);
            }
        } catch (error) {
            console.error('Error marking unit as sold:', error);
            alert('An error occurred while marking the unit as sold.');
        }
    },
  redirectToLogin() {
    this.$router.push({ name: "BrkLogin" });
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
  border-collapse: separate; /* Enables border radius */
  border-spacing: 0; /* Ensures proper alignment for border radius */
  text-align: left;
  background-color: white; /* Ensure the table has a distinct background */

  box-shadow: 0 15px 12px rgba(0, 0, 0, 0.1); /* Adds subtle shadow */

}

.sales-table th,
.sales-table td {
  padding: 8px;
  border-bottom: 1px solid #ccc;
  text-align: start
}

.sales-table th {
  background-color: #c2ffd1;
}





.sales-table tr:hover {
  background-color: #c2c2c2;
  transition: ease 0.3s;
}


/* .modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  display: flex;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-height: 90%; 
  overflow-y: auto; 
} */

/* Modal Background */
/* Modal Background */
.modal {

  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  display: flex;
}

/* Modal Content */
.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 500px;
  max-height: 80%;
  overflow-y: auto;
  text-align: left; /* Align all text to the left */
}

/* Headings */
.modal-content h2 {
  color: #333;
  margin-bottom: 10px;
  text-align: left; /* Ensure headings are aligned to the left */
}

/* Paragraph Styling */
.modal-content p {
  font-size: 14px;
  margin: 8px 0;
  text-align: left; /* Align paragraphs to the left */
}

/* Buttons */
.button {
  background: #ddd;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
  transition: all 0.3s;
  text-align: center; /* Center-align button text */
}

.button:hover {
  background: #ccc;
}

.button.primary {
  background: #007bff;
  color: #fff;
}

.button.primary:hover {
  background: #0056b3;
}



/* BUTTON FOR ADD CUSTOMER AND CLOSE */

button {
  padding: 10px 20px; /* Add padding for a comfortable size */
  border: none; /* Remove default border */
  border-radius: 8px; /* Rounded corners */
  font-size: 16px; /* Increase text size for better readability */
  cursor: pointer; /* Change cursor to pointer for interactivity */
  transition: all 0.3s ease; /* Smooth transition for hover effects */
}

/* Submit to Customer Button */
button:first-of-type {
  background-color: #28a745; /* Green background */
  color: white; /* White text */
}

button:first-of-type:hover {
  background-color: #218838; /* Darker green on hover */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* Subtle shadow on hover */
}

button:first-of-type:active {
  background-color: #1e7e34; /* Even darker green on click */
  transform: scale(0.98); /* Slight shrink effect on click */
}

/* Close Button */
button:last-of-type {
  background-color: #dc3545; /* Red background */
  color: white; /* White text */
  margin-left: 10px; /* Add spacing between buttons */
}

button:last-of-type:hover {
  background-color: #c82333; /* Darker red on hover */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* Subtle shadow on hover */
}

button:last-of-type:active {
  background-color: #bd2130; /* Even darker red on click */
  transform: scale(0.98); /* Slight shrink effect on click */
}





/* Dropdown Styling */
.dropdown {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
  background: #f9f9f9;
  cursor: pointer;
  text-align: left; /* Ensure dropdown text aligns to the left */
}

.dropdown:focus {
  border-color: #007bff;
  outline: none;
}

/* Scrollable Content */
.modal-content::-webkit-scrollbar {
  width: 6px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: #555;
}







.payment-summary {
  margin-bottom: 20px;
}

.detailed-schedule {
  color: #0056b3;
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

table,
th,
td {
  border: 1px solid #ddd;
}

th,
td {
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
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.error-message {
  color: red;
  font-weight: bold;
  margin-bottom: 10px;
}




















/* Form Group Styling */
.form-group {
  margin-bottom: 15px;
}

/* Dropdown Styling */
.form-group select {
  background-color: white; /* Set the background to white */
  color: black; /* Set the text color to white */
  padding: 8px;
  border: 1px solid #ccc; /* Add a subtle border for visibility */
  border-radius: 5px;
  font-size: 14px;
  width: 100%; /* Make it responsive */
  cursor: pointer;
}

.form-group select:focus {
  outline: none;
  border-color: #007bff; /* Highlight border on focus */
}

/* Dropdown Hover Text */
.form-group select:hover {
  color: black; /* Change text color to black on hover for better visibility */
}



/* Style for File Input Button */
input[type="file"] {
  display: inline-block;
  padding: 8px 12px;
  border: 1px solid #ccc; /* Optional: Add a border for better visibility */
  border-radius: 8px; /* Apply border radius */
  font-size: 14px;
  background-color: #f9f9f9; /* Light background for better contrast */
  color: #333; /* Text color */
  cursor: pointer;
  outline: none;
  transition: all 0.3s ease;
}

input[type="file"]::file-selector-button {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 6px 10px;
  background-color: #007bff; /* Blue background */
  color: white; /* White text */
  cursor: pointer;
  transition: all 0.3s ease;
}

input[type="file"]::file-selector-button:hover {
  background-color: #0056b3; /* Darker blue on hover */
}

input[type="file"]::file-selector-button:focus {
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.8); /* Add focus effect */
}




.form-group label {
  font-size: 16px; /* Increase label size */
  font-weight: bold; /* Make label bold */
  color: #0056b3; /* Use a professional blue tone */
  margin-bottom: 8px; /* Add spacing below the label */
}

.form-group input[type="number"] {
  width: 100%; /* Make the input take up full width */
  padding: 10px; /* Add padding for a better click area */
  font-size: 16px; /* Match font size with the label */
  border: 1px solid #ccc; /* Light border for input */
  border-radius: 8px; /* Add rounded corners */
  background-color: #f9f9f9; /* Light background for input */
  color: #333; /* Text color */
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  transition: all 0.3s ease; /* Smooth transition for hover/focus */
}

.form-group input[type="number"]:hover {
  border-color: #007bff; /* Change border color on hover */
}

.form-group input[type="number"]:focus {
  border-color: #0056b3; /* Darker border color on focus */
  outline: none; /* Remove default outline */
  box-shadow: 0 0 6px rgba(0, 123, 255, 0.5); /* Glow effect on focus */
}

.form-group input[type="number"]::placeholder {
  color: #888; /* Lighter text for placeholder */
  font-style: italic; /* Italicize placeholder text */
}

</style>
