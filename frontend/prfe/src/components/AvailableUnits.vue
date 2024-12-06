<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
    <div class="content">
      <router-link class="text-start" to="/broker/affiliated-units">
        <div class = "back-container">
          <i class="fas fa-arrow-left"></i> Back to Sites
        </div>
      </router-link>

      <div class="title-wrapper">
        <div class="title-left">
          <div class="title-icon"></div>
          <div class="edit-title">Available Units for Site {{ siteName }} </div>
        </div>
      </div>

      <div
          class="card border-0 rounded-1 mx-auto"
          style="max-width: 1100px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 15px;"
      >
    
      <div class = "card-body">
        <div class = "row">
          <!-- Toolbar -->
           <div class = "toolbar">
            <div class = "left-section">
              <label>View </label>
              <select v-model="selectedView" class = "dropdown-select">
              <option value="all">All</option>
              <option value="north">North</option>
              <option value="south">South</option>
              <option value="east">East</option>
              <option value="west">West</option>
            </select>
            <label>Balcony</label>
            <select v-model="selectedBalcony" class = "dropdown-select">
              <option value="all">All</option>
              <option value="has">Has Balcony</option>
              <option value="no">No Balcony</option>
            </select>
            <label>Floor</label>
            <select v-model="selectedFloor" class = "dropdown-select">
              <option value="all">All</option>
              <option v-for="floor in availableFloors" :key="floor" :value="floor">{{ floor }}</option>
            </select>
            <label>Unit Type</label>
            <select v-model="selectedUnitType" class = "dropdown-select">
              <option value="all">All</option>
              <option v-for="unitType in availableUnitTypes" :key="unitType" :value="unitType">{{ unitType }}</option>
            </select>
           </div>
        </div>
      </div>
      </div>
    </div>

    <div v-if = "filteredUnits.length" class = "site-grid">
      <div
      v-for="unit in filteredUnits"
      :key="unit.id"
      class="site-card"
      @click="showUnitDetails(unit)"
      >
        <p>{{ unit.unit_title }}</p>
      </div>
    </div>

    <div v-else>
      <p>No sites with available units.</p>
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
      <b-modal
      id="unitDetailsModal"
      v-model="isModalVisible"
      title="Unit Details"
      hide-footer
      size="lg"
      @hide="closeModal"
    >

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
    <div class="line mb-4"></div>
    <div class="col-12 text-center mb-3 text-center">
      <h5 class="property-header">Payment Plan</h5><br>
    </div>
    <div class="row mb-3 ps-5">
      <div class="col-12 d-flex justify-content-around align-items-center">
        <!-- Left Section: Property Price -->
        <div class="text-center">
          <h5 class="muted price-header">Property Price</h5>
          <p class="property-price1">₱ {{ selectedUnit.price }}</p>
        </div>
        <!-- Right Section: Payment Plan -->
        <div class="text-center1">
          <h5 class="price-header">Payment Plan</h5>
          <select v-model="selectedPaymentPlan" id="paymentPlan" class="form-select mt-2" required>
            <option value="Spot Cash">Spot Cash</option>
            <option value="Deffered Payment">Deffered Payment</option>
          </select>
        </div>

      </div>
    </div>

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
    
    <p class = "description-align"><strong>Spot Discount:</strong> ₱{{ spotDiscount }}</p>
    
    <p class = "description-align">
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

    <p class = "description-align"><strong>TLP Discount:</strong> ₱{{ tlpDiscountAmount }}</p>

    <!-- Net Unit Price -->
    <p class = "description-align"><strong>Net Unit Price:</strong> ₱{{ netUnitPrice }}</p>

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
    
    <p class = "description-align"><strong>Other Charges:</strong> ₱{{ otherCharges }}</p>

    <!-- VAT Calculation -->
    <p v-if="netUnitPrice > 3600000">
      <strong>VAT (12%):</strong> ₱{{ vatAmount }}
    </p>

    <!-- Total Amount Payable -->
    <p class = "description-align">
      <strong>Total Amount Payable:</strong> ₱{{ totalAmountPayable }}
    </p>

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

    <p v-if="selectedPaymentPlan === 'Deffered Payment'" class = "description-align">
      <strong>Spot Downpayment:</strong> ₱{{ spotDownpayment }}
    </p>

    <!-- Reservation Fee -->
    <p class = "description-align"><strong>Reservation Fee:</strong> ₱{{ this.reservationFee }}</p>
    <p v-if="selectedPaymentPlan === 'Spot Cash'" class = "description-align">
      <strong>Net Full Payment:</strong> ₱{{ netFullPayment }}
    </p>

    <!-- Net Downpayment -->
    <p v-if="selectedPaymentPlan === 'Deffered Payment'" class = "description-align">
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
          class="form-select mt-2"
          style="width: 100px;"
          required
        >
          <option value="0">0%</option>
          <option value="5">5%</option>
          <option value="10">10%</option>
          <option value="15">15%</option>
        </select>
      </div>
      
      <p class = "description-align"><strong>Spread Downpayment:</strong> ₱{{ spreadDownpayment }}</p>

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
      <p class = "description-align"><strong>Payable Per Month:</strong> ₱{{ payablePerMonth }}</p>
      <!-- Balance Upon Turnover -->
      <p class = "description-align">
        <strong>Balance Upon Turnover:</strong> ₱{{ balanceUponTurnover }}
      </p>
      <br>    
      <div class="line mb-4"></div>
      <div class="col-12 text-center mb-3 text-center">
            <h5 class="property-header">Payment Schedule Summary</h5>
      </div>

      <!-- Payment Summary -->
      <div class="payment-summary">
        <p class = "description-align">
          <strong>Spot Downpayment:</strong> ₱{{
            spotDownpayment.toFixed(2)
          }}
        </p>
        <p class = "description-align">
          <strong>Spread Downpayment:</strong> ₱{{
            spreadDownpayment.toFixed(2)
          }}
        </p>
        <p class = "description-align">
          <strong>Monthly Payment:</strong> ₱{{
            payablePerMonth.toFixed(2)
          }}
          / month for {{ payableMonths }} months
        </p>
        <p class = "description-align">
          <strong>Balance Upon Turnover:</strong> ₱{{
            balanceUponTurnover.toFixed(2)
          }}
        </p>
      </div>
      <!-- Expandable Detailed Schedule Section -->
      <button @click="toggleDetailedSchedule" class="toggle-button">
        {{
          showDetailedSchedule
            ? "Hide Detailed Schedule"
            : "Show Detailed Schedule"
        }}
      </button>

      <!-- Detailed Monthly Schedule (Visible when expanded) -->
      <div v-if="showDetailedSchedule" class="detailed-schedule">
        <table class = "table">
          <thead>
            <tr>
              <th><center>Payment Type</center></th>
              <th><center>Amount (₱)</center></th>
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
    <div
      class="d-flex justify-content-end gap-2 mt-30"
      style="padding-top: 15px"
    >
      <button class="reserve-btn" @click="openReserveModal">
        Reserve Unit
      </button>
    </div>

    <!-- Reserve Unit Modal -->
    <b-modal
      v-model="isReserveModalVisible"
      @hide="closeReserveModal"
      hide-footer
      title="Reserve Unit"
    >
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
        <div
          class="d-flex justify-content-end gap-2 mt-30"
          style="padding-top: 15px"
        >
        <button type="submit" class="btn-add">
            Submit Reservation
        </button>
        <button @click="closeReserveModal" class="btn-cancel">Cancel</button>
        </div>
      </form>
      
      <!-- Error Message -->
      <div v-if="errorMessage">
        <p>{{ errorMessage }}</p>
        <b-button @click="closeModal" variant="secondary">Close</b-button>
      </div>
      
      <!-- Cancel Button -->
      <!-- <b-button @click="closeReserveModal" variant="danger">Cancel</b-button> -->
    </b-modal>

      </b-modal>
  </div>
  </div>
</div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { BModal } from "bootstrap-vue-3"; 
import axios from "axios";

export default {
  name: "AvailableUnits",
  components: {
    SideNav,
    BModal,
    AppHeader,
  },
  data() {
    return {
      siteId: this.$route.params.siteId,
      units: [],
      siteName: "",
      siteYear: "",
      isModalVisible: false,
      selectedUnit: {
        images: null, // Initially null
      },
      showDetailedSchedule: false, // To toggle detailed payment schedule
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
      selectedFloor: 'all',
      selectedUnitType: 'all', // Default unit type filter
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
  availableUnitTypes() {
    // Get unique unit type values from available units
    const unitTypes = this.units.map(unit => unit.type);
    return [...new Set(unitTypes)].sort(); // Add 'all' option and remove duplicates
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

      const unitTypeMatch =
        this.selectedUnitType === 'all' || unit.type === this.selectedUnitType;

      return viewMatch && balconyMatch && floorMatch && unitTypeMatch;
    });
  },
},
  created() {
      this.fetchImages(); // Fetch images when the component is created
  },

  methods: {
    toggleDetailedSchedule() {
      // Toggle the visibility of the detailed payment schedule
      this.showDetailedSchedule = !this.showDetailedSchedule;
    },
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

    async fetchImages() {
      try {
        // Replace with your actual API endpoint
        const response = await fetch("https://api.example.com/units/123/images");

        // Assuming the API returns an array of image URLs
        const data = await response.json();

        // Update the images array
        this.selectedUnit.images = data.images; // Use the correct field from your API response
      } catch (error) {
        console.error("Error fetching images:", error);
        this.selectedUnit.images = []; // Fallback to an empty array on error
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

html,
body {
  height: 100%;
  margin: 0;
  /* Removes default margin */
  padding: 0;
  /* Removes default padding */
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
  /* Ensures it spans the full viewport height */
  background-color: #e8f0fa;
  /* Gray background */
}
.main-content {
  display: flex;
  flex-direction: column;
  margin-top: 80px;
  margin-left: 250px;
  /* Offset for header height */
  flex: 1;
  /* margin-left: 250px; */
  /* Set margin equal to sidebar width */
}
.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}

.text-start{
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

.site-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  max-width: 1100px;
  /* Matches the max-width of the card */
  margin: 0 auto;
  /* Centers the grid within the parent */
}

.site-card {
  background: #fff;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  /* transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)
}

.site-card:hover {
  transform: translateY(-2px);
}

.toolbar {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
  padding-left: 20px;
  /* Space on the left side */
  padding-right: 20px;
  /* Space on the right side */
}

.left-section {
  display: flex;
  align-items: center;
  gap: 20px;
  /* Space between search bar and dropdown */
}

.dropdown-select {
  padding: 8px 12px;
  height: 38px;
  /* Explicitly set height */
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  width: 80%;
  max-width: 150px;
  background-color: white;
  color: #333;
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

.form-select {
  margin-left: 5px;
}


.line {
    border-top: 2px solid #000; /* Adjust thickness and color */
    width: 100%; /* Full-width */
    margin: 0 auto; /* Center it */
}

.text-center1 {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Align the content to the left */
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
  margin-left: 30px;
}

.toggle-button:hover {
  background-color: #0056b3;
}

.btn-add {
  background-color: #42b983;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 10px;
}

.btn-add:hover {
  background-color: #3e9c73;  /* Slightly darker green */
  color: #fff;
  border: none;
}


.btn-cancel {
  background-color: #343a40;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 10px;
}

.btn-cancel:hover {
  background-color: #495057;  /* Slightly lighter gray */
  color: #fff;
  border: none;
}




/* juju */

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
  margin-left: 30px;
}

.form-group select:focus {
  outline: none;
  border-color: #007bff; /* Highlight border on focus */
}

/* Dropdown Hover Text */
.form-group select:hover {
  color: black; /* Change text color to black on hover for better visibility */
}

.form-group input[type="number"] {
  width: 70%; /* Make the input take up full width */
  padding: 10px; /* Add padding for a better click area */
  font-size: 16px; /* Match font size with the label */
  border: 1px solid #ccc; /* Light border for input */
  border-radius: 8px; /* Add rounded corners */
  color: #333; /* Text color */
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

/* Style for File Input Button */
input[type="file"] {
  border: 1px solid #ccc;
  border-radius: 8px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.description-align {
  margin-left: 30px;
}

/* Dropdown Styling */

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
