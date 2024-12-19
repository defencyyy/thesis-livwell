<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title"><strong>Manage Customer Sales</strong></div>
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
                  <!-- Sort Dropdown -->
                  <select
                    v-model="sortBy"
                    @change="sortCustomers"
                    class="dropdown"
                  >
                    <option value="All">All</option>
                    <option value="Sold">Sold</option>
                    <option value="Pending Sold">Pending Sold</option>
                    <option value="Reserved">Reserved</option>
                    <option value="Pending Reservation">Pending Reservation</option>
                    <!-- New sorting option -->
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Sales Table -->
        <div>
          <div class="outside-headers">
            <span class="header-item">Customer Name</span>
            <span class="header-item">Customer Code</span>
            <span class="header-item">Site Name</span>
            <span class="header-item">Unit Title</span>
            <span class="header-item">Status</span>
            <span class="header-item">Actions</span>
          </div>
        </div> 

        <div v-if="sales.length === 0">
            No sales found.
        </div>

        <div
        v-else
        v-for="sale in paginatedCustomers"
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
                    <span class = "customer-name">
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
                  <h5> {{ formatCurrency(salesDetails.unit_price) }} </h5>
                </div>
                <div class="col-md-6">
                  <h6 class = "customer-title">Payment Plan</h6>
                  <h5> {{ salesDetails.payment_plan }} </h5>
                </div>
              </div>
              <br>

              <div class = "sales-box">
                <h6><strong>Spot Discount</strong></h6>
                <div class = "sales-item">
                  <span class="label">Spot Discount Percentage:</span>
                  <span class="value">{{ salesDetails.spot_discount }}%</span>
                </div>
                <div class = "sales-item">
                  <span class="label">Spot Discount: </span>
                  <span class="value">{{ formatCurrency(this.spotDiscount) }}</span>
                </div>
                <div class = "sales-item">
                  <span class="label">Unit Price after Spot Discount:</span>
                  <span class="value">{{formatCurrency(this.unitPriceAfterSpotDiscount)}}</span>
                </div>
                <hr class="separator">
                <h6><strong>TLP Discount</strong></h6>
                <div class = "sales-item">
                  <span class="label">TLP Discount Percentage:</span>
                  <span class="value">{{ salesDetails.tlp_discount }}%</span>
                </div>
                <div class = "sales-item">
                  <span class="label">TLP Discount: </span>
                  <span class="value">{{ formatCurrency(this.tlpDiscountAmount) }}</span>
                </div>
                <div class = "sales-item">
                  <span class="label">Net Unit Price:</span>
                  <span class="value">{{ formatCurrency(netUnitPrice) }}</span>
                </div>
                <hr class="separator">
                <h6><strong>Other Charges</strong></h6>
                <div class = "sales-item">
                  <span class="label">Other Charges Percentage:</span>
                  <span class="value">{{ salesDetails.other_charges_percent }}%</span>
                </div>
                <div class = "sales-item">
                  <span class="label">Other Charges:</span>
                  <span class="value">{{ formatCurrency(otherCharges) }}</span>
                </div>
                <div class = "sales-item">
                  <span class="label">Net Unit Price:</span>
                  <span class="value">{{ formatCurrency(netUnitPrice) }}</span>
                </div>
                <hr class="separator">
                <div v-if="netUnitPrice > 3600000" class = "sales-item">
                  <span class="label">VAT (12%):</span>
                  <span class="value">{{ formatCurrency(vatAmount) }}</span>
                </div>
                <div class = "sales-item">
                  <span class="label">Total Amount Payable:</span>
                  <span class="value">{{formatCurrency(totalAmountPayable)}}</span>
                </div>
                <div v-if="salesDetails.payment_plan === 'Deffered Payment'" class = "sales-item">
                  <span class="label">Spot Downpayment Percentage:</span>
                  <span class="value">{{ salesDetails.spot_downpayment_percent }}% </span>
                </div>
                <div v-if="salesDetails.payment_plan === 'Deffered Payment'" class = "sales-item">
                  <span class="label">Spot Downpayment:</span>
                  <span class="value">₱{{ spotDownpayment }}</span>
                </div>
                <div class = "sales-item">
                  <span class="label">Reservation Fee:</span>
                  <span class="value">{{formatCurrency(salesDetails.reservation_fee)}}</span>
                </div>
                <div v-if="salesDetails.payment_plan === 'Spot Cash'" class = "sales-item">
                  <span class="label">Net Full Payment:</span>
                  <span class="value">{{ formatCurrency(netFullPayment) }}</span>
                </div>
                <div v-if="salesDetails.payment_plan === 'Deffered Payment'" class = "sales-item">
                  <span class="label">Net Downpayment:</span>
                  <span class="value">{{ formatCurrency(netDownpayment) }}</span>
                </div>
                <div v-if="salesDetails.payment_plan === 'Deffered Payment'" class = "sales-item">
                  <span class="label">Spread Downpayment Percentage:</span>
                  <span class="value">{{ salesDetails.spread_downpayment_percent }}%</span>
                </div>
                <div v-if="salesDetails.payment_plan === 'Deffered Payment'" class = "sales-item">
                  <span class="label">Spread Downpayment:</span>
                  <span class="value">₱{{ spreadDownpayment }}</span>
                </div>
                <div v-if="salesDetails.payment_plan === 'Deffered Payment'" class = "sales-item">
                  <span class="label">Payable Months:</span>
                  <span class="value">{{ salesDetails.payable_months }}</span>
                </div>
                <div v-if="salesDetails.payment_plan === 'Deffered Payment'" class = "sales-item">
                  <span class="label">Payable Per Month:</span>
                  <span class="value">₱{{ payablePerMonth }}</span>
                </div>
                <div v-if="salesDetails.payment_plan === 'Deffered Payment'" class = "sales-item">
                  <span class="label">Balance Upon Turnover:</span>
                  <span class="value">₱{{balanceUponTurnover}}</span>
                </div>
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
                <br>
                <div class="row">
                  <div class="col-md-6">
                    <h6 class = "customer-title">Unit Price</h6>
                    <h5> ₱{{ unitPrice }} </h5>
                  </div>
                  <div class="col-md-6">
                    <h6 class = "customer-title">Payment Plan</h6>
                    <div class = "form-group">
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
                  </div>
                </div>

                <div class="line mb-4"></div>

                <form>
                  <div class = "row">
                    <div class = "col-md-6">
                      <div class = "mb-3">
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
                        <p class = "p-label"><strong>Spot Discount:</strong> ₱{{ spotDiscount }}</p>
                        <p class = "p-label">
                          <strong>Unit Price after Spot Discount:</strong> ₱{{
                            unitPriceAfterSpotDiscount
                          }}
                        </p>
                      </div>
                      <div class = "mb-3">
                        <label for="otherChargesPercentage" class="form-label text-start">Other Charges (%)</label>
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
                        <p class = "p-label"><strong>Other Charges:</strong> ₱{{ otherCharges }}</p>

                        <!-- VAT Calculation -->
                        <p v-if="netUnitPrice > 3600000" class = "p-label">
                          <strong>VAT (12%):</strong> ₱{{ vatAmount }}
                        </p>

                        <!-- Total Amount Payable -->
                        <p class = "p-label">
                          <strong>Total Amount Payable:</strong> ₱{{
                            totalAmountPayable
                          }}
                        </p>

                      </div>
                      <br><br>
                      <div v-if="selectedPaymentPlan === 'Deffered Payment'">
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
                        <p class = "p-label">
                          <strong>Spread Downpayment:</strong> ₱{{
                            spreadDownpayment
                          }}
                        </p>
                      </div>
                    </div>

                    <div class = "col-md-6">
                      <div class = "mb-3">
                        <label for="tlpDiscount" class="form-label text-start">LP Discount (Optional)</label>
                        <input
                        type="number"
                        id="tlpDiscount"
                        v-model="tlpDiscount"
                        @input="updatePaymentDetails"
                        class="form-control"
                        min="0"
                        max="maxtlpDiscount"
                      />

                      <p class = "p-label"><strong>TLP Discount:</strong> ₱{{ tlpDiscountAmount }}</p>
                      <!-- Net Unit Price -->
                      <p class = "p-label"><strong>Net Unit Price:</strong> ₱{{ netUnitPrice }}</p>
                      </div>

                      <div v-if="selectedPaymentPlan === 'Deffered Payment'" class = "mb-3">
                        <label for="spotDownpayment" class="form-label text-start">Spot Downpayment</label>
                        <input
                          type="number"
                          id="spotDownpayment"
                          v-model="spotDownpaymentPercentage"
                          @input="updatePaymentDetails"
                          class="form-control"
                          min="0"
                          step="5"
                          placeholder="Enter downpayment percentage"
                          required
                        />
                        <p v-if="selectedPaymentPlan === 'Deffered Payment'" class = "p-label">
                          <strong>Spot Downpayment:</strong> ₱{{ spotDownpayment }}
                        </p>

                        <!-- Reservation Fee -->
                        <p class = "p-label" ><strong>Reservation Fee:</strong> ₱{{ reservationFee }}</p>
                        <p v-if="selectedPaymentPlan === 'Spot Cash'" class = "p-label" >
                          <strong>Net Full Payment:</strong> ₱{{ netFullPayment }}
                        </p>

                        <!-- Net Downpayment -->
                        <p v-if="selectedPaymentPlan === 'Deffered Payment'" class = "p-label">
                          <strong>Net Downpayment:</strong> ₱{{ netDownpayment }}
                        </p>
                      </div>

                      <br>
                      <div v-if="selectedPaymentPlan === 'Deffered Payment'" class = "mb-3">
                        <label for="months" class="form-label text-start">Months to Pay</label>
                        <input
                          type="number"
                          v-model="payableMonths"
                          id="months"
                          @input="updatePaymentDetails"
                          class="form-control"
                          min="1"
                          max="maxpayableMonths"
                          step="1"
                          required
                        />
                        <p class = "p-label">
                          <strong>Payable Per Month:</strong> ₱{{ payablePerMonth }}
                        </p>

                        <!-- Balance Upon Turnover -->
                        <p class = "p-label">
                          <strong>Balance Upon Turnover:</strong> ₱{{
                            balanceUponTurnover
                          }}
                        </p>
                      </div>
                    </div>
                  </div>
                </form>

                <div class="line mb-4"></div>

                <!-- Required Documents Section (Always Displayed) -->
                <div class="form-group">
                  <div class="col-12 text-center mb-3 text-center">
                    <h5 class="property-header">Required Documents</h5>
                  </div>
                  <ul>
                    <li>
                    <strong>Reservation Agreement</strong><br>
                    <input type="file" @change="handleFileChange" id="reservationAgreement"   ref="reservationAgreementInput"  required/>
                    </li>
                    <li v-for="document in documentTypes" :key="document.id">
                      <strong>{{ document.name }}</strong>
                      <br v-if="document.id === 'reservationAgreement'">
                      <input
                        v-if="document.id === 'reservationAgreement'"
                        type="file"
                        @change="handleFileChange"
                        :id="document.id"
                        class = "form-control"
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
          title="Cancel Confirmation"
          hide-footer
          centered
        >
          <p>
            Are you sure you want to cancel this Sale affiliation for this
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
     // Filter and sort customers dynamically
sortedAndFilteredCustomers() {
  const query = this.searchQuery.toLowerCase();
  const filtered = this.sales.filter((customer) => {
    const customerName = customer.customer_name.toLowerCase();
    const customerCode = customer.customer_code ? customer.customer_code.toLowerCase() : "";
    return !query || customerName.includes(query) || customerCode.includes(query);
  });

  // Filter by the selected status
  if (this.sortBy && this.sortBy !== 'All') {
    return filtered.filter((sale) => sale.status === this.sortBy);
  }

  // Sort by status if needed
  return filtered.sort((a, b) => {
    const statusOrder = {
      'Sold': 1,
      'Pending Sold': 2,
      'Reserved': 3,
      'Pending Reservation': 4
    };
    const statusComparison = statusOrder[a.status] - statusOrder[b.status];
    return statusComparison !== 0 ? statusComparison : 0;
  });
},
  // Paginate filtered and sorted customers
  paginatedCustomers() {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    return this.sortedAndFilteredCustomers.slice(startIndex, endIndex);
  },

  // Total pages based on filtered customers
  totalPages() {
    return Math.ceil(this.sortedAndFilteredCustomers.length / this.itemsPerPage);
    },
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
      payableMonths: 1,
      maxpayableMonths: 0,
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
      currentPage: 1, // Current page number
      itemsPerPage: 15, // Number of customers per page
      sortBy: "All", // Selected sorting option (default is "Name (A-Z)")

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
    formatCurrency(amount) {
    if (isNaN(amount)) return "₱0.00";  // Return '₱0.00' if the amount is not a number
    return new Intl.NumberFormat("en-PH", {
      style: "currency",
      currency: "PHP",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
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
    goToPage(pageNumber) {
      if (pageNumber > 0 && pageNumber <= this.totalPages) {
        this.currentPage = pageNumber;
      }
    },
     validateSpotCashDiscount() {
      if (this.spotCashDiscount < 0) {
        this.spotCashDiscount = 0;
      } else if (this.spotCashDiscount > this.maxSpotCashDiscount) {
        this.spotCashDiscount = this.maxSpotCashDiscount;
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
            this.sortCustomers();
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
      this.payableMonths = this.selectedSale.months;
      this.maxpayableMonths = this.payableMonths;
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
       if (this.payableMonths < 0) {
        this.payableMonths = 1;
      } else if (this.payableMonths > this.maxpayableMonths) {
        this.payableMonths = this.maxpayableMonths;
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
        this.$refs.reservationAgreementInput.setCustomValidity("");

      }
    },

    async submitToCustomer() {
      this.loading = true;
      this.updatePaymentDetails();

      // Check if the selected payment plan is "Spot Cash" and validate required fields
      if (!this.file) {
        this.$refs.reservationAgreementInput.setCustomValidity("Please upload the required reservation agreement file.");
        this.$refs.reservationAgreementInput.reportValidity();
        this.loading = false;
        return; // Stop further processing if validation fails
      }
      if (  this.selectedPaymentPlan === "Deffered Payment" &&(this.netDownpayment < 0 || this.spreadDownpaymentPercentage <= 0)
      ) {
        this.notificationTitle = "Error!";
        this.notificationMessage = "Please specify a valid spread downpayment percentage!";
        this.showNotification = true; // Show the notification modal
        this.loading = false;
        return; // Stop further processing if validation fails
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
          this.notificationTitle = "Success!";
          this.notificationMessage = "Sales agreement submitted successfully!";
          this.showNotification = true; // Show the notification modal
          this.closeModal(); // Close the modal after submission
        } else {
          alert("Error: " + response.data.message);
        }
      } catch (error) {
        this.notificationTitle = "Error!";
        this.notificationMessage = error.response.data.message || "Failed to add customer.";
        this.showNotification = true; // Show the notification modal
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
          this.notificationTitle = "Success!";
          this.notificationMessage = "Unit successfully marked as sold!";
          this.showNotification = true;
          this.showModal=false;
          this.fetchSales();

        } else {
          this.notificationTitle = "Failed!";
          this.notificationMessage = "Customer has not submitted all required documents!";
          this.showNotification = true;
          this.showModal=false;
          this.fetchSales();

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
        const response = await fetch(`http://localhost:8000/document-types/?company_id=${this.companyId}`);
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
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.main-page {
  display: flex;
  min-height: 100vh;
  background-color: #e8f0fa;
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
  grid-template-columns: 25% 15% 15% 15% 20% 10%;
  padding: 0px 18px;
  margin: 20px auto 10px;
  max-width: 1100px;
}

.header-item {
  flex: 1;
  text-align: left;
  font-size: 14px;
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
  margin-left: auto;
  margin-right: auto;
}

.customer-name {
  font-weight: bold;
}

.sales-table {
  width: 100%;
  font-size: 14px;
  border-collapse: collapse;
  text-align: left;
}

.sales-table td {
  padding: 10px 0;
}

.sales-table td:nth-child(1),
.outside-headers .header-item:nth-child(1) {
  width: 25%;
}

.sales-table td:nth-child(2),
.outside-headers .header-item:nth-child(2) {
  width: 15%;
}

.sales-table td:nth-child(3),
.outside-headers .header-item:nth-child(3) {
  width: 15%;
}

.sales-table td:nth-child(4),
.outside-headers .header-item:nth-child(4) {
  width: 15%;
}

.sales-table td:nth-child(5),
.outside-headers .header-item:nth-child(5) {
  width: 20%;
}

.sales-table td:nth-child(6),
.outside-headers .header-item:nth-child(6) {
  width: 10%;
}

.button-container {
  display: flex;
  justify-content: flex-end; 
}

.btn-cancel-right {
  background-color: #343a40; 
  color: #fff;
  border: none;
  border-radius: 3px; 
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

.dropdown {
  padding: 8px 12px;
  height: 38px;
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
  background-color: #f8f9fa; 
  border-radius: 8px; 
  padding: 15px; 
  margin-bottom: 15px; 
}

.line {
    border-top: 2px solid  #6c757d;; 
    width: 100%; 
    margin: 0 auto; 
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
  border-radius: 5px;
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
  border: 4px solid #f3f3f3; 
  border-top: 4px solid #3498db; 
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

.form-group {
  margin-bottom: 15px;
}

.form-group select {
  background-color: white; 
  color: black; 
  padding: 8px;
  border: 1px solid #ccc; 
  border-radius: 5px;
  font-size: 14px;
  width: 100%; 
  cursor: pointer;
}

.form-group select:focus {
  outline: none;
  border-color: #007bff; 
}

.form-group select:hover {
  color: black; 
}

input[type="file"] {
  border: 1px solid #ccc;
  border-radius: 8px;
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

.search-bar-container {
  position: relative;
  width: 100%;
  max-width: 400px;
}

.search-bar {
  width: 400px;
  padding: 8px 12px 8px 40px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.search-icon {
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
  color: #777;
  font-size: 16px;
  pointer-events: none;
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


.sales-box {
  min-width: 300px;
  background-color: #f8f9fa; 
  border-radius: 8px;
  padding: 20px;
  overflow-y: auto;
}

.sales-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-size: 16px;
}

.sales-item .label {
  color: #555;
}

.s-item .value {
  font-weight: bold;
  color: #000;
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

.form-label {
  color: #333;
}

.p-label {
  margin: 5px 0;
  font-size: 0.9rem;
  text-align: center;
}

.align-field {
  margin-top: 43px;
}

/* Responsive layout tweaks */
@media (max-width: 1440px) {
  .main-page {
    flex-direction: column;
  }

  .main-content {
    margin-left: 0;
  }

  .outside-headers {
    grid-template-columns: 25% 15% 15% 15% 20% 10%;
  }

  .sales-table td {
    padding: 8px;
  }
}

@media (max-width: 1080px) {
  .title-wrapper {
    flex-direction: column;
    align-items: center;
  }

  .sales-table td {
    font-size: 13px;
  }

  .card {
    max-width: 100%;
    margin-left: 0;
    margin-right: 0;
  }

  .button-container {
    justify-content: center;
  }

  .search-bar {
    width: 100%;
    max-width: 300px;
  }

  .pagination-controls {
    justify-content: center;
  }
}

@media (max-width: 720px) {
  .outside-headers {
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }

  .sales-table td {
    padding: 6px;
    font-size: 12px;
  }

  .button-container {
    flex-direction: column;
    align-items: center;
  }

  .card {
    max-width: 100%;
  }

  .modal {
    width: 90%;
    height: 60%;
  }

  .modal-content {
    height: 100%;
    overflow-y: auto;
  }

  .search-bar {
    width: 100%;
    max-width: 250px;
  }

  .page-button {
    font-size: 10px;
    padding: 4px 8px;
  }
}
.dropdown {
  padding: 8px 12px;
  height: 38px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  width: 80%;
  max-width: 150px;
  background-color: white;
  color: #333;
}
.left-section {
  display: flex;
  align-items: center;
  gap: 10px;
}


</style>
