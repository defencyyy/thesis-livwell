<template>
  <div class="main-page">
    <!-- Side Navigation -->
    <SideNav />
    <div class="main-content">
      <!-- App Header -->
      <AppHeader />
      <div class="content">
        <!-- Back Button -->
        <button class="back-button" @click="$router.back()">Back</button>

        <!-- Site Details -->
        <div v-if="site" class="site-details">
          <h2>{{ site.name }}</h2>
          <p>{{ site.location }}</p>
          <p>Status: {{ site.status }}</p>

          <!-- Floors List -->
          <h3>Floors</h3>
          <div v-if="site.floors.length > 0" class="floor-list">
            <div
              v-for="(floor, index) in site.floors"
              :key="index"
              class="floor-card"
            >
              <h4>Floor {{ floor.floor_number }}</h4>
              <p>{{ floor.description || "No description available" }}</p>
              <p v-if="floor.units !== undefined">
                Units: {{ floor.units.length }}
              </p>
              <p v-else>Units: N/A</p>

              <button @click="openUnitManagement(floor)">Manage Units</button>
            </div>
          </div>
          <div v-else>
            <p>No floors available for this site.</p>
          </div>
        </div>
        <div v-else>
          <p>Loading site details...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";

export default {
  name: "DevUnitManagement",
  components: { SideNav, AppHeader },
  data() {
    return {
      site: null,
    };
  },
  props: ["siteId"],
  mounted() {
    console.log("Site ID from prop:", this.siteId);
    console.log("Site ID from route params:", this.$route.params.siteId);
    this.fetchSiteDetails();
  },
  methods: {
    async fetchSiteDetails() {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/sites/${this.$route.params.siteId}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          this.site = response.data.data;

          // Check and initialize floor.units if undefined
          this.site.floors = this.site.floors.map((floor) => ({
            ...floor,
            units: floor.units || [], // Default to an empty array if units are not provided
          }));
        }
      } catch (error) {
        console.error("Error fetching site details:", error);
      }
    },
    openUnitManagement(floor) {
      console.log(
        `Navigating to unit management for Floor ${floor.floor_number}`
      );
      // Navigate to a dedicated unit management page
      this.$router.push({
        name: "UnitManagementPage",
        params: { floorId: floor.floor_number },
      });
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

.floor-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.floor-card {
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 8px;
  width: 200px;
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
