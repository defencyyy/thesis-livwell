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
                    <option value="relative_id">Sort: ID</option>
                    <option value="name">Sort: Name</option>
                    <option value="status">Sort: Status</option>
                  </select>
                  <!-- Sort Order Dropdown -->
                  <select v-model="sortOrder" class="dropdown">
                    <option value="asc">Ascending</option>
                    <option value="desc">Descending</option>
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

        <!-- Table View -->
        <div v-if="viewMode === 'table'">
          <!-- Headers outside the card -->
          <div class="outside-headers">
            <span class="header-item">ID</span>
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
                    <td class="site-relative-id">
                      {{ site.relative_id || "N/A" }}
                    </td>
                    <td>
                      <div class="site-info">
                        <img
                          v-if="site.picture"
                          :src="getPictureUrl(site.picture)"
                          alt="Image of {{ site.name }}"
                          class="table-image"
                        />
                        <i
                          v-else
                          class="fas fa-image fa-2x"
                          aria-label="Default site image"
                          style="margin-right: 12px"
                        ></i>
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
                      <div class="broker-actions d-flex gap-2">
                        <button
                          @click="openEditModal(site)"
                          style="
                            border: none;
                            background-color: transparent;
                            color: #343a40;
                            cursor: pointer;
                            font-size: 18px;
                          "
                        >
                          <i class="fas fa-edit"></i>
                        </button>
                        <button
                          v-if="!site.archived"
                          @click="archiveSite(site)"
                          style="
                            border: none;
                            background-color: transparent;
                            color: #343a40;
                            cursor: pointer;
                            font-size: 18px;
                          "
                        >
                          <i class="fas fa-archive"></i>
                        </button>
                        <button
                          v-else
                          @click="unarchiveSite(site)"
                          class="btn btn-sm btn-success"
                          style="
                            border: none;
                            background-color: transparent;
                            color: #343a40;
                            cursor: pointer;
                            font-size: 18px;
                          "
                        >
                          <i class="fas fa-undo"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
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
              <a class="page-link" href="#" @click.prevent="goToPage(page)">
                {{ page }}
              </a>
            </li>
            <li
              :class="['page-item', { disabled: currentPage === totalPages }]"
            >
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
                      @change="handlePictureUpload($event, 'add')"
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
                      <option value="unit">Level</option>
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
                <button type="submit" class="btn-add" style="width: 150px">
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
        <b-modal
          v-model="showNotification"
          :title="notificationTitle"
          hide-footer
          centered
        >
          <p>{{ notificationMessage }}</p>
          <div class="button-container">
            <button
              type="button"
              @click="showNotification = false"
              class="btn-cancel-right"
            >
              Close
            </button>
          </div>
        </b-modal>
        <b-modal
          v-model="showConfirmModal"
          :title="'Confirmation'"
          hide-footer
          centered
        >
          <p>{{ confirmMessage }}</p>
          <div class="button-container">
            <!-- Confirm Button -->
            <button
              type="button"
              @click="confirmAction"
              class="btn btn-primary"
            >
              Confirm
            </button>
            <!-- Cancel Button -->
            <button
              type="button"
              @click="cancelAction"
              class="btn btn-secondary"
            >
              Cancel
            </button>
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
      // View and UI-related data
      viewMode: "table",
      sortBy: "relative_id",
      sortOrder: "asc",
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
      showSectionModal: false, // Modal for adding/editing sections
      newSectionsToAdd: 0,

      // Editing site-related data
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
        newSectionsToAdd: 0,
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

      // Current site and pagination related data
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
      totalSections: 0, // Total number of sections (formerly totalFloors)
      newSectionNumber: null,
      newSectionCount: null,

      // Site lists and filters
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

      // Picture handling
      newPictureFile: null,
      imagePreview: null,

      // Pagination
      currentPage: 1,
      itemsPerPage: 10,

      // Notifications
      showNotification: false,
      notificationTitle: "",
      notificationMessage: "",
      showConfirmModal: false, // Controls modal visibility
      confirmMessage: "", // Stores the confirmation message
      actionToConfirm: null, // The action to confirm
      confirmParams: [], // Parameters for the action
    };
  },

  computed: {
    // Vuex store data
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
      const sitesToFilter =
        this.viewFilter === "archived" ? this.archivedSites : this.sites;

      return sitesToFilter
        .filter((site) =>
          site?.name?.toLowerCase().includes(this.searchQuery.toLowerCase())
        ) // Filter by search query
        .sort((a, b) => {
          const aName = a?.name || "";
          const bName = b?.name || "";
          const aStatus = a?.status || "";
          const bStatus = b?.status || "";
          const aRelativeId = a?.relative_id?.toString().toLowerCase() || "";
          const bRelativeId = b?.relative_id?.toString().toLowerCase() || "";

          let comparison = 0;

          // Sort by selected criteria
          if (this.sortBy === "name") {
            comparison = aName.localeCompare(bName);
          } else if (this.sortBy === "status") {
            comparison = aStatus.localeCompare(bStatus);
          } else if (this.sortBy === "relative_id") {
            comparison = aRelativeId.localeCompare(bRelativeId, undefined, {
              numeric: true,
            });
          }

          // If the selected order is "desc", reverse the comparison result
          return this.sortOrder === "desc" ? -comparison : comparison;
        });
    },
    // Count of sections for the current site
    numberOfSections() {
      return this.currentSite.sections.length;
    },

    // Paginate filtered sites
    paginatedSites() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.filteredSites.slice(startIndex, endIndex); // Slice filtered sites for pagination
    },

    // Calculate the total number of pages
    totalPages() {
      return Math.ceil(this.filteredSites.length / this.itemsPerPage); // Total pages based on filtered sites
    },
  },

  mounted() {
    this.fetchSites();
    this.loadRegionData();

    // If showing archived sites, fetch them
    if (this.showArchived) {
      this.fetchArchivedSites();
    }
  },

  watch: {
    showArchived() {
      // Watch for archived view toggle (can be expanded in the future)
    },
  },

  created() {
    this.fetchStatusOptions(); // Fetch status options when the component is created
  },
  methods: {
    // Toggle visibility of dropdown for each site
    toggleDropdown(site) {
      this.visibleDropdown = this.visibleDropdown === site ? null : site; // Toggle visibility
    },

    // Check if dropdown should be visible for the given site
    isDropdownVisible(site) {
      return this.visibleDropdown === site; // Check if dropdown should be shown for this site
    },

    // Toggle between grid and table view modes
    toggleView() {
      this.viewMode = this.viewMode === "grid" ? "table" : "grid";
    },

    // Toggle visibility of archived sites and fetch them if necessary
    toggleArchived() {
      this.showArchived = !this.showArchived;
      console.log("Toggled archived view:", this.showArchived);

      if (this.showArchived && this.archivedSites.length === 0) {
        // Fetch archived sites only when switching to archived view
        this.fetchArchivedSites();
      }
    },

    // Navigate to a specific page
    goToPage(pageNumber) {
      if (pageNumber > 0 && pageNumber <= this.totalPages) {
        this.currentPage = pageNumber;
      }
    },

    // Fetch available status options
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

    // Format status by capitalizing each word
    formatStatus(status) {
      return status
        .split("_") // Split the string at underscores
        .map(
          (word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
        ) // Capitalize each word
        .join(" "); // Join the words back with spaces
    },

    // Convert formatted status back to original format
    revertStatusToOriginal(status) {
      return status
        .split(" ") // Split by space
        .map((word) => word.toLowerCase()) // Convert each word to lowercase
        .join("_"); // Join the words back with underscores
    },

    // Capitalize the first letter of a string
    capitalizeFirstLetter(str) {
      if (!str) return str;
      return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    },

    // Function to generate picture URL from the picture path
    getPictureUrl(picture) {
      return `http://localhost:8000${picture}`; // Adjust the URL path as needed
    },

    // Upload a picture for a specific site
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

    // Handle picture upload event and update preview
    handlePictureUpload(event, mode) {
      const file = event.target.files[0];
      console.log("Selected file:", file); // Debug log for selected file

      if (file) {
        // Set the image preview to the file's URL for preview
        this.imagePreview = URL.createObjectURL(file);
        console.log("Image preview URL:", this.imagePreview); // Debug log for preview URL

        // Handle picture update depending on the mode (edit or add)
        if (mode === "edit") {
          this.newPictureFile = file;
          console.log("File set for edit:", this.newPictureFile); // Debug log for edit mode
        } else if (mode === "add") {
          this.newSite.picture = file;
          console.log("File set for add:", this.newSite.picture); // Debug log for add mode
        }
      } else {
        this.imagePreview = null;
        console.warn("No file selected"); // Warn if no file is selected
      }
    },

    // Reset picture preview and clear file input
    resetPicturePreview() {
      this.newPictureFile = null;
      this.imagePreview = null;
      const fileInput = document.getElementById("picture"); // Get the file input element
      if (fileInput) {
        fileInput.value = ""; // Clear the file input
      }
    },

    // Fetch sites and dynamically build location and sections
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
            location: this.constructLocation(site),
            isArchived: site.isArchived ?? false,
            sections: site.sections || [],
            relative_id: site.relative_id || null,
          }));
        }
      } catch (error) {
        console.error("Error fetching sites:", error.response || error);
      }
    },

    // Fetch archived sites and dynamically build location
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
            location: this.constructLocation(site),
          }));
        }
      } catch (error) {
        if (error.response?.status === 401) {
          const refreshedToken = await this.refreshAccessToken();
          if (refreshedToken) {
            this.fetchArchivedSites();
          }
        } else {
          console.error(
            "Error fetching archived sites:",
            error.response || error
          );
        }
      }
    },
    // Show confirmation modal
    showConfirmation(message, action, params) {
      this.confirmMessage = message;
      this.actionToConfirm = action;
      this.confirmParams = params;
      this.showConfirmModal = true;
    },

    // Cancel confirmation action
    cancelAction() {
      this.showConfirmModal = false;
    },

    // Confirm the action
    async confirmAction() {
      try {
        await this.actionToConfirm(...this.confirmParams);
        this.showConfirmModal = false;
      } catch (error) {
        this.showConfirmModal = false;
        this.notificationTitle = "Error";
        this.notificationMessage = "An error occurred during the action.";
        this.showNotification = true;
      }
    },

    // Archive a site
    async archiveSite(site) {
      const siteId = site.id;
      this.showConfirmation(
        "Are you sure you want to archive this site?",
        this.executeArchiveSite,
        [siteId, site]
      );
    },

    // Unarchive a site
    async unarchiveSite(site) {
      const siteId = site.id;
      this.showConfirmation(
        "Are you sure you want to unarchive this site?",
        this.executeUnarchiveSite,
        [siteId, site]
      );
    },

    // Execute archive action
    async executeArchiveSite(siteId, site) {
      try {
        const response = await axios.put(
          `http://localhost:8000/developer/sites/archived/${siteId}/`,
          {
            name: site.name,
            description: site.description,
            region: site.region,
            province: site.province,
            municipality: site.municipality,
            barangay: site.barangay,
            postal_code: site.postal_code,
            picture: site.picture,
            status: site.status,
            maximum_months: site.maximum_months,
            archived: true,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            params: { action: "archive" },
          }
        );

        if (response.status === 200) {
          this.notificationTitle = "Success";
          this.notificationMessage = "Site archived successfully!";
          this.showNotification = true;
          this.fetchSites();
          this.fetchArchivedSites();
        }
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage =
          "An error occurred while archiving the site.";
        this.showNotification = true;
      }
    },

    // Execute unarchive action
    async executeUnarchiveSite(siteId, site) {
      try {
        const response = await axios.put(
          `http://localhost:8000/developer/sites/archived/${siteId}/`,
          {
            name: site.name,
            description: site.description,
            region: site.region,
            province: site.province,
            municipality: site.municipality,
            barangay: site.barangay,
            postal_code: site.postal_code,
            picture: site.picture,
            status: site.status,
            maximum_months: site.maximum_months,
            archived: false,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            params: { action: "unarchive" },
          }
        );

        if (response.status === 200) {
          this.notificationTitle = "Success";
          this.notificationMessage = "Site unarchived successfully!";
          this.showNotification = true;
          this.fetchSites();
          this.fetchArchivedSites();
        }
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage =
          "An error occurred while unarchiving the site.";
        this.showNotification = true;
      }
    },

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
      formData.append("status", formattedStatus);

      // Debug: Log formatted status
      console.log("Formatted status:", formattedStatus);

      // Sections
      formData.append("number_of_sections", this.newSite.number_of_sections);
      formData.append("numbering_type", this.newSite.numbering_type);
      formData.append("section_label", this.newSite.section_label);

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
      if (this.newSite.sections?.length) {
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
        console.log("Picture file before appending:", pictureFile); // Debug log
      } else {
        console.warn("No picture file selected for upload."); // Debug warning
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

          this.notificationTitle = "Success";
          this.notificationMessage = "Site created successfully!";
          this.showNotification = true;

          if (siteId && pictureFile) {
            await this.uploadPicture(siteId, pictureFile);
          }
          this.resetForm();
          this.imagePreview = null;
          this.showAddModal = false;
          this.fetchSites();
        }
      } catch (error) {
        console.error("Error response:", error.response || error); // Debug log for error response
        this.notificationTitle = "Error";
        this.notificationMessage = "An error occurred while creating the site.";
        this.showNotification = true;
      }
    },

    resetForm() {
      this.newSite = {
        name: "",
        description: "",
        region: "",
        province: "",
        municipality: "",
        barangay: "",
        address: "",
        postalCode: "",
        status: "",
        number_of_sections: 1,
        numbering_type: "numeric",
        section_label: "floor",
        maximum_months: 60,
        commission: null,
        spot_discount_percentage: null,
        spot_discount_flat: null,
        vat_percentage: 12.0,
        reservation_fee: null,
        other_charges: null,
        sections: [],
      };

      // Reset dependent fields as well
      this.selectedRegion = null;
      this.selectedProvince = null;
      this.selectedMunicipality = null;
      this.selectedBarangay = null;

      this.newPictureFile = null;
      this.imagePreview = null;
      this.newSectionsToAdd = 0; // Reset the section counter
    },
    // Trigger site update confirmation
    async updateSite() {
      this.showConfirmation(
        "Are you sure you want to update this site?",
        this.executeUpdateSite,
        [this.selectedSite]
      );
    },

    // Execute site update
    async executeUpdateSite() {
      const formData = new FormData();

      formData.append("companyId", this.vuexCompanyId);
      formData.append("name", this.editSite.name);
      formData.append("description", this.editSite.description || "");
      formData.append("region", this.editSite.region);
      formData.append("province", this.editSite.province);
      formData.append("municipality", this.editSite.municipality);
      formData.append("barangay", this.editSite.barangay);
      formData.append("address", this.editSite.address || "");
      formData.append("postal_code", this.editSite.postalCode || "null");
      formData.append("status", this.editSite.status);
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
      formData.append("number_of_sections", this.newSectionsToAdd);
      formData.append("section_label", this.editSite.section_label || "");

      if (this.newSectionsToAdd > 0) {
        const newSections = this.editSite.sections.slice(
          -this.newSectionsToAdd
        );
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

      const pictureFile =
        this.newPictureFile ||
        (this.editSite.picture && this.editSite.picture instanceof File
          ? this.editSite.picture
          : null);

      if (pictureFile && pictureFile instanceof File) {
        formData.append("picture", pictureFile);
      }

      try {
        const response = await axios.put(
          `http://localhost:8000/developer/sites/${this.selectedSite.id}/`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.status === 200) {
          this.notificationTitle = "Success";
          this.notificationMessage = "Site updated successfully!";
          this.showNotification = true;

          this.resetPicturePreview();
          this.newPictureFile = null;

          const fileInput = document.getElementById("picture");
          if (fileInput) {
            fileInput.value = "";
          }

          this.showEditModal = false;
          this.fetchSites();
        }
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage = "An error occurred while editing the site.";
        this.showNotification = true;
      }
    },

    // Add new sections to the site
    addSections() {
      let lastSectionNumber = 0;
      if (this.editSite.sections.length > 0) {
        lastSectionNumber = Math.max(
          ...this.editSite.sections.map((section) => section.sectionNumber)
        );
      }

      const newSections = [];
      for (let i = 0; i < this.newSectionsToAdd; i++) {
        newSections.push({
          sectionNumber: lastSectionNumber + i + 1,
          sectionLabel: this.editSite.section_label,
        });
      }

      this.editSite.sections.push(...newSections);
      this.editSite.number_of_sections = this.editSite.sections.length;
      this.newSectionsToAdd = 0;
    },

    // Open the edit modal and prepare the data
    openEditModal(selectedSite) {
      this.selectedSite = selectedSite;
      const numberOfSections = this.selectedSite.sections.length;

      this.editSite = {
        ...this.selectedSite,
        sections: [...this.selectedSite.sections], // Clone sections array to avoid mutation
        number_of_sections: numberOfSections,
        postalCode: this.selectedSite.postal_code,
      };

      this.newSectionsToAdd = 0;
      this.showEditModal = true;
    },

    cancelEdit() {
      this.resetPicturePreview();
      this.showEditModal = false;
    },

    constructLocation(site) {
      const addressParts = [
        site.region,
        site.province,
        site.municipality,
        site.barangay,
        site.address,
      ];
      return addressParts.filter(Boolean).join(", ");
    },

    // Load region data
    async loadRegionData() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/sites/locations/"
        );
        this.regionData = response.data;
        this.regionOptions = Object.keys(this.regionData).sort((a, b) => {
          const isANumeric = !isNaN(parseInt(a));
          const isBNumeric = !isNaN(parseInt(b));

          if (isANumeric && isBNumeric) {
            return parseInt(a) - parseInt(b);
          } else if (!isANumeric && !isBNumeric) {
            return a.localeCompare(b);
          } else {
            return isANumeric ? 1 : -1;
          }
        });
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage = "Error loading region data.";
        this.showNotification = true;
      }
    },

    // Load province data based on region
    loadProvinceData(regionCode) {
      if (!regionCode) return;

      const region = this.regionData[regionCode];
      if (region) {
        this.provinceOptions = Object.keys(region.province_list);
        this.newSite.region = regionCode;
        this.municipalityOptions = [];
        this.barangayOptions = [];
        this.newSite.province = "";
        this.newSite.municipality = "";
        this.newSite.barangay = "";
      }
    },

    // Load municipality data based on province
    loadMunicipalityData(provinceName) {
      if (!this.newSite.region || !provinceName) return;

      const region = this.regionData[this.newSite.region];
      const province = region?.province_list[provinceName];
      if (province) {
        this.municipalityOptions = Object.keys(province.municipality_list);
        this.newSite.province = provinceName;
        this.barangayOptions = [];
        this.newSite.municipality = "";
        this.newSite.barangay = "";
      }
    },

    // Load barangay data based on municipality
    loadBarangayData(municipalityName) {
      if (!municipalityName) return;

      const region = this.regionData[this.newSite.region];
      const province = region?.province_list[this.newSite.province];
      const municipality = province?.municipality_list[municipalityName];
      if (municipality) {
        this.barangayOptions = municipality.barangay_list || [];
        this.newSite.municipality = municipalityName;
      }
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
  width: 27%;
}

.site-table th:nth-child(3),
.site-table td:nth-child(3) {
  /* Location column */
  width: 43%;
  padding-right: 60px;
}

.site-table th:nth-child(4),
.site-table td:nth-child(4) {
  /* Status column */
  width: 16%;
}

.site-table th:nth-child(5),
.site-table td:nth-child(5) {
  /* Actions column */
  width: 7%;
}

.outside-headers {
  display: grid;
  /* Change to grid layout */
  grid-template-columns: 7% 27% 43% 16% 7%;
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

.page-button:disabled {
  cursor: not-allowed;
  background-color: #f5f5f5;
}

.page-button:hover:not(:disabled) {
  background-color: #e9ecef;
  /* Light gray */
}

.button-container {
  display: flex;
  justify-content: flex-end;
}

.btn-cancel-right {
  background-color: #0560fd;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 12px 20px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn-cancel-right:hover {
  background-color: #004bb5;
}

.btn-cancel-right:focus {
  outline: none;
}
</style>
