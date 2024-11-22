<template>
  <div class="available-units-page">
    <SideNav />
    <div class="content">
      <h2>Available Units for Site: {{ siteName }}</h2>
      <div v-if="units.length">
        <div class="units-container">
          <div 
            v-for="unit in units" 
            :key="unit.id" 
            class="unit-card" 
            @click="showUnitDetails(unit)"
          >
            <p>{{ unit.unit_title }}</p>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No units available for this site.</p>
      </div>

      <!-- Success Message Pop-up -->
      <div v-if="successMessage" class="popup-overlay">
        <div class="popup-content">
          <p>{{ successMessage }}</p>
          <button @click="closePopup" class="ok-btn">OK</button>
        </div>
      </div>

      <!-- Unit Details Modal -->
      <div v-if="isModalVisible" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div v-if="selectedUnit.images.length">
            <img v-for="(image, index) in selectedUnit.images" 
                 :key="index" 
                 :src="image" 
                 alt="Unit Picture" 
                 class="unit-picture" />
          </div>
          <p>P{{ selectedUnit.price }} Bedroom: {{ selectedUnit.bedroom }} Bathroom: {{ selectedUnit.bathroom }} Floor Area: {{ selectedUnit.floor_area }}</p>
          <hr>
          <center>Details</center>
          <p>Unit/Floor Number: {{ selectedUnit.floor }} Balcony: {{ selectedUnit.balcony }} Built(Year):{{ siteYear }} </p>
          <p>Baths:{{ selectedUnit.bathroom }} Bedrooms: {{ selectedUnit.bedroom }} Floor area(m<sup>2</sup>):{{ selectedUnit.floor_area }} </p>
          <p>View: {{ selectedUnit.view }} </p>
          <hr>

          <!-- Payment Plan Section -->
          <div class="form-group">
            <label for="paymentPlan">Payment Plan</label>
            <select v-model="selectedPaymentPlan" id="paymentPlan" required>
              <option value="spot_cash">Spot Cash</option>
              <option value="in_house_financing">Deffered Payment</option>
            </select>
          </div>

            <p><strong>Unit Price:</strong> ₱{{ unitPrice }}</p>

            <!-- Spot Discount -->
            <div class="form-group">
              <label for="spotDiscount">Spot Discount</label>
              <select v-model="spotCashDiscount" id="spotDiscount" @change="updatePaymentDetails">
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
              <select v-model="tlpDiscount" id="tlpDiscount" @change="updatePaymentDetails">
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
              <select v-model="otherChargesPercentage" id="otherCharges" @change="updatePaymentDetails">
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
            <div  v-if="selectedPaymentPlan === 'in_house_financing'" class="form-group">
            <label for="spotDownpayment">Spot Downpayment</label>
            <input 
              type="number" 
              id="spotDownpayment" 
              v-model="spotDownpaymentPercentage" 
              @input="updatePaymentDetails"
              min="0"
              step="5"
              placeholder="Enter downpayment percentage"
            />
          </div>

            <p  v-if="selectedPaymentPlan === 'in_house_financing'"><strong>Spot Downpayment:</strong> ₱{{ spotDownpayment }}</p>

            <!-- Reservation Fee -->
            <p><strong>Reservation Fee:</strong> ₱{{ reservationFee }}</p>
            <p v-if="selectedPaymentPlan === 'spot_cash'"><strong>Net Full Payment:</strong> ₱{{ netFullPayment }}</p>


            <!-- Net Downpayment -->
            <p v-if="selectedPaymentPlan === 'in_house_financing'"><strong>Net Downpayment:</strong> ₱{{ netDownpayment }}</p>

            <div v-if="selectedPaymentPlan === 'in_house_financing'">
            <!-- Spread Downpayment -->
            <div class="form-group">
              <label for="spreadDownpayment">Spread Downpayment</label>
              <select v-model="spreadDownpaymentPercentage" id="spreadDownpayment" @change="updatePaymentDetails">
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
              <input type="number" v-model="payableMonths" id="months" @input="updatePaymentDetails" min="1" step="1" />
            </div>
            <p><strong>Payable Per Month:</strong> ₱{{ payablePerMonth }}</p>


            <!-- Balance Upon Turnover -->
            <p><strong>Balance Upon Turnover:</strong> ₱{{ balanceUponTurnover }}</p>
          </div>


          <div class="button-container">
            <button class="reserve-btn" @click="openReserveModal">Reserve Unit</button>
            <button class="schedule-btn" @click="scheduleVisit">Schedule Visit</button>
          </div>
        </div>
      </div>
      <!-- Reserve Unit Modal -->
      <div v-if="isReserveModalVisible" class="modal-overlay" @click="closeReserveModal">
        <div class="modal-content" @click.stop>
          <h3>Reserve Unit</h3>
          <form @submit.prevent="submitReservation">
            <!-- Customer Name Dropdown -->
            <div class="form-group">
              <label for="customerName">Customer Name</label>
              <select v-model="reservationForm.customerName" id="customerName" required>
                <option value="" disabled selected>Select Customer</option>
                <option v-for="customer in customers" :key="customer.id" :value="customer.id">
                  {{ customer.name }}
                </option>
              </select>
            </div>
            <!-- File Upload -->
            <div class="form-group">
              <label for="fileUpload">Upload File (Required)</label>
              <input type="file" @change="handleFileUpload" id="fileUpload" required />
            </div>
            <!-- Payment Amount -->
            <div class="form-group">
              <label for="paymentAmount">Payment Amount</label>
              <input type="number" v-model="reservationForm.paymentAmount" id="paymentAmount" required />
            </div>
            <!-- Payment Method -->
            <div class="form-group">
              <label for="paymentMethod">Payment Method</label>
              <select v-model="reservationForm.paymentMethod" id="paymentMethod" required>
                <option value="bank_transfer">Bank Transfer</option>
                <option value="cash">Cash</option>
                <option value="online_payment">Online Payment</option>
              </select>
            </div>
            <!-- Payment Date -->
            <div class="form-group">
              <label for="paymentDate">Date of Payment</label>
              <input type="date" v-model="reservationForm.paymentDate" id="paymentDate" required />
            </div>
            <!-- Payment Reference (only if payment method is not cash) -->
            <div class="form-group" v-if="reservationForm.paymentMethod !== 'cash'">
              <label for="paymentReference">Payment Reference Number</label>
              <input type="text" v-model="reservationForm.paymentReference" id="paymentReference" required />
            </div>
            <!-- Submit Button -->
            <div class="form-group">
              <button type="submit" class="submit-btn">Submit Reservation</button>
            </div>
          </form>
          <button @click="closeReserveModal" class="cancel-btn">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import SideNav from "@/components/SideNav.vue";
import axios from 'axios';

export default {
  name: "AvailableUnits",
  components: {
    SideNav,
  },
  data() {
    return {
      siteId: this.$route.params.siteId,
      units: [],
      siteName: '',
      siteYear: '',
      isModalVisible: false,
      selectedUnit: null,
      isReserveModalVisible: false,
      reservationForm: {
        customerName: '',
        paymentAmount: '',
        paymentMethod: '',
        paymentDate: '',
        paymentReference: '',
        file: null, // This will hold the file
      },
      customers: [],
      successMessage: '',  // Success message
      errorMessage: '',    // Error message

      // Payment Scheme Data
      selectedPaymentPlan: 'spot_cash', // Default payment plan
      unitPrice: 0, // Example price of the unit
      spotCashDiscount: 0,
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
      payableMonths: 40,
      payablePerMonth: 0,
      balanceUponTurnover: 0,
    };
  },

  mounted() {
    this.fetchAvailableUnits();
    this.fetchSiteName();
    this.fetchCustomers();

    // Call updatePaymentDetails to show the default payment details
    this.updatePaymentDetails();
  },

  methods: {
    async fetchAvailableUnits() {
      try {
        const response = await axios.get(`http://localhost:8000/units/available/?site_id=${this.siteId}`);
        this.units = response.data.units.map(unit => ({
          ...unit,
          company_id: unit.company_id
        }));
      } catch (error) {
        console.error("Error fetching available units:", error);
      }
    },

    async fetchSiteName() {
      try {
        const response = await axios.get(`http://localhost:8000/sites/${this.siteId}`);
        this.siteName = response.data.name;
        this.siteYear = response.data.created_year;
      } catch (error) {
        console.error("Error fetching site name:", error);
      }
    },

    async fetchCustomers() {
      const brokerId = localStorage.getItem("broker_id");
      if (!brokerId) {
        this.errorMessage = "Broker ID not found. Please log in again.";
        return;
      }

      try {
        const response = await fetch(`http://localhost:8000/customers/broker/${brokerId}/?include_sales=false`);
        const data = await response.json();
        if (data && data.customers) {
          this.customers = data.customers;
        } else {
          this.errorMessage = "No customers found.";
        }
      } catch (error) {
        this.errorMessage = "Failed to fetch customer data.";
      }
    },

    showUnitDetails(unit) {
      this.selectedUnit = unit;
      this.unitPrice = unit.price; // Set the price of the selected unit
      this.isModalVisible = true;

      // Recalculate payment details when the unit is selected
      this.updatePaymentDetails();
    },

    closeModal() {
      this.isModalVisible = false;
    },

    openReserveModal() {
      this.isReserveModalVisible = true;
    },

    closeReserveModal() {
      this.isReserveModalVisible = false;
      this.reservationForm = {
        customerName: '',
        paymentAmount: '',
        paymentMethod: '',
        paymentDate: '',
        paymentReference: '',
        file: null,
      };
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.reservationForm.file = file;
      }
    },

    updatePaymentDetails() {
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
      console.log(this.balanceUponTurnover, this.spotDownpaymentPercentage, this.spreadDownpaymentPercentage);
    },

       
    async submitReservation() {
      // Check if all required fields are filled, including the file
      if (!this.reservationForm.customerName || !this.reservationForm.paymentAmount || 
          !this.reservationForm.paymentMethod || !this.reservationForm.paymentDate || 
          !this.reservationForm.file || (this.reservationForm.paymentMethod !== 'cash' && !this.reservationForm.paymentReference)) {
        this.errorMessage = "All fields are required except the payment reference (if payment method is 'cash').";
        return;
      }

      const data = {
        customer_name: this.reservationForm.customerName,
        site_id: parseInt(this.siteId, 10),  // Convert to integer
        unit_id: this.selectedUnit.id,
        broker_id: parseInt(localStorage.getItem("broker_id"), 10),  // Convert to integer
        company_id: this.selectedUnit.company_id,  // Ensure this is correctly passed
        payment_amount: this.reservationForm.paymentAmount,
        payment_method: this.reservationForm.paymentMethod,
        payment_reference: this.reservationForm.paymentReference || null, // Payment reference is optional if payment is "cash"
        reservation_file: this.reservationForm.file ? this.reservationForm.file.name : null // Ensure file is present
      };
      

      try {
        const response = await axios.post('http://localhost:8000/reserve-unit/', data, {
          headers: {
            'Content-Type': 'application/json',  // Sending JSON data
          }
        });

        // Set the success message to display in the pop-up
        this.successMessage = "Reservation submitted successfully!";

        // Close the modal after success
        this.closeReserveModal();

        // Reset the reservation form
        this.reservationForm = {
          customerName: '',
          paymentAmount: '',
          paymentMethod: '',
          paymentDate: '',
          paymentReference: '',
          file: null,
        };

        console.log("Sale created:", response.data);

      } catch (error) {
        console.error("Error submitting reservation:", error);
        this.errorMessage = "There was an error submitting the reservation. Please try again.";  // Display error message
      }
    },

    closePopup() {
      this.successMessage = '';  // Hide the success message pop-up
      this.$router.push({ name: 'AffiliatedUnits' });  // Redirect to the 'AffiliatedUnits' page
    },
  }
};
</script>


<style scoped>
  .popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000; /* Ensure it appears on top of other content */
}

.popup-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  width: 300px; /* Set a fixed width */
}

.ok-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
}

.ok-btn:hover {
  background: #0056b3;
}
.available-units-page {
  display: flex;
  height: 100vh;
}
.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}
.units-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin: 0 auto;
}
.unit-card {
  border: 1px solid #ccc;
  margin: 10px;
  padding: 10px;
  text-align: center;
  cursor: pointer;
}
.unit-picture {
  max-width: 100%;
  height: auto;
  margin-bottom: 10px;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  max-height: 80vh; /* Set max height for the modal */
  overflow-y: auto; /* Allow vertical scrolling if content overflows */
}
.unit-picture {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
}
</style>
