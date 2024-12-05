<template>
  <div class="available-units-page">
    <!-- <SideNav /> -->
    <div class="content">
      <router-link class="text-start" to="/broker/affiliated-units">
        <i class="fas fa-arrow-left"></i> Back to Units
      </router-link>

      <h2 class="display-5 fw-bolder text-capitalize">
        Available Units for Site: {{ siteName }}
      </h2>
      <!-- filter for units -->

     
    <div class="filters">
      <label>View:</label>
      <select v-model="selectedView">
        <option value="all">All</option>
        <option value="north">North</option>
        <option value="south">South</option>
        <option value="east">East</option>
        <option value="west">West</option>
      </select>

      <label>Balcony:</label>
      <select v-model="selectedBalcony">
        <option value="all">All</option>
        <option value="has">Has Balcony</option>
        <option value="no">No Balcony</option>
      </select>

       <label>Floor:</label>
  <select v-model="selectedFloor">
    <option value="all">All</option>
    <option v-for="floor in availableFloors" :key="floor" :value="floor">{{ floor }}</option>
  </select>

    </div>


 <div v-if="filteredUnits.length">
  <div class="units-container">
    <div
      v-for="unit in filteredUnits"
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
      <div
        v-if="successMessage"
        class="success-message"
        :class="{ show: showSuccessMessage }"
      >
        <p>{{ successMessage }}</p>
        <button @click="closePopup" class="ok-btn">OK</button>
      </div>

      <!-- Unit Details Modal -->
      <div v-if="isModalVisible" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <!-- Image Section -->
          <div v-if="selectedUnit.images.length" class="image-gallery">
            <img
              v-for="(image, index) in selectedUnit.images"
              :key="index"
              :src="image"
              alt="Unit Picture"
              class="unit-picture"
            />
          </div>
          <p>
            P{{ selectedUnit.price }} Bedroom:
            {{ selectedUnit.bedroom }} Bathroom:
            {{ selectedUnit.bathroom }} Floor Area:
            {{ selectedUnit.floor_area }}
          </p>
          <hr />
          <center>Details</center>
          <p>
            Unit/Floor Number: {{ selectedUnit.floor }} Balcony:
            {{ selectedUnit.balcony }} Built(Year):{{ siteYear }}
          </p>
          <p>
            Baths:{{ selectedUnit.bathroom }} Bedrooms:
            {{ selectedUnit.bedroom }} Floor area(m<sup>2</sup>):{{
              selectedUnit.floor_area
            }}
          </p>
          <p>View: {{ selectedUnit.view }}</p>
          <hr />

          <!-- Unit Details -->
          <div class="unit-details">
            <p>
              <strong>Price:</strong> ₱{{ selectedUnit.price }} |
              <strong>Bedrooms:</strong> {{ selectedUnit.bedroom }} |
              <strong>Bathrooms:</strong> {{ selectedUnit.bathroom }} |
              <strong>Floor Area:</strong> {{ selectedUnit.floor_area }}m<sup
                >2</sup
              >
            </p>
            <hr />
            <h3 class="details-heading">Details</h3>
            <p>
              <strong>Unit/Floor Number:</strong> {{ selectedUnit.floor }} |
              <strong>Balcony:</strong> {{ selectedUnit.balcony }} |
              <strong>Built (Year):</strong> {{ siteYear }}
            </p>
            <p><strong>View:</strong> {{ selectedUnit.view }}</p>
            <hr />
          </div>

          <!-- Payment Plan Section -->
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
            <label for="spotDiscount">Spot Discount</label>
            <input
              type="number"
              id="spotDiscount"
              v-model="spotCashDiscount"
              @input="updatePaymentDetails"
              class="form-control"
              min="0"
              max="100"
            />
          </div>
          <p><strong>Spot Discount:</strong> ₱{{ spotDiscount }}</p>

          <p>
            <strong>Unit Price after Spot Discount:</strong> ₱{{
              unitPriceAfterSpotDiscount
            }}
          </p>

          <!-- TLP Discount -->
          <div class="form-group">
            <label for="tlpDiscount">TLP Discount (Optional)</label>
            <input
              type="number"
              id="tlpDiscount"
              v-model="tlpDiscount"
              @input="updatePaymentDetails"
              class="form-control"
              min="0"
              max="100"
            />
          </div>
          <p><strong>TLP Discount:</strong> ₱{{ tlpDiscountAmount }}</p>

          <!-- Net Unit Price -->
          <p><strong>Net Unit Price:</strong> ₱{{ netUnitPrice }}</p>

          <!-- Other Charges -->
          <div class="form-group">
            <label for="otherChargesPercentage">Other Charges (%)</label>
            <input
              type="number"
              id="otherChargesPercentage"
              v-model="otherChargesPercentage"
              @input="updatePaymentDetails"
              class="form-control"
              min="0"
              step="0.1"
            />
          </div>
          <p><strong>Other Charges:</strong> ₱{{ otherCharges }}</p>

          <!-- VAT Calculation -->
          <p v-if="netUnitPrice > 3600000">
            <strong>VAT (12%):</strong> ₱{{ vatAmount }}
          </p>

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

          <p v-if="selectedPaymentPlan === 'Deffered Payment'">
            <strong>Spot Downpayment:</strong> ₱{{ spotDownpayment }}
          </p>

          <!-- Reservation Fee -->
          <p><strong>Reservation Fee:</strong> ₱{{ this.reservationFee }}</p>
          <p v-if="selectedPaymentPlan === 'Spot Cash'">
            <strong>Net Full Payment:</strong> ₱{{ netFullPayment }}
          </p>

          <!-- Net Downpayment -->
          <p v-if="selectedPaymentPlan === 'Deffered Payment'">
            <strong>Net Downpayment:</strong> ₱{{ netDownpayment }}
          </p>

          <div v-if="selectedPaymentPlan === 'Deffered Payment'">
            <!-- Spread Downpayment -->
            <div class="form-group">
              <label for="spreadDownpayment">Spread Downpayment</label>
              <select
                v-model="spreadDownpaymentPercentage"
                id="spreadDownpayment"
                @change="updatePaymentDetails"
                required
              >
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
              <input
                type="number"
                v-model="payableMonths"
                id="months"
                @input="updatePaymentDetails"
                min="1"
                step="1"
                required
              />
            </div>
            <p><strong>Payable Per Month:</strong> ₱{{ payablePerMonth }}</p>
            <!-- Balance Upon Turnover -->
            <p>
              <strong>Balance Upon Turnover:</strong> ₱{{ balanceUponTurnover }}
            </p>
            <h3>Payment Schedule Summary</h3>

            <!-- Payment Summary -->
            <div class="payment-summary">
              <p>
                <strong>Spot Downpayment:</strong> ₱{{
                  spotDownpayment.toFixed(2)
                }}
              </p>
              <p>
                <strong>Spread Downpayment:</strong> ₱{{
                  spreadDownpayment.toFixed(2)
                }}
              </p>
              <p>
                <strong>Monthly Payment:</strong> ₱{{
                  payablePerMonth.toFixed(2)
                }}
                / month for {{ payableMonths }} months
              </p>
              <p>
                <strong>Balance Upon Turnover:</strong> ₱{{
                  balanceUponTurnover.toFixed(2)
                }}
              </p>
            </div>
          </div>
          <!-- Button Container -->
          <div class="button-container">
            <button class="reserve-btn" @click="openReserveModal">
              Reserve Unit
            </button>
            <button class="schedule-btn" @click="scheduleVisit">
              Schedule Visit
            </button>
          </div>
        </div>
      </div>

      <!-- Reserve Unit Modal -->
      <div
        v-if="isReserveModalVisible"
        class="modal-overlay"
        @click="closeReserveModal"
      >
        <div class="modal-content" @click.stop>
          <h3>Reserve Unit</h3>
          <!-- Success Message Pop-up -->
          <form @submit.prevent="submitReservation">
            <!-- Customer Name Dropdown -->
            <div class="form-group">
              <label for="customerName">Customer Name</label>
              <select
                v-model="reservationForm.customerName"
                id="customerName"
                required
              >
                <option value="" disabled selected>Select Customer</option>
                <option
                  v-for="customer in customers"
                  :key="customer.id"
                  :value="customer.id"
                >
                  {{ customer.name }} ({{ customer.customer_code }})
                </option>
              </select>
            </div>
            <!-- File Upload -->
            <div class="form-group">
              <label for="fileUpload">Upload File (Required)</label>
              <input
                type="file"
                @change="handleFileUpload"
                id="fileUpload"
                required
              />
            </div>
            <!-- Payment Amount -->
            <div class="form-group">
              <label for="paymentAmount">Payment Amount</label>
              <input
                type="number"
                v-model="reservationForm.paymentAmount"
                id="paymentAmount"
                required
              />
            </div>
            <!-- Payment Method -->
            <div class="form-group">
              <label for="paymentMethod">Payment Method</label>
              <select
                v-model="reservationForm.paymentMethod"
                id="paymentMethod"
                required
              >
                <option value="bank_transfer">Bank Transfer</option>
                <option value="cash">Cash</option>
                <option value="online_payment">Online Payment</option>
              </select>
            </div>
            <!-- Payment Date -->
            <div class="form-group">
              <label for="paymentDate">Date of Payment</label>
              <input
                type="date"
                v-model="reservationForm.paymentDate"
                id="paymentDate"
                required
              />
            </div>
            <!-- Payment Reference (only if payment method is not cash) -->
            <div
              class="form-group"
              v-if="reservationForm.paymentMethod !== 'cash'"
            >
              <label for="paymentReference">Payment Reference Number</label>
              <input
                type="text"
                v-model="reservationForm.paymentReference"
                id="paymentReference"
                required
              />
            </div>
            <!-- Submit Button -->
            <div class="form-group">
              <button type="submit" class="submit-btn">
                Submit Reservation
              </button>
            </div>
          </form>
          <div v-if="errorMessage" class="modal-overlay">
            <p>{{ errorMessage }}</p>
            <button @click="closeModal">Close</button>
          </div>
          <button @click="closeReserveModal" class="cancel-btn">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//import SideNav from "@/components/SideNav.vue";
import axios from "axios";

export default {
  name: "AvailableUnits",
  components: {
    // SideNav,
  },
  data() {
    return {
      siteId: this.$route.params.siteId,
      units: [],
      siteName: "",
      siteYear: "",
      isModalVisible: false,
      selectedUnit: null,
      isReserveModalVisible: false,
      reservationForm: {
        customerName: "",
        paymentAmount: "",
        paymentMethod: "",
        paymentDate: "",
        paymentReference: "",
        file: null, // This will hold the file
      },
      customers: [],
      successMessage: "", // Success message
      errorMessage: "", // Error message
      showSuccessMessage: false, // Control the visibility of the success message

      // Payment Scheme Data
      selectedPaymentPlan: "Spot Cash", // Default payment plan
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
      vat: 0,
      selectedView: 'all',      // Default to "all"
      selectedBalcony: 'all',   // Default to "all"
      selectedFloor:'all',
    };
  },

  mounted() {
    this.fetchAvailableUnits();
    this.fetchSiteName();
    this.fetchCustomers();

    // Call updatePaymentDetails to show the default payment details
    this.updatePaymentDetails();
  },
  computed: {
  availableFloors() {
    // Get unique floor values from available units
    const floors = this.units.map(unit => unit.floor);
    return [...new Set(floors)].sort(); // Remove duplicates and sort them
  },
  filteredUnits() {
    return this.units.filter((unit) => {
      const viewMatch =
        this.selectedView === 'all' ||
        unit.view.toLowerCase() === this.selectedView;

      const balconyMatch =
        this.selectedBalcony === 'all' ||
        (this.selectedBalcony === 'has' && unit.balcony.toLowerCase() !== 'no balcony') ||
        (this.selectedBalcony === 'no' && unit.balcony.toLowerCase() === 'no balcony');
      const floorMatch =
        this.selectedFloor === 'all' || unit.floor === this.selectedFloor;

      return viewMatch && balconyMatch && floorMatch;
    });
  },
},

  methods: {
    async fetchAvailableUnits() {
      try {
        const response = await axios.get(
          `http://localhost:8000/units/available/?site_id=${this.siteId}`
        );
        this.units = response.data.units.map((unit) => ({
          ...unit,
          company_id: unit.company_id,
        }));
      } catch (error) {
        console.error("Error fetching available units:", error);
      }
    },

    async fetchSiteName() {
      try {
        const response = await axios.get(
          `http://localhost:8000/sites/${this.siteId}`
        );
        this.siteName = response.data.name;
        this.siteYear = response.data.created_year;
      } catch (error) {
        console.error("Error fetching site name:", error);
      }
    },

    async fetchCustomers() {
      const brokerId = this.$store.getters.getUserId; // Use Vuex getter to get broker ID
      if (!brokerId) {
        this.errorMessage = "Broker ID not found. Please log in again.";
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:8000/customers/broker/${brokerId}/?include_sales=false`
        );
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
      this.spotCashDiscount = this.selectedUnit.spot_discount;
      this.tlpDiscount = this.selectedUnit.TLP_Discount;
      this.otherChargesPercentage = this.selectedUnit.other_charges;
      this.reservationFee = this.selectedUnit.reservation_fee;
      this.vat = this.selectedUnit.vat_percent;
      // Recalculate payment details when the unit is selected
      this.updatePaymentDetails();
    },

    closeModal() {
      this.isModalVisible = false;
      this.errorMessage = ""; // Clear the error message and close the modal
    },

    openReserveModal() {
      this.isReserveModalVisible = true;
    },

    closeReserveModal() {
      this.isReserveModalVisible = false;
      this.reservationForm = {
        customerName: "",
        paymentAmount: "",
        paymentMethod: "",
        paymentDate: "",
        paymentReference: "",
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

    async submitReservation() {
      this.errorMessage = null;
      // Check if all required fields are filled, including the file
      if (
        !this.reservationForm.customerName ||
        !this.reservationForm.paymentAmount ||
        !this.reservationForm.paymentMethod ||
        !this.reservationForm.paymentDate ||
        !this.reservationForm.file ||
        (this.reservationForm.paymentMethod !== "cash" &&
          !this.reservationForm.paymentReference)
      ) {
        this.errorMessage =
          "All fields are required except the payment reference (if payment method is 'cash').";
        return;
      }
      if (this.reservationForm.paymentAmount < this.reservationFee) {
        this.errorMessage = "Payment Amount Insufficient";
        return;
      }
      const data = {
        customer_name: this.reservationForm.customerName,
        site_id: parseInt(this.siteId, 10), // Convert to integer
        unit_id: this.selectedUnit.id,
        broker_id: parseInt(this.$store.getters.getUserId, 10), // Use Vuex getter for broker_id
        company_id: this.selectedUnit.company_id, // Ensure this is correctly passed
        payment_amount: this.reservationForm.paymentAmount,
        payment_method: this.reservationForm.paymentMethod,
        payment_reference: this.reservationForm.paymentReference || null, // Payment reference is optional if payment is "cash"
        reservation_file: this.reservationForm.file
          ? this.reservationForm.file.name
          : null, // Ensure file is present
      };

      try {
        const response = await axios.post(
          "http://localhost:8000/reserve-unit/",
          data,
          {
            headers: {
              "Content-Type": "application/json", // Sending JSON data
            },
          }
        );

        // Set the success message to display in the pop-up
        this.successMessage = "Reservation submitted successfully!";

        setTimeout(() => {
          this.showSuccessMessage = true; // Trigger to show success message
        }, 500);

        // Close the modal after success
        this.closeReserveModal();

        // Reset the reservation form
        this.reservationForm = {
          customerName: "",
          paymentAmount: "",
          paymentMethod: "",
          paymentDate: "",
          paymentReference: "",
          file: null,
        };

        console.log("Sale created:", response.data);
      } catch (error) {
        console.error("Error submitting reservation:", error);
        this.errorMessage =
          "There was an error submitting the reservation. Please try again."; // Display error message
      }
    },

    closePopup() {
      this.successMessage = ""; // Hide the success message pop-up
      this.$router.push({ name: "AffiliatedUnits" }); // Redirect to the 'AffiliatedUnits' page
    },
  },
};
</script>

<style scoped>
.content {
  border: 2px solid #ccc;
  border-radius: 10px;
  margin: 20px 20px 20px 20px;
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.2);
  background-color: rgb(223, 255, 223);
}

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
  border-radius: 8px;
}
.unit-card:hover {
  background-color: #e8e8e8;
  transition: ease 0.3s;
}

/* .unit-picture {
  max-width: 100%;
  height: auto;
  margin-bottom: 10px;
} */

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

/* Modal Content */
.modal-content {
  background: #fff;
  width: 90%;
  max-width: 700px;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  overflow-y: auto;
  max-height: 90vh;
}

.success-message {
  position: fixed; /* Position it relative to the screen */
  top: 50%; /* Center the message */
  left: 50%;
  transform: translate(-50%, -50%); /* Adjust to truly center */
  background-color: rgba(
    0,
    128,
    0,
    0.8
  ); /* Green background, slightly transparent */
  color: white;
  padding: 20px;
  border-radius: 5px;
  font-size: 18px;
  z-index: 1100; /* Make sure it's on top of the modal */
  display: none; /* Initially hidden */
}

.success-message.show {
  display: block; /* Show the success message when it's needed */
}

/* Image Gallery */
.image-gallery {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.unit-picture {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

/* Unit Details */
.unit-details {
  margin-bottom: 20px;
}

.details-heading {
  text-align: center;
  font-weight: bold;
  margin: 10px 0;
}

/* Form Group */
.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

/* Dropdown Styling */
.select-field {
  width: 100%;
  padding: 8px;
  background-color: #dadada; /* White background */
  color: #000000; /* Black text */
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;

  cursor: pointer;
}

.select-field:focus {
  outline: none;
  border-color: #007bff; /* Optional: blue border on focus */
  box-shadow: 0 0 3px rgba(0, 123, 255, 0.5);
}

.select-field option {
  background-color: #fff; /* White background for options */
  color: #000; /* Black text for options */
}

/* Payment Plan Section */
.payment-plan {
  margin-top: 20px;
}

.plan-heading {
  font-size: 18px;
  color: #007bff;
  margin-bottom: 10px;
}

/* Button Container */
.button-container {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

button {
  padding: 10px 15px;
  font-size: 14px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}
button:hover {
  background-color: #0056b3;
}

.reserve-btn {
  background-color: #28a745;
  color: #fff;
}

.reserve-btn:hover {
  background-color: #218838;
}

.schedule-btn {
  background-color: #007bff;
  color: #fff;
}

.schedule-btn:hover {
  background-color: #0056b3;
}

.filters {
  display: flex;
  align-items: center;   /* Align vertically */
  gap: 20px;             /* Add space between elements */
}

.filters label {
  margin-right: 5px;     /* Small space between label and select */
}

.filters select {
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Style the list for better appearance */
.unit-list {
  list-style: none;      /* Remove default bullets */
  padding: 0;
}

.unit-list li {
  padding: 10px;
  border-bottom: 1px solid #ddd; /* Add separator between units */
}
</style>
