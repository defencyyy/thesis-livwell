<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="dashboard-container">
          <!-- Loading Indicator -->
          <div v-if="isLoading" class="loading-indicator">Loading...</div>
          <!-- Error Message -->
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <!-- Actions -->
          <div class="actions" v-if="!isLoading && !errorMessage">
            <button @click="redirectToUnits">Manage Units</button>
            <button @click="redirectToUnitTemplates">
              Manage Unit Templates
            </button>
            <button @click="redirectToUnitTypes">Manage Unit Types</button>
          </div>

          <!-- Grid View Section for Sites -->
          <div>
            <h2>Sites</h2>
            <!-- Filters and View Switch -->
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

            <div v-if="viewMode === 'grid'" class="site-grid">
              <div
                v-for="(site, index) in filteredSites"
                :key="site.id || index"
                class="site-card"
                @click="openSiteModal(site)"
              >
                <img
                  :src="site.picture || require('@/assets/home.png')"
                  alt="Site Image"
                  class="site-image"
                />
                <h2 class="site-name">{{ site.name || "Unknown" }}</h2>
                <p class="site-location">
                  {{ site.location || "Location unavailable" }}
                </p>

                <div class="site-stats">
                  <p>Total Floors: {{ site.floors.length }}</p>
                  <p>Total Units: {{ site.total_units }}</p>
                  <p>Available Units: {{ site.available_units }}</p>
                </div>

                <button @click.stop="openFloorManagement(site)">
                  Manage Floors
                </button>
              </div>
            </div>

            <!-- Table View Section for Sites -->
            <div v-if="viewMode === 'table'">
              <div class="outside-headers">
                <span class="header-item">Name</span>
                <span class="header-item">Location</span>
                <span class="header-item">Status</span>
                <span class="header-item">Floors</span>
                <span class="header-item">Units</span>
                <span class="header-item">Available Units</span>
                <span class="header-item">Actions</span>
              </div>
              <div
                v-for="(site, index) in filteredSites"
                :key="site.id || index"
                class="card"
              >
                <div class="card-body">
                  <table>
                    <tbody>
                      <tr
                        v-for="(site, index) in filteredSites"
                        :key="site.id || index"
                      >
                        <td>{{ site.name || "Unknown" }}</td>
                        <td>{{ site.location || "Location unavailable" }}</td>
                        <td>{{ site.status || "Status unavailable" }}</td>
                        <td>
                          <p>{{ site.total_floors }}</p>
                        </td>
                        <td>
                          <p>{{ site.total_units }}</p>
                        </td>
                        <td>
                          <p>{{ site.available_units }}</p>
                        </td>
                        <td>
                          <button @click.stop="openEditSiteModal(site)">
                            Edit
                          </button>
                          <button @click.stop="openFloorManagement(site)">
                            Manage Floors
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          <!-- Units Section -->
          <div>
            <h2>Units</h2>
            <button @click="addUnit">Add Unit</button>
            <table>
              <thead>
                <tr>
                  <th>Unit Number</th>
                  <th>Title</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="unit in units" :key="unit.id">
                  <td>{{ unit.unit_number }}</td>
                  <td>{{ unit.unit_title }}</td>
                  <td>{{ unit.status }}</td>
                  <td>
                    <button @click="editUnit(unit)">Edit</button>
                    <button @click="deleteUnit(unit.id)">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
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
  name: "DevFuncUnits",
  components: { SideNav, AppHeader },
  data() {
    return {
      units: [],
      sites: [],
      availableUnits: 0, // Holds the count of available units
      totalFloors: 0, // Holds the total number of floors
      totalUnits: 0, // Holds the total number of units
      isLoading: false,
      errorMessage: null,
      viewMode: "grid",
      searchQuery: "",
      sortBy: "name",
      viewFilter: "active",
    };
  },
  computed: {
    filteredSites() {
      const sitesToFilter =
        this.viewFilter === "active"
          ? this.sites.filter((s) => !s.archived)
          : this.sites;
      return sitesToFilter
        .filter((site) =>
          site.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        )
        .sort((a, b) =>
          this.sortBy === "name"
            ? a.name.localeCompare(b.name)
            : a.status.localeCompare(b.status)
        );
    },
  },
  methods: {
    redirectToUnits() {
      this.$router.push({ name: "DevFuncUnits" });
    },

    redirectToUnitTemplates() {
      this.$router.push({ name: "DevUnitTemplates" });
    },

    redirectToUnitTypes() {
      this.$router.push({ name: "DevUnitTypes" });
    },
    async fetchSites() {
      try {
        this.isLoading = true;
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
            isArchived: site.isArchived ?? false,
            floors: site.floors || [], // Ensure floors is always an array
            units: site.units || [], // Ensure units is always an array
          }));
        }
      } catch (error) {
        console.error("Error fetching sites:", error.response || error);
        this.errorMessage = "Failed to load sites.";
      } finally {
        this.isLoading = false;
      }
    },
    async fetchUnits() {
      try {
        this.isLoading = true;
        const response = await axios.get(
          "http://localhost:8000/developer/units/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        const units = response.data.data || [];
        this.totalUnits = units.length; // Set the total number of units
        this.availableUnits = units.filter(
          (unit) => unit.status === "Available"
        ).length; // Count available units
        this.units = units; // Store all units in the units array
      } catch (error) {
        console.error("Error fetching units data:", error);
        this.errorMessage = "Failed to load units.";
      } finally {
        this.isLoading = false;
      }
    },

    openSiteModal(site) {
      console.log("Site clicked:", site);
    },

    openEditSiteModal(site) {
      console.log("Edit site:", site);
    },

    openFloorManagement(site) {
      // Navigate to the DevUnitManagement.vue page
      this.$router.push({
        name: "DevUnitManagement",
        params: { siteId: site.id },
      });
    },

    updateFloorAndUnitCounts() {
      // This method updates the total floors and available units for the sites
      this.totalFloors = this.sites.reduce(
        (sum, site) => sum + (site.floors?.length || 0),
        0
      );
    },

    addUnit() {
      console.log("Add unit logic.");
    },

    editUnit(unit) {
      console.log("Edit unit:", unit);
    },

    deleteUnit(unitId) {
      if (confirm("Are you sure you want to delete this unit?")) {
        this.units = this.units.filter((unit) => unit.id !== unitId);
      }
    },
  },
  mounted() {
    this.fetchUnits();
    this.fetchSites();
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
  background-color: #e8f0fa;
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
}

.dropdown2 {
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
  font-size: 15px;
  font-weight: bold;
}

.site-location {
  font-size: 14px;
  color: #777;
}

.site-table {
  width: 100%;
  border-collapse: collapse;
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
  width: 35%;
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
  width: 20%;
}

.outside-headers {
  display: grid;
  /* Change to grid layout */
  grid-template-columns: 25% 35% 20% 20%;
  /* Match the column widths */
  padding: 0px 18px;
  margin: 20px auto 10px;
  max-width: 1100px;
}

.header-item {
  flex: 1;
  text-align: left;
  font-size: 15px;
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

.btn-cancel {
  background-color: #343a40;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 10px;
}
</style>
