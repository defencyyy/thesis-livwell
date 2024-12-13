<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <button class="back-button" @click="$router.back()">
          <div class="back-container">
            <i class="fas fa-arrow-left"></i> Back
          </div>
        </button>

        <div v-if="site" class="site-details">
          <!-- Site Overview -->
          <div class="site-overview">
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
              <h2>{{ site.name }}</h2>
              <p>{{ site.description }}</p>
              <p><strong>Location:</strong> {{ site.location }}</p>
              <button class="add-units-button" @click="toggleAddUnitsModal">
                Add Units
              </button>
            </div>
          </div>

          <!-- Sections Section -->
          <div v-if="site.sections.length > 0">
            <h3>Sections ({{ site.sections.length }})</h3>
            <div class="section-sort">
              <label for="sortSections">Sort Sections:</label>
              <select
                id="sortSections"
                v-model="sectionSortOrder"
                @change="sortSections"
              >
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
              </select>
            </div>

            <div v-if="sortedSections.length > 0" class="section-list">
              <div
                v-for="section in sortedSections"
                :key="section.id"
                class="section-card"
              >
                <h4>Section {{ section.section_number }}</h4>
                <div class="site-summary">
                  <p><strong>Total Units:</strong> {{ section.total_units }}</p>
                  <p>
                    <strong>Available Units:</strong>
                    {{ section.available_units }}
                  </p>
                </div>
                <button @click="openUnitManagement(section)">
                  Manage Units
                </button>
              </div>
            </div>
          </div>

          <!-- If no sections are available -->
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
                  <th>Section Area</th>
                  <th>Balcony</th>
                  <th>View</th>
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
                  <!-- Section Area -->
                  <td>{{ unit.balcony }}</td>
                  <!-- Balcony -->
                  <td>{{ unit.view }}</td>
                  <!-- View -->
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
              <button @click="nextPage" :disabled="currentPage === totalPages">
                Next
              </button>
            </div>
          </div>
        </b-modal>

        <!-- Add Units Modal -->
        <b-modal
          id="add-units-modal"
          title="Add Units"
          v-model="showAddUnitsModal"
          :disabled="isSaveButtonDisabled"
          ok-title="Save"
          @ok="addUnits"
        >
          <form @submit.prevent="addUnits">
            <!-- Section Selection (Multiple Selection) -->
            <b-form-group
              label="Sections:"
              description="Select sections to add units to"
            >
              <b-form-select
                v-model="newUnitSections"
                :options="sectionOptions"
                required
                multiple
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

            <!-- Section Area -->
            <b-form-group label="Section Area (sq.m):">
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
                required
              ></b-form-select>
            </b-form-group>

            <!-- Balcony -->
            <b-form-group label="Balcony:">
              <b-form-select
                v-model="newUnitBalcony"
                :options="balconyOptions"
                required
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

              <b-form-group label="Section Area:">
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
              <b-button variant="primary" @click="saveUnitChanges" class="mr-2">
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

            <!-- Section Area -->
            <b-form-group label="Section Area (sq.m):">
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
        { value: "has balcony", text: "Has Balcony" },
        { value: "no balcony", text: "No Balcony" },
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
      // Ensure the site and sections are available
      if (this.site && this.site.sections) {
        // Clone the sections array to avoid mutating the original array
        const sectionsCopy = [...this.site.sections];

        // Sort the cloned sections array based on the selected order (asc or desc)
        const sortedSections = sectionsCopy.sort((a, b) => {
          // Ascending order (if `sectionSortOrder` is 'asc')
          if (this.sectionSortOrder === "asc") {
            return a.section_number - b.section_number;
          }
          // Descending order (if `sectionSortOrder` is 'desc')
          return b.section_number - a.section_number;
        });

        // Map the sorted sections to the options for the dropdown
        return sortedSections.map((section) => ({
          value: section.id, // section ID is the value sent to the backend
          text: `Section ${section.section_number}`, // section number is displayed as text
        }));
      } else {
        return []; // Return an empty array if no site or sections are available
      }
    },
    unitTypeOptions() {
      return [
        { value: null, text: "Default" },
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
          if (priceRange === "1-5") return price >= 1000000 && price <= 5000000;
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
          ? a.section_number - b.section_number
          : b.section_number - a.section_number
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
        console.log("Selected images:", this.newUnitImages);
        for (let i = 0; i < this.newUnitImages.length; i++) {
          const image = this.newUnitImages[i];

          // Append image file with a unique key based on index
          formData.append(`images[${i}]`, image);

          // Append image type and primary flag with unique keys as well
          formData.append(`image_types[${i}]`, image.image_type || "Unit");
          formData.append(`primaries[${i}]`, image.primary || false);

          // Log the data for debugging
          console.log(`Appending image ${i + 1}:`, image);
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

        console.log("Response from backend:", response);

        if (response.status === 201) {
          this.openUnitManagement({ id: sectionId });
          this.fetchSiteDetails(); // Refresh site details
          this.showAddSectionUnitsModal = false; // Close the modal
          alert("Units successfully added to the section!");
        }
      } catch (error) {
        console.error("Error adding units to section:", error);
        alert("Failed to add the unit. Please try again.");
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
      console.log("Selected section IDs:", this.newUnitSections);

      // Append the selected section IDs as an array
      this.newUnitSections.forEach((sectionId) => {
        formData.append("section_ids[]", sectionId);
      });

      if (this.newUnitImages && this.newUnitImages.length) {
        console.log("Selected images:", this.newUnitImages);
        for (let i = 0; i < this.newUnitImages.length; i++) {
          const image = this.newUnitImages[i];

          // Append image file with a unique key based on index
          formData.append(`images[${i}]`, image);

          // Append image type and primary flag with unique keys as well
          formData.append(`image_types[${i}]`, image.image_type || "Unit");
          formData.append(`primaries[${i}]`, image.primary || false);

          // Log the data for debugging
          console.log(`Appending image ${i + 1}:`, image);
        }
      } else {
        console.log("No images selected.");
      }

      // Log FormData content for debugging
      console.log("FormData contents before sending to backend:");
      for (let pair of formData.entries()) {
        console.log(pair[0], pair[1]);
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

        console.log("Response from backend:", response);

        if (response.status === 201) {
          this.fetchSiteDetails(); // Refresh the site details
          this.showAddUnitsModal = false; // Close the modal
          alert("Units successfully added!");
        }
      } catch (error) {
        console.error("Error adding unit:", error);
        alert("Failed to add the unit. Please try again.");
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
          console.log("Selected Unit Images:", this.selectedUnit.images);
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
      const formData = new FormData();
      formData.append("unit_number", this.selectedUnit.unit_number);
      formData.append("unit_type_id", this.selectedUnit.unit_type);
      formData.append("status", this.selectedUnit.status);
      formData.append("price", this.selectedUnit.price);
      formData.append("lot_area", this.selectedUnit.lot_area);
      formData.append("floor_area", this.selectedUnit.floor_area);
      formData.append("commission", this.selectedUnit.commission);
      formData.append("balcony", this.selectedUnit.balcony); // Add balcony
      formData.append("view", this.selectedUnit.view); // Add view

      // Handle image files if any
      this.selectedUnit.images.forEach((image, index) => {
        if (this.imageFile[index]) {
          formData.append(`image_${index}`, this.imageFile[index]);
        }
      });

      try {
        let response;

        this.selectedUnit.id;
        // If the unit has an id, it's an update (PUT request)
        response = await axios.put(
          `http://localhost:8000/developer/units/${this.selectedUnit.id}/`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.status === 200 || response.status === 201) {
          this.showEditUnitModal = false;
          this.fetchUnits(); // Fetch the updated list of units
        }
      } catch (error) {
        console.error("Error saving unit changes:", error.response || error);
      }
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
      console.log("New unit images:", this.newUnitImages);
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
          (a, b) => a.section_number - b.section_number
        );
      } else if (this.sectionSortOrder === "desc") {
        this.sortedSections = this.site.sections.sort(
          (a, b) => b.section_number - a.section_number
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
  background-color: #ebebeb;
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
  text-align: center;
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
  margin-right: 20px;
}
.site-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  height: 300px;
}
.site-info {
  flex: 1;
}
.section-sort {
  margin-bottom: 10px;
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
  font-size: 16px; /* Adjust as needed */
  text-decoration: none;
}

.back-button:disabled {
  cursor: not-allowed;
  opacity: 0.6; /* Make it slightly transparent when disabled */
}

.unit-image-preview {
  max-height: 150px;
  object-fit: cover;
  border: 1px solid #ccc;
}
</style>
