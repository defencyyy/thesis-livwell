<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <button class="back-button" @click="$router.back()">Back</button>
        <div v-if="site" class="site-details">
          <div class="site-overview">
            <!-- Site Image (50%) -->
            <div class="site-picture">
              <img :src="site.picture" alt="Site Image" class="site-image" />
            </div>
            <!-- Site Info (50%) -->
            <div class="site-info">
              <h2>{{ site.name }}</h2>
              <p>{{ site.description }}</p>
              <p><strong>Location:</strong> {{ site.location }}</p>
              <button class="add-units-button" @click="toggleAddUnitsModal">
                Add Units
              </button>
            </div>
          </div>

          <!-- Floors List -->
          <h3>Floors ({{ site.floors.length }})</h3>
          <div class="floor-sort">
            <label for="sortFloors">Sort Floors:</label>
            <select
              id="sortFloors"
              v-model="floorSortOrder"
              @change="sortFloors"
            >
              <option value="asc">Ascending</option>
              <option value="desc">Descending</option>
            </select>
          </div>

          <div v-if="sortedFloors.length > 0" class="floor-list">
            <div
              v-for="floor in sortedFloors"
              :key="floor.id"
              class="floor-card"
            >
              <h4>Floor {{ floor.floor_number }}</h4>
              <div class="site-summary">
                <p><strong>Total Units:</strong> {{ floor.total_units }}</p>
                <p>
                  <strong>Available Units:</strong> {{ floor.available_units }}
                </p>
              </div>
              <button @click="openUnitManagement(floor)">Manage Units</button>
            </div>
          </div>
        </div>
        <div v-else>
          <p>Loading site details...</p>
        </div>

        <!-- Unit Management Modal -->
        <b-modal
          v-model="showUnitManagementModal"
          title="Manage Units"
          @hide="closeUnitManagementModal"
        >
          <button @click="openAddUnitModalForFloor(selectedFloor.id)">
            Add Units to Floor
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
                  <th>Lot Area</th>
                  <th>Floor Area</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="unit in filteredUnits" :key="unit.id">
                  <td>{{ unit.unit_number }}</td>
                  <td>
                    {{
                      unitTypes.find((type) => type.id === unit.unit_type_id)
                        ?.name || "Unknown"
                    }}
                  </td>

                  <td>{{ unit.status }}</td>
                  <td>{{ formatCurrency(unit.price) }}</td>
                  <td>{{ unit.lot_area }}</td>
                  <td>{{ unit.floor_area }}</td>
                  <td>
                    <button @click="manageUnit(unit)">Edit</button>
                  </td>
                </tr>
              </tbody>
            </table>

            <div v-else>
              <p>No units available for this floor.</p>
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
          ok-title="Save"
          @ok="addUnits"
        >
          <form @submit.prevent="addUnits">
            <!-- Floor Selection (Multiple Selection) -->
            <b-form-group
              label="Floors:"
              description="Select floors to add units to"
            >
              <b-form-select
                v-model="newUnitFloors"
                :options="floorOptions"
                required
                multiple
              ></b-form-select>
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

        <b-modal
          v-model="showEditUnitModal"
          title="Edit Unit"
          @hide="clearSelectedUnit"
        >
          <template v-if="selectedUnit">
            <form>
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
                  v-model="newUnitBalcony"
                  :options="balconyOptions"
                ></b-form-select>
              </b-form-group>

              <b-form-group label="View:">
                <b-form-select
                  v-model="selectedUnit.view"
                  :options="viewOptions"
                />
              </b-form-group>

              <b-button
                type="submit"
                variant="primary"
                @click="saveUnitChanges"
              >
                Save Changes
              </b-button>
            </form>
          </template>

          <template v-else>
            <p>Loading unit details...</p>
          </template>
        </b-modal>

        <!-- Add Units to Floor Modal -->
        <b-modal
          id="add-floor-units-modal"
          title="Add Units to Floor"
          v-model="showAddFloorUnitsModal"
          ok-title="Save"
          @ok="addFloorUnits(newUnitFloors[0])"
        >
          <form @submit.prevent="addFloorUnits(newUnitFloors[0])">
            <!-- Only one floor (already set) -->
            <b-form-group
              label="Floor:"
              description="This floor will have new units added."
            >
              <b-form-select
                v-model="newUnitFloors"
                :options="floorOptions"
                required
                disabled
              ></b-form-select>
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
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";
import {
  BModal,
  BFormGroup,
  BFormSelect,
  BFormInput,
  BButton,
} from "bootstrap-vue-3";
import { mapState } from "vuex";

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
  },
  data() {
    return {
      showAddUnitsModal: false,
      unitTypes: [],
      site: null,
      floors: [],
      newUnitFloor: null,
      newUnitFloors: [],
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
      selectedSort: null,
      // Updated options with "All"
      statusOptions: [
        { value: null, text: "All" },
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
        { value: null, text: "All" },
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
      selectedStatus: null,
      selectedPriceRange: null,
      selectedUnitType: null,
      totalUnits: 0,
      totalAvailableUnits: 0,
      showUnitManagementModal: false,
      unitFields: [],
      selectedFloor: {},
      unitsData: [],
      currentPage: 1,
      unitsPerPage: 25,
      searchQuery: "",
      floorSortOrder: "asc",
      showEditUnitModal: false,
      selectedUnit: {},
      totalItems: 100, // Example: Set this value based on your API response or logic
      itemsPerPage: 10,
      showAddFloorUnitsModal: false, // Track the modal visibility
      // showSuccessToast: false, // Controls success toast visibility
      // showConfirmToast: false, // Controls confirmation toast visibility
    };
  },
  computed: {
    ...mapState({
      loggedIn: (state) => state.loggedIn,
      userId: (state) => state.userId,
      companyId: (state) => state.companyId,
    }),
    floorOptions() {
      // Ensure the site and floors are available
      if (this.site && this.site.floors) {
        // Clone the floors array to avoid mutating the original array
        const floorsCopy = [...this.site.floors];

        // Sort the cloned floors array based on the selected order (asc or desc)
        const sortedFloors = floorsCopy.sort((a, b) => {
          // Ascending order (if `floorSortOrder` is 'asc')
          if (this.floorSortOrder === "asc") {
            return a.floor_number - b.floor_number;
          }
          // Descending order (if `floorSortOrder` is 'desc')
          return b.floor_number - a.floor_number;
        });

        // Map the sorted floors to the options for the dropdown
        return sortedFloors.map((floor) => ({
          value: floor.id, // floor ID is the value sent to the backend
          text: `Floor ${floor.floor_number}`, // floor number is displayed as text
        }));
      } else {
        return []; // Return an empty array if no site or floors are available
      }
    },
    unitTypeOptions() {
      return [
        { value: null, text: "All" },
        ...this.unitTypes.map((type) => ({
          value: type.id, // Ensure type.id matches the type of unit_type_id
          text: type.name,
        })),
      ];
    },

    filteredUnits() {
      let units = this.unitsData;

      // Filter by search query
      if (this.searchQuery) {
        units = units.filter((unit) =>
          unit.unit_title.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }

      // Filter by status
      if (this.selectedStatus) {
        units = units.filter((unit) => unit.status === this.selectedStatus);
      }

      // Filter by unit type
      if (this.selectedUnitType !== null) {
        units = units.filter(
          (unit) => unit.unit_type_id === Number(this.selectedUnitType)
        );
      }

      // Filter by price range
      if (this.selectedPriceRange) {
        let priceRange = this.selectedPriceRange;
        units = units.filter((unit) => {
          const price = unit.price;
          if (priceRange === "1-5") return price >= 1000000 && price <= 5000000;
          if (priceRange === "5-10")
            return price >= 5000001 && price <= 10000000;
          if (priceRange === "10+") return price > 10000000;
          return true;
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
          }
        });
      }
      return units;
    },
    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage); // Adjust according to your data
    },
    sortedFloors() {
      if (!this.site?.floors) return [];
      return [...this.site.floors].sort((a, b) =>
        this.floorSortOrder === "asc"
          ? a.floor_number - b.floor_number
          : b.floor_number - a.floor_number
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

        if (this.site && this.site.floors) {
          this.fetchFloorsData();
        } else {
          console.error("No floors data available");
        }
      } catch (error) {
        console.error("Error fetching site details:", error);
      }
    },
    async fetchFloorsData() {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/sites/${this.$route.params.siteId}/floors/`, // Correct endpoint for floor data
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        if (response.data.success) {
          this.floors = response.data.data; // This will be an array of floors with total and available unit counts
        } else {
          console.error("Error fetching floor data:", response.data.error);
        }
      } catch (error) {
        console.error("Error fetching floors:", error);
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
        this.newUnitFloor = null;
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
    openAddUnitModalForFloor(floorId) {
      this.newUnitFloors = [floorId]; // Set the floor ID in the array
      this.showAddFloorUnitsModal = true; // Open the modal to add units to the specific floor
    },
    async addFloorUnits(floorId) {
      if (
        !this.newUnitType ||
        !this.newUnitPrice ||
        !this.newUnitLotArea ||
        !this.newUnitFloorArea ||
        !this.newUnitQuantity
      ) {
        alert("Please fill in all the required fields.");
        return;
      }

      try {
        const response = await axios.post(
          "http://localhost:8000/developer/units/bulk-add/",
          {
            floor_ids: [floorId], // Send the selected floor ID
            quantity: this.newUnitQuantity,
            unit_type_id: this.newUnitType,
            unit_title: this.newUnitTitle,
            bedroom: this.newUnitBedroom,
            bathroom: this.newUnitBathroom,
            lot_area: this.newUnitLotArea,
            floor_area: this.newUnitFloorArea,
            price: this.newUnitPrice,
            status: this.newUnitStatus,
            view: this.newUnitView,
            balcony: this.newUnitBalcony,
            commission: this.newUnitCommission,
            spot_discount_percentage: this.newUnitSpotDiscountPercentage,
            spot_discount_flat: this.newUnitSpotDiscountFlat,
            reservation_fee: this.newUnitReservationFee,
            other_charges: this.newUnitOtherCharges,
            vat_percentage: this.newUnitVatPercentage,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        if (response.status === 201) {
          // Refresh the unit management modal for the floor
          this.openUnitManagement({ id: floorId });
          this.fetchSiteDetails(); // Refresh the site details
          this.showAddUnitsModal = false; // Close the modal
        }
      } catch (error) {
        console.error("Error adding unit:", error);
        alert("Failed to add the unit. Please try again.");
      }
    },
    async addUnits() {
      if (
        !this.newUnitFloors.length ||
        !this.newUnitType ||
        !this.newUnitPrice ||
        !this.newUnitLotArea ||
        !this.newUnitFloorArea ||
        !this.newUnitQuantity
      ) {
        alert("Please fill in all the required fields.");
        return;
      }

      try {
        const response = await axios.post(
          "http://localhost:8000/developer/units/bulk-add/",
          {
            floor_ids: this.newUnitFloors, // Send the correct floor IDs
            quantity: this.newUnitQuantity,
            unit_type_id: this.newUnitType,
            unit_title: this.newUnitTitle,
            bedroom: this.newUnitBedroom,
            bathroom: this.newUnitBathroom,
            lot_area: this.newUnitLotArea,
            floor_area: this.newUnitFloorArea,
            price: this.newUnitPrice,
            status: this.newUnitStatus,
            view: this.newUnitView,
            balcony: this.newUnitBalcony,
            commission: this.newUnitCommission,
            spot_discount_percentage: this.newUnitSpotDiscountPercentage,
            spot_discount_flat: this.newUnitSpotDiscountFlat,
            reservation_fee: this.newUnitReservationFee,
            other_charges: this.newUnitOtherCharges,
            vat_percentage: this.newUnitVatPercentage,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        if (response.status === 201) {
          this.fetchSiteDetails(); // Refresh the site details
          this.showAddUnitsModal = false; // Close the modal
        }
      } catch (error) {
        console.error("Error adding unit:", error);
        alert("Failed to add the unit. Please try again.");
      }
    },
    async openUnitManagement(floor) {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/units/${this.$route.params.siteId}/floors/${floor.id}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.selectedFloor = floor;
        this.unitsData = response.data.data;
        this.showUnitManagementModal = true;
      } catch (error) {
        console.error("Error fetching units:", error);
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
      const formData = new FormData();
      formData.append("unit_number", this.selectedUnit.unit_number);
      formData.append("unit_title", this.selectedUnit.unit_title);
      formData.append("bedroom", this.selectedUnit.bedroom);
      formData.append("bathroom", this.selectedUnit.bathroom);
      formData.append("floor_area", this.selectedUnit.floor_area);
      formData.append("lot_area", this.selectedUnit.lot_area);
      formData.append("status", this.selectedUnit.status);
      formData.append("price", this.selectedUnit.price);
      formData.append("view", this.selectedUnit.view);
      formData.append("balcony", this.selectedUnit.balcony);
      formData.append("commission", this.selectedUnit.commission);
      formData.append(
        "spot_discount_percentage",
        this.selectedUnit.spot_discount_percentage || ""
      );
      formData.append(
        "spot_discount_flat",
        this.selectedUnit.spot_discount_flat || ""
      );
      formData.append(
        "reservation_fee",
        this.selectedUnit.reservation_fee || ""
      );
      formData.append("other_charges", this.selectedUnit.other_charges || "");
      formData.append("vat_percentage", this.selectedUnit.vat_percentage);

      try {
        let response;

        if (this.selectedUnit.id) {
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
        } else {
          // If no id, it's a new unit (POST request)
          response = await axios.post(
            `http://localhost:8000/developer/units/`,
            formData,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                "Content-Type": "multipart/form-data",
              },
            }
          );
        }

        if (response.status === 200 || response.status === 201) {
          // Update local state or fetch updated units list
          if (this.selectedUnit.id) {
            const index = this.units.findIndex(
              (unit) => unit.id === this.selectedUnit.id
            );
            if (index !== -1) {
              this.units[index] = response.data;
            }
          } else {
            this.units.push(response.data); // If it's a new unit, just push to list
          }

          this.showEditUnitModal = false; // Close the modal
          this.fetchUnits(); // Optional: Fetch the updated list of units from the backend
        }
      } catch (error) {
        console.error("Error saving unit changes:", error.response || error);
      }
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
    getUnitTypeName(unitTypeId) {
      const unitType = this.unitTypeOptions.find(
        (type) => type.id === unitTypeId
      );
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

    sortFloors() {
      if (this.floorSortOrder === "asc") {
        this.sortedFloors = this.site.floors.sort(
          (a, b) => a.floor_number - b.floor_number
        );
      } else if (this.floorSortOrder === "desc") {
        this.sortedFloors = this.site.floors.sort(
          (a, b) => b.floor_number - a.floor_number
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

/* Back Button */
.back-button {
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  margin-bottom: 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.back-button:hover {
  background-color: #45a049;
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
}
.site-info {
  flex: 1;
}
.floor-sort {
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

.floor-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.floor-card {
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

button:hover {
  background-color: #0056b3;
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
button:hover {
  background-color: #0056b3;
}
</style>
