<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
    <AppHeader />
    <div class="content">
      <router-link v-if="siteId" :to="{ name: 'AvailableUnits', params: { siteId: siteId } }" class="text-start">
      <div class="back-container">
        <i class="fas fa-arrow-left"></i> Back to Units
      </div>
    </router-link>
    <!-- Optionally display a fallback message if siteId is not set -->
    <div v-else>
      Loading Units ...
    </div>   


      <h1>Reserve a Unit</h1>
   <form @submit.prevent="submitReservation" style = "margin-left: -25px;">
        <!-- Customer Name Dropdown -->
        <div class="form-group">
          <label for="customerName">Customer Name {{ this.siteId }}</label>
          <select
            v-model="reservationForm.customerName"
            id="customerName"
            class = "form-select"
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
            class = "form-control"
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
            class = "form-select"
            style="width: 250px; margin-left: 1px;"
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
            class = "form-select"
            style="width: 250px; margin-left: 1px;"
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
            class = "form-control"
            style="width: 250px; margin-left: 1px;"
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
        <div class="button-container" v-if="isErrorModalVisible">
          <button @click="closeErrorModal" class="btn-cancel-right">Close</button>
        </div>
      </b-modal>

      <!-- Success Message Pop-up -->
      <b-modal
        v-model="showSuccessMessage"
        title="Reservation Submitted"
        @hide="closePopup"
        centered
        hide-footer
      >
        <p>{{ successMessage }}</p>
        <div class="buttons-container" v-if="showSuccessMessage">
          <button @click="closePopup" class="btn btn-primary">OK</button>
        </div>
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
    components: {
    SideNav,
    BModal,
    AppHeader,
  },
data() {
    return {
    reservationForm: {
        customerName: "",
        paymentAmount: "",
        paymentMethod: "bank_transfer",
        paymentDate: "",
        paymentReference: "",
        file: null,
    },
    customers: [],
    successMessage: "",
    errorMessage: "",
    unitId: null,
    siteId: null,
    siteName: null,
    companyId: null,
    brokerId: null,
    commission: null,
    reservationFee: null,
    isErrorModalVisible: false, // To control modal visibility
    showSuccessMessage: false, // Control the visibility of the success message

    };
  },
mounted() {
   const { unitId, siteId, siteName, companyId, brokerId, commission,reservationFee } = this.$route.query;
   this.unitId = unitId; // Set it to data
   this.siteId = siteId; // Set it to data
   this.siteName = siteName;
   this.companyId = companyId;
   this.brokerId = brokerId;
    this.commission = commission;
  this.reservationFee = reservationFee;   
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
    this.errorMessage = "All fields are required except the payment reference (if payment method is 'cash').";
    this.isErrorModalVisible = true;
    return;
  }
  if (this.reservationForm.paymentAmount < this.reservationFee) {
    this.errorMessage = "Payment Amount Insufficient";
    this.isErrorModalVisible = true;
    return;
  }
  
  const data = {
    customer_name: this.reservationForm.customerName,
    site_id: parseInt(this.siteId, 10), // Convert to integer
    unit_id: this.unitId,
    commission: this.commission,
    broker_id: parseInt(this.$store.getters.getUserId, 10), // Use Vuex getter for broker_id
    company_id: this.companyId, // Ensure this is correctly passed
    payment_amount: this.reservationForm.paymentAmount,
    payment_method: this.reservationForm.paymentMethod,
    payment_reference: this.reservationForm.paymentReference || null, // Payment reference is optional if payment is "cash"
    reservation_file: this.reservationForm.file
      ? this.reservationForm.file.name
      : null, // Ensure file is present
  };

  console.log(this.commission);
  console.log("Data being sent to the API:", data);

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
    this.errorMessage = "";  // Clear error message in case of success

    setTimeout(() => {
      this.showSuccessMessage = true; // Trigger to show success message
    }, 500);

    // Reset the reservation form
    this.reservationForm = {
      customerName: "",
      paymentAmount: "",
      paymentMethod: "bank_transfer",
      paymentDate: "",
      paymentReference: "",
      file: null,
    };

    console.log("Sale created:", response.data);
  } catch (error) {
    console.error("Error submitting reservation:", error);
    this.errorMessage =
      "There was an error submitting the reservation. Please try again."; // Display error message
    this.isErrorModalVisible = true; // Show the error modal
  }
},
     handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.reservationForm.file = file;
      }
    },
   handleErrorModalClose() {
      this.isErrorModalVisible = false;
      this.errorMessage = "";
    },
    closeErrorModal() {
      this.handleErrorModalClose();
    },
    closePopup() {
      this.successMessage = "";
      this.showSuccessMessage = false;
      this.$router.push({ name: "AffiliatedUnits" });
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
.form-group {
  margin-bottom: 15px;
  margin-left: 30px;
}

.form-group select:focus {
  outline: none;
  border-color: #007bff; 
}

.form-group select:hover {
  color: black; 
}

.form-group input[type="number"] {
  width: 70%; 
  padding: 10px; 
  font-size: 16px; 
  border: 1px solid #ccc; 
  border-radius: 8px; 
  color: #333; 
  transition: all 0.3s ease; 
}

.form-group input[type="number"]:hover {
  border-color: #007bff; 
}

.form-group input[type="number"]:focus {
  border-color: #0056b3; 
  outline: none; 
  box-shadow: 0 0 6px rgba(0, 123, 255, 0.5); 
}

.form-group input[type="number"]::placeholder {
  color: #888; 
  font-style: italic; 
}
label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}
.text-start{
  color: black;
  text-decoration: none !important;
}
.error {
  color: red;
}
</style>
