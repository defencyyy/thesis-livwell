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
          <div class="edit-title"><strong>Available Units for Site {{ siteName }}</strong> </div>
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
      v-for="unit in paginatedUnits"
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

    <!-- Pagination Controls -->
    <nav aria-label="Page navigation example">
      <ul class="pagination">
        <li :class="['page-item', { disabled: currentPage === 1 }]">
          <a 
            class="page-link" 
            href="#" 
            @click.prevent="goToPage(currentPage - 1)"
            aria-label="Previous"
          >
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        <li 
          v-for="page in totalPages" 
          :key="page" 
          :class="['page-item', { active: page === currentPage }]"
        >
          <a 
            class="page-link" 
            href="#" 
            @click.prevent="goToPage(page)"
          >
            {{ page }}
          </a>
        </li>
        <li :class="['page-item', { disabled: currentPage === totalPages }]">
          <a 
            class="page-link" 
            href="#" 
            @click.prevent="goToPage(currentPage + 1)"
            aria-label="Next"
          >
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    </nav>

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

    <div
      class="d-flex justify-content-end gap-2 mt-30"
      style="padding-top: 15px"
    >
      <button class="reserve-btn" @click="openReserveModal">Reserve Unit</button>
      <button class="payment-plan-btn" @click="redirectToPaymentPlan">View Payment Plan</button>
    </div>

    <!-- Success Message Pop-up -->

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
      isErrorModalVisible: false, // To control modal visibility
      showSuccessMessage: false, // Control the visibility of the success message
      unitPrice: 0, // Example price of the unit
      selectedView: 'all',      // Default to "all"
      selectedBalcony: 'all',   // Default to "all"
      selectedFloor: 'all',
      selectedUnitType: 'all', // Default unit type filter
      currentPage: 1, // Current page number
      itemsPerPage: 20, // Number of customers per page
    };
  },

  mounted() {
    this.fetchAvailableUnits();
    this.fetchSiteName();
    this.fetchCustomers();
  },
  computed: {
 // Paginate filtered units
    paginatedUnits() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.filteredUnits.slice(startIndex, endIndex);
    },
    // Calculate total pages based on the number of filtered units
    totalPages() {
      return Math.ceil(this.filteredUnits.length / this.itemsPerPage);
    },
  availableFloors() {
    // Get unique floor values from available units
    const floors = this.units.map(unit => unit.section);
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
        this.selectedFloor === 'all' || unit.section === this.selectedFloor;

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
    redirectToPaymentPlan() {
      // Redirect to the payment plan page
      this.$router.push({ name: 'PaymentPlan', params: { unitId: this.selectedUnit.id } });
    },
     goToPage(pageNumber) {
      if (pageNumber > 0 && pageNumber <= this.totalPages) {
        this.currentPage = pageNumber;
      }
    },
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

.button-container {
  display: flex;
  justify-content: flex-end; /* Align button to the right */
}

.btn-cancel-right {
  background-color: #343a40; /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px; /* Adjust the border radius */
  padding: 10px;
  cursor: pointer;
}

.btn-add {
  background-color: #0560fd;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 10px;
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

.buttons-container {
  text-align: right;
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

.row .col-md-6 {
  padding-left: 5px;
  padding-right: 5px;
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
  width: 100%; /* Make the input take up full width */
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

.form-group input[type="text"]::placeholder {
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

/* Payment Plan Section */
.payment-plan {
  margin-top: 20px;
}

.plan-heading {
  font-size: 18px;
  color: #007bff;
  margin-bottom: 10px;
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
  background-color: #0560fd;
  color: #fff;
}

.schedule-btn {
  background-color: #343a40;
  color: #fff;
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

.pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: -15px; /* Reduce margin */
  padding-right: 40px; /* Reduce padding */
  font-size: 14px; /* Smaller font size */
  line-height: 1.2; /* Adjust line height for compactness */
}

.page-item {
  margin: 0 2px; /* Reduce spacing between buttons */
}

.page-link {
  padding: 4px 8px; /* Smaller button padding */
  font-size: 14px; /* Match font size for consistency */
}

</style>