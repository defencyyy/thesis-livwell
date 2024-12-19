<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <router-link class="text-start text" :to="`/units/${siteId}`">
          <div class = "back-container">
            <i class="fas fa-arrow-left"></i> Back to Units
          </div>
        </router-link>
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title"><strong>Unit {{ unitDetails ? unitDetails.unit_title : unitId }}</strong></div>
          </div>
          <div
      class="d-flex justify-content-end gap-2 mt-30"
      style="padding-top: 15px"
    >
      <button class="reserve-btn" @click="openReserveModal">Reserve Unit</button>
    </div>
        </div>
        <div v-if="selectedUnit.images && selectedUnit.images.length" id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel">
        <!-- Indicators -->
        <div class="carousel-indicators">
          <button
            v-for="(image, index) in selectedUnit.images"
            :key="index"
            :data-bs-target="'#carouselExampleIndicators'"
            :data-bs-slide-to="index"
            :class="{ active: index === 0 }"
            :aria-current="index === 0 ? 'true' : null"
            :aria-label="'Slide ' + (index + 1)"
          ></button>
        </div>

        <!-- Carousel Items -->
        <div class="carousel-inner">
          <div
            v-for="(image, index) in selectedUnit.images"
            :key="index"
            :class="['carousel-item', { active: index === 0 }]"
          >
            <img :src="image" class="d-block w-100" alt="Unit Picture" style="width: 100%; height: 500px; object-fit: cover;" />
          </div>
        </div>

        <!-- Navigation Controls -->
        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
      <!-- Loading State -->
      <div v-else class="text-center">
        <p>No unit images.</p>
      </div>
      <div class="row mb-3">
        <div class="col-12 d-flex justify-content-between align-items-center">
            <!-- Left Section: Price and Installment Badge -->
            <div class="d-flex align-items-center gap-2">
                <span class="property-price">₱ {{ selectedUnit.price }}</span>
            </div>
            <!-- Right Section: Icons and Details -->
            <div class="d-flex align-items-center gap-3">
                <div class="d-flex align-items-center gap-1">
                    <i class="fa-solid fa-bed"></i>
                    <span>{{ selectedUnit.bedroom }}</span>
                </div>
                <div class="d-flex align-items-center gap-1">
                  <i class="fa-solid fa-bath"></i>
                    <span>{{ selectedUnit.bathroom }}</span>
                </div>
                <div class="d-flex align-items-center gap-1">
                    <i class="bi bi-arrows-fullscreen"></i>
                    <span>{{ selectedUnit.floor_area }}m<sup>2</sup></span>
                </div>
                <span class="text-muted">Studio Type</span>
            </div>
        </div>
      </div>
      <div class="line mb-4"></div>
      <div class="col-12 text-center mb-3 text-center">
            <h5 class="property-header">Details</h5>
      </div>
      <div class="row ps-5">
        <!-- Column 1 -->
        <div class="col-md-4">
            <ul class="list-unstyled mb-0">
              <li><strong>Balcony:</strong> {{ selectedUnit.balcony }} </li>
              <li><strong>Floor Area (m²):</strong> {{ selectedUnit.floor_area }}m<sup>2</sup></li>
              <li><strong>View:</strong> {{ selectedUnit.view }}</li>
            </ul>
        </div>
        <!-- Column 2 -->
        <div class="col-md-4">
            <ul class="list-unstyled mb-0">
                <li><strong>Unit/Floor Number:</strong> {{ selectedUnit.floor }}</li>
                <li><strong>Build (Year):</strong> {{ siteYear }}</li>
            </ul>
        </div>
        <!-- Column 3 -->
        <div class="col-md-4">
            <ul class="list-unstyled mb-0">
              <li><strong>Baths:</strong> {{ selectedUnit.bathroom }}</li>
              <li><strong>Bedrooms:</strong> {{ selectedUnit.bedroom }}</li>
            </ul>
        </div>
      </div>
      <br>
      <hr>
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
          <div v-if="selectedPaymentPlan === 'Deferred Payment'">
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
                  <span class="value">₱{{ spotDownpayment.toFixed(2) }}</span>
                </div>
                <hr class="separator">
                <div class="summary-item">
                  <span class="label">Spread Downpayment:</span>
                  <span class="value">₱{{ spreadDownpayment.toFixed(2) }}</span>
                </div>
                <hr class="separator">
                <div class="summary-item highlight">
                  <span class="label">Monthly Payment:</span>
                  <span class="value">₱{{ payablePerMonth.toFixed(2) }} / month for {{ payableMonths }} months</span>
                </div>
                <hr class="separator">
                <div class="summary-item">
                  <span class="label">Balance Upon Turnover:</span>
                  <span class="value">₱{{ balanceUponTurnover.toFixed(2) }}</span>
                </div>
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
          <div class="detailed-schedule">
            <table class="payment-table">
              <thead>
                <tr>
                  <th colspan="3"><strong>Payment Schedule</strong></th> <!-- Group Header -->
                </tr>
              </thead>
              <tbody>
                <!-- Spot and Spread Downpayments Section -->
                <tr>
                  <td colspan="3"><strong>Initial Payments</strong></td> <!-- Heading for initial payments -->
                </tr>
                <tr>
                  <td>Spot Downpayment</td>
                  <td class="amount-column highlight">₱{{ spotDownpayment.toFixed(2) }}</td>
                  <td class="amount-column">{{ spotDueDate }}</td> <!-- Spot due date -->
                </tr>
                <tr>
                  <td>Spread Downpayment</td>
                  <td class="amount-column highlight">₱{{ spreadDownpayment.toFixed(2) }}</td>
                  <td class="amount-column">{{ spreadDueDate }}</td> <!-- Spread due date -->
                </tr>

                <!-- Monthly Payments Section -->
                <tr>
                  <td colspan="3"><strong>Monthly Payments</strong></td> <!-- Heading for monthly payments -->
                </tr>
                <tr v-for="month in payableMonths" :key="month">
                  <td>Month {{ month }} Payment</td>
                  <td class="amount-column">₱{{ payablePerMonth.toFixed(2) }}</td>
                  <td class="amount-column">{{ getPaymentDueDate(month) }}</td> <!-- Specific due date for each month -->
                </tr>

                <!-- Balance Upon Turnover Section -->
                <tr>
                  <td colspan="3"><strong>Balance Upon Turnover</strong></td> <!-- Heading for balance -->
                </tr>
                <tr>
                  <td>Balance Upon Turnover</td>
                  <td class="amount-column highlight">₱{{ balanceUponTurnover.toFixed(2) }}</td>
                  <td class="amount-column">{{ turnoverDueDate }}</td> <!-- Balance turnover due date -->
                </tr>
              </tbody>
            </table>
          </div>


          </div>
        </div>
          <div v-if="selectedPaymentPlan === 'Spot Cash'">
          <div class="title-wrapper">
            <div class="title-left">
              <div class="title-icon"></div>
              <div class="edit-title"><strong>Payment Schedule Summary</strong></div>
            </div>
          </div>

          <div class="payment-container">
            <div class="detailed-schedule">
              <table class="payment-table">
                <thead>
                  <tr>
                    <th>Payment Type</th>
                    <th>Amount (₱)</th>
                    <th>Due Date</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Spot Cash</td>
                    <td>₱{{ totalAmountPayable }}</td>
                    <td>{{ dueDate }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        </div>
         <b-modal
        v-model="showSuccessMessage"
        title="Reservation Submitted"
        @hide="closePopup"
        centered
        hide-footer
        :visible="successMessage"
        >
          <p>{{ successMessage }}</p>
          <div class = "buttons-container">
            <button @click="closePopup" class="btn btn-primary">OK</button>
          </div>
      </b-modal>
          <!-- Reserve Unit Modal -->
      <b-modal
        v-model="isReserveModalVisible"
        @hide="closeReserveModal"
        hide-footer
        title="Reserve Unit"
        centered
      >
        <form @submit.prevent="submitReservation" style="margin-left: -25px;">
          <!-- Customer Name Dropdown -->
          <div class="form-group">
            <label for="customerName">Customer Name</label>
            <select
              v-model="reservationForm.customerName"
              id="customerName"
              class="form-select"
              style="margin-left: 1px;"
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
              class="form-control"
              required
            />
          </div>
          <!-- Payment Details -->
          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label for="paymentAmount">Payment Amount</label>
                <input
                  type="number"
                  v-model="reservationForm.paymentAmount"
                  id="paymentAmount"
                  class="form-control"
                  placeholder="Enter payment amount"
                  required
                />
              </div>
            </div>
            <div class="col-md-6">
              <div class="form-group">
                <label for="paymentMethod">Payment Method</label>
                <select
                  v-model="reservationForm.paymentMethod"
                  id="paymentMethod"
                  class="form-select"
                  required
                >
                  <option value="bank_transfer">Bank Transfer</option>
                  <option value="cash">Cash</option>
                  <option value="online_payment">Online Payment</option>
                </select>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label for="paymentDate">Date of Payment</label>
                <input
                  type="date"
                  v-model="reservationForm.paymentDate"
                  id="paymentDate"
                  class="form-control"
                  required
                />
              </div>
            </div>
            <div class="col-md-6" v-if="reservationForm.paymentMethod !== 'cash'">
              <div class="form-group">
                <label for="paymentReference">Payment Reference Number</label>
                <input
                  type="text"
                  v-model="reservationForm.paymentReference"
                  id="paymentReference"
                  class="form-control"
                  placeholder="Enter reference number"
                  required
                />
              </div>
            </div>
          </div>
          <!-- Submit Button -->
          <div
            class="d-flex justify-content-end gap-2 mt-3"
            style="padding-top: 15px"
          >
          <button type="submit" class="btn-add">
              Submit Reservation
          </button>
          <button @click="closeReserveModal" class="btn-cancel">Cancel</button>
          </div>
        </form>
        <!-- Error Message Modal -->
        <b-modal 
          v-model="isErrorModalVisible" 
          hide-footer 
          title="Error"
          @hide="handleErrorModalClose"
        >
          <p>{{ errorMessage }}</p>
          <div class="button-container">
            <button @click="closeErrorModal" class="btn-cancel-right">Close</button>
          </div>
        </b-modal>
        </b-modal>
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
      siteId:null,
      siteName: "",
      siteYear: "",
      isModalVisible: false,
      selectedUnit: {
        images: null, // Initially null
      },
      customers: [],
      isReserveModalVisible: false,
      reservationForm: {
        customerName: "",
        paymentAmount: "",
        paymentMethod: "",
        paymentDate: "",
        paymentReference: "",
        file: null, // This will hold the file
      },
      successMessage: "", // Success message
      errorMessage: "", // Error message
      isErrorModalVisible: false, // To control modal visibility
      showSuccessMessage: false, // Control the visibility of the success message

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
      reservationDate: new Date().toISOString().split('T')[0], // Default to today's date
      dueDate: null,
      spotDueDate: null,
    spreadDueDate: null,
    turnoverDueDate: null,
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
    this.fetchCustomers();
  },
  methods: {
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
    this.siteId = this.selectedUnit.site.id;
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
   calculateDueDate() {
  const reservationDate = new Date(this.reservationDate);

  if (this.selectedPaymentPlan === 'Spot Payment') {
    // For Spot Payment, add 30 days
    reservationDate.setDate(reservationDate.getDate() + 30);
  } else if (this.selectedPaymentPlan === 'Deferred Payment') {
    // For Deferred Payment, you could adjust the logic (e.g., add a different amount of days or use other criteria)
    const spotDate = new Date(reservationDate);
    spotDate.setDate(spotDate.getDate() + 30);
    this.spotDueDate = spotDate.toISOString().split('T')[0];

    // Spread due date: Due 60 days after reservation
    const spreadDate = new Date(reservationDate);
    spreadDate.setDate(spreadDate.getDate() + 60);
    this.spreadDueDate = spreadDate.toISOString().split('T')[0];

    // Balance upon turnover: Due on turnover date (or can be custom)
    const turnoverDate = new Date(reservationDate);
    turnoverDate.setFullYear(turnoverDate.getFullYear() + 1); // For example, turnover 1 year later
    this.turnoverDueDate = turnoverDate.toISOString().split('T')[0];  }
  // You can add more conditions for other payment plans if necessary

  this.dueDate = reservationDate.toISOString().split('T')[0]; // Format as YYYY-MM-DD
    },
getPaymentDueDate(month) {
    const reservationDate = new Date(this.reservationDate);
    const paymentDate = new Date(reservationDate);
    paymentDate.setMonth(paymentDate.getMonth() + month);
    return paymentDate.toISOString().split('T')[0];
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
      this.calculateDueDate(); // Call this whenever payment details update

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
    async submitReservation() {
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
        this.errorMessage ="All fields are required except the payment reference (if payment method is 'cash').";
        this.isErrorModalVisible = true;
        return;
      }
      if (this.reservationForm.paymentAmount < this.selectedUnit.reservation_fee ) {
        this.errorMessage = "Payment Amount Insufficient";
        this.isErrorModalVisible = true;
        return;
      }
      const data = {
        customer_name: this.reservationForm.customerName,
        site_id: parseInt(this.siteId, 10), // Convert to integer
        unit_id: this.selectedUnit.id,
        commission:this.selectedUnit.commission,
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
     // Trigger the error modal
  showErrorModal(message) {
    this.errorMessage = message; // Set the error message
    this.isErrorModalVisible = true; // Open the error modal
  },
  // Handle closing of the modal
  handleErrorModalClose() {
    this.isErrorModalVisible = false; // Ensure modal closes
    this.errorMessage = ''; // Clear the error message
  },
  closeErrorModal() {
    this.handleErrorModalClose();
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
  height: 640px;
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
.carousel-inner img {
  max-height: 400px; /* Adjust as needed */
  object-fit: cover;
}

.carousel-control-prev:hover,
.carousel-control-next:hover {
  background-color: transparent; /* Remove the background color */
  color: inherit; /* Remove the default text color change */
  border: none; /* Remove any border if present */
}

.property-price {
  font-size: 2rem;
  color: black;
}

.property-price1 {
  margin-top: 5px; /* Adjust spacing as needed */
  font-size: 1.5rem;
  font-weight: bold;
  text-align: left;
}

.price-header {
  font-weight: bold;
  color: #6c757d; /* Example muted color */
}

.property-header {
  font-weight: bold;
  font-size: 1.5rem;
}

.row.mb-3.ps-5 .d-flex {
  gap: 30px; /* Adjust as needed for closer spacing */
}

</style>
