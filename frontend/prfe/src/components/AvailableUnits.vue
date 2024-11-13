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
            <p>{{ unit.unit_title }}</p> <!-- Display the unit title -->
          </div>
        </div>
      </div>
      <div v-else>
        <p>No units available for this site.</p>
      </div>

      <!-- Unit Details Modal -->
      <div v-if="isModalVisible" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <img :src="selectedUnit.picture" alt="Unit Picture" class="unit-picture" />
          <p>P{{ selectedUnit.price }} Bedroom: {{ selectedUnit.bedroom }} Bathroom: {{ selectedUnit.bathroom }} Floor Area: {{ selectedUnit.floor_area }}</p>
          <hr>
          <center>Details</center>
          <p>Unit/Floor Number: {{ selectedUnit.floor }} Balcony: {{ selectedUnit.balcony }} Built(Year):{{ siteYear }} </p>
          <p>Baths:{{ selectedUnit.bathroom }} Bedrooms: {{ selectedUnit.bedroom }}  Floor area(m<sup>2</sup>):{{ selectedUnit.floor_area }} </p>
          <p>View: {{ selectedUnit.view }} </p>
          <hr>

          <!-- Buttons -->
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
            <!-- Payment Reference -->
            <div class="form-group">
              <label for="paymentReference">Payment Reference Number</label>
              <input type="text" v-model="reservationForm.paymentReference" id="paymentReference" />
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
      siteId: this.$route.params.siteId, // Get site ID from route params
      units: [],
      siteName: '',
      siteYear: '',
      isModalVisible: false,
      selectedUnit: null,
      isReserveModalVisible: false,  // Control visibility of reservation modal
      reservationForm: {
        customerName: '',
        paymentAmount: '',
        paymentMethod: '',
        paymentDate: '',
        paymentReference: ''
      },
      customers: [],  // List of customers for the dropdown
    };
  },
  mounted() {
    this.fetchAvailableUnits();
    this.fetchSiteName();
    this.fetchCustomers();  // Fetch customers when the component is mounted
  },
  methods: {
    async fetchAvailableUnits() {
      try {
        const response = await axios.get(`http://localhost:8000/units/available/?site_id=${this.siteId}`);
        this.units = response.data.units;
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
    this.error = "Broker ID not found. Please log in again.";
    return;
  }

  try {
    const response = await fetch(`http://localhost:8000/customers/broker/${brokerId}/?include_sales=false`);
    if (response.ok) {
      const data = await response.json();
      if (data.success) {
        this.customers = data.customers; // This will exclude sales data
      } else {
        this.error = data.message || "Failed to fetch customer data.";
      }
    } else {
      const errorData = await response.json();
      this.error = errorData.message || "Failed to fetch customer data.";
    }
  } catch (error) {
    this.error = "An error occurred while fetching customer data.";
  }
},
    showUnitDetails(unit) {
      this.selectedUnit = unit;
      this.isModalVisible = true;
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
        paymentReference: ''
      };
    },
    submitReservation() {
      // Handle the form submission (e.g., call an API to save reservation details)
      console.log("Reservation submitted:", this.reservationForm);
      this.closeReserveModal();
    }
  },
};
</script>

<style scoped>
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
