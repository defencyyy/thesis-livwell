<template>
  <div class="available-units-page">
    <SideNav />
    <div class="content">
      <h2>Available Units for Site: {{ siteName }}</h2>
      <div v-if="units.length">
        <div class="units-container">
          <div v-for="unit in units" :key="unit.id" class="unit-card">
            <p>{{ unit.title }}</p> <!-- Display the unit title -->
          </div>
        </div>
      </div>
      <div v-else>
        <p>No units available for this site.</p>
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
    };
  },
  mounted() {
    this.fetchAvailableUnits();
    this.fetchSiteName(); // Fetch the site's name
  },
  methods: {
    async fetchAvailableUnits() {
      try {
        const response = await axios.get(`http://localhost:8000/units/available/?site_id=${this.siteId}`); // Fetch units based on site ID
        this.units = response.data.units; // Assume your API returns a 'units' field
      } catch (error) {
        console.error("Error fetching available units:", error);
      }
    },
    async fetchSiteName() {
      try {
        const response = await axios.get(`http://localhost:8000/sites/${this.siteId}`); // Adjust the URL based on your API
        this.siteName = response.data.name; // Assume your API returns a 'name' field
      } catch (error) {
        console.error("Error fetching site name:", error);
      }
    },
  },
};
</script>

<style scoped>
.available-units-page{
  display: flex;
  height: 100vh;
}
.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}
.units-container {
  display: grid; /* Use grid layout */
  grid-template-columns: repeat(3, 1fr); /* Three cards per row */
  gap: 20px; /* Space between cards */
  margin: 0 auto; /* Center the container */
}

.unit-card {
  border: 1px solid #ccc;
  margin: 10px;
  padding: 10px;
  text-align: center;
  width: 150px; /* Set a consistent width */
}
</style>
