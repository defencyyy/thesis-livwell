<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">Manage Customer Sales</div>
          </div>
        </div>
         <div
          class="card border-0 rounded-1 mx-auto"
          style="max-width: 1100px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
        >
          <div class="card-body">
            <div class="row">
              <!-- Toolbar -->
              <div class="toolbar">
                <div class="left-section">
                  <!-- Search Bar -->
                  <div class="search-bar-container">
                    <input
                      type="text"
                      v-model="searchQuery"
                      placeholder="Search by Name or Customer Code"
                      class="search-bar"
                      @input="filterCustomers"
                    />
                    <i class="fa fa-search search-icon"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Sales Table -->
        <div style = "margin-top: 50px;">
          <div class="outside-headers">
            <span class="header-item">Customer Name</span>
            <span class="header-item">Customer Code</span>
            <span class="header-item">Site Name</span>
            <span class="header-item">Unit Title</span>
            <span class="header-item">Status</span>
            <span class="header-item">Action</span>

          </div>
        </div> 
        <div v-if="sales.length === 0">
            No sales found.
        </div>

        <div
        v-else
        v-for="sale in filteredCustomers"
        :key="sale.id"
        class="card border-0 rounded-1 mx-auto my-2"
        style="
          max-width: 1100px;
          box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        ">
          <div class = "card-body">
            <table class = "sales-table">
              <tbody>
                <tr>
                  <td>
                    <span>
                      {{ sale.customer_name }}
                    </span>
                  </td>
                  <td>
                    <span>
                      {{ sale.customer_code }}
                    </span>
                  </td>
                  <td>
                    <span>
                      {{ sale.site_name }}
                    </span>
                  </td>
                  <td>
                    <span>
                      {{ sale.unit_title }}
                    </span>
                  </td>
                  <td>
                    <span>
                      {{ sale.status }}
                    </span>
                  </td>
                  <td>
                    <div class="broker-actions d-flex gap-2">
                      <button @click="openSalesAgreementModal(sale)" style="
                      border: none;
                      background-color: transparent;
                      color: #343a40;
                      cursor: pointer;
                      font-size: 18px;
                      ">
                        <i class="fas fa-dollar-sign"></i>
                      </button>
                      <button @click="openDocumentModal(sale)" style="
                      border: none;
                      background-color: transparent;
                      color: #343a40;
                      cursor: pointer;
                      font-size: 18px;
                      ">
                        <i class="fas fa-file-alt"></i>
                      </button>
                      <button @click="DeleteSaleModal(sale)" style="
                      border: none;
                      background-color: transparent;
                      color: #343a40;
                      cursor: pointer;
                      font-size: 18px;
                      ">
                        <i class="fas fa-archive"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Sales Agreement Modal -->
        <b-modal v-model="showModal" title = "Sales Agreement" size="lg" centered hide-footer >
          <div v-if="selectedSale.status === 'Pending Reservation'">
            <p style="text-align: center">
              Reservation not yet confirmed
            </p>
            <div class = "button-container">
              <button @click="closeModal" class = "btn-cancel-right">Close</button>
            </div>
          </div>
          
          <div v-else>
            <div class="row">
              <div class="col-md-6">
                <h6 class = "customer-title">Customer</h6>
                <h4> {{ selectedSale.customer_name }} </h4>
              </div>
              <div class="col-md-6">
                <h6 class = "customer-title">Site</h6>
                <h4> {{ selectedSale.site_name }} </h4>
                <h6 class = "customer-title">Unit</h6>
                <h4> {{ selectedSale.unit_title }} </h4>
              </div>
            </div>

            <div v-if="salesDetailsExists">
              <br>
              <div class="row">
                <div class="col-md-6">
                  <h6 class = "customer-title">Unit Price</h6>
                  <h5> ₱{{ salesDetails.unit_price }} </h5>
                </div>
                <div class="col-md-6">
                  <h6 class = "customer-title">Payment Plan</h6>
                  <h5> {{ salesDetails.payment_plan }} </h5>
                </div>
              </div>
              <br>
              <div class="info-box">
                <h6 class="fw-bold">Spot Discount</h6>
                <ul class="list-unstyled mb-0">
                  <li><strong>Spot Discount Percentage:</strong> {{ salesDetails.spot_discount }}%</li>
                  <li><strong>Spot Discount:</strong> ₱{{ this.spotDiscount }}</li>
                  <li><strong>Unit Price after Spot Discount:</strong> ₱{{
                    this.unitPriceAfterSpotDiscount
                  }}</li>
                </ul>
              </div>

              <div class="info-box">
                <h6 class="fw-bold">TLP Discount</h6>
                <ul class="list-unstyled mb-0">
                  <li><strong>TLP Discount Percentage:</strong> {{ salesDetails.tlp_discount }}%</li>
                  <li><strong>TLP Discount:</strong> ₱{{ this.tlpDiscountAmount }}</li>
                  <li><strong>Net Unit Price:</strong> ₱{{ netUnitPrice }} </li>
                </ul>
              </div>

              <div class="info-box">
                <h6 class="fw-bold">Other Charges</h6>
                <ul class="list-unstyled mb-0">
                  <li><strong>Other Charges Percentage:</strong> {{ salesDetails.other_charges_percent }}%</li>
                  <li><strong>Other Charges:</strong> ₱{{ otherCharges }}</li>
                  <li><strong>Net Unit Price:</strong> ₱{{ netUnitPrice }} </li>
                </ul>
              </div>

              <div class="info-box">
                <!-- <h6 class="fw-bold">Other Charges</h6> -->
                <ul class="list-unstyled mb-0">
                  <li v-if="netUnitPrice > 3600000"><strong>VAT (12%):</strong> ₱{{ vatAmount }}</li>
                  <li><strong>Total Amount Payable:</strong> ₱{{totalAmountPayable}}</li>
                  <li v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Spot Downpayment Percentage:</strong> {{ salesDetails.spot_downpayment_percent }}% </li>
                  <li v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Spot Downpayment:</strong> ₱{{ spotDownpayment }}</li>
                  <li><strong>Reservation Fee:</strong> ₱{{salesDetails.reservation_fee}}</li>
                  <li v-if="salesDetails.payment_plan === 'Spot Cash'"><strong>Net Full Payment:</strong> ₱{{ netFullPayment }}</li>
                  <li v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Net Downpayment:</strong> ₱{{ netDownpayment }}</li>
                  <li v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Spread Downpayment Percentage:</strong> {{ salesDetails.spread_downpayment_percent }}%</li>
                  <li v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Spread Downpayment:</strong> ₱{{ spreadDownpayment }}</li>
                  <li v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Payable Months:</strong> {{ salesDetails.payable_months }}</li>
                  <li v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Payable Per Month:</strong> ₱{{ payablePerMonth }}</li>
                  <li v-if="salesDetails.payment_plan === 'Deffered Payment'"><strong>Balance Upon Turnover:</strong> ₱{{balanceUponTurnover}}</li>
                </ul>
              </div>

              <div
              class="d-flex justify-content-end gap-2 mt-30"
              style="padding-top: 15px"
              >
              <button
                v-if="
                  selectedSale.status !== 'Pending Sold' &&
                  selectedSale.status !== 'Sold'
                "
                @click="markUnitAsSold"
                class = "btn-add"
              >
                Mark Unit as Sold
              </button>
              <button @click="closeModal" class = "btn-cancel">Close</button>
              </div>
              </div>
              
              <div v-if="!salesDetailsExists">
                <div class="form-group">
                  <br>
                  <label for="paymentPlan"><b>Payment Plan </b></label>
                  <br>
                  <select
                    v-model="selectedPaymentPlan"
                    id="paymentPlan"
                    class = "dropdown"
                    required
                  >
                    <option value="Spot Cash">Spot Cash</option>
                    <option value="Deffered Payment">Deffered Payment</option>
                  </select>
                </div>

                <!-- In-House Financing Plan -->
                <p><strong>Unit Price:</strong> ₱{{ unitPrice }}</p>

                <!-- Spot Discount -->
              <div class="form-group">
              <br>
              <label for="spotDiscount">Spot Discount</label>
              <input
                type="number"
                id="spotDiscount"
                v-model="spotCashDiscount"
                @input="updatePaymentDetails"
                class="form-control"
                :min="0"
                :max="maxSpotCashDiscount" 
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
                  <br>
                  <label for="tlpDiscount">TLP Discount (Optional)</label>
                  <input
                    type="number"
                    id="tlpDiscount"
                    v-model="tlpDiscount"
                    @input="updatePaymentDetails"
                    class="form-control"
                    min="0"
                    max="maxtlpDiscount"
                  />
                </div>
                <p><strong>TLP Discount:</strong> ₱{{ tlpDiscountAmount }}</p>

                <!-- Net Unit Price -->
                <p><strong>Net Unit Price:</strong> ₱{{ netUnitPrice }}</p>

                <!-- Other Charges -->
                <div class="form-group">
                  <br>
                  <label for="otherChargesPercentage">Other Charges (%)</label>
                  <input
                    type="number"
                    id="otherChargesPercentage"
                    v-model="otherChargesPercentage"
                    @input="updatePaymentDetails"
                    class="form-control"
                    min="0"
                    max="maxotherChargesPercentage"
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
                  <strong>Total Amount Payable:</strong> ₱{{
                    totalAmountPayable
                  }}
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
                <p><strong>Reservation Fee:</strong> ₱{{ reservationFee }}</p>
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
                    <input
                    type="number"
                    v-model="spreadDownpaymentPercentage"
                    id="spreadDownpayment"
                    @input="updatePaymentDetails"
                    min="0"
                    max="100"
                    step="1"
                    required
                    placeholder="Enter percentage"
                  />
                  </div>
                  <p>
                    <strong>Spread Downpayment:</strong> ₱{{
                      spreadDownpayment
                    }}
                  </p>

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
                  <p>
                    <strong>Payable Per Month:</strong> ₱{{ payablePerMonth }}
                  </p>
                  <!-- Balance Upon Turnover -->
                  <p>
                    <strong>Balance Upon Turnover:</strong> ₱{{
                      balanceUponTurnover
                    }}
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
                    <table class = "sched-table">
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
                  <br>
                  <h3>Required Documents</h3>
                  <ul>
                    <li>
                    <strong>Reservation Agreement:</strong>
                    <input type="file" @change="handleFileChange" id="reservationAgreement" required/>
                    </li>
                    <li v-for="document in documentTypes" :key="document.id">
                      <strong>{{ document.name }}:</strong>
                      <br v-if="document.id === 'reservationAgreement'">
                      <input
                        v-if="document.id === 'reservationAgreement'"
                        type="file"
                        @change="handleFileChange"
                        :id="document.id"
                        required
                      />
                      <span v-else>{{ document.description }}</span>
                    </li>
                  </ul>
                </div>  

                <div
                class="d-flex justify-content-end gap-2 mt-30"
                style="padding-top: 15px"
                >
                  <button @click="submitToCustomer" class = "btn-add">Submit to Customer</button>
                  <button @click="closeModal" class = "btn-cancel">Close</button>
                </div>

                <!-- Loading Indicator -->
                <div v-if="loading" class="loading-overlay">
                  <div class="loading-spinner">
                    <div class="spinner"></div>
                    <p>Submitting...</p>
                  </div>
                </div>
                <!-- Display error message if there's an error -->
                <p v-if="errorMessage" class="error-message">
                  {{ errorMessage }}
                </p>

              </div>
          </div>
        </b-modal>

         <!-- Documents -->
        <b-modal v-model="showDocumentModal" hide-header hide-footer centered>
          <div class="modal-title p-3">
            <h5 class="mb-0">Customer Documents</h5>
          </div>

          <div class="p-3">
            <div v-if="showStatusMessage">
              <p>Waiting for Developer to confirm Reservation</p>
              <div class="button-container">
                <button
                  type="button"
                  @click="showDocumentModal = false"
                  class="btn-cancel-right"
                >
                  Close
                </button>
              </div>
            </div>
            <div v-else>
              <form @submit.prevent="uploadDocuments">
                <div class="document-upload-form">
                  <div
                    v-for="(docType, index) in documentTypes"
                    :key="index"
                    class="document-upload-section mb-3"
                  >
                    <label
                      :for="'documentType' + docType.id"
                      class="form-label"
                    >
                      <b> Upload {{ docType.name }} </b>
                    </label>

                    <div
                      class="file-input-wrapper d-flex align-items-center gap-2"
                    >
                      <!-- Show the file input if no file has been selected -->
                      <input
                        type="file"
                        :id="'documentType' + docType.id"
                        @change="handleFileUpload($event, docType.id)"
                        class="form-control"
                        v-if="!filePreviews[docType.id]"
                      />

                      <!-- Show the file name after file has been selected -->
                      <div
                        v-if="filePreviews[docType.id]"
                        class="d-flex align-items-center gap-2"
                      >
                        <span class="file-name">
                          {{ filePreviews[docType.id].name }}
                        </span>

                        <button
                          type="button"
                          @click="removeFile(docType.id)"
                          class="btn btn-danger btn-sm"
                        >
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="form-actions">
                  <div
                    class="d-flex justify-content-end gap-2 mt-30"
                    style="padding-top: 15px"
                  >
                    <button type="submit" class="btn-add" style="width: 150px">
                      Upload Document
                    </button>
                    <button
                      type="button"
                      @click="showDocumentModal = false"
                      class="btn-cancel"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </b-modal>
        <!-- Delete -->
         <b-modal
          v-model="showDeleteModal"
          title="Delete Confirmation"
          hide-footer
          centered
        >
          <p>
            Are you sure you want to delete this unit affiliation for this
            customer?
          </p>

          <div class="d-flex justify-content-end gap-2 mt-30" style="padding-top: 15px">
            <button
              type="button"
              @click="
                deleteSaleFromBackend(
                  selectedCustomer.sale_id
                )
              "
              class="btn-add"
            >
              Yes
            </button>
            <button
              type="button"
              @click="showDeleteModal = false"
              class="btn-cancel"
            >
              Cancel
            </button>
          </div>
        </b-modal>
        <b-modal
          v-model="showNotification"
          :title="notificationTitle"
          hide-footer
          centered
        >
          <p>{{ notificationMessage }}</p>
          <div class = "button-container">
            <button type="button" @click="showNotification = false" class = "btn-cancel-right">Close</button>
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
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "ManageSales",
  components: {
    SideNav,
    BModal,
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
      showDocumentModal: false, // Controls the visibility of the document modal
      selectedSale: {
      status: '', // Initialize with a default value
      },
      salesDetailsExists: false, // Flag to check if sales details already exist
      salesDetails: null, // S
      // Payment Scheme Data
      selectedPaymentPlan: "Spot Cash", // Default payment plan
      unitPrice: 0, // Example price of the unit
      spotCashDiscount: 0,
      maxSpotCashDiscount: 0, // Default value fetched from DB
      tlpDiscount: 0,
      maxotherChargesPercentage: 0,
      maxtlpDiscount:0,
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
      errorMessage: "", // Error message
      showDetailedSchedule: false, // To toggle detailed payment schedule
      loading: false, // Track loading state
      showStatusMessage: false,
      selectedCustomer: null, // To hold the currently selected customer
      documentFiles: {},
      filePreviews: {}, // Object to store file previews for each document type
      notificationMessage: "", // Message for the notification modal
      notificationTitle: "", // Title for the notification modal (Success/Failure)
      showNotification: false, // Controls the visibility of the notification modal
      showDeleteModal: false, // To toggle the delete modal visibility
      searchQuery: "", // New property for search input
      filteredCustomers: [], // Holds the filtered list based on search query


    };
  },
  mounted() {
    this.fetchSales(); // Fetch sales when the component is mounted
    this.fetchDocumentTypes(); // New function to fetch document types
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
     validateSpotCashDiscount() {
      if (this.spotCashDiscount < 0) {
        this.spotCashDiscount = 0;
      } else if (this.spotCashDiscount > this.maxSpotCashDiscount) {
        this.spotCashDiscount = this.maxSpotCashDiscount;
      }
    },
    filterCustomers() {
      const query = this.searchQuery.toLowerCase(); // Convert search query to lowercase for case-insensitive comparison

      if (!query) {
        // If there's no search query, show all customers
        this.filteredCustomers = this.sales;
      } else {
        // Filter customers by name or customer code
        this.filteredCustomers = this.sales.filter((customer) => {
          const customerName = customer.customer_name.toLowerCase();
          console.log(customerName);
          const customerCode = customer.customer_code
            ? customer.customer_code.toLowerCase()
            : ""; // Assuming customer code is in customer_code field
          return customerName.includes(query) || customerCode.includes(query);
        });
      }
    },
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
            this.filteredCustomers = this.sales; // Initialize filteredCustomers with all customers
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
      this.spotCashDiscount = this.selectedSale.spot_discount;
      this.maxSpotCashDiscount= this.spotCashDiscount; // Default value fetched from DB
      this.tlpDiscount = this.selectedSale.TLP_Discount;
      this.maxtlpDiscount = this.tlpDiscount;
      this.otherChargesPercentage = this.selectedSale.other_charges;
      this.maxotherChargesPercentage = this.otherChargesPercentage;
      this.reservationFee = this.selectedSale.reservation_fee;
      this.vat = this.selectedSale.vat_percent;

      // Check if the sales details already exist for this customer and unit
      this.checkSalesDetails();
      this.updatePaymentDetails();
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
      this.balanceUponTurnover =
        ((100 -
          (Number(this.spreadDownpaymentPercentage) +
            Number(this.spotDownpaymentPercentage))) /
          100) *
        this.totalAmountPayable; // Correct sum of percentages
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
        this.errorMessage =
          "All fields are required except the payment reference.";
        this.loading = false;
        return; // Stop further processing if validation fails
      }
      if (this.selectedPaymentPlan === "Deffered Payment" && this.netDownpayment < 0) {
        this.errorMessage = "Select Down Payment Percent";
        this.loading = false;
        return; // Stop further processing if validation fails
      }
      if (this.selectedPaymentPlan === "Deferred Payment" && (this.spreadDownpaymentPercentage <= 0)) {
        this.errorMessage = "Please specify a valid spread downpayment percentage for deferred payment.";
        this.loading = false;
        return; // Stop further processing
      }
      const formData = new FormData();
      // Add sales details
      formData.append("customer_id", this.selectedSale.customer_id);
      formData.append("site_id", this.selectedSale.site_id);
      formData.append("unit_id", this.selectedSale.unit_id);
      formData.append("sales_id", this.selectedSale.sale_id);
      formData.append("broker_id", this.selectedSale.broker_id);
      formData.append("payment_plan", this.selectedPaymentPlan);
      formData.append("spot_discount_percent", this.spotCashDiscount);
      formData.append("tlp_discount_percent", this.tlpDiscount);
      formData.append("other_charges_percent", this.otherChargesPercentage);
      formData.append(
        "spot_downpayment_percent",
        this.spotDownpaymentPercentage
      );
      formData.append("reservation_fee", this.reservationFee);
      formData.append(
        "spread_downpayment_percent",
        this.spreadDownpaymentPercentage
      );
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
        const response = await axios.post(
          `http://localhost:8000/mark/${this.selectedSale.customer_id}/${this.selectedSale.sale_id}/`
        );

        if (response.data.success) {
          // Successfully marked as sold
          alert("Unit successfully marked as sold!");
          // Optionally, update the UI to reflect this change (e.g., mark the unit in the list as sold)
        } else {
          // Handle failure (e.g., customer has not submitted all required documents)
          alert(response.data.message);
        }
      } catch (error) {
        console.error("Error marking unit as sold:", error);
        alert("An error occurred while marking the unit as sold.");
      }
    },
    redirectToLogin() {
      this.$router.push({ name: "BrkLogin" });
    },
    closeModal() {
      this.showModal = false;
      this.salesAgreement = {
        payment_plan: "",
        down_payment: "",
        installment_term: "",
        special_terms: "",
      };
    },
    // Opens the document upload modal for the selected customer
    openDocumentModal(sale) {
      this.selectedCustomer = sale; // Set the selected customer
      if (this.selectedCustomer.status === "Pending Reservation") {
        this.showStatusMessage = true; // Show the message to create sales first
      } else {
        this.showStatusMessage = false; // Show the message to create sales first
      }
      this.fetchCustomerDocuments(
        this.selectedCustomer.customer_id,
        this.selectedCustomer.sale_id
      );

      this.showDocumentModal = true; // Open the document upload modal
    },
    async fetchCustomerDocuments(customerId, salesId) {
      try {
        const response = await fetch(
          `http://localhost:8000/documents/customer/${customerId}/${salesId}/`
        );
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            // Store the documents in the component's data
            this.customerDocuments = data.documents; // An array of the customer's documents
            this.updateDocumentPreviews(); // Update the file previews based on existing documents
          } else {
            this.error = data.message || "Failed to fetch customer documents.";
          }
        }
      } catch (error) {
        this.error = "An error occurred while fetching customer documents.";
      }
    },
     // Update file previews based on existing documents
    updateDocumentPreviews() {
      // Initialize filePreviews as an empty object
      this.filePreviews = {};

      // Loop through each document type and check if it's already uploaded
      this.documentTypes.forEach((docType) => {
        const existingDoc = this.customerDocuments.find(
          (doc) => doc.document_type_id === docType.id
        );

        if (existingDoc) {
          // If a document exists for this document type, set the preview
          this.filePreviews[docType.id] = {
            name: existingDoc.file_name, // Use the file name from the database
            url: existingDoc.file_url, // Optionally, you could store the file URL for further use
          };
        }
      });
    },

    // Fetch document types from the API
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

    // Handle file selection for multiple document types
    handleFileUpload(event, docTypeId) {
      const file = event.target.files[0];
      if (file) {
        if (this.filePreviews[docTypeId]) {
          this.removeFile(docTypeId); // This will remove the old file
        }
        this.filePreviews[docTypeId] = file; // Store the file preview
        this.documentFiles[docTypeId] = file; // Store the actual file
      }
    },

    // Remove file preview and file data for a document type
    removeFile(docTypeId) {
      delete this.filePreviews[docTypeId];
      delete this.documentFiles[docTypeId];
    },

    // Upload multiple documents
    async uploadDocuments() {
      console.log("k");
      const formData = new FormData();

      // Loop through the documentFiles object to process each file and its document type
      for (const docTypeId in this.documentFiles) {
        const file = this.documentFiles[docTypeId];

        // Append the file and the associated document type to formData
        formData.append("files[]", file); // Append the file under "files[]"
        formData.append("document_types[]", docTypeId); // Append the document type ID under "document_types[]"
        formData.append("sales_id", this.selectedCustomer.sale_id);
      }

      // Append customer and company information
      formData.append("customer", this.selectedCustomer.customer_id);
      formData.append("company", this.companyId);
      // Log the formData for debugging

  
      try {
        const response = await fetch("http://localhost:8000/upload-document/", {
          method: "POST",
          body: formData,
          headers: {
            "X-CSRFToken": this.getCookie("csrftoken"),
          },
        });

        const data = await response.json();
        if (response.ok && data.success) {
          console.log("ll");
          this.notificationTitle = "Success!";
          this.notificationMessage = "Documents uploaded successfully!";
          this.showNotification = true;
          this.showDocumentModal = false;
          this.resetForm();
        } else {
          this.notificationTitle = "Error!";
          this.notificationMessage =
            data.message || "Failed to upload documents.";
          this.showNotification = true;
        }
      } catch (error) {
        this.showNotification = true;
      }
    },

    DeleteSaleModal(sale) {
      this.selectedCustomer = sale; // Set the selected customer
      this.showDeleteModal = true; // Show the modal
    },

    async deleteSaleFromBackend(salesId) {
      try {
        let url = "";
          // Otherwise, delete the sale
        url = `http://localhost:8000/delete_sale/${salesId}/`;
        // Send a POST request with DELETE override if CSRF protection is enabled
        const response = await fetch(url, {
          method: "POST", // Use POST with _method override
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.getCookie("csrftoken"),
          },
          body: JSON.stringify({ _method: "DELETE" }), // Overriding method to DELETE
        });

        if (response.ok) {
          this.notificationTitle = "Success!";
          this.notificationMessage = this.showSalesMessage
            ? "Customer Removed Successfully!"
            : "Customer Sale Removed Successfully!";
          this.showNotification = true;
          this.showDeleteModal = false; // Close the modal
          this.fetchSales();
        } else {
          this.notificationTitle = "Error!";
          this.notificationMessage = this.showSalesMessage
            ? "Customer Removal Failed!"
            : "Customer Sale Removal Failed!";
          this.showNotification = true;
          this.showDeleteModal = false; // Close the modal
          this.fetchSales();
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while deleting the sale or customer");
      }
    },
    // Reset the form when the modal is closed
    resetForm() {
      this.email = "";
      this.contactNumber = "";
      this.lastName = "";
      this.firstName = "";
      this.documentFiles = {}; // Clear the actual files
      // Optionally, clear any other form-related fields
      this.selectedCustomer = null; // Clear selected customer
    },
    
    getCookie(name) {
      let value = "; " + document.cookie;
      let parts = value.split("; " + name + "=");
      if (parts.length === 2) return parts.pop().split(";").shift();
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

/* Ensure .main-page fills the available space */
.main-page {
  display: flex;
  min-height: 100vh;
  /* Ensures it spans the full viewport height */
  background-color: #e8f0fa;
  /* Gray background */
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

.outside-headers {
  display: grid;
  grid-template-columns: 16% 16% 16% 16% 16% 16%; /* Adjust column widths */
  padding: 0px 18px;
  margin: 20px auto 10px;
  max-width: 1100px;
}

.header-item {
  flex: 1;
  text-align: left;
  font-size: 15px;
  color: #333;
  font-weight: bold;
  white-space: nowrap;
}

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  margin-top: 0;
  max-width: 1100px;
  /* Ensures the card and grid align */
  margin-left: auto;
  /* Centers the card */
  margin-right: auto;
}

.sales-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left; /* Consistent with headers */
}

.sales-table td {
  padding: 10px 0; /* Matches outside-headers padding */
}

.sales-table  td:nth-child(1),
.outside-headers .header-item:nth-child(1) {
  width: 16%;
}

.sales-table  td:nth-child(2),
.outside-headers .header-item:nth-child(2) {
  width: 16%;
}

.sales-table  td:nth-child(3),
.outside-headers .header-item:nth-child(3) {
  width: 16%;
}

.sales-table td:nth-child(4),
.outside-headers .header-item:nth-child(4) {
  width: 16%;
}

.sales-table td:nth-child(5),
.outside-headers .header-item:nth-child(5) {
  width: 16%;
}

.sales-table td:nth-child(6),
.outside-headers .header-item:nth-child(6) {
  width: 16%;
}




/* Flex container for button alignment */
.button-container {
  display: flex;
  justify-content: flex-end; /* Align button to the right */
}

/* Button styling */
.btn-cancel-right {
  background-color: #343a40; /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px; /* Adjust the border radius */
  padding: 10px;
  cursor: pointer;
}

.btn-add {
  background-color: #42b983;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
}

.btn-cancel {
  background-color: #343a40;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
}

/* Dropdown Styling */
.dropdown {
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

.customer-title{
  color: #6c757d;
  margin-bottom: 1px;
}

.info-box {
  background-color: #f8f9fa; /* Light gray background */
  border-radius: 8px; /* Rounded corners */
  padding: 15px; /* Padding for spacing */
  margin-bottom: 15px; /* Spacing between boxes */
}

/* juju end */

/* Modal Background */
.modal {
  width: 80%; 
  max-width: 800px; /* Ensure a max-width to prevent excessive stretching */
  height: 70%; 
  max-height: 600px; /* Optional */
  background-color: #fff; 
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); 
  border-radius: 10px; 
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 50%; 
  left: 50%; 
  transform: translate(-50%, -50%);
}

.modal-content {
  width: 100%; /* Adjust to parent width */
  padding: 20px;
  overflow-y: auto;
  text-align: left;
  height: 100%; /* Allow content to use the full height */
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

.sched-table, 
.sched-table th,
.sched-table td {
  border: 1px solid #ddd;
}

.sched-table th,
.sched-table td {
  padding: 10px;
  text-align: left;
}

.sched-table th {
  background-color: #f4f4f4;
}

.sched-table td {
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
  border: 1px solid #ccc;
  border-radius: 8px;
}

.form-group label {
  font-size: 16px; /* Increase label size */
  font-weight: bold; /* Make label bold */
  color: #0056b3; /* Use a professional blue tone */
  margin-bottom: 8px; /* Add spacing below the label */
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
.search-bar-container {
  position: relative;
  width: 100%;
  max-width: 400px;
  /* Adjust the width as needed */
}

.search-bar {
  width: 400px;
  padding: 8px 12px 8px 40px;
  /* Add left padding to make space for the icon */
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.search-icon {
  position: absolute;
  top: 50%;
  left: 10px;
  /* Position the icon inside the input */
  transform: translateY(-50%);
  color: #777;
  font-size: 16px;
  pointer-events: none;
  /* Prevent the icon from blocking clicks in the input */
}
</style>
