<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">Unit Management</div>
          </div>
          <!-- Header Section -->

          <button class="back-button" @click="$router.back()">
            <div class="back-container">
              <i class="fas fa-arrow-left"></i> Back
            </div>
          </button>
        </div>

        <div v-if="site" class="site-container">
          <!-- Left Section: Site Details -->
          <div class="site-details-section">
            <div class="site-picture">
              <img
                :src="
                  getPictureUrl(site.picture) || require('@/assets/home.png')
                "
                alt="Site Image"
                class="site-image"
              />
            </div>
            <div class="site-info">
              <div class="site-name">
                <p>
                  <strong>{{ site.name }}</strong>
                </p>
              </div>

              <div class="site-description-location">
                <div class="description-icon">
                  <i class="fas fa-info-circle"></i>
                  <!-- Example icon for description -->
                  <span>{{ site.description }}</span>
                </div>
                <div class="location-icon">
                  <i class="fas fa-map-marker-alt"></i>
                  <!-- Example icon for location -->
                  <span>{{ site.location }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Section: Floors -->
          <div class="sections-section">
            <div
              class="card border-0 rounded-1 mx-auto"
              style="box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
            >
              <div class="card-body-toolbar">
                <div class="row">
                  <div class="toolbar">
                    <div class="left-section">
                      <p>
                        <strong>Total Sections: </strong>
                        {{ site.sections.length }}
                      </p>
                      <div class="section-sort">
                        <!-- <label for="sortSections">Sort Sections:</label> -->
                        <select
                          id="sortSections"
                          v-model="sectionSortOrder"
                          @change="sortSections"
                          class="dropdown"
                        >
                          <option value="asc">Ascending</option>
                          <option value="desc">Descending</option>
                        </select>
                      </div>
                    </div>
                    <div class="right-section">
                      <button class="btn-add" @click="toggleAddUnitsModal">
                        Add Units
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="sortedSections.length > 0" class="section-table">
              <div class="outside-headers">
                <span class="header-item">Section #</span>
                <span class="header-item">Total Units</span>
                <span class="header-item">Available Units</span>
                <span class="header-item">Actions</span>
              </div>

              <div
                v-for="section in sortedSections"
                :key="section.id"
                class="card border-0 rounded-1 mx-auto my-2"
                style="box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
              >
                <div class="table-container">
                  <table class="section-info">
                    <tbody>
                      <tr>
                        <td>
                          <span class="section-number">
                            <!-- Use sectionOptions method to display the section name dynamically -->
                            {{ sectionOptionsForSection(section) }}
                          </span>
                        </td>
                        <td>
                          <span class="section-total-units">
                            {{ section.total_units }}
                          </span>
                        </td>
                        <td>
                          <span class="section-available-units">
                            {{ section.available_units }}
                          </span>
                        </td>
                        <td>
                          <div class="section-actions d-flex gap-2">
                            <button
                              @click="openUnitManagement(section)"
                              class="btn-manage"
                            >
                              Manage Units
                            </button>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <div v-else>
              <p>No Sections Available</p>
            </div>
          </div>

          <!-- Unit Management Modal -->
          <b-modal
            v-model="showUnitManagementModal"
            title="Manage Units"
            @hide="closeUnitManagementModal"
          >
            <button @click="openAddUnitModalForSection(selectedSection.id)">
              Add Units to Section
            </button>

            <div class="unit-management-content">
              <div class="search-bar">
                <b-form-input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search units"
                  @input="onSearch"
                />
              </div>

              <!-- Filter Options -->
              <b-form-group label="Status:">
                <b-form-select
                  v-model="selectedStatus"
                  :options="statusOptions"
                />
              </b-form-group>
              <b-form-group label="Price Range:">
                <b-form-select
                  v-model="selectedPriceRange"
                  :options="priceRangeOptions"
                />
              </b-form-group>
              <b-form-group label="Unit Type:">
                <b-form-select
                  v-model="selectedUnitType"
                  :options="unitTypeOptions"
                />
              </b-form-group>
              <b-form-group label="Sort by:">
                <b-form-select
                  v-model="selectedSort"
                  :options="sortOptions"
                ></b-form-select>
              </b-form-group>

              <!-- Unit Table -->
              <table v-if="filteredUnits.length" class="unit-table">
                <thead>
                  <tr>
                    <th>Unit Number</th>
                    <th>Unit Type</th>
                    <th>Status</th>
                    <th>Price</th>
                    <th>Floor Area</th>
                    <th>Lot Area</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="unit in filteredUnits" :key="unit.id">
                    <td>{{ unit.unit_number }}</td>
                    <td>
                      {{
                        unitTypes.find((type) => type.id === unit.unit_type)
                          ?.name || "Unknown"
                      }}
                    </td>
                    <!-- Unit Type -->
                    <td>{{ unit.status }}</td>
                    <!-- Status -->
                    <td>{{ formatCurrency(unit.price) }}</td>
                    <!-- Price -->
                    <td>{{ unit.floor_area }}</td>
                    <td>{{ unit.lot_area }}</td>
                    <!-- Floor Area -->

                    <td>
                      <button @click="manageUnit(unit)">Edit</button>
                    </td>
                  </tr>
                </tbody>
              </table>

              <div v-else>
                <p>No units available for this section.</p>
              </div>

              <!-- Pagination -->
              <div class="pagination-controls">
                <button @click="previousPage" :disabled="currentPage === 1">
                  Previous
                </button>
                <span>Page {{ currentPage }} of {{ totalPages }}</span>
                <button
                  @click="nextPage"
                  :disabled="currentPage === totalPages"
                >
                  Next
                </button>
              </div>
            </div>
          </b-modal>

          <b-modal
            id="add-units-modal"
            title="Add Units"
            v-model="showAddUnitsModal"
            :disabled="isSaveButtonDisabled"
            ok-title="Save"
            @ok="addUnits"
            hide-footer
            hide-header
            centered
            size="xl"
          >
            <div class="modal-title p-3">
              <h5 class="mb-0">New Units</h5>
            </div>
            <div class="p-3">
              <form @submit.prevent="addUnits">
                <b-row>
                  <!-- Left Column: Unit Details -->
                  <b-col cols="12" md="6">
                    <!-- Section Selection (Multiple Selection) -->
                    <b-form-group label-for="unit-sections">
                      <b-row>
                        <b-col cols="12">
                          <small>Sections: (Select to add units)</small>
                          <div class="checkbox-container">
                            <b-form-checkbox-group
                              v-model="newUnitSections"
                              :options="sectionOptions"
                              name="section-checkbox"
                              id="unit-sections"
                              class="select-style"
                            ></b-form-checkbox-group>
                          </div>
                        </b-col>
                      </b-row>
                    </b-form-group>

                    <!-- Unit Type and Quantity -->
                    <b-form-group>
                      <b-row>
                        <b-col cols="12" md="6">
                          <small>Unit Type</small>
                          <b-form-select
                            v-model="newUnitType"
                            :options="unitTypeOptions"
                            required
                          ></b-form-select>
                        </b-col>
                        <b-col cols="12" md="6">
                          <small>Quantity</small>
                          <b-form-input
                            type="number"
                            v-model.number="newUnitQuantity"
                            min="1"
                            required
                          ></b-form-input>
                        </b-col>
                      </b-row>
                    </b-form-group>

                    <!-- Bedrooms, Bathrooms, and Balcony -->
                    <b-form-group>
                      <b-row>
                        <b-col cols="12" md="4">
                          <small>Bedroom</small>
                          <b-form-input
                            type="number"
                            v-model.number="newUnitBedroom"
                            min="1"
                            required
                          ></b-form-input>
                        </b-col>
                        <b-col cols="12" md="4">
                          <small>Bathroom</small>
                          <b-form-input
                            type="number"
                            v-model.number="newUnitBathroom"
                            min="1"
                            required
                          ></b-form-input>
                        </b-col>
                        <b-col cols="12" md="4">
                          <small>Balcony</small>
                          <b-form-select
                            v-model="newUnitBalcony"
                            :options="balconyOptions"
                            required
                          ></b-form-select>
                        </b-col>
                      </b-row>
                    </b-form-group>

                    <!-- Lot Area and Floor Area -->
                    <b-form-group>
                      <b-row>
                        <b-col cols="12" md="6">
                          <small>Lot Area</small>
                          <b-form-input
                            type="number"
                            v-model.number="newUnitLotArea"
                            min="1"
                            required
                          ></b-form-input>
                        </b-col>
                        <b-col cols="12" md="6">
                          <small>Floor Area</small>
                          <b-form-input
                            type="number"
                            v-model.number="newUnitFloorArea"
                            min="1"
                            required
                          ></b-form-input>
                        </b-col>
                      </b-row>
                    </b-form-group>

                    <!-- Status and View -->
                    <b-form-group>
                      <b-row>
                        <b-col cols="12" md="6">
                          <small>Status</small>
                          <b-form-select
                            v-model="newUnitStatus"
                            :options="statusOptions"
                            required
                          ></b-form-select>
                        </b-col>
                        <b-col cols="12" md="6">
                          <small>View</small>
                          <b-form-select
                            v-model="newUnitView"
                            :options="viewOptions"
                            required
                          ></b-form-select>
                        </b-col>
                      </b-row>
                    </b-form-group>
                  </b-col>

                  <!-- Right Column: Price, Commission, Discounts, etc. -->
                  <b-col cols="12" md="6">
                    <!-- Price -->
                    <b-form-group>
                      <small>Price</small>
                      <b-form-input
                        type="number"
                        v-model.number="newUnitPrice"
                        min="0"
                        required
                      ></b-form-input>
                    </b-form-group>

                    <!-- Reservation Fee and Commission -->
                    <b-form-group>
                      <b-row>
                        <b-col cols="12" md="6">
                          <small>Reservation</small>
                          <b-form-input
                            type="number"
                            v-model.number="newUnitReservationFee"
                            min="0"
                          ></b-form-input>
                        </b-col>
                        <b-col cols="12" md="6">
                          <small>Commission</small>
                          <b-form-input
                            type="number"
                            v-model.number="newUnitCommission"
                            min="0"
                          ></b-form-input>
                        </b-col>
                      </b-row>
                    </b-form-group>

                    <!-- Spot Discount Percentage and Flat -->
                    <b-form-group>
                      <b-row>
                        <b-col cols="12" md="6">
                          <small>Spot Discount Percentage</small>
                          <b-form-input
                            type="number"
                            v-model.number="newUnitSpotDiscountPercentage"
                            min="0"
                          ></b-form-input>
                        </b-col>
                        <b-col cols="12" md="6">
                          <small>Spot Discount Flat</small>
                          <b-form-input
                            type="number"
                            v-model.number="newUnitSpotDiscountFlat"
                            min="0"
                          ></b-form-input>
                        </b-col>
                      </b-row>
                    </b-form-group>

                    <!-- VAT Percentage and Other Charges -->
                    <b-form-group>
                      <b-row>
                        <b-col cols="12" md="6">
                          <small>VAT Percentage</small>
                          <b-form-input
                            type="number"
                            v-model.number="newUnitVatPercentage"
                            min="0"
                          ></b-form-input>
                        </b-col>
                        <b-col cols="12" md="6">
                          <small>Other Charges</small>
                          <b-form-input
                            type="number"
                            v-model.number="newUnitOtherCharges"
                            min="0"
                          ></b-form-input>
                        </b-col>
                      </b-row>
                    </b-form-group>
                    <b-form-group>
                      <small>Upload Photos (Max:5)</small>
                      <input
                        type="file"
                        @change="handleFileChange"
                        multiple
                        accept="image/jpeg, image/png, image/jpg"
                        class="form-control"
                      />
                    </b-form-group>
                  </b-col>
                </b-row>
                <div
                  class="d-flex justify-content-end gap-2 mt-3"
                  style="padding-top: 15px"
                >
                  <button type="submit" class="btn-add" style="width: 150px">
                    Add New Site
                  </button>
                  <button
                    type="button"
                    @click="showAddUnitsModal = false"
                    class="btn-cancel"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </b-modal>

          <!-- View Selected Unit Modal -->
          <b-modal
            v-model="showEditUnitModal"
            title="Edit Unit"
            @hide="clearSelectedUnit"
          >
            <template v-if="selectedUnit">
              <form>
                <!-- Unit Images Section -->
                <b-form-group label="Unit Images:">
                  <div v-if="selectedUnit.images && selectedUnit.images.length">
                    <b-row class="mb-3">
                      <!-- Loop through images and display them -->
                      <b-col
                        v-for="(image, index) in selectedUnit.images"
                        :key="index"
                        cols="12"
                        sm="6"
                        md="4"
                        lg="3"
                        class="mb-2"
                      >
                        <div class="d-flex flex-column align-items-center">
                          <b-img
                            v-if="image && image.image"
                            :src="getPictureUrl(image.image)"
                            alt="Unit Image"
                            thumbnail
                            fluid
                            class="unit-image-preview"
                          />
                          <p v-else class="text-danger">Invalid image path</p>

                          <!-- Image Name, Update, and Delete buttons -->
                          <div class="text-center mt-2">
                            <span>{{ image.image_name || "Untitled" }}</span>
                            <b-button
                              size="sm"
                              variant="primary"
                              class="ml-2"
                              @click="toggleImageEdit(index)"
                            >
                              Update
                            </b-button>
                            <b-button
                              size="sm"
                              variant="danger"
                              class="ml-2"
                              @click="deleteImage(index)"
                            >
                              Delete
                            </b-button>
                          </div>

                          <!-- Image Replace Form (Toggled) -->
                          <div v-if="imageEditIndex === index" class="mt-2">
                            <input
                              type="file"
                              accept="image/*"
                              @change="onImageSelected(index, $event)"
                            />
                            <b-button
                              variant="secondary"
                              @click="replaceImage(index)"
                            >
                              Replace Image
                            </b-button>
                          </div>
                        </div>
                      </b-col>
                    </b-row>
                  </div>
                  <p v-else>No images available for this unit.</p>

                  <!-- Add Image Button if less than 5 images -->
                  <div
                    v-if="selectedUnit.images && selectedUnit.images.length < 5"
                    class="mt-3"
                  >
                    <b-button variant="primary" @click="triggerAddImage">
                      Add Image
                    </b-button>

                    <!-- Immediately show file input when Add Image is clicked -->
                    <input
                      v-if="isAddingImage"
                      type="file"
                      accept="image/*"
                      @change="handleFileChangeImage"
                      class="form-control mt-2"
                    />
                  </div>
                </b-form-group>

                <!-- Unit Information -->
                <b-form-group label="Unit Number:">
                  <b-form-input v-model="selectedUnit.unit_number" disabled />
                </b-form-group>

                <b-form-group label="Unit Type:">
                  <b-form-input
                    :value="getUnitTypeName(selectedUnit.unit_type)"
                    disabled
                  />
                </b-form-group>

                <b-form-group label="Status:">
                  <b-form-select
                    v-model="selectedUnit.status"
                    :options="editStatusOptions"
                    disabled
                  />
                </b-form-group>

                <b-form-group label="Price:">
                  <b-form-input
                    v-model="selectedUnit.price"
                    type="number"
                    disabled
                  />
                </b-form-group>

                <b-form-group label="Lot Area:">
                  <b-form-input
                    v-model="selectedUnit.lot_area"
                    type="number"
                    disabled
                  />
                </b-form-group>

                <b-form-group label="Floor Area:">
                  <b-form-input
                    v-model="selectedUnit.floor_area"
                    type="number"
                    disabled
                  />
                </b-form-group>

                <b-form-group label="Commission:">
                  <b-form-input
                    v-model="selectedUnit.commission"
                    type="number"
                    disabled
                  />
                </b-form-group>

                <b-form-group label="Balcony:">
                  <b-form-select
                    v-model="selectedUnit.balcony"
                    :options="balconyOptions"
                  ></b-form-select>
                </b-form-group>

                <b-form-group label="View:">
                  <b-form-select
                    v-model="selectedUnit.view"
                    :options="viewOptions"
                  ></b-form-select>
                </b-form-group>

                <!-- Save Changes Button -->
                <b-button
                  variant="primary"
                  @click="saveUnitChanges"
                  class="mr-2"
                >
                  Save Changes
                </b-button>
              </form>
            </template>

            <template v-else>
              <p>Loading unit details...</p>
            </template>
          </b-modal>

          <!-- Add Units to Section Modal -->
          <b-modal
            id="add-section-units-modal"
            title="Add Units to Section"
            v-model="showAddSectionUnitsModal"
            ok-title="Save"
            @ok="addSectionUnits(newUnitSections[0])"
          >
            <form @submit.prevent="addSectionUnits(newUnitSections[0])">
              <!-- Only one section (already set) -->
              <b-form-group
                label="Section:"
                description="This section will have new units added."
              >
                <b-form-select
                  v-model="newUnitSections"
                  :options="sectionOptions"
                  required
                  disabled
                ></b-form-select>
              </b-form-group>

              <!-- Image Upload (Multiple Files) -->
              <b-form-group
                label="Upload Images:"
                description="You can upload up to 5 images."
              >
                <input
                  type="file"
                  @change="handleFileChange"
                  multiple
                  accept="image/jpeg, image/png, image/jpg"
                  class="form-control"
                />
              </b-form-group>

              <!-- Unit Type -->
              <b-form-group
                label="Unit Type:"
                description="Select the type of unit"
              >
                <b-form-select
                  v-model="newUnitType"
                  :options="unitTypeOptions"
                  required
                ></b-form-select>
              </b-form-group>

              <!-- Quantity -->
              <b-form-group label="Quantity:">
                <b-form-input
                  type="number"
                  v-model.number="newUnitQuantity"
                  min="1"
                  required
                ></b-form-input>
              </b-form-group>

              <!-- Additional Fields (Bedrooms, Bathrooms, etc.) -->
              <b-form-group label="Bedrooms:">
                <b-form-input
                  type="number"
                  v-model.number="newUnitBedroom"
                  min="1"
                  required
                ></b-form-input>
              </b-form-group>

              <!-- Bathroom -->
              <b-form-group label="Bathrooms:">
                <b-form-input
                  type="number"
                  v-model.number="newUnitBathroom"
                  min="1"
                  required
                ></b-form-input>
              </b-form-group>

              <!-- Lot Area -->
              <b-form-group label="Lot Area (sq.m):">
                <b-form-input
                  type="number"
                  v-model.number="newUnitLotArea"
                  min="1"
                  required
                ></b-form-input>
              </b-form-group>

              <!-- Floor Area -->
              <b-form-group label="Floor Area (sq.m):">
                <b-form-input
                  type="number"
                  v-model.number="newUnitFloorArea"
                  min="1"
                  required
                ></b-form-input>
              </b-form-group>

              <!-- Price -->
              <b-form-group
                label="Price:"
                description="Enter the price of the unit"
              >
                <b-form-input
                  type="number"
                  v-model.number="newUnitPrice"
                  min="0"
                  required
                ></b-form-input>
              </b-form-group>

              <!-- Status -->
              <b-form-group label="Status:">
                <b-form-select
                  v-model="newUnitStatus"
                  :options="statusOptions"
                  required
                ></b-form-select>
              </b-form-group>

              <!-- View -->
              <b-form-group label="View:">
                <b-form-select
                  v-model="newUnitView"
                  :options="viewOptions"
                ></b-form-select>
              </b-form-group>

              <!-- Balcony -->
              <b-form-group label="Balcony:">
                <b-form-select
                  v-model="newUnitBalcony"
                  :options="balconyOptions"
                ></b-form-select>
              </b-form-group>

              <!-- Commission -->
              <b-form-group label="Commission:">
                <b-form-input
                  type="number"
                  v-model.number="newUnitCommission"
                  min="0"
                  required
                ></b-form-input>
              </b-form-group>

              <!-- Spot Discount Percentage -->
              <b-form-group label="Spot Discount Percentage:">
                <b-form-input
                  type="number"
                  v-model.number="newUnitSpotDiscountPercentage"
                  min="0"
                ></b-form-input>
              </b-form-group>

              <!-- Spot Discount Flat -->
              <b-form-group label="Spot Discount Flat:">
                <b-form-input
                  type="number"
                  v-model.number="newUnitSpotDiscountFlat"
                  min="0"
                ></b-form-input>
              </b-form-group>

              <!-- Reservation Fee -->
              <b-form-group label="Reservation Fee:">
                <b-form-input
                  type="number"
                  v-model.number="newUnitReservationFee"
                  min="0"
                ></b-form-input>
              </b-form-group>

              <!-- Other Charges -->
              <b-form-group label="Other Charges:">
                <b-form-input
                  type="number"
                  v-model.number="newUnitOtherCharges"
                  min="0"
                ></b-form-input>
              </b-form-group>

              <!-- VAT Percentage -->
              <b-form-group label="VAT Percentage:">
                <b-form-input
                  type="number"
                  v-model.number="newUnitVatPercentage"
                  min="0"
                ></b-form-input>
              </b-form-group>
            </form>
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
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";
import { mapState } from "vuex";
import {
  BModal,
  BFormGroup,
  BFormSelect,
  BFormInput,
  BButton,
  BImg,
  BRow,
  BCol,
} from "bootstrap-vue-3";

export default {
  name: "DevUnitManagement",
  components: {
    SideNav,
    AppHeader,
    BModal,
    BFormGroup,
    BFormSelect,
    BFormInput,
    BButton,
    BImg,
    BRow,
    BCol,
  },
  data() {
    return {
      showAddUnitsModal: false,
      unitTypes: [],
      site: null,
      sections: [],
      newUnitSection: null,
      newUnitSections: [],
      newUnitQuantity: 1,
      newUnitType: null,
      newUnitTitle: "",
      newUnitBedroom: 1,
      newUnitBathroom: 1,
      newUnitFloorArea: null,
      newUnitPrice: null,
      newUnitStatus: "Available",
      newUnitView: null,
      newUnitBalcony: "no balcony",
      newUnitLotArea: null,
      newUnitCommission: null,
      newUnitSpotDiscountPercentage: null,
      newUnitSpotDiscountFlat: null,
      newUnitReservationFee: null,
      newUnitOtherCharges: null,
      newUnitVatPercentage: null,
      sortOptions: [
        { value: null, text: "Default" },
        { value: "unit_number_asc", text: "Unit Number (Asc)" },
        { value: "unit_number_desc", text: "Unit Number (Desc)" },
        { value: "price_asc", text: "Price (Asc)" },
        { value: "price_desc", text: "Price (Desc)" },
      ],
      // Updated options with "All"
      statusOptions: [
        { value: null, text: "Default" },
        { value: "Available", text: "Available" },
        { value: "Sold", text: "Sold" },
        { value: "Pending Reservation", text: "Pending Reservation" },
        { value: "Reserved", text: "Reserved" },
      ],
      editStatusOptions: [
        { value: "Available", text: "Available" },
        { value: "Sold", text: "Sold" },
        { value: "Pending Reservation", text: "Pending Reservation" },
        { value: "Reserved", text: "Reserved" },
      ],
      priceRangeOptions: [
        { value: null, text: "Default" },
        { value: "1-5", text: "1M - 5M" },
        { value: "5-10", text: "5M - 10M" },
        { value: "10-15", text: "10M - 15M" },
        { value: "15-20", text: "15M - 20M" },
        { value: "20-25", text: "20M - 25M" },
        { value: "25+", text: "25M+" },
      ],
      viewOptions: [
        { value: "south", text: "South" },
        { value: "north", text: "North" },
        { value: "east", text: "East" },
        { value: "west", text: "West" },
      ],
      balconyOptions: [
        { value: "has balcony", text: "Yes" },
        { value: "no balcony", text: "No" },
      ],
      totalUnits: 0,
      totalAvailableUnits: 0,
      unitFields: [],
      unitsData: [],
      currentPage: 1,
      unitsPerPage: 25,
      searchQuery: "",
      newUnitImages: [],
      sectionSortOrder: "asc",
      showEditUnitModal: false,
      selectedUnit: {},
      totalItems: 100, // Example: Set this value based on your API response or logic
      itemsPerPage: 10,
      showAddSectionUnitsModal: false, // Track the modal visibility
      showUnitManagementModal: false,
      selectedSection: {},
      selectedStatus: null,
      selectedPriceRange: null,
      selectedUnitType: null,
      selectedSort: null,
      imageEditIndex: null, // To track which image is being edited
      imageFile: [], // To store the new files selected for replacement
      isAddingImage: false,
      showNotification: false,
      notificationTitle: "",
      notificationMessage: "",
      showConfirmModal: false, // Controls modal visibility
      confirmMessage: "", // Stores the confirmation message
      actionToConfirm: null, // Renamed this from 'confirmAction'
      confirmParams: [],
    };
  },
  computed: {
    ...mapState({
      loggedIn: (state) => state.loggedIn,
      userId: (state) => state.userId,
      companyId: (state) => state.companyId,
    }),
    isSaveButtonDisabled() {
      return this.newUnitFloorArea < this.newUnitLotArea;
    },

    sectionOptions() {
      if (this.site && this.site.sections) {
        const sectionsCopy = [...this.site.sections];
        const sortedSections = sectionsCopy.sort((a, b) => {
          if (this.sectionSortOrder === "asc") {
            return a.number - b.number;
          }
          return b.number - a.number;
        });

        return sortedSections.map((section) => {
          let sectionName = section.name || `Section ${section.number}`;

          // Adjust naming based on the site's `section_label`
          if (this.site.section_label === "block") {
            if (section.number > 0) {
              sectionName = `Block ${String.fromCharCode(
                65 + section.number - 1
              )} (${section.number})`;
            } else {
              sectionName = `Block ${section.number}`;
            }
          } else if (this.site.section_label === "level") {
            // Customize naming for level-based section_label
            sectionName = `Level ${section.number}`;
          } else if (this.site.section_label === "floor") {
            // Customize naming for floor-based section_label
            sectionName = `Floor ${section.number}`;
          } else {
            // Default case (e.g., section_label not recognized)
            sectionName = `Section ${section.number}`;
          }

          return {
            value: section.id,
            text: sectionName,
          };
        });
      } else {
        return [];
      }
    },
    unitTypeOptions() {
      return [
        { value: null, text: "Select" },
        ...this.unitTypes.map((type) => ({
          value: type.id,
          text: type.name,
        })),
      ];
    },

    filteredUnits() {
      let units = this.unitsData;

      // Filter by search query
      if (this.searchQuery) {
        units = units.filter((unit) =>
          unit.unit_number
            .toLowerCase()
            .includes(this.searchQuery.toLowerCase())
        );
      }

      // Filter by status
      if (this.selectedStatus) {
        units = units.filter((unit) => unit.status === this.selectedStatus);
      }

      // Filter by unit type
      if (this.selectedUnitType !== null) {
        units = units.filter(
          (unit) => unit.unit_type === Number(this.selectedUnitType)
        );
      }

      // Filter by price range
      if (this.selectedPriceRange) {
        const priceRange = this.selectedPriceRange;
        units = units.filter((unit) => {
          const price = unit.price;
          // Price range filters based on selected range
          if (priceRange === "1-5") return price >= 1 && price <= 5000000;
          if (priceRange === "5-10")
            return price >= 5000001 && price <= 10000000;
          if (priceRange === "10-15")
            return price >= 10000001 && price <= 15000000;
          if (priceRange === "15-20")
            return price >= 15000001 && price <= 20000000;
          if (priceRange === "20-25")
            return price >= 20000001 && price <= 25000000;
          if (priceRange === "25+") return price > 25000000;
          return true; // Default case: no filtering by price range
        });
      }

      // Sort units
      if (this.selectedSort) {
        units = [...units].sort((a, b) => {
          switch (this.selectedSort) {
            case "unit_number_asc":
              return a.unit_number - b.unit_number;
            case "unit_number_desc":
              return b.unit_number - a.unit_number;
            case "price_asc":
              return a.price - b.price;
            case "price_desc":
              return b.price - a.price;
            default:
              return 0; // No sorting if no option is selected
          }
        });
      }

      return units;
    },

    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage);
    },
    sortedSections() {
      if (!this.site?.sections) return [];
      return [...this.site.sections].sort((a, b) =>
        this.sectionSortOrder === "asc"
          ? a.number - b.number
          : b.number - a.number
      );
    },
  },
  mounted() {
    if (!this.loggedIn || !this.companyId) {
      this.redirectToLogin();
    } else {
      this.fetchSiteDetails();
      this.fetchUnitTypes();
    }
    this.fetchUnits();
  },
  methods: {
    sectionOptionsForSection(section) {
      let sectionName = section.name || `Section ${section.number}`;

      // Adjust naming based on the site's `section_label`
      if (this.site.section_label === "block") {
        if (section.number > 0) {
          sectionName = `Block ${String.fromCharCode(
            65 + section.number - 1
          )} (${section.number})`;
        } else {
          sectionName = `Block ${section.number}`;
        }
      } else if (this.site.section_label === "unit") {
        // Customize naming for unit-based section_label
        sectionName = `Unit ${section.number}`;
      } else if (this.site.section_label === "level") {
        // Customize naming for level-based section_label
        sectionName = `Level ${section.number}`;
      } else if (this.site.section_label === "floor") {
        // Customize naming for floor-based section_label
        sectionName = `Floor ${section.number}`;
      } else {
        // Default case (e.g., section_label not recognized)
        sectionName = `Section ${section.number}`;
      }

      return sectionName;
    },

    async fetchSiteDetails() {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/sites/${this.$route.params.siteId}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.site = response.data.data;

        // Log the site object to see its properties

        if (this.site && this.site.sections) {
          this.fetchSectionsData();
        } else {
          console.error("No sections data available");
        }
      } catch (error) {
        console.error("Error fetching site details:", error);
      }
    },
    async fetchSectionsData() {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/sites/${this.$route.params.siteId}/sections/`, // Correct endpoint for section data
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        if (response.data.success) {
          this.sections = response.data.data; // This will be an array of sections with total and available unit counts
        } else {
          console.error("Error fetching section data:", response.data.error);
        }
      } catch (error) {
        console.error("Error fetching sections:", error);
      }
    },
    async fetchUnitTypes() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/units/types/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          this.unitTypes = response.data.data; // This assumes the response contains a `data` key
        } else {
          console.error("Error fetching unit types:", response);
          alert("Error fetching unit types.");
        }
      } catch (error) {
        console.error("Error fetching unit types:", error);
        alert("An error occurred while fetching unit types.");
      }
    },
    async addUnits() {
      // Validate form fields
      if (
        !this.newUnitSections.length ||
        !this.newUnitType ||
        !this.newUnitPrice ||
        !this.newUnitLotArea ||
        !this.newUnitFloorArea ||
        !this.newUnitQuantity
      ) {
        alert("Please fill in all the required fields.");
        return;
      }

      // Create a FormData object to send both unit data and images
      const formData = new FormData();
      formData.append("quantity", this.newUnitQuantity);
      formData.append("unit_type_id", this.newUnitType);
      formData.append("unit_title", this.newUnitTitle);
      formData.append("bedroom", this.newUnitBedroom);
      formData.append("bathroom", this.newUnitBathroom);
      formData.append("lot_area", this.newUnitLotArea);
      formData.append("floor_area", this.newUnitFloorArea);
      formData.append("price", this.newUnitPrice);
      formData.append("status", this.newUnitStatus);
      formData.append("view", this.newUnitView);
      formData.append("balcony", this.newUnitBalcony);
      formData.append("commission", this.newUnitCommission);
      formData.append(
        "spot_discount_percentage",
        this.newUnitSpotDiscountPercentage
      );
      formData.append("spot_discount_flat", this.newUnitSpotDiscountFlat);
      formData.append("reservation_fee", this.newUnitReservationFee);
      formData.append("other_charges", this.newUnitOtherCharges);
      formData.append("vat_percentage", this.newUnitVatPercentage);

      // Log the selected section IDs

      // Append the selected section IDs as an array
      this.newUnitSections.forEach((sectionId) => {
        formData.append("section_ids[]", sectionId);
      });

      if (this.newUnitImages && this.newUnitImages.length) {
        for (let i = 0; i < this.newUnitImages.length; i++) {
          const image = this.newUnitImages[i];

          // Append image file with a unique key based on index
          formData.append(`images[${i}]`, image);

          // Append image type and primary flag with unique keys as well
          formData.append(`image_types[${i}]`, image.image_type || "Unit");
          formData.append(`primaries[${i}]`, image.primary || false);

          // Log the data for debugging
        }
      } else {
        console.log("No images selected.");
      }

      try {
        // Send the FormData to the backend
        const response = await axios.post(
          "http://localhost:8000/developer/units/bulk-add/",
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.status === 201) {
          this.fetchSiteDetails(); // Refresh the site details
          this.showAddUnitsModal = false; // Close the modal
          this.notificationTitle = "Success";
          this.notificationMessage = "Unit/s updated successfully!";
          this.showNotification = true;
        }
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage = "An error occurred while adding unit/s.";
        this.showNotification = true;
      }
    },
    toggleAddUnitsModal() {
      this.showAddUnitsModal = !this.showAddUnitsModal;
      if (!this.showAddUnitsModal) {
        // Reset fields when closing the modal
        this.newUnitSection = null;
        this.newUnitType = null;
        this.newUnitTitle = "";
        this.newUnitBedroom = 1;
        this.newUnitBathroom = 1;
        this.newUnitLotArea = null;
        this.newUnitFloorArea = null;
        this.newUnitPrice = null;
        this.newUnitStatus = "Available";
        this.newUnitView = null;
        this.newUnitBalcony = "no balcony";
      }
    },
    openAddUnitModalForSection(sectionId) {
      this.newUnitSections = [sectionId]; // Set the section ID in the array
      this.showAddSectionUnitsModal = true; // Open the modal to add units to the specific section
    },
    async addSectionUnits(sectionId) {
      // Validate form fields
      if (
        !this.newUnitType ||
        !this.newUnitPrice ||
        !this.newUnitLotArea ||
        !this.newUnitFloorArea ||
        !this.newUnitQuantity ||
        !sectionId
      ) {
        alert("Please fill in all the required fields.");
        return;
      }

      // Create FormData to send both unit data and images
      const formData = new FormData();
      formData.append("quantity", this.newUnitQuantity);
      formData.append("unit_type_id", this.newUnitType);
      formData.append("unit_title", this.newUnitTitle);
      formData.append("bedroom", this.newUnitBedroom);
      formData.append("bathroom", this.newUnitBathroom);
      formData.append("lot_area", this.newUnitLotArea);
      formData.append("floor_area", this.newUnitFloorArea);
      formData.append("price", this.newUnitPrice);
      formData.append("status", this.newUnitStatus);
      formData.append("view", this.newUnitView);
      formData.append("balcony", this.newUnitBalcony);
      formData.append("commission", this.newUnitCommission);
      formData.append(
        "spot_discount_percentage",
        this.newUnitSpotDiscountPercentage
      );
      formData.append("spot_discount_flat", this.newUnitSpotDiscountFlat);
      formData.append("reservation_fee", this.newUnitReservationFee);
      formData.append("other_charges", this.newUnitOtherCharges);
      formData.append("vat_percentage", this.newUnitVatPercentage);

      // Append the selected section ID
      formData.append("section_ids[]", sectionId); // Directly pass the sectionId

      // Log the selected images
      if (this.newUnitImages && this.newUnitImages.length) {
        for (let i = 0; i < this.newUnitImages.length; i++) {
          const image = this.newUnitImages[i];

          // Append image file with a unique key based on index
          formData.append(`images[${i}]`, image);

          // Append image type and primary flag with unique keys as well
          formData.append(`image_types[${i}]`, image.image_type || "Unit");
          formData.append(`primaries[${i}]`, image.primary || false);

          // Log the data for debugging
        }
      } else {
        console.log("No images selected.");
      }

      try {
        const response = await axios.post(
          "http://localhost:8000/developer/units/bulk-add/",
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.status === 201) {
          this.openUnitManagement({ id: sectionId });
          this.fetchSiteDetails(); // Refresh site details
          this.showAddSectionUnitsModal = false; // Close the modal
          this.notificationTitle = "Success";
          this.notificationMessage = "Unit/s updated successfully!";
          this.showNotification = true;
        }
      } catch (error) {
        this.notificationTitle = "Error";
        this.notificationMessage = "An error occurred while adding unit/s.";
        this.showNotification = true;
      }
    },

    async openUnitManagement(section) {
      if (!section.id) {
        console.error("Invalid section ID:", section);
        alert("Invalid section ID.");
        return;
      }

      try {
        const response = await axios.get(
          `http://localhost:8000/developer/units/${this.$route.params.siteId}/sections/${section.id}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.selectedSection = section;
        this.unitsData = response.data.data;
        this.showUnitManagementModal = true;
      } catch (error) {
        console.error("Error fetching units:", error);
        alert("Failed to fetch units.");
      }
    },
    closeUnitManagementModal() {
      this.showUnitManagementModal = false;
      this.unitsData = [];
      this.searchQuery = "";
      this.currentPage = 1;
    },
    async fetchUnits(unitId = null) {
      if (unitId) {
        try {
          this.isLoading = true;
          const response = await axios.get(
            `http://localhost:8000/developer/units/${unitId}/`,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
            }
          );
          this.selectedUnit = response.data; // Set the fetched unit data to selectedUnit
        } catch (error) {
          console.error("Error fetching unit details:", error);
          this.errorMessage = "Failed to load unit details.";
        } finally {
          this.isLoading = false;
        }
      } else {
        console.error("No unit ID provided to fetch.");
      }
    },
    async manageUnit(unit = null) {
      if (unit) {
        try {
          this.selectedUnit = unit; // Make sure selectedUnit is set
          this.showEditUnitModal = true; // Show the modal for editing
        } catch (error) {
          console.error(
            "Error fetching unit details:",
            error.response || error
          );
        }
      } else {
        this.selectedUnit = {}; // Initialize an empty object for a new unit
        this.showEditUnitModal = true; // Show modal for new unit creation
      }
    },
    async saveUnitChanges() {
      this.showConfirmation(
        "Are you sure you want to save the changes to this unit?",
        async () => {
          const formData = new FormData();
          formData.append("unit_number", this.selectedUnit.unit_number);
          formData.append("unit_type_id", this.selectedUnit.unit_type);
          formData.append("status", this.selectedUnit.status);
          formData.append("price", this.selectedUnit.price);
          formData.append("lot_area", this.selectedUnit.lot_area);
          formData.append("floor_area", this.selectedUnit.floor_area);
          formData.append("commission", this.selectedUnit.commission);
          formData.append("balcony", this.selectedUnit.balcony);
          formData.append("view", this.selectedUnit.view);

          // Handle image files if any
          if (this.selectedUnit.images && this.imageFile) {
            this.selectedUnit.images.forEach((image, index) => {
              if (this.imageFile[index]) {
                formData.append(`image_${index}`, this.imageFile[index]);
              }
            });
          }

          try {
            let response;

            // If the unit has an id, it's an update (PUT request)
            response = await axios.put(
              `http://localhost:8000/developer/units/${this.selectedUnit.id}/`,
              formData,
              {
                headers: {
                  Authorization: `Bearer ${localStorage.getItem(
                    "accessToken"
                  )}`,
                  "Content-Type": "multipart/form-data",
                },
              }
            );

            if (response.status === 200 || response.status === 201) {
              this.showEditUnitModal = false;
              this.fetchUnits(); // Fetch the updated list of units
            }
          } catch (error) {
            console.error(
              "Error saving unit changes:",
              error.response || error
            );
          }
        },
        []
      );
    },
    // Method to toggle the image edit state (show/hide replace form)
    toggleImageEdit(index) {
      this.imageEditIndex = this.imageEditIndex === index ? null : index;
    },

    // Trigger Add Image and show the file input
    triggerAddImage() {
      if (this.selectedUnit.images.length < 5) {
        this.isAddingImage = true; // Show the file input
      }
    },

    // Handle file change when user selects an image
    handleFileChangeImage(event) {
      const file = event.target.files[0];
      if (file) {
        this.imageFile.push(file); // Store the selected file
        this.uploadNewImage();
      }
    },

    // Upload the new image
    async uploadNewImage() {
      const formData = new FormData();
      formData.append("image", this.imageFile[this.imageFile.length - 1]);

      try {
        const response = await axios.post(
          `http://localhost:8000/developer/units/${this.selectedUnit.id}/images/`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.status === 201) {
          // Add the uploaded image to the unit's images array
          this.selectedUnit.images.push(response.data);
          this.isAddingImage = false; // Hide the file input after upload
        }
      } catch (error) {
        console.error("Error uploading image:", error.response || error);
      }
    },

    onImageSelected(index, event) {
      // This stores the selected file into the imageFile array for the specific index
      this.imageFile[index] = event.target.files[0];
    },

    async replaceImage(index) {
      const formData = new FormData();
      // Ensure the file exists before appending it to FormData
      if (!this.imageFile[index]) {
        console.error("No image selected for replacement.");
        return;
      }

      formData.append("image", this.imageFile[index]);

      try {
        const response = await axios.put(
          `http://localhost:8000/developer/units/${this.selectedUnit.id}/images/${this.selectedUnit.images[index].id}/`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.status === 200) {
          // Update the image source if the replacement was successful
          this.selectedUnit.images[index].image = response.data.image;
        }
      } catch (error) {
        console.error("Error replacing image:", error.response || error);
      }
    },

    // Delete the image from the selected unit
    async deleteImage(index) {
      try {
        const response = await axios.delete(
          `http://localhost:8000/developer/units/${this.selectedUnit.id}/images/${this.selectedUnit.images[index].id}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        if (response.status === 200) {
          this.selectedUnit.images.splice(index, 1); // Remove the image from the array
        }
      } catch (error) {
        console.error("Error deleting image:", error.response || error);
      }
    },

    showConfirmation(message, action, params) {
      this.confirmMessage = message;
      this.actionToConfirm = action; // Use the renamed key here
      this.confirmParams = params;
      this.showConfirmModal = true;
    },

    cancelAction() {
      this.showConfirmModal = false; // Close modal on cancel
    },

    async confirmAction() {
      try {
        // Dynamically call the function stored in actionToConfirm with the provided params
        await this.actionToConfirm(...this.confirmParams);
        this.showConfirmModal = false; // Close modal after confirmation
      } catch (error) {
        this.showConfirmModal = false; // Close modal on error
        this.notificationTitle = "Error";
        this.notificationMessage = "An error occurred during the action.";
        this.showNotification = true;
      }
    },

    getPictureUrl(picture) {
      return `http://localhost:8000${picture}`;
    },
    // This is the method that opens the modal for editing a unit
    openEditUnitModal(unit) {
      // Ensure the selected unit is properly set before opening the modal
      this.selectedUnit = unit;
      this.showEditUnitModal = true;
    },
    closeEditUnitModal() {
      this.showEditUnitModal = false;
      this.selectedUnit = null; // Clear selected unit when closing the modal
    },
    clearSelectedUnit() {
      this.selectedUnit = null; // Reset selectedUnit when the modal is closed
    },
    handleFileChange(event) {
      this.newUnitImages = Array.from(event.target.files);
    },
    getUnitTypeName(unitTypeId) {
      // Find the unit type by id
      const unitType = this.unitTypes.find((type) => type.id === unitTypeId);
      // Return the name if found, otherwise return 'Unknown'
      return unitType ? unitType.name : "Unknown";
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    previousPage() {
      if (this.currentPage > 1) this.currentPage--;
    },
    formatCurrency(value) {
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "PHP",
      }).format(value);
    },
    onSearch() {
      this.currentPage = 1; // Reset pagination on new search
    },

    sortSections() {
      if (this.sectionSortOrder === "asc") {
        this.sortedSections = this.site.sections.sort(
          (a, b) => a.number - b.number
        );
      } else if (this.sectionSortOrder === "desc") {
        this.sortedSections = this.site.sections.sort(
          (a, b) => b.number - a.number
        );
      }
    },
    redirectToLogin() {
      this.$router.push({ name: "DevLogin" });
    },
  },
};
</script>

<style scoped>
/* General Styles */
html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

/* Main Page Layout */
.main-page {
  display: flex;
  min-height: 100vh;
  background-color: #e8f0fa;
}

/* Side Navigation */
.SideNav {
  width: 250px;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #343a40;
}

/* Header */
.AppHeader {
  width: 100%;
  height: 60px;
  background-color: #343a40;
  display: flex;
  align-items: center;
  padding-left: 10px;
  color: #ffffff;
}

/* Content Layout */
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
  display: flex;
  /* Use flexbox to center the content */
  align-items: center;
  /* Center vertically */
  flex-direction: column;
  /* Stack the dashboard boxes and sales table vertically */
}

.title-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1100px;
  width: 100%;
  margin: 20px auto;
  /* Center the wrapper */
}

.title-left {
  display: flex;
  align-items: center;
}

.total-broker {
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
  gap: 30px;

  /* Space between search bar and dropdown */
}

.left-section p {
  margin: 0;
  /* Remove default margin */
  line-height: 38px;
  /* Match the dropdown height */
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
  border-radius: 4px;
  font-size: 14px;
  width: 150px;
  background-color: white;
  color: #333;
  padding-right: 30px;
  background-image: url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"%3E%3Cpath d="M7 10l5 5 5-5z"/%3E%3C/svg%3E');
  background-position: right 10px center;
  background-repeat: no-repeat;
  background-size: 14px;
}

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  margin-top: 0;
  padding: 15px;
  max-width: 1100px;
  width: 100%;
  /* Ensures the card and grid align */
  margin-left: auto;
  /* Centers the card */
  margin-right: auto;
}

.outside-headers {
  display: grid;
  /* Change to grid layout */
  grid-template-columns: 40% 20% 25% 15%;
  /* Match the column widths */
  padding: 0px 15px;
  margin: 20px auto 10px;
  width: 100%;
  max-width: 1100px;
}

.header-item {
  flex: 1;
  text-align: left;
  font-size: 14px;
  color: #333;
  font-weight: bold;
}

.section-info {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background: #fff;
  font-size: 14px;
}

.section-info th,
.section-info td {
  padding-bottom: 5px;
  text-align: left;
  vertical-align: middle;
  border: none;
  padding: 0;
}

.section-info th:nth-child(2),
.section-info td:nth-child(2) {
  /* Location column */
  width: 20%;
}

.section-info th:nth-child(3),
.section-info td:nth-child(3) {
  /* Status column */
  width: 25%;
}

.section-info th:nth-child(4),
.section-info td:nth-child(4) {
  /* Actions column */
  width: 15%;
}

/* Site Details */
.site-overview {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.site-picture {
  flex: 1;
  margin-bottom: 20px;
}

.site-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}

.site-description-location {
  text-align: left;
  font-size: 14px;
}

.site-info {
  flex: 1;
}

.site-details {
  text-align: center;
}

.site-header {
  text-align: center;
  margin-bottom: 20px;
}

.site-header img.site-image {
  max-width: 100%;
  height: auto;
  margin-bottom: 15px;
}

.section-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.section-card {
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 8px;
  width: 200px;
  margin: 10px;
  text-align: center;
}

button {
  background-color: #0560fd;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  text-align: center;
}

.close {
  position: absolute;
  top: 10px;
  right: 20px;
  cursor: pointer;
}

.unit-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

.unit-table th,
.unit-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

.unit-table th {
  background-color: #f2f2f2;
}

.search-bar {
  margin-bottom: 20px;
  text-align: center;
}

.pagination-controls {
  text-align: center;
  margin-top: 20px;
}

button {
  background-color: #0560fd;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.back-button {
  background-color: transparent;
  color: black;
  border: none;
  padding: 0;
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 13px;
  /* Adjust as needed */
  text-decoration: none;
}

.back-button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
  /* Make it slightly transparent when disabled */
}

.unit-image-preview {
  max-height: 150px;
  object-fit: cover;
  border: 1px solid #ccc;
}

.site-container {
  display: flex;
  gap: 20px;
  width: 100%;
  max-width: 1100px;
  align-items: flex-start;
  /* Align items at the top */
}

.site-name {
  font-size: 18px;
  margin-bottom: 20px;
}

.site-details-section {
  flex: 1;
  /* Left section takes 1/4th of the space */
  background: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.sections-section {
  flex: 3;
  /* Right section takes 3/4th of the space */
}

.section-card {
  background: #ffffff;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.site-image {
  max-width: 100%;
  border-radius: 8px;
}

.add-units-button {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.add-units-button:hover {
  background-color: #0056b3;
}

.btn-add {
  background-color: #0560fd;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
  font-size: 14px;
  /* Match dropdown height */
}

.btn-cancel {
  background-color: #343a40;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
  font-size: 14px;
}

.btn-manage {
  background-color: #8b8b8b;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 7px;
  font-size: 10 px;
}

.site-description-location {
  display: flex;
  flex-direction: column;
  /* Stack description and location vertically */
  gap: 20px;
  /* Space between rows */
}

.description-icon,
.location-icon {
  display: flex;
  align-items: flex-start;
  /* Align icon and text vertically */
  gap: 10px;
  /* Space between icon and text */
}

.description-icon span,
.location-icon span {
  font-size: 13px;
  /* Adjust text size */
  color: #333;
  /* Text color */
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

.checkbox-container {
  display: flex;
  flex-direction: column; /* Stack items vertically */
  justify-content: flex-start; /* Align items at the top */
  align-items: stretch; /* Ensure full width alignment */
  max-height: 115px; /* Increase max-height for better visibility */
  overflow-y: auto; /* Enable vertical scrolling */
  overflow-x: hidden; /* Prevent horizontal scroll */
  padding: 5px;
  border: 1px solid #dee2e6; /* Optional: Customize border as needed */
  box-sizing: border-box; /* Ensure padding doesn't break layout */
}

/* Flexbox layout for horizontally aligned items */
.select-style {
  display: grid;
  grid-template-columns: 20% 20% 20% 20% 20%;
  /* Allow items to wrap to the next line */
}

/* Each checkbox will take up 1/5 of the container width (to fit 5 per row) */
.select-style .custom-checkbox {
  flex: 1 1 calc(20% - 10px);
  /* 5 items per row with space between */
}

.b-form-checkbox {
  margin: 0;
  /* Remove any extra margin around checkboxes */
}
</style>
