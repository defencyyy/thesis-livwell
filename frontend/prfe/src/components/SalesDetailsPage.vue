<template>
  <div>
    <!-- Header -->
    <div>
      <!-- Header -->
      <div class="header">
        <div class="top-bar">
          <!-- Add conditional rendering to prevent errors -->
          <div v-if="salesDetail?.customer_name" class="welcome-text">
            Welcome Back, <b>{{ salesDetail.customer_name }}!</b>
          </div>
          <div v-else class="welcome-text">Welcome Back!</div>
        </div>
      </div>
    </div>
    <div class="main-page">
      <!-- Side Bar -->
      <div class="sidebar">
        <div class="sidebar-header">
          <!-- If company.logo exists, show the company logo -->
          <img
            v-if="salesDetail?.company_logo"
            :src="salesDetail.company_logo"
            alt="Company Logo"
            class="sidebar-logo"
            style="max-width: 100%; height: auto"
          />
          <!-- Fallback to the Font Awesome icon if no logo is available -->
          <i v-else class="fas fa-cogs sidebar-logo" style="color: #0560fd"></i>

          <!-- Company Name -->
          <h4 id="sidebar-title">
            {{ salesDetail?.company_name || "Company Name" }}
          </h4>
        </div>

        <nav class="sidebar-nav">
          <b-nav vertical pills>
            <!-- Document Status Tab -->
            <b-nav-item
              href="#"
              @click.prevent="setActiveTab('document-status')"
              :class="{ active: activeTab === 'document-status' }"
              exact
              custom
            >
              <i class="menu-icon fas fa-file-alt"></i>
              <span class="item-name">Document Status</span>
            </b-nav-item>

            <!-- Payment Schedule Tab -->
            <b-nav-item
              href="#"
              @click.prevent="setActiveTab('payment-schedule')"
              :class="{ active: activeTab === 'payment-schedule' }"
              exact
              custom
            >
              <i class="menu-icon fas fa-calendar-alt"></i>
              <span class="item-name">Payment Schedule</span>
            </b-nav-item>
          </b-nav>
        </nav>
      </div>

      <div class="main-content">
        <div class="content">
          <!-- Document Status Content -->
          <div v-if="activeTab === 'document-status'">
            <div v-if="salesDetail">
              <div class="container mt-5">
                <div class="mb-4">
                  <h3
                    class="text-start display-5 fw-bolder text-capitalize pb-6"
                  >
                    {{ salesDetail.customer_name }}
                  </h3>
                  <p class="text-start display-7" style="margin-bottom: 1px">
                    Assigned Broker:
                    <strong>{{ salesDetail.broker_name }}</strong>
                  </p>
                  <p class="text-start display-7">
                    Selected Unit: <strong>{{ salesDetail.unit_name }}</strong>
                  </p>
                </div>
                <div class="mb-4">
                  <p class="text-start">
                    <strong>DOCUMENTS NEEDED:</strong> Please submit the
                    following documents to complete the process.
                  </p>
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
                          <td>
                            <strong>{{ doc.document_type_name }}</strong>
                          </td>
                          <td>{{ doc.status }}</td>
                          <td>{{ doc.uploaded_at || "Pending" }}</td>
                        </tr>
                      </tbody>
                    </table>
                    <div
                      class="download-button"
                      v-if="salesDetail.reservation_agreement_url"
                      style="text-align: right"
                    >
                      <a
                        :href="`http://localhost:8000/download_reservation_agreement/${salesDetail.id}`"
                        download
                      >
                        <button>Download Reservation Agreement</button>
                      </a>
                    </div>
                  </div>
                  <p v-else>No document types available.</p>

                  <div style="margin-top: 30px">
                    <p class="text-start">
                      Ensure that all documents are up-to-date and complete.
                      <br />
                      If you have any questions or need further assistance,
                      please contact
                      <strong>{{ salesDetail.broker_name }}</strong
                      >.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Payment Schedule Content -->
          <div v-if="activeTab === 'payment-schedule'" class="tab-content">
            <div>
              <div class="container mt-5">
                <div class="mb-4">
                  <h3
                    class="text-start display-5 fw-bolder text-capitalize pb-6"
                  >
                    {{ salesDetail.customer_name }}
                  </h3>
                  <p class="text-start display-7" style="margin-bottom: 1px">
                    Assigned Broker:
                    <strong>{{ salesDetail.broker_name }}</strong>
                  </p>
                  <p class="text-start display-7">
                    Selected Unit: <strong>{{ salesDetail.unit_name }}</strong>
                  </p>
                </div>
                <div class="mb-4">
                  <div
                    v-if="salesDetail.payment_plan === 'Spot Cash'"
                    class="additional-box1"
                  >
                    <div class="summary-item">
                      <span class="label">Total Amount Due:</span>
                      <span class="value"
                        >₱{{ netFullPayment.toFixed(2) }}
                      </span>
                    </div>
                    <!-- <p v-if="salesDetail.payment_plan === 'Spot Cash'" class="text-start" style="margin-bottom: 1px">
                    <strong>Total Amount Due: </strong>₱{{
                      netFullPayment.toFixed(2)
                    }}
                  </p> -->
                  </div>

                  <div v-if="salesDetail.payment_plan === 'Deffered Payment'">
                    <div class="payment-container">
                      <div class="summary-and-info">
                        <div class="payment-schedule-summary">
                          <div class="summary-item">
                            <span class="label">Balance Upon Turnover: </span>
                            <span class="value"
                              >₱{{ balanceUponTurnover.toFixed(2) }}
                            </span>
                          </div>
                          <hr class="separator" />
                          <div class="summary-item">
                            <span class="label">Installment Terms:</span>
                            <span class="value"
                              >{{ salesDetail.payable_months }} months
                            </span>
                          </div>
                        </div>
                        <div class="additional-box">
                          <h4><center>Monthly Amortization (6.5%)</center></h4>
                          <div class="summary-item">
                            <span class="label">10 years</span>
                            <span class="value"
                              >₱{{ amortization10Years.toFixed(2) }}</span
                            >
                          </div>
                          <hr class="separator" />
                          <div class="summary-item">
                            <span class="label">15 years</span>
                            <span class="value"
                              >₱{{ amortization15Years.toFixed(2) }}</span
                            >
                          </div>
                          <hr class="separator" />
                          <div class="summary-item">
                            <span class="label">20 years</span>
                            <span class="value"
                              >₱{{ amortization20Years.toFixed(2) }}</span
                            >
                          </div>
                          <hr class="separator" />
                          <div class="summary-item">
                            <span class="label">25 years</span>
                            <span class="value"
                              >₱{{ amortization25Years.toFixed(2) }}</span
                            >
                          </div>
                        </div>
                      </div>
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
                            <td class="amount-column highlight">₱{{ netDownpayment.toFixed(2) }}</td>
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
                  <div v-if="salesDetail.payment_plan === 'Spot Cash'">
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
                            <td>Net Full Payment</td>
                            <td>₱{{ netFullPayment }}</td>
                            <td>{{ dueDate }}</td>
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
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { BNav, BNavItem } from "bootstrap-vue-3";
import { mapState } from "vuex";

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
      reservationDate: new Date().toISOString().split('T')[0], // Default to today's date
      dueDate: null,
      spotDueDate: null,
      spreadDueDate: null,
      turnoverDueDate: null,
      payableMonths:1,
    };
  },
  created() {
    const salesDetailUuid = this.$route.params.id; // Get the UUID from the URL
    this.fetchSalesDetail(salesDetailUuid);
    this.fetchDocumentTypes(); // Fetch the document types on component creation
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId || null,
      userType: (state) => state.userType || null,
      companyId: (state) => state.companyId || null,
      loggedIn: (state) => state.loggedIn, // Use Vuex loggedIn state
    }),
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
  methods: {
    calculateAmortization(balance, years) {
      const interestRate = 6.5 / 100; // 6.5% annual interest
      const monthlyRate = interestRate / 12; // Monthly interest rate
      const totalMonths = years * 12; // Total number of months
      return (
        (balance * (monthlyRate * Math.pow(1 + monthlyRate, totalMonths))) /
        (Math.pow(1 + monthlyRate, totalMonths) - 1)
      );
    },
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
              uploaded_at: submittedDoc
                ? new Date(submittedDoc.uploaded_at).toLocaleDateString()
                : "Pending",
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
          this.payableMonths = this.salesDetail.payable_months;
          this.applySpotCashDiscount(); // Call the function after the data is fetched
          this.applyTLPDiscount();
          this.updateNetUnitPrice();
          this.applyOtherCharges();
          this.calculateVAT();
          this.calculateFinancingDetails();
          this.fetchDocuments();
          this.calculateDueDate(); // Call this whenever payment details update
          this.salesDetail.company_logo = `${this.salesDetail.company_logo}`; // Set the logo URL
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
        const response = await fetch(
          `http://localhost:8000/document-types/?company_id=${this.companyId}`
        );
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
  calculateDueDate() {
  const reservationDate = new Date(this.reservationDate);
  if (this.salesDetail.payment_plan === 'Spot Cash') {
    // For Spot Payment, add 30 days
    reservationDate.setDate(reservationDate.getDate() + 30);
    this.dueDate = reservationDate.toISOString().split('T')[0]; // Format as YYYY-MM-DD
  } else if (this.salesDetail.payment_plan === 'Deffered Payment') {         
    // For Deferred Payment:
    // Spot Payment Due Date: 30 days from the reservation date
    const spotDate = new Date(reservationDate);
    spotDate.setDate(spotDate.getDate() + 30);
    this.spotDueDate = spotDate.toISOString().split('T')[0];

    // Spread Payment Due Date: Last month of the payment term
    const spreadDate = new Date(reservationDate);
    spreadDate.setMonth(spreadDate.getMonth() + this.payableMonths - 1); // Set to the last month
    this.spreadDueDate = spreadDate.toISOString().split('T')[0];

    // Balance Upon Turnover Due Date: 1 year after reservation
    const turnoverDate = new Date(reservationDate);
    turnoverDate.setFullYear(turnoverDate.getFullYear() + 1); // 1 year later
    this.turnoverDueDate = turnoverDate.toISOString().split('T')[0];

    // Optionally set a "main" due date if needed
    this.dueDate = this.spreadDueDate; 

  }
},
getPaymentDueDate(month) {
    const reservationDate = new Date(this.reservationDate);
    const paymentDate = new Date(reservationDate);
    paymentDate.setMonth(paymentDate.getMonth() + month);
    return paymentDate.toISOString().split('T')[0];
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
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* Adds a shadow at the bottom */
}

.welcome-text {
  font-size: 18px;
}

.d-flex {
  display: flex;
}

.d-flex .btn i {
  font-size: 20px;
  color: #fff;
}

.main-page {
  display: flex;
  min-height: 100vh;
  /* Ensures it spans the full viewport height */
  background-color: #e8f0fa;
  /* Gray background */
}

.sidebar {
  position: fixed;
  width: 250px;
  background-color: #ffffff;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1); /* Adds shadow on the right */
  z-index: 2;
}

.sidebar.collapsed {
  transform: translateX(-100%); /* Hide the sidebar when collapsed */
}

.sidebar-header {
  display: flex;
  align-items: center;
  padding: 17px;
  height: 68px;
  box-sizing: border-box;
  margin-top: 5px;
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
  color: #0d6efd !important; /* Blue color when hovered */
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
  color: #343a40;
}

/* Main Content Responsiveness */
.main-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  margin-left: 250px;
  margin-top: 60px;
  padding: 20px;
  box-sizing: border-box; /* Include padding in width calculation */
  background-color: #fff; /* Ensure a clean background for content */
}

.content {
  flex: 1;
  padding: 20px;
  text-align: left; /* Align text to the left for readability */
}

/* Adjustments for smaller screens */
@media (max-width: 1440px) {
  .main-content {
    margin-left: 200px; /* Adjust for sidebar (larger screens may need more space) */
    padding: 20px;
  }
  .content {
    padding: 20px;
  }
}

@media (max-width: 1024px) {
  .main-content {
    margin-left: 200px; /* Adjust for narrower sidebar */
    padding: 15px;
  }
  .content {
    padding: 15px;
  }
}

@media (max-width: 720px) {
  .main-content {
    margin-left: 60px; /* Adjust for collapsed sidebar */
    padding: 10px;
  }
  .content {
    padding: 10px;
    font-size: 14px; /* Reduce font size for smaller screens */
  }
}

/* Specific styling for tables inside main content */
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  font-size: 14px; /* Default table font size */
}

th,
td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

@media (max-width: 720px) {
  table {
    font-size: 12px; /* Scale down table font size */
  }
  th,
  td {
    padding: 8px;
  }
}

/* Ensure buttons in the main content are responsive */
button {
  padding: 8px 16px; /* Smaller padding for smaller screens */
  font-size: 14px;
}

@media (max-width: 720px) {
  button {
    font-size: 12px;
    padding: 6px 12px;
  }
}

/* Specific adjustments for document and payment content */
.documents-table {
  width: 100%;
  margin-top: 15px;
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
.additional-box,
.additional-box1 {
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
  height: 130px;
  max-width: 400px;
  margin-left: 1px !important;
}

.additional-box {
  background: #f9f9f9;
  text-align: left;
  margin-top: -5px;
  max-width: 400px;
  height: 270px;
  margin-left: 1px !important;
}

.additional-box1 {
  background: #f9f9f9;
  text-align: left;
  margin-top: -5px;
  max-width: 400px;
  height: 90px;
  margin-left: 1px !important;
}

.detailed-schedule {
  flex: 1; /* Flex item for dynamic width */
  height: 415px;
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
.documents-table th,
.documents-table td {
  padding: 10px;
  font-size: 14px;
}

@media (max-width: 720px) {
  .documents-table th,
  .documents-table td {
    font-size: 12px;
  }
}

/* Button */
button {
  padding: 10px 20px;
  background-color: #0560fd;
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

.sidebar-logo {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  margin-right: 10px;
  margin-left: 5px;
  object-fit: cover;
}

/* Media queries for responsiveness in HEADER */
@media (max-width: 1440px) {
  .top-bar {
    left: 200px; /* Adjust for the narrower sidebar */
    width: calc(100% - 220px);
  }

  .welcome-text {
    font-size: 16px; /* Adjust font size */
  }

  .profile-icon {
    font-size: 20px; /* Scale down icon */
  }

  .dropdown-menu {
    width: 200px; /* Adjust dropdown width */
  }
}

@media (max-width: 1024px) {
  .top-bar {
    left: 200px; /* Adjust for smaller sidebar */
    width: calc(100% - 200px);
    padding: 10px 20px; /* Adjust padding */
  }

  .welcome-text {
    font-size: 15px; /* Scale down text */
  }

  .profile-icon {
    font-size: 18px;
  }
}

@media (max-width: 720px) {
  .top-bar {
    left: 60px; /* Adjust for collapsed sidebar */
    width: calc(100% - 60px);
    padding: 8px 15px; /* Minimal padding */
  }

  .welcome-text {
    display: none; /* Hide welcome text for small screens */
  }

  .profile-icon {
    font-size: 16px;
  }

  .d-flex .dropdown {
    margin-left: 10px; /* Reduce spacing */
  }
}

/* RESPONSIVENESS  IN SIDENAV*/
/* Media queries for responsive behavior */

@media (max-width: 1440px) {
  .sidebar {
    width: 220px; /* Reduce sidebar width for medium screens */
  }

  #sidebar-title {
    font-size: 1.1rem; /* Adjust font size */
  }

  .menu-icon {
    width: 18px; /* Adjust icon size */
  }

  .item-name {
    font-size: 13px; /* Adjust item font size */
  }
}

@media (max-width: 1024px) {
  .sidebar {
    width: 200px; /* Reduce sidebar width further for smaller screens */
  }

  #sidebar-title {
    font-size: 1rem;
  }

  .menu-icon {
    width: 16px;
  }

  .item-name {
    font-size: 12px;
  }
}

@media (max-width: 720px) {
  .sidebar {
    width: 60px; /* Collapse sidebar */
  }

  #sidebar-title {
    display: none; /* Hide title for small screens */
  }

  .menu-icon {
    margin-right: 0; /* Center icon without extra space */
  }

  .item-name {
    display: none; /* Hide text for small screens */
  }
}

@media (max-width: 480px) {
  .sidebar {
    width: 50px; /* Narrower collapsed sidebar */
  }

  #sidebar-title {
    display: none; /* Keep the title hidden */
  }

  .menu-icon {
    font-size: 16px; /* Slightly smaller icons for compact view */
    margin: 0 auto; /* Center the icons */
  }

  .item-name {
    display: none; /* Hide text labels */
  }

  .main-content {
    margin-left: 90px; /* Adjust for narrower sidebar */
    padding: 8px; /* Reduce padding for more usable space */
  }

  .content {
    padding: 8px;
    font-size: 13px; /* Slightly smaller font size */
  }

  /* Tables should be scrollable to prevent overflow */
  table {
    display: block;
    overflow-x: auto;
    font-size: 12px; /* Reduce table font size */
  }

  th,
  td {
    padding: 6px; /* Smaller cell padding */
  }

  /* Buttons */
  button {
    font-size: 12px; /* Compact button text */
    padding: 6px 12px; /* Smaller button size */
  }

  /* Top bar adjustments */
  .top-bar {
    left: 50px; /* Align with sidebar */
    width: calc(100% - 50px); /* Adjust width dynamically */
    padding: 6px 10px; /* Minimal padding */
  }

  .welcome-text {
    font-size: 12px; /* Smaller font for welcome text */
  }

  /* Hide non-essential elements for small screens */
  .welcome-text {
    display: none; /* Hide welcome text completely for extra space */
  }
}
</style>
