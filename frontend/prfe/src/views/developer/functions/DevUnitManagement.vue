<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <button class="back-button" @click="$router.back()">Back</button>
        <div v-if="site" class="site-details">
          <!-- Site Information -->
          <div class="site-header">
            <div v-if="site.picture">
              <img :src="site.picture" alt="Site Image" class="site-image" />
            </div>
            <h2>{{ site.name }}</h2>
            <p>{{ site.description }}</p>
            <p><strong>Location:</strong> {{ site.location }}</p>
          </div>

          <!-- Add Units Button -->
          <button class="add-units-button" @click="toggleAddUnitsModal">
            Add Units
          </button>

          <!-- Floors List -->
          <h3>Floors ({{ site.floors.length }})</h3>

          <div v-if="site.floors.length > 0" class="floor-list">
            <div
              v-for="floor in site.floors"
              :key="floor.id"
              class="floor-card"
            >
              <h4>Floor {{ floor.floor_number }}</h4>
              <!-- Total Units and Available Units -->
              <div class="site-summary">
                <p><strong>Total Units:</strong> {{ floor.total_units }}</p>
                <p>
                  <strong>Total Available Units:</strong>
                  {{ floor.available_units }}
                </p>
              </div>
              <button @click="openUnitManagement(floor)">Manage Units</button>
            </div>
          </div>
        </div>
        <div v-else>
          <p>Loading site details...</p>
        </div>

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

        <!-- Unit Management Modal -->
        <b-modal
          v-model="showUnitManagementModal"
          title="Manage Units"
          @hide="closeUnitManagementModal"
        >
          <div v-if="unitsData.length > 0">
            <div v-for="unit in unitsData" :key="unit.id" class="unit-card">
              <h5>{{ unit.unit_title }}</h5>
              <p><strong>Type:</strong> {{ unit.unit_type.name }}</p>
              <p><strong>Status:</strong> {{ unit.status }}</p>
              <button @click="handleEditUnit(unit)">Edit</button>
              <button @click="handleDeleteUnit(unit)">Delete</button>
            </div>
          </div>
          <div v-else>
            <p>No units available for this floor.</p>
          </div>
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";
import { BModal, BFormGroup, BFormSelect, BFormInput } from "bootstrap-vue-3";
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
      statusOptions: [
        { value: "available", text: "Available" },
        { value: "sold", text: "Sold" },
        { value: "pending reservation", text: "Pending Reservation" },
        { value: "reserved", text: "Reserved" },
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
      showUnitManagementModal: false,
      unitsData: [], // Store all the unit data for the selected floor
      selectedFloor: {
        floor_number: null,
        id: null,
        units: [],
      },
      currentPage: 1, // Current page for pagination
      unitsPerPage: 25, // Units per page for pagination
      searchQuery: "", // Search query for filtering
      unitFields: [],
    };
  },
  computed: {
    ...mapState({
      loggedIn: (state) => state.loggedIn,
      userId: (state) => state.userId,
      companyId: (state) => state.companyId,
    }),
    floorOptions() {
      return this.site
        ? this.site.floors.map((floor) => ({
            value: floor.id, // floor ID is the value sent to the backend
            text: `Floor ${floor.floor_number}`, // floor number is displayed as text in the dropdown
          }))
        : []; // Return an empty array if no site is available
    },
    unitTypeOptions() {
      return this.unitTypes.map((type) => ({
        value: type.id,
        text: type.name,
      }));
    },
    filteredUnits() {
      // Log the selectedFloor's units array before filtering
      console.log("Selected Floor Units:", this.selectedFloor.units);

      // Filter units based on the search query
      const filtered = this.selectedFloor.units.filter((unit) =>
        unit.unit_title.toLowerCase().includes(this.searchQuery.toLowerCase())
      );

      console.log("Filtered Units:", filtered); // Log filtered units
      console.log("Search Query:", this.searchQuery); // Log search query
      console.log("Current Page:", this.currentPage); // Log current page

      // Return the filtered units based on pagination
      return filtered.slice(
        (this.currentPage - 1) * this.unitsPerPage,
        this.currentPage * this.unitsPerPage
      );
    },
    totalPages() {
      return Math.ceil(this.unitsData.length / this.unitsPerPage);
    },
  },
  mounted() {
    if (!this.loggedIn || !this.companyId) {
      this.redirectToLogin();
    } else {
      this.fetchSiteDetails();
      this.fetchUnitTypes();
    }
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
        this.isLoading = true; // Set loading state
        const response = await axios.get(
          `http://localhost:8000/developer/units/${this.$route.params.siteId}/floors/${floor.id}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        if (response.data.success) {
          this.selectedFloor = floor;
          this.unitsData = response.data.data || []; // Ensure fallback to an empty array
          this.currentPage = 1; // Reset pagination
          this.showUnitManagementModal = true;
          console.log(response.data.data); // Log the data
        } else {
          console.error("Error fetching units:", response.data.error);
          this.errorMessage = "Failed to load unit management data."; // Set an error message
        }
      } catch (error) {
        console.error("Error fetching units:", error);
        this.errorMessage = "Failed to load unit management data."; // Set an error message
      } finally {
        this.isLoading = false; // Reset loading state
      }
    },
    closeUnitManagementModal() {
      this.showUnitManagementModal = false;
      this.unitsData = [];
      this.searchQuery = "";
      this.currentPage = 1;
    },
    handleEditUnit(unit) {
      alert(`Edit unit: ${unit.unit_title}`);
      // Logic for editing a unit goes here
    },
    handleDeleteUnit(unit) {
      if (
        confirm(`Are you sure you want to delete unit: ${unit.unit_title}?`)
      ) {
        // Logic for deleting a unit goes here
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    previousPage() {
      if (this.currentPage > 1) this.currentPage--;
    },

    onSearch() {
      this.currentPage = 1; // Reset pagination on new search
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
</style>
