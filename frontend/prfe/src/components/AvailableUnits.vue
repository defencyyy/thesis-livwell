<template>
  <div class="available-units-page">
    <SideNav />
    <div class="content">
      <h2>Available Units for Site: {{ siteName }}</h2>
      <div v-if="units.length">
        <div class="units-container">
          <div 
            v-for="unit in units" 
            :key="unit.id" 
            class="unit-card" 
            @click="showUnitDetails(unit)"
          >
            <p>{{ unit.unit_title }}</p> <!-- Display the unit title -->
          </div>
        </div>
      </div>
      <div v-else>
        <p>No units available for this site.</p>
      </div>

      <!-- Modal -->
      <div v-if="isModalVisible" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <img :src="selectedUnit.picture" alt="Unit Picture" class="unit-picture" />
          <p>P{{ selectedUnit.price }} Bedroom: {{ selectedUnit.bedroom }} Bathroom: {{ selectedUnit.bathroom }} Floor Area: {{ selectedUnit.floor_area }}</p>
          <hr>
          <center>Details</center>
          <p>Unit/Floor Number: {{ selectedUnit.floor }} Balcony: {{ selectedUnit.balcony }} Built(Year): </p>
          <p>Baths:{{ selectedUnit.bathroom }} Bedrooms: {{ selectedUnit.bedroom }}  Floor area(m<sup>2</sup>):{{ selectedUnit.floor_area }} </p>
          <p>View: {{ selectedUnit.view }} </p>
          <hr>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import axios from 'axios';

export default {
  name: "AvailableUnits",
  components: {
    SideNav,
  },
  data() {
    return {
      siteId: this.$route.params.siteId, // Get site ID from route params
      units: [],
      siteName: '', // To store the site's name
      isModalVisible: false, // To control modal visibility
      selectedUnit: null, // To store the selected unit details
    };
  },
  mounted() {
    this.fetchAvailableUnits();
    this.fetchSiteName(); // Fetch the site's name
  },
  methods: {
    async fetchAvailableUnits() {
      try {
        const response = await axios.get(`http://localhost:8000/units/available/?site_id=${this.siteId}`);
        this.units = response.data.units; // Assume your API returns a 'units' field
      } catch (error) {
        console.error("Error fetching available units:", error);
      }
    },
    async fetchSiteName() {
      try {
        const response = await axios.get(`http://localhost:8000/sites/${this.siteId}`);
        this.siteName = response.data.name; // Assume your API returns a 'name' field
      } catch (error) {
        console.error("Error fetching site name:", error);
      }
    },
    showUnitDetails(unit) {
      this.selectedUnit = unit;
      this.isModalVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
    },
  },
};
</script>

<style scoped>
.available-units-page {
  display: flex;
  height: 100vh;
}
.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}
.units-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin: 0 auto;
}
.unit-card {
  border: 1px solid #ccc;
  margin: 10px;
  padding: 10px;
  text-align: center;
  cursor: pointer;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  max-height: 80vh; /* Set max height for the modal */
  overflow-y: auto; /* Allow vertical scrolling if content overflows */
}
.unit-picture {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
}
</style>
