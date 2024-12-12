<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">Company Site Management</div>
          </div>

          <div class="view-switch">
            <div
              class="view-icon"
              :class="{ active: viewMode === 'grid' }"
              @click="viewMode = 'grid'"
            >
              <i class="fa fa-th"></i>
              <!-- Grid Icon -->
            </div>
            <div class="separator"></div>
            <div
              class="view-icon"
              :class="{ active: viewMode === 'table' }"
              @click="viewMode = 'table'"
            >
              <i class="fa fa-list"></i>
              <!-- Table Icon -->
            </div>
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
                      placeholder="Search Site"
                      class="search-bar"
                    />
                    <i class="fa fa-search search-icon"></i>
                  </div>

                  <!-- Sort Dropdown -->
                  <select v-model="sortBy" class="dropdown">
                    <option value="name">Sort: Name</option>
                    <option value="status">Sort: Status</option>
                    <option value="creation">Sort: Date Created</option>
                  </select>

                  <select
                    v-model="viewFilter"
                    @change="toggleArchived"
                    class="dropdown2"
                  >
                    <option value="active">View: Active</option>
                    <option value="archived">View: Archived</option>
                  </select>
                </div>

                <div class="right-section">
                  <!-- Add Site Button -->
                  <button
                    @click="showAddModal = true"
                    class="btn-primary add-button"
                  >
                    Add Site
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Grid View -->
        <div v-if="viewMode === 'grid'" class="site-grid">
          <div
            v-for="(site, index) in filteredSites"
            :key="site.id || index"
            class="site-card"
            @click="openEditModal(site)"
          >
            <!-- Site Image -->
            <img
              :src="getPictureUrl(site.picture) || require('@/assets/home.png')"
              alt="Site Image"
              class="site-image"
            />

            <!-- Site Name -->
            <h2 class="site-name">
              {{ site.name || "Unknown" }}
            </h2>

            <!-- Site Location -->
            <p class="site-location">
              {{ site.location || "Location unavailable" }}
            </p>
          </div>
        </div>

        <!-- Table View -->
        <div v-if="viewMode === 'table'">
          <!-- Headers outside the card -->
          <div class="outside-headers">
            <span class="header-item">Name</span>
            <span class="header-item">Location</span>
            <span class="header-item">Status</span>
            <span class="header-item">Actions</span>
          </div>

          <!-- Table inside the card -->
          <div
            v-for="(site, index) in paginatedSites"
            :key="site.id || index"
            class="card border-0 rounded-1 mx-auto"
            style="
              max-width: 1100px;
              box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <div class="card-body">
              <table class="site-table">
                <tbody>
                  <tr>
                    <td>
                      <div class="site-info">
                        <img
                          :src="
                            getPictureUrl(site.picture) ||
                            require('@/assets/home.png')
                          "
                          alt="Site Image"
                          class="table-image"
                        />
                        <span class="site-name">
                          {{ site.name || "Unknown" }}
                        </span>
                      </div>
                    </td>
                    <td>{{ site.location || "Location unavailable" }}</td>
                    <td>
                      {{ site.status.toUpperCase() || "Status unavailable" }}
                    </td>

                    <td>
                      <!-- Three Dots Icon for each row -->
                      <button
                        class="btn btn-link"
                        type="button"
                        @click.stop="toggleDropdown(site)"
                        style="
                          border: none;
                          background-color: transparent;
                          color: #343a40;
                          cursor: pointer;
                          font-size: 18px;
                        "
                      >
                        <i class="fas fa-ellipsis-h"></i>
                        <!-- Horizontal Three Dots Icon -->
                      </button>

                      <!-- Dropdown Menu -->
                      <div
                        v-if="isDropdownVisible(site)"
                        class="dropdown-menu show"
                        style="position: absolute; right: 0"
                      >
                        <a
                          class="dropdown-item"
                          href="#"
                          @click.stop="openEditModal(site)"
                          >Edit</a
                        >

                        <a
                          class="dropdown-item"
                          v-if="!site.archived"
                          href="#"
                          @click.stop="archiveSite(site)"
                          >Archive</a
                        >
                        <a
                          class="dropdown-item"
                          v-else
                          href="#"
                          @click.stop="unarchiveSite(site)"
                          >Unarchive</a
                        >
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Pagination Controls -->
        <div class="pagination-controls">
          <button
            @click="goToPage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="page-button"
          >
            Previous
          </button>
          <span v-for="page in totalPages" :key="page">
            <button
              @click="goToPage(page)"
              :class="{ active: page === currentPage }"
              class="page-button"
            >
              {{ page }}
            </button>
          </span>
          <button
            @click="goToPage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="page-button"
          >
            Next
          </button>
        </div>

        <b-modal
          v-model="showAddModal"
          hide-header
          hide-footer
          centered
          size="lg"
        >
          <div class="modal-title p-3">
            <h5 class="mb-0">New Site</h5>
          </div>
          <div class="p-3">
            <form @submit.prevent="addSite">
              <div class="row">
                <!-- Left Side (Site Name to Status) -->
                <div class="col-md-6">
                  <!-- Site Name -->
                  <div class="form-group mb-3">
                    <label for="siteName" class="form-label">Site Name</label>
                    <input
                      type="text"
                      v-model="newSite.name"
                      id="siteName"
                      class="form-control"
                      required
                    />
                  </div>

                  <!-- Location -->
                  <div class="row mb-3">
                    <!-- Region Dropdown -->
                    <div class="col-md-6">
                      <label for="region" class="form-label">Region</label>
                      <select
                        v-model="selectedRegion"
                        id="region"
                        class="form-select"
                        @change="loadProvinceData(selectedRegion)"
                      >
                        <option
                          v-for="region in regionOptions"
                          :key="region"
                          :value="region"
                        >
                          {{ region }}
                        </option>
                      </select>
                    </div>

                    <!-- Province Dropdown -->
                    <div class="col-md-6">
                      <label for="province" class="form-label">Province</label>
                      <select
                        v-model="selectedProvince"
                        id="province"
                        class="form-select"
                        @change="loadMunicipalityData(selectedProvince)"
                      >
                        <option
                          v-for="province in provinceOptions"
                          :key="province"
                          :value="province"
                        >
                          {{ province }}
                        </option>
                      </select>
                    </div>
                  </div>

                  <!-- Municipality Dropdown -->
                  <div class="form-group mb-3">
                    <label for="municipality" class="form-label"
                      >Municipality</label
                    >
                    <select
                      v-model="selectedMunicipality"
                      id="municipality"
                      class="form-select"
                      @change="loadBarangayData(selectedMunicipality)"
                    >
                      <option
                        v-for="municipality in municipalityOptions"
                        :key="municipality"
                        :value="municipality"
                      >
                        {{ municipality }}
                      </option>
                    </select>
                  </div>

                  <!-- Barangay Dropdown -->
                  <div class="form-group mb-3">
                    <label for="barangay" class="form-label">Barangay</label>
                    <select
                      v-model="newSite.barangay"
                      id="barangay"
                      class="form-select"
                      required
                    >
                      <option
                        v-for="barangay in barangayOptions"
                        :key="barangay"
                        :value="barangay"
                      >
                        {{ barangay }}
                      </option>
                    </select>
                  </div>

                  <!-- Address Field (New) -->
                  <div class="form-group mb-3">
                    <label for="address" class="form-label"
                      >Additional Address</label
                    >
                    <input
                      type="text"
                      v-model="newSite.address"
                      id="address"
                      class="form-control"
                      placeholder="Enter additional address"
                    />
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label for="postalCode" class="form-label"
                        >Postal Code</label
                      >
                      <input
                        type="text"
                        v-model="newSite.postalCode"
                        id="postalCode"
                        class="form-control"
                      />
                    </div>

                    <div class="col-md-6">
                      <label for="siteStatus" class="form-label">Status</label>
                      <select
                        v-model="newSite.status"
                        id="siteStatus"
                        class="form-select"
                        required
                      >
                        <option
                          v-for="status in statusOptions"
                          :key="status"
                          :value="status"
                        >
                          {{ status.toUpperCase() }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>

                <!-- Right Side (Photo Upload with Preview) -->
                <div class="col-md-6">
                  <!-- Image Upload Section -->
                  <div class="form-group mb-3">
                    <label for="sitePicture" class="form-label"
                      >Upload Photo</label
                    >
                    <input
                      type="file"
                      @change="handlePictureUpload"
                      id="sitePicture"
                      class="form-control"
                      accept="image/*"
                    />
                  </div>

                  <!-- Image Preview Section -->
                  <div v-if="imagePreview" class="text-center">
                    <h6>Image Preview</h6>
                    <img
                      :src="imagePreview"
                      alt="Image Preview"
                      class="img-fluid"
                      style="max-height: 200px; object-fit: cover"
                    />
                  </div>
                </div>

                <!-- New Fields for Commission, Discounts, and Charges -->
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="commission" class="form-label"
                      >Commission (Total)</label
                    >
                    <input
                      type="number"
                      v-model="newSite.commission"
                      id="commission"
                      class="form-control"
                      placeholder="Enter commission"
                      min="0"
                      required
                    />
                  </div>

                  <div class="col-md-6">
                    <label for="spotDiscountPercentage" class="form-label"
                      >Spot Discount Percentage</label
                    >
                    <input
                      type="number"
                      v-model="newSite.spot_discount_percentage"
                      id="spotDiscountPercentage"
                      class="form-control"
                      placeholder="Enter spot discount percentage"
                      min="0"
                    />
                  </div>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="spotDiscountFlat" class="form-label"
                      >Spot Discount Flat</label
                    >
                    <input
                      type="number"
                      v-model="newSite.spot_discount_flat"
                      id="spotDiscountFlat"
                      class="form-control"
                      placeholder="Enter flat discount amount"
                      min="0"
                    />
                  </div>

                  <div class="col-md-6">
                    <label for="vatPercentage" class="form-label"
                      >VAT Percentage</label
                    >
                    <input
                      type="number"
                      v-model="newSite.vat_percentage"
                      id="vatPercentage"
                      class="form-control"
                      placeholder="Enter VAT percentage"
                      min="0"
                      required
                    />
                  </div>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="reservationFee" class="form-label"
                      >Reservation Fee</label
                    >
                    <input
                      type="number"
                      v-model="newSite.reservation_fee"
                      id="reservationFee"
                      class="form-control"
                      placeholder="Enter reservation fee"
                      min="0"
                    />
                  </div>

                  <div class="col-md-6">
                    <label for="otherCharges" class="form-label"
                      >Other Charges</label
                    >
                    <input
                      type="number"
                      v-model="newSite.other_charges"
                      id="otherCharges"
                      class="form-control"
                      placeholder="Enter other charges"
                      min="0"
                    />
                  </div>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="numberOfSections" class="form-label"
                      >Number of Sections</label
                    >
                    <input
                      type="number"
                      v-model="newSite.number_of_sections"
                      id="numberOfSections"
                      class="form-control"
                      placeholder="Enter the number of sections"
                      min="1"
                      required
                    />
                  </div>

                  <div class="col-md-6">
                    <label for="maximumMonths" class="form-label"
                      >Maximum Months to Pay</label
                    >
                    <input
                      type="number"
                      v-model="newSite.maximum_months"
                      id="maximumMonths"
                      class="form-control"
                      placeholder="Enter the maximum months to pay"
                      min="1"
                      required
                    />
                  </div>
                </div>
                <!-- New Fields for Numbering Type and Section Label -->
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="numberingType" class="form-label"
                      >Numbering Type</label
                    >
                    <select
                      v-model="newSite.numbering_type"
                      id="numberingType"
                      class="form-select"
                      required
                    >
                      <option value="numeric">Numeric (1, 2, 3,...)</option>
                      <option value="alphabetic">
                        Alphabetic (A, B, C,...)
                      </option>
                    </select>
                  </div>

                  <div class="col-md-6">
                    <label for="sectionLabel" class="form-label"
                      >Section Label</label
                    >
                    <select
                      v-model="newSite.section_label"
                      id="sectionLabel"
                      class="form-select"
                      required
                    >
                      <option value="floor">Floor</option>
                      <option value="block">Block</option>
                      <option value="unit">Unit</option>
                      <option value="unit">Section</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Buttons -->
              <div
                class="d-flex justify-content-end gap-2 mt-3"
                style="padding-top: 15px"
              >
                <button type="submit" class="btn-add" style="width: 150px">
                  Add New Site
                </button>
                <button
                  type="button"
                  @click="showAddModal = false"
                  class="btn-cancel"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </b-modal>

        <!-- View and Edit Site Modal -->
        <b-modal
          v-model="showEditModal"
          title="Site Details / Edit"
          hide-header
          hide-footer
          centered
          size="lg"
        >
          <div class="modal-title p-3">
            <h5 class="mb-0">Site Details / Edit</h5>
          </div>
          <div class="p-3">
            <form @submit.prevent="updateSite">
              <div class="row">
                <!-- Left Side (Site Name to Status) -->
                <div class="col-md-6">
                  <!-- Site Name (Read-Only) -->
                  <div class="form-group mb-3">
                    <label for="editSiteName" class="form-label"
                      >Site Name</label
                    >
                    <input
                      type="text"
                      v-model="editSite.name"
                      id="editSiteName"
                      class="form-control"
                      readonly
                    />
                  </div>

                  <!-- Location Fields (Region, Province, etc.) (Read-Only) -->
                  <div class="row mb-3">
                    <!-- Region -->
                    <div class="col-md-6">
                      <label for="editRegion" class="form-label">Region</label>
                      <input
                        type="text"
                        v-model="editSite.region"
                        id="editRegion"
                        class="form-control"
                        readonly
                      />
                    </div>

                    <!-- Province -->
                    <div class="col-md-6">
                      <label for="editProvince" class="form-label"
                        >Province</label
                      >
                      <input
                        type="text"
                        v-model="editSite.province"
                        id="editProvince"
                        class="form-control"
                        readonly
                      />
                    </div>
                  </div>

                  <!-- Municipality -->
                  <div class="form-group mb-3">
                    <label for="editMunicipality" class="form-label"
                      >Municipality</label
                    >
                    <input
                      type="text"
                      v-model="editSite.municipality"
                      id="editMunicipality"
                      class="form-control"
                      readonly
                    />
                  </div>

                  <!-- Barangay -->
                  <div class="form-group mb-3">
                    <label for="editBarangay" class="form-label"
                      >Barangay</label
                    >
                    <input
                      type="text"
                      v-model="editSite.barangay"
                      id="editBarangay"
                      class="form-control"
                      readonly
                    />
                  </div>

                  <!-- Address (Editable as Single String) -->
                  <div class="form-group mb-3">
                    <label for="editAddress" class="form-label"
                      >Additional Address</label
                    >
                    <input
                      type="text"
                      v-model="editSite.address"
                      id="editAddress"
                      class="form-control"
                      placeholder="Enter additional address"
                    />
                  </div>

                  <!-- Postal Code -->
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label for="editPostalCode" class="form-label"
                        >Postal Code</label
                      >
                      <input
                        type="text"
                        v-model="editSite.postalCode"
                        id="editPostalCode"
                        class="form-control"
                      />
                    </div>

                    <!-- Status (Editable) -->
                    <div class="col-md-6">
                      <label for="editSiteStatus" class="form-label"
                        >Status</label
                      >
                      <select
                        v-model="editSite.status"
                        id="editSiteStatus"
                        class="form-select"
                        required
                      >
                        <option
                          v-for="status in statusOptions"
                          :key="status"
                          :value="status"
                        >
                          {{ status.toUpperCase() }}
                        </option>
                      </select>
                    </div>
                  </div>

                  <!-- Maximum Months Field -->
                  <div class="form-group mb-3">
                    <label for="editMaximumMonths" class="form-label"
                      >Maximum Months to Pay</label
                    >
                    <input
                      type="number"
                      v-model="editSite.maximum_months"
                      id="editMaximumMonths"
                      class="form-control"
                      readonly
                    />
                  </div>
                </div>

                <!-- Right Side (Image Upload with Preview) -->
                <div class="col-md-6">
                  <!-- Display Current Picture (if any) -->
                  <div class="mb-3">
                    <label for="current-picture" class="form-label"
                      >Current Picture</label
                    >
                    <div v-if="editSite.picture">
                      <img
                        :src="getPictureUrl(editSite.picture)"
                        alt="Current Site Picture"
                        class="img-fluid rounded shadow-sm"
                        style="max-width: 150px; max-height: 150px"
                      />
                    </div>
                    <div v-else>
                      <p>No current picture available.</p>
                    </div>
                  </div>

                  <!-- Upload New Picture -->
                  <div class="mb-3">
                    <label for="picture" class="form-label"
                      >Upload New Picture</label
                    >
                    <input
                      type="file"
                      class="form-control"
                      id="picture"
                      accept="image/*"
                      @change="handlePictureUpload($event, 'edit')"
                    />
                  </div>

                  <!-- Preview of Uploaded Picture -->
                  <div class="mb-3">
                    <strong>Preview:</strong>
                    <div v-if="imagePreview">
                      <img
                        :src="imagePreview"
                        alt="Site Picture Preview"
                        class="img-fluid rounded shadow-sm"
                        style="max-width: 150px; max-height: 150px"
                      />
                    </div>
                    <p v-else>No picture selected</p>
                  </div>
                </div>
              </div>

              <!-- Commission and Charges -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="editCommission" class="form-label"
                    >Commission (Total)</label
                  >
                  <input
                    type="number"
                    v-model="editSite.commission"
                    id="editCommission"
                    class="form-control"
                    min="0"
                    required
                  />
                </div>

                <div class="col-md-6">
                  <label for="editSpotDiscountPercentage" class="form-label"
                    >Spot Discount (%)</label
                  >
                  <input
                    type="number"
                    v-model="editSite.spot_discount_percentage"
                    id="editSpotDiscountPercentage"
                    class="form-control"
                    min="0"
                  />
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="editSpotDiscountFlat" class="form-label"
                    >Spot Discount (Flat)</label
                  >
                  <input
                    type="number"
                    v-model="editSite.spot_discount_flat"
                    id="editSpotDiscountFlat"
                    class="form-control"
                    min="0"
                  />
                </div>

                <div class="col-md-6">
                  <label for="editVatPercentage" class="form-label"
                    >VAT Percentage</label
                  >
                  <input
                    type="number"
                    v-model="editSite.vat_percentage"
                    id="editVatPercentage"
                    class="form-control"
                    min="0"
                    required
                  />
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="editReservationFee" class="form-label"
                    >Reservation Fee</label
                  >
                  <input
                    type="number"
                    v-model="editSite.reservation_fee"
                    id="editReservationFee"
                    class="form-control"
                    min="0"
                  />
                </div>

                <div class="col-md-6">
                  <label for="editOtherCharges" class="form-label"
                    >Other Charges</label
                  >
                  <input
                    type="number"
                    v-model="editSite.other_charges"
                    id="editOtherCharges"
                    class="form-control"
                    min="0"
                  />
                </div>
              </div>

              <!-- Number of Sections (Editable) -->
              <div class="form-group mb-3">
                <div class="row">
                  <!-- Current Number of Sections -->
                  <div class="col-md-4">
                    <label for="numberOfSections" class="form-label"
                      >Current Number of Sections</label
                    >
                    <input
                      type="number"
                      v-model="editSite.number_of_sections"
                      id="numberOfSections"
                      class="form-control"
                      placeholder="Current Sections"
                      min="1"
                      readonly
                    />
                  </div>

                  <!-- Add Sections -->
                  <div class="col-md-4">
                    <label for="addSections" class="form-label"
                      >Add Sections</label
                    >
                    <input
                      type="number"
                      v-model="newSectionsToAdd"
                      id="addSections"
                      class="form-control"
                      placeholder="Add Sections"
                      min="0"
                    />
                  </div>

                  <!-- Total Sections -->
                  <div class="col-md-4">
                    <label for="totalSections" class="form-label"
                      >Total Sections</label
                    >
                    <input
                      type="number"
                      :value="editSite.number_of_sections + newSectionsToAdd"
                      id="totalSections"
                      class="form-control"
                      readonly
                    />
                  </div>
                </div>
              </div>

              <!-- Section Label and Numbering Type (Disabled) -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="editSectionLabel" class="form-label"
                    >Section Label</label
                  >
                  <input
                    type="text"
                    :value="capitalizeFirstLetter(editSite.section_label)"
                    id="editSectionLabel"
                    class="form-control"
                    readonly
                  />
                </div>

                <div class="col-md-6">
                  <label for="editNumberingType" class="form-label"
                    >Numbering Type</label
                  >
                  <input
                    type="text"
                    :value="capitalizeFirstLetter(editSite.numbering_type)"
                    id="editNumberingType"
                    class="form-control"
                    readonly
                  />
                </div>
              </div>

              <!-- Buttons -->
              <div
                class="d-flex justify-content-end gap-2 mt-3"
                style="padding-top: 15px"
              >
                <button
                  type="submit"
                  class="btn btn-success"
                  style="width: 150px"
                >
                  Save Changes
                </button>
                <button
                  type="button"
                  @click="cancelEdit"
                  class="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
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
  name: "DevSites",
  components: {
    SideNav,
    AppHeader,
    BModal,
  },
  data() {
    return {
      viewMode: "table",
      sortBy: "name",
      searchQuery: "",
      visibleDropdown: null,
      viewFilter: "active",
      showAddModal: false,
      showEditModal: false,
      selectedSite: {},
      selectedSiteModal: false,
      statusOptions: [],
      newSite: {
        name: "",
        status: "",
        region: "",
        province: "",
        municipality: "",
        barangay: "",
        postalCode: 0,
        address: "",
        description: "",
        picture: "",
        maximum_months: 24,
        number_of_sections: 15,
        numbering_type: "numeric",
        section_label: "floor",
        commission: 200000,
        spot_discount_percentage: 0,
        spot_discount_flat: 0,
        vat_percentage: 12.0,
        reservation_fee: 50000,
        other_charges: 0,
      },
      showSectionModal: false, // Updated from showFloorModal
      newSectionsToAdd: 0,
      editSite: {
        id: "",
        name: "",
        status: "",
        region: "",
        province: "",
        municipality: "",
        barangay: "",
        postalCode: 0,
        description: "",
        picture: "",
        address: "",
        sections: [],
        section_label: "",
        number_of_sections: 0,
        numbering_type: "",
        maximum_months: 0,
        commission: 0,
        spot_discount_percentage: 0,
        spot_discount_flat: 0,
        vat_percentage: 12.0,
        reservation_fee: 0,
        other_charges: 0,
      },
      currentSite: {
        id: "",
        name: "",
        status: "",
        region: "",
        province: "",
        municipality: "",
        barangay: "",
        description: "",
        picture: "",
        address: "",
        postalCode: 0,
        // Section
        sections: [],
        section_label: "",
        number_of_sections: 0,
        numbering_type: "",
        // Payment
        maximum_months: 0,
        commission: 0,
        spot_discount_percentage: 0,
        spot_discount_flat: 0,
        vat_percentage: 12.0,
        reservation_fee: 0,
        other_charges: 0,
      },
      totalSections: 0, // Updated from totalFloors
      newSectionNumber: null,
      newSectionCount: null,
      sites: [],
      archivedSites: [],
      regionOptions: [],
      provinceOptions: [],
      municipalityOptions: [],
      barangayOptions: [],
      selectedRegion: null,
      selectedProvince: null,
      selectedMunicipality: null,
      selectedBarangay: null,
      newPictureFile: null,
      imagePreview: null,
      currentPage: 1,
      itemsPerPage: 15,
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId,
      userType: (state) => state.userType,
      companyId: (state) => state.companyId,
    }),
    vuexUserId() {
      return this.userId;
    },
    vuexCompanyId() {
      return this.companyId;
    },
    filteredSites() {
      // Determine whether to filter active or archived sites
      const sitesToFilter =
        this.viewFilter === "archived" ? this.archivedSites : this.sites;

      // Apply search and sorting
      return sitesToFilter
        .filter(
          (site) =>
            site?.name?.toLowerCase().includes(this.searchQuery.toLowerCase()) // Optional chaining for safety
        )
        .sort((a, b) => {
          const aName = a?.name || "";
          const bName = b?.name || "";
          const aStatus = a?.status || "";
          const bStatus = b?.status || "";
          const aCreatedAt = new Date(a?.created_at) || new Date(0); // Default to epoch if undefined
          const bCreatedAt = new Date(b?.created_at) || new Date(0);

          if (this.sortBy === "name") {
            return aName.localeCompare(bName);
          } else if (this.sortBy === "status") {
            return aStatus.localeCompare(bStatus);
          } else if (this.sortBy === "creation") {
            return aCreatedAt - bCreatedAt; // Sort by date (ascending)
          }
          return 0; // Default case
        });
    },
    numberOfSections() {
      return this.currentSite.sections.length;
    },
    paginatedSites() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.filteredSites.slice(startIndex, endIndex); // Use filteredSites here
    },
    totalPages() {
      return Math.ceil(this.filteredSites.length / this.itemsPerPage); // Use filteredSites here
    },
  },
  methods: {
    toggleDropdown(site) {
      this.visibleDropdown = this.visibleDropdown === site ? null : site; // Toggle visibility
    },
    isDropdownVisible(site) {
      return this.visibleDropdown === site; // Check if dropdown should be shown for this site
    },
    goToPage(pageNumber) {
      if (pageNumber > 0 && pageNumber <= this.totalPages) {
        this.currentPage = pageNumber;
      }
    },
    formatStatus(status) {
      return status
        .split("_") // Split the string at underscores
        .map(
          (word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
        ) // Capitalize each word
        .join(" "); // Join the words back with spaces
    },
    revertStatusToOriginal(status) {
      return status
        .split(" ") // Split by space
        .map((word) => word.toLowerCase()) // Convert each word to lowercase
        .join("_"); // Join the words back with underscores
    },
    capitalizeFirstLetter(str) {
      if (!str) return str;
      return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    },
    async fetchSites() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/sites/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          this.sites = response.data.data.map((site) => ({
            ...site,
            name: site.name || "Unknown Site",
            location: this.constructLocation(site), // Dynamically build location
            isArchived: site.isArchived ?? false,
            sections: site.sections || [], // Ensure floors is always an array
          }));
        }
      } catch (error) {
        console.error("Error fetching sites:", error.response || error);
      }
    },
    async fetchArchivedSites() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/sites/archived/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        if (response.status === 200) {
          this.archivedSites = response.data.data.map((site) => ({
            ...site,
            location: this.constructLocation(site), // Build location dynamically
          }));
          console.log("Archived sites fetched:", this.archivedSites);
        }
      } catch (error) {
        if (error.response?.status === 401) {
          const refreshedToken = await this.refreshAccessToken();
          if (refreshedToken) {
            this.fetchArchivedSites(); // Retry fetching archived sites
          }
        } else {
          console.error(
            "Error fetching archived sites:",
            error.response || error
          );
        }
      }
    },
    async archiveSite(site) {
      const siteId = site.id; // Get the site ID
      console.log("Archiving site with ID:", siteId);

      if (confirm("Are you sure you want to archive this site?")) {
        try {
          const response = await axios.put(
            `http://localhost:8000/developer/sites/archived/${siteId}/`, // Correct endpoint for updating the site
            {
              name: site.name, // Pass the existing name or other required fields
              description: site.description,
              region: site.region,
              province: site.province,
              municipality: site.municipality,
              barangay: site.barangay,
              postal_code: site.postal_code,
              picture: site.picture, // If you want to keep the picture
              status: site.status,
              maximum_months: site.maximum_months,
              archived: true, // If you need to update the archive status
            },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
              params: { action: "archive" }, // Send action=archive as query parameter
            }
          );

          if (response.status === 200) {
            console.log("Site archived successfully.");
            this.fetchSites();
            this.fetchArchivedSites();
          }
        } catch (error) {
          console.error("Error archiving site:", error.response?.data || error);
        }
      }
    },
    async unarchiveSite(site) {
      const siteId = site.id; // Get the site ID
      console.log("Unarchiving site with ID:", siteId);

      if (confirm("Are you sure you want to unarchive this site?")) {
        try {
          const response = await axios.put(
            `http://localhost:8000/developer/sites/archived/${siteId}/`, // Correct endpoint for updating the site
            {
              name: site.name, // Pass the existing name or other required fields
              description: site.description,
              region: site.region,
              province: site.province,
              municipality: site.municipality,
              barangay: site.barangay,
              postal_code: site.postal_code,
              picture: site.picture, // If you want to keep the picture
              status: site.status,
              maximum_months: site.maximum_months,
              archived: false, // Update the archived status to false (unarchive)
            },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
              params: { action: "unarchive" }, // Send action=unarchive as query parameter
            }
          );

          if (response.status === 200) {
            console.log("Site unarchived successfully.");
            this.fetchSites(); // Refresh the site list
            this.fetchArchivedSites(); // Refresh the archived site list
          }
        } catch (error) {
          console.error(
            "Error unarchiving site:",
            error.response?.data || error
          );
        }
      }
    },
    toggleArchived() {
      this.showArchived = !this.showArchived;
      console.log("Toggled archived view:", this.showArchived);

      if (this.showArchived && this.archivedSites.length === 0) {
        // Fetch archived sites only when switching to archived view
        this.fetchArchivedSites();
      }
    },
    toggleView() {
      this.viewMode = this.viewMode === "grid" ? "table" : "grid";
    },

    // Function to get the picture URL (for the current image)
    getPictureUrl(picture) {
      return `http://localhost:8000${picture}`; // Adjust the URL path as needed
    },
    async uploadPicture(siteId, pictureFile) {
      const formData = new FormData();
      formData.append("picture", pictureFile);

      // Debug: Log the formData content and pictureFile to make sure it's valid
      console.log("Uploading picture for siteId:", siteId);
      console.log("Form data content:", formData);
      console.log("Picture file:", pictureFile);

      try {
        const response = await axios.put(
          `http://localhost:8000/developer/sites/picture/${siteId}/`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.status === 200) {
          console.log("Picture updated successfully:", response.data);
          return response.data;
        } else {
          // Debug: Log unexpected status codes
          console.error("Unexpected response status:", response.status);
        }
      } catch (error) {
        // Debug: Log the error response and status
        console.error("Error updating picture:", error.response || error);
      }
    },
    handlePictureUpload(event, mode) {
      const file = event.target.files[0];
      if (file) {
        // Set the image preview to the file's URL for preview
        this.imagePreview = URL.createObjectURL(file);

        // Handle picture update depending on the mode (edit or add)
        if (mode === "edit") {
          // In edit mode, we store the file in newPictureFile for the update
          this.newPictureFile = file;
        } else if (mode === "add") {
          // In add mode, we set the file to the newSite.picture
          this.newSite.picture = file;
        }
      } else {
        this.imagePreview = null; // Clear preview if no file is selected
      }
    },
    // Save new site, including floors
    async addSite() {
      const formData = new FormData();
      formData.append("companyId", this.vuexCompanyId);
      formData.append("name", this.newSite.name);
      formData.append("description", this.newSite.description || "");
      formData.append("region", this.newSite.region);
      formData.append("province", this.newSite.province);
      formData.append("municipality", this.newSite.municipality);
      formData.append("barangay", this.newSite.barangay);
      formData.append("address", this.newSite.address);
      formData.append("postal_code", this.newSite.postalCode);
      const formattedStatus = this.revertStatusToOriginal(this.newSite.status);
      this.newSite.status = formattedStatus;
      formData.append("status", this.newSite.status);

      // Sections
      formData.append("number_of_sections", this.newSite.number_of_sections); // Updated field
      formData.append("numbering_type", this.newSite.numbering_type); // Added field
      formData.append("section_label", this.newSite.section_label); // Added field

      // Payment Fields
      formData.append("maximum_months", this.newSite.maximum_months);
      formData.append("commission", this.newSite.commission || "");
      formData.append(
        "spot_discount_percentage",
        this.newSite.spot_discount_percentage || ""
      );
      formData.append(
        "spot_discount_flat",
        this.newSite.spot_discount_flat || ""
      );
      formData.append("vat_percentage", this.newSite.vat_percentage || "");
      formData.append("reservation_fee", this.newSite.reservation_fee || "");
      formData.append("other_charges", this.newSite.other_charges || "");

      // Add Sections
      if (this.newSite.sections && this.newSite.sections.length > 0) {
        this.newSite.sections.forEach((section, index) => {
          formData.append(
            `sections[${index}][sectionNumber]`,
            section.sectionNumber || ""
          );
        });
      }

      // Add Picture
      const pictureFile = this.newPictureFile || this.newSite.picture;
      if (pictureFile) {
        formData.append("picture", pictureFile);
      }

      try {
        const response = await axios.post(
          "http://localhost:8000/developer/sites/",
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.status === 201) {
          const parsedData =
            typeof response.data === "string"
              ? JSON.parse(response.data)
              : response.data;
          const siteId = parsedData.id;
          console.log("New site created with ID:", siteId);

          if (siteId && pictureFile) {
            await this.uploadPicture(siteId, pictureFile);
          }

          // Reset form and reload sites
          //this.newSite = this.resetNewSite();
          this.imagePreview = null;
          this.showAddModal = false;
          this.fetchSites();
        }
      } catch (error) {
        console.error("Error adding site:", error.response || error);
      }
    },
    addSections() {
      // Find the last section number from the existing sections
      let lastSectionNumber = 0;
      if (this.editSite.sections.length > 0) {
        lastSectionNumber = Math.max(
          ...this.editSite.sections.map((section) => section.sectionNumber)
        );
      }

      // Generate new sections, starting from the correct number
      const newSections = [];
      for (let i = 0; i < this.newSectionsToAdd; i++) {
        // Make sure the new sections start from the last section number + 1
        newSections.push({
          sectionNumber: lastSectionNumber + i + 1, // Generate new section numbers
          sectionLabel: this.editSite.section_label, // Section label from the input
        });
      }

      // Append the new sections to the existing ones
      this.editSite.sections.push(...newSections); // Add the new sections to the current ones
      this.editSite.number_of_sections = this.editSite.sections.length; // Update the total section count

      // Reset the input field after adding sections
      this.newSectionsToAdd = 0;
    },
    async updateSite() {
      const formData = new FormData();

      // Log the editSite data for debugging
      console.log("Data for updateSite:", this.editSite);

      // Site fields
      formData.append("companyId", this.vuexCompanyId);
      formData.append("name", this.editSite.name);
      formData.append("description", this.editSite.description || "");
      formData.append("region", this.editSite.region);
      formData.append("province", this.editSite.province);
      formData.append("municipality", this.editSite.municipality);
      formData.append("barangay", this.editSite.barangay);
      formData.append("address", this.editSite.address || "null");
      formData.append("postal_code", this.editSite.postalCode || "null");
      formData.append("status", this.editSite.status);

      // Payment Fields
      formData.append("maximum_months", this.editSite.maximum_months);
      formData.append("commission", this.editSite.commission || "");
      formData.append(
        "spot_discount_percentage",
        this.editSite.spot_discount_percentage || ""
      );
      formData.append(
        "spot_discount_flat",
        this.editSite.spot_discount_flat || ""
      );
      formData.append("vat_percentage", this.editSite.vat_percentage || "");
      formData.append("reservation_fee", this.editSite.reservation_fee || "");
      formData.append("other_charges", this.editSite.other_charges || "");

      // Sections - only append newly added sections
      formData.append("number_of_sections", this.newSectionsToAdd); // Use newSectionsToAdd here
      formData.append("section_label", this.editSite.section_label || ""); // Section label

      // Append only the newly added sections
      if (this.newSectionsToAdd > 0) {
        const newSections = this.editSite.sections.slice(
          -this.newSectionsToAdd
        ); // Get only the newly added sections
        newSections.forEach((section, index) => {
          formData.append(
            `sections[${index}][sectionNumber]`,
            section.sectionNumber || ""
          );
          formData.append(
            `sections[${index}][sectionLabel]`,
            section.sectionLabel || this.editSite.section_label
          );
        });
      }

      // Handle Picture (If there's a new picture, include it)
      const pictureFile =
        this.newPictureFile ||
        (this.editSite.picture && this.editSite.picture instanceof File
          ? this.editSite.picture
          : null);

      if (pictureFile && pictureFile instanceof File) {
        formData.append("picture", pictureFile); // Append the file directly
      }

      // Log the formData content before making the request
      console.log("Form Data being sent:", formData);

      try {
        const response = await axios.put(
          `http://localhost:8000/developer/sites/${this.selectedSite.id}/`, // Ensure to use the selected site's ID
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.status === 200) {
          const parsedData =
            typeof response.data === "string"
              ? JSON.parse(response.data)
              : response.data;
          const siteId = parsedData.id;
          console.log("Site updated with ID:", siteId);

          // Reset the picture preview and clear the file input
          this.resetPicturePreview();
          this.newPictureFile = null; // Clear the file input field

          // Reset the input field itself
          const fileInput = document.getElementById("picture");
          if (fileInput) {
            fileInput.value = ""; // Reset the file input
          }

          // Reset form and close the modal
          this.showEditModal = false;
          this.fetchSites(); // Reload the list of sites after editing
        }
      } catch (error) {
        // Log full error details for debugging
        console.error("Error editing site:", error.response || error);
        if (error.response) {
          console.log("Error Response Status:", error.response.status);
          console.log("Error Response Data:", error.response.data);
          console.log("Error Response Headers:", error.response.headers);
        }
      }
    },
    // Open the edit modal and prepare the data
    openEditModal(selectedSite) {
      console.log("Selected Site:", selectedSite); // Debugging line to see the selected site
      this.selectedSite = selectedSite;

      // Get the length of the sections array
      const numberOfSections = this.selectedSite.sections.length;

      console.log("Number of Sections:", numberOfSections); // Log the number of sections

      this.editSite = {
        ...this.selectedSite,
        sections: [...this.selectedSite.sections], // Clone sections array to avoid mutation
        number_of_sections: numberOfSections, // Set the length of sections in the editSite object
        postalCode: this.selectedSite.postal_code,
      };

      console.log("Edit Site after cloning sections:", this.editSite);

      this.showEditModal = true;
    },

    cancelEdit() {
      this.resetPicturePreview();
      this.showEditModal = false;
    },
    resetPicturePreview() {
      this.newPictureFile = null;
      this.imagePreview = null;
      const fileInput = document.getElementById("picture"); // Get the file input element
      if (fileInput) {
        fileInput.value = ""; // Clear the file input
      }
    },
    async fetchStatusOptions() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/sites/status-options/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.statusOptions = Object.keys(response.data.status_options); // Extract keys (the stored values)
      } catch (error) {
        console.error("Error fetching status options:", error);
      }
    },

    constructLocation(site) {
      const addressParts = [
        site.province,
        site.municipality,
        site.barangay,
        site.postal_code ? `Postal Code: ${site.postal_code}` : null,
      ];
      return addressParts.filter(Boolean).join(", "); // Join non-empty parts
    },
    async loadRegionData() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/sites/locations/"
        );
        this.regionData = response.data; // Store region data for further processing

        // Sort region options: non-numeric values at the top, followed by numeric ones in ascending order
        this.regionOptions = Object.keys(this.regionData).sort((a, b) => {
          // Check if the keys are numeric
          const isANumeric = !isNaN(parseInt(a));
          const isBNumeric = !isNaN(parseInt(b));

          // If both are numeric or both are non-numeric, sort numerically or lexicographically
          if (isANumeric && isBNumeric) {
            return parseInt(a) - parseInt(b); // Numeric sorting
          } else if (!isANumeric && !isBNumeric) {
            return a.localeCompare(b); // Non-numeric sorting (lexicographically)
          } else {
            // If one is numeric and the other is non-numeric, non-numeric goes first
            return isANumeric ? 1 : -1;
          }
        });
      } catch (error) {
        console.error("Error loading region data:", error);
      }
    },
    loadProvinceData(regionCode) {
      if (!regionCode) {
        console.error("No region selected.");
        return;
      }

      const region = this.regionData[regionCode]; // Get the region using selectedRegion
      if (region) {
        this.provinceOptions = Object.keys(region.province_list); // Map available provinces from province_list

        // Set the region to newSite
        this.newSite.region = regionCode;

        // Clear previous municipality and barangay options
        this.municipalityOptions = [];
        this.barangayOptions = [];
        this.newSite.province = ""; // Reset province in newSite
        this.newSite.municipality = ""; // Reset municipality in newSite
        this.newSite.barangay = ""; // Reset barangay in newSite
      } else {
        console.error("Invalid region selected.");
      }
    },
    loadMunicipalityData(provinceName) {
      if (!this.newSite.region) {
        console.error("No region selected.");
        return;
      }
      if (!provinceName) {
        console.error("No province selected.");
        return;
      }

      const region = this.regionData[this.newSite.region]; // Get the region using newSite.region
      if (region) {
        const province = region.province_list[provinceName]; // Get the province using provinceName
        if (province) {
          this.municipalityOptions = Object.keys(province.municipality_list); // Map available municipalities from municipality_list

          // Set the province to newSite
          this.newSite.province = provinceName;

          // Clear barangay options when a new province is selected
          this.barangayOptions = [];
          this.newSite.municipality = ""; // Reset municipality in newSite
          this.newSite.barangay = ""; // Reset barangay in newSite
        } else {
          this.municipalityOptions = []; // Clear if no province found
          this.barangayOptions = []; // Clear barangay options if no province is found
        }
      }
    },
    loadBarangayData(municipalityName) {
      if (!municipalityName) {
        console.error("No municipality selected.");
        return;
      }

      const region = this.regionData[this.newSite.region]; // Get the region using newSite.region
      if (region) {
        const province = region.province_list[this.newSite.province]; // Get the province using newSite.province
        if (province) {
          const municipality = province.municipality_list[municipalityName]; // Get municipality using municipalityName
          if (municipality) {
            this.barangayOptions = municipality.barangay_list || []; // Map available barangays from barangay_list

            // Set the municipality to newSite
            this.newSite.municipality = municipalityName;
          }
        }
      }
    },
  },
  mounted() {
    this.fetchSites();
    this.loadRegionData();
    if (this.showArchived) {
      this.fetchArchivedSites();
    }
  },
  watch: {
    showArchived() {},
  },
  created() {
    this.fetchStatusOptions(); // Fetch the status options when the component is created
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
  background-color: #eff4fb;
  /* Gray background */
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
  /* Push items to opposite sides */
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
  font-weight: bold;
}

.view-switch {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 3px;
  overflow: hidden;
  background-color: #f6f6f6;
}

.view-icon {
  flex: 1;
  padding: 6px;
  text-align: center;
  cursor: pointer;
  font-size: 15px;
  color: #343a40;
  transition: background-color 0.3s, color 0.3s;
}

.view-icon.active {
  background-color: #343a40;
  color: #f6f6f6;
}

.separator {
  width: 1px;
  background-color: #f6f6f6;
  height: 100%;
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
  gap: 10px;
  /* Space between search bar and dropdown */
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
  border-radius: 3px;
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

.dropdown-container {
  position: relative;
}

.dropdown {
  appearance: none;
  padding: 8px 12px;
  height: 38px;
  /* Explicitly set height */
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 14px;
  width: 80%;
  max-width: 150px;
  background-color: white;
  color: #333;
  padding-right: 30px;
  background-image: url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"%3E%3Cpath d="M7 10l5 5 5-5z"/%3E%3C/svg%3E');
  background-position: right 10px center;
  background-repeat: no-repeat;
  background-size: 14px;
}

.dropdown2 {
  appearance: none;
  padding: 8px 12px;
  height: 38px;
  /* Explicitly set height */
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 14px;
  width: 90%;
  max-width: 150px;
  background-color: white;
  color: #333;
  padding-right: 30px;
  background-image: url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"%3E%3Cpath d="M7 10l5 5 5-5z"/%3E%3C/svg%3E');
  background-position: right 10px center;
  background-repeat: no-repeat;
  background-size: 14px;
}

/* Button Styles */
.btn-primary.add-button {
  padding: 8px 12px;
  border: 1px solid #0560fd;
  border-radius: 3px;
  font-size: 14px;
  background-color: #0560fd;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary.add-button:hover {
  background-color: #0056b3;
}

.card {
  background-color: #fff;
  margin-bottom: 10px;
  margin-top: 0;
  max-width: 1100px;
  /* Ensures the card and grid align */
  margin-left: auto;
  /* Centers the card */
  margin-right: auto;
}

/* .search-bar {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
} */

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
}

.site-card:hover {
  transform: translateY(-2px);
}

.site-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  /* Ensures the image is cropped to fit the area */
  border-radius: 12px;
  margin-bottom: 10px;
}

.table-image {
  width: 30px;
  /* Small size for the table */
  height: 30px;
  /* Make the image smaller */
  object-fit: cover;
  /* Crop the image if necessary */
  margin-right: 10px;
  /* Adds some spacing between the image and the name */
}

.site-info {
  flex-direction: row;
}

.site-name {
  font-size: 14px;
  font-weight: bold;
}

.site-location {
  font-size: 14px;
  color: #777;
}

.site-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  text-align: left;
  background: #fff;
}

.site-table th,
.site-table td {
  padding-bottom: 5px;
  text-align: left;
  vertical-align: middle;
  border: none;
  /* Remove borders from all cells */
}

.site-table th {
  background-color: #f9f9f9;
  font-weight: bold;
}

.site-table th:nth-child(2),
.site-table td:nth-child(2) {
  /* Location column */
  width: 43%;
  padding-right: 60px;
}

.site-table th:nth-child(3),
.site-table td:nth-child(3) {
  /* Status column */
  width: 20%;
}

.site-table th:nth-child(4),
.site-table td:nth-child(4) {
  /* Actions column */
  width: 7%;
}

.outside-headers {
  display: grid;
  /* Change to grid layout */
  grid-template-columns: 30% 43% 20% 7%;
  /* Match the column widths */
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
}

.form-group .form-label,
.row .form-label {
  font-size: 0.9rem;
  color: #6c757d;
  /* Adjust the value to your preferred size */
}

.btn-add {
  background-color: #0560fd;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
}

.btn-add-floors {
  background-color: #8b8b8b;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
  font-size: 12px;
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

.pagination-controls {
  display: flex;
  justify-content: flex-end;
  /* Align to the right */
  margin-top: 20px;
  /* Add spacing from the content above */
  gap: 10px;
  /* Spacing between buttons */
  padding-right: 20px;
  /* Add padding to push it away from the edge */
}

.page-button {
  padding: 5px 10px;
  font-size: 12px;
  /* Slightly smaller font */
  border: 1px solid #ddd;
  background-color: #fff;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.page-button.active {
  background-color: #007bff;
  color: white;
}

.page-button:disabled {
  cursor: not-allowed;
  background-color: #f5f5f5;
}

.page-button:hover:not(:disabled) {
  background-color: #e9ecef;
  /* Light gray */
}
</style>
