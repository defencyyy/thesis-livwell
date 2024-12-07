<template>
  <div>
    <!-- Header -->
    <div class = "header">
      <div class="top-bar">
        <div class="welcome-text">Welcome Back, <b>Customer!</b></div>
      </div>
    </div>

    <div class = "main-page">
      <!-- Side Bar -->
      <div class = "sidebar">
        <div class = "sidebar-header">
          <i class="fas fa-cogs sidebar-logo" style="color: #0560fd;"></i> <!-- Font Awesome Icon -->
          <h4 id="sidebar-title">{{ "Company Name" }}</h4>
        </div>
        <nav class = "sidebar-nav">
          <b-nav vertical pills>
            <!-- Document Status Tab -->
            <b-nav-item
              href="#"
              @click.prevent="setActiveTab('document-status')"
              :class="{ active: activeTab === 'document-status' }"
              exact
              custom
            >
          
              <i class = " menu-icon fas fa-file-alt"></i>
              <span class = "item-name">Document Status</span>
            </b-nav-item>

            <!-- Payment Schedule Tab -->
            <b-nav-item
              href="#"
              @click.prevent="setActiveTab('payment-schedule')"
              :class="{ active: activeTab === 'payment-schedule' }"
              exact
              custom
            >
              <i class = " menu-icon fas fa-calendar-alt"></i>
              <span class = "item-name">Payment Schedule</span>
            </b-nav-item>
          </b-nav>
        </nav>
      </div>

      <div class = "main-content">
        <div class = "content">

          <!-- Document Status Content -->
          <div v-if="activeTab === 'document-status'">
            <div v-if="salesDetail">
              <div class = "container mt-5">
                <div class="mb-4">
                  <h3 class="text-start display-5 fw-bolder text-capitalize pb-6">{{ salesDetail.customer_name }}</h3>
                  <p class="text-start display-7" style = "margin-bottom: 1px;"> Assigned Broker: <strong>{{ salesDetail.broker_name }}</strong></p>
                  <p class="text-start display-7"> Selected Unit: <strong>{{ salesDetail.unit_name }}</strong></p>
                </div>
                <div class="mb-4">
                  <p class = "text-start"><strong>DOCUMENTS NEEDED:</strong> Please submit the following documents to complete the process.</p>
                  <div v-if="documentTypes.length">
                    <table class="documents-table">
                      <thead>
                        <tr>
                          <th>Document Name</th>
                          <th>Document Status</th>
                          <th>Date Submitted</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="doc in documents" :key="doc.id">
                              <td><strong>{{ doc.document_type_name }}</strong></td>
                              <td>{{ doc.status }}</td>
                              <td>{{ doc.uploaded_at || 'Pending' }}</td>
                            </tr>
                      </tbody>
                    </table>
                    <div class="download-button" v-if="salesDetail.reservation_agreement_url" style="text-align: right;">
                      <a
                        :href="`http://localhost:8000/download_reservation_agreement/${salesDetail.id}`"
                        download
                      >
                        <button>Download Reservation Agreement</button>
                      </a>
                    </div>
                  </div>
                  <p v-else>No document types available.</p>

                  <div style = "margin-top: 30px;">
                    <p class = "text-start">Ensure that all documents are up-to-date and complete. <br> If you have any questions or need further assistance, please contact <strong>{{ salesDetail.broker_name }}</strong>.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Payment Schedule Content -->
          <div v-if="activeTab === 'payment-schedule'" class="tab-content">
            
            <div class="detailed-schedule">
              <p>{{ salesDetail.customer_name }}</p>
              <p><strong>Assigned Broker:</strong> {{ salesDetail.broker_name }}</p>
              <p><strong>Selected Unit:</strong> {{ salesDetail.unit_name }}</p>    
              <p>Total Amount Due: ₱{{ balanceUponTurnover.toFixed(2) }}</p>  
              <div v-if="salesDetail.payment_plan === 'Deffered Payment'">    
              <p>Installment Terms: {{salesDetail.payable_months}} months</p> 
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
                  <tr v-for="month in salesDetail.payable_months" :key="month">
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
        </div>
      </div>

    </div>
  </div>
  </div>
</template>

<script>
import { BNav, BNavItem } from "bootstrap-vue-3";

export default {
  name: "SalesDetails",
  components: { BNav, BNavItem },
  data() {
    return {
      activeTab: "document-status", // Default active tab
      salesDetail: null, // Store the sales details
      spotDiscount: 0,
      unitPriceAfterSpotDiscount: 0,
      tlpDiscountAmount: 0,
      netUnitPrice: 0,
      otherCharges: 0,
      totalAmountPayable: 0,
      reservationFee: 0, // Fixed reservation fee as per your example
      netFullPayment: 0,
      spotDownpayment: 0,
      spreadDownpayment: 0,
      payablePerMonth: 0,
      balanceUponTurnover: 0,
      showDetailedSchedule: false, // To toggle the detailed schedule
      documentTypes: [], // Store the document types fetched from the API
      documents: [], // Store the documents fetched from the API
    };
  },
  created() {
    const salesDetailUuid = this.$route.params.id; // Get the UUID from the URL
    this.fetchSalesDetail(salesDetailUuid);
    this.fetchDocumentTypes(); // Fetch the document types on component creation

  },
  methods: {
    setActiveTab(tab) {
      this.activeTab = tab;
    },
    async fetchDocuments() {
  try {
    const response = await fetch(
      `http://localhost:8000/documents/customer/${this.salesDetail.customer_id}/${this.salesDetail.sales_id}/`
    );
    const data = await response.json();
    if (data.success) {
      // Update document status based on submission
      this.documents = this.documentTypes.map((docType) => {
        const submittedDoc = data.documents.find(
          (doc) => doc.document_type_name === docType.name
        );
        return {
          document_type_name: docType.name,
          status: submittedDoc ? "Submitted" : "Pending",
          uploaded_at: submittedDoc ? new Date(submittedDoc.uploaded_at).toLocaleDateString() : "Pending",
        };
      });
    } else {
      console.error("Failed to fetch documents:", data.message);
    }
  } catch (error) {
    console.error("Error fetching documents:", error);
  }
},
    async fetchSalesDetail(salesDetailUuid) {
      try {
        const response = await fetch(
          `http://localhost:8000/sales-detail/${salesDetailUuid}/`
        ); // Update the URL with UUID
        const data = await response.json();
        if (data.success === false) {
          alert("Sales details not found");
        } else {
          this.salesDetail = data; // Store the sales details in data
          this.applySpotCashDiscount(); // Call the function after the data is fetched
          this.applyTLPDiscount();
          this.updateNetUnitPrice();
          this.applyOtherCharges();
          this.calculateVAT();
          this.calculateFinancingDetails();
          this.fetchDocuments(); 
        }
      } catch (error) {
        console.error("Error fetching sales details:", error);
      }
    },

    // Method to apply spot discount
    applySpotCashDiscount() {
      const discountPercentage = parseFloat(
        this.salesDetail.spot_discount_percent
      );
      this.spotDiscount =
        (this.salesDetail.unit_price * discountPercentage) / 100;
      this.unitPriceAfterSpotDiscount =
        this.salesDetail.unit_price - this.spotDiscount;
      this.updateNetUnitPrice();
    },

    // Method to apply TLP discount
    applyTLPDiscount() {
      const discountPercentage = parseFloat(
        this.salesDetail.tlp_discount_percent
      );
      this.tlpDiscountAmount =
        (this.unitPriceAfterSpotDiscount * discountPercentage) / 100;
      this.updateNetUnitPrice();
    },

    // Update net unit price after discounts
    updateNetUnitPrice() {
      this.netUnitPrice =
        this.unitPriceAfterSpotDiscount - this.tlpDiscountAmount;
      this.applyOtherCharges();
    },

    // Apply other charges
    applyOtherCharges() {
      const otherChargesPercentage = parseFloat(
        this.salesDetail.other_charges_percent
      );
      this.otherCharges = (this.netUnitPrice * otherChargesPercentage) / 100;
      this.totalAmountPayable = this.netUnitPrice + this.otherCharges;
      this.netFullPayment = this.totalAmountPayable - this.reservationFee;
      this.calculateFinancingDetails();
    },

    // Calculate VAT if applicable
    calculateVAT() {
      if (this.netUnitPrice > 3600000) {
        this.vatAmount = this.netUnitPrice * 0.12;
        this.totalAmountPayable += this.vatAmount;
      }
    },

    // Calculate financing details like downpayment, payable per month, and balance upon turnover
    calculateFinancingDetails() {
      const spotDownpaymentPercentage = parseFloat(
        this.salesDetail.spot_downpayment_percent
      );
      const spreadDownpaymentPercentage = parseFloat(
        this.salesDetail.spread_downpayment_percent
      );
      this.spotDownpayment =
        this.totalAmountPayable * (spotDownpaymentPercentage / 100);
      this.spreadDownpayment =
        this.totalAmountPayable * (spreadDownpaymentPercentage / 100);
      this.reservationFee = this.salesDetail.reservation_fee;
      if (spotDownpaymentPercentage === 0) {
        this.netDownpayment = this.spreadDownpayment - this.reservationFee;
        this.payablePerMonth =
          this.netDownpayment / this.salesDetail.payable_months;
      } else {
        this.netDownpayment = this.spotDownpayment - this.reservationFee;
        this.payablePerMonth =
          this.spreadDownpayment / this.salesDetail.payable_months;
      }

      this.balanceUponTurnover =
        ((100 - (spotDownpaymentPercentage + spreadDownpaymentPercentage)) /
          100) *
        this.totalAmountPayable;
    },
    // Fetch Document Types
    async fetchDocumentTypes() {
      try {
        const response = await fetch("http://localhost:8000/document-types/");
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            this.documentTypes = data.documentTypes;
          } else {
            this.error = data.message || "Failed to fetch document types.";
          }
        }
      } catch (error) {
        this.error = "An error occurred while fetching document types.";
      }
    },

    // Toggle the visibility of the detailed schedule
    toggleDetailedSchedule() {
      this.showDetailedSchedule = !this.showDetailedSchedule;
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

.top-bar {
  background-color: #eff4fb;
  color: #343a40;
  padding: 12px 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: fixed;
  top: 0;
  left: 250px; /* Sidebar width */
  width: calc(100% - 250px);
  z-index: 1;
  height: 68px;
  margin-top: 3px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* Adds a shadow at the bottom */
}

.welcome-text {
  font-size: 18px;
}

.main-page {
  display: flex;
  min-height: 100vh;
  /* Ensures it spans the full viewport height */
  background-color: #e8f0fa;
  /* Gray background */
}

.sidebar {
  background-color: white;
  width: 250px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
  position: fixed;
  z-index: 2;
}

.sidebar-header {
  display: flex;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #ddd;
}

.sidebar-logo {
  font-size: 24px;
  margin-right: 10px;
}

#sidebar-title {
  color: #343a40;
  font-size: 18px;
  margin: 0;
}

.sidebar-nav {
  text-align: left;
  margin-top: 50px;
  padding-left: 13px !important;
}

.sidebar-nav .nav-item {
  border-radius: 4px;
  margin-bottom: 8px;
}

.sidebar-nav .nav-item.active {
  background-color: #0d6efd;
  color: white !important;
}

.sidebar-nav .nav-item.active .item-name,
.sidebar-nav .nav-item.active .menu-icon {
  color: white !important;
}

.sidebar-nav .nav-item .item-name:hover {
  color: #0d6efd !important;  /* Blue color when hovered */
}

.menu-icon {
  width: 20px;
  text-align: center;
  margin-right: 8px;
  flex-shrink: 0;
  color: #343a40;
}

.item-name {
  font-size: 14px;
  color:#343a40;
}

.main-content {
  display: flex;
  margin-left: 250px;
  flex-direction: column;
  flex: 1;
  margin-top: 60px;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f8f8f8;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
}

.documents-table th {
  text-align: center;
}


/* juju */

/* Button */
button {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #45a049;
}

.download-button {
  margin-top: 20px;
}

/* Document List */
.details-card {
  background-color: white;
  padding: 20px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.details-card p {
  margin-bottom: 15px;
  font-size: 16px;
  line-height: 1.5;
}

.details-card strong {
  font-weight: bold;
}

</style>
