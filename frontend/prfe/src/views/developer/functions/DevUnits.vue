<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="dashboard-container">
          <div v-if="isLoading" class="loading-indicator">Loading...</div>
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <div class="actions" v-if="!isLoading && !errorMessage">
            <div class="nav nav-tabs">
              <!-- Manage Units Tab -->
              <button class="nav-link active" id="units-tab" type="button" role="tab" aria-selected="true" @click="redirectToUnits">
                Manage Units
              </button>
              
              <!-- Manage Unit Templates Tab -->
              <button class="nav-link" id="unit-templates-tab" type="button" role="tab" aria-selected="false" @click="redirectToUnitTemplates">
                Manage Unit Templates
              </button>
              
              <!-- Manage Unit Types Tab -->
              <button class="nav-link" id="unit-types-tab" type="button" role="tab" aria-selected="false" @click="redirectToUnitTypes">
                Manage Unit Types
              </button>
            </div>

          </div>

          <div>
            <h2>Sites</h2>
            <div class="view-switch">
              <div
                class="view-icon"
                :class="{ active: viewMode === 'grid' }"
                @click="viewMode = 'grid'"
              >
                <i class="fa fa-th"></i>
              </div>
              <div class="separator"></div>
              <div
                class="view-icon"
                :class="{ active: viewMode === 'table' }"
                @click="viewMode = 'table'"
              >
                <i class="fa fa-list"></i>
              </div>
            </div>

            <div v-if="viewMode === 'grid'" class="site-grid">
              <div
                v-for="site in filteredSites"
                :key="site.id"
                class="site-card"
                @click="openFloorManagement(site)"
              >
                <img
                  :src="
                    getPictureUrl(site.picture) || require('@/assets/home.png')
                  "
                  alt="Site Image"
                  class="site-image"
                />
                <h2 class="site-name">{{ site.name || "Unknown" }}</h2>
                <p class="site-location">
                  {{ site.location || "Location unavailable" }}
                </p>
                <div class="site-stats">
                  <p>
                    Floors:
                    {{ site.floors.length > 0 ? site.floors.length : "None" }}
                  </p>
                  <p>
                    Units:
                    {{ site.total_units > 0 ? site.total_units : "None" }}
                  </p>
                  <p v-if="site.total_units > 0">
                    Available Units:
                    {{
                      site.available_units > 0
                        ? site.available_units
                        : "No Available Units"
                    }}
                  </p>
                </div>
                <button @click.stop="openFloorManagement(site)">
                  Manage Floors
                </button>
              </div>
            </div>

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
              <div v-for="site in filteredSites" :key="site.id" class="card">
                <div class="card-body">
                  <table>
                    <tbody>
                      <tr>
                        <td>{{ site.name || "Unknown" }}</td>
                        <td>{{ site.location || "Location unavailable" }}</td>
                        <td>{{ site.status || "Status unavailable" }}</td>
                        <td>
                          <p>
                            {{
                              site.floors?.length > 0
                                ? site.floors.length
                                : "None"
                            }}
                          </p>
                        </td>
                        <td>
                          <p>
                            {{
                              site.total_units > 0 ? site.total_units : "None"
                            }}
                          </p>
                        </td>
                        <td>
                          <p>
                            {{
                              site.available_units > 0
                                ? site.available_units
                                : "None"
                            }}
                          </p>
                        </td>
                        <td>
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

          <hr />
        </div>

        <div class="filters">
          <b-form-group label="Select Site:">
            <b-form-select
              v-model="selectedSite"
              :options="siteOptions"
              required
            />
          </b-form-group>
          <b-form-group label="Unit Number (optional):">
            <b-form-input
              v-model="unitNumberFilter"
              placeholder="Search by Unit Number"
            />
          </b-form-group>
          <b-form-group label="Unit Type (optional):">
            <b-form-input
              v-model="unitTypeFilter"
              placeholder="Search by Unit Type"
            />
          </b-form-group>
          <b-button @click="searchUnits" :disabled="!selectedSite"
            >Search</b-button
          >
        </div>

        <div v-if="units.length > 0">
          <h2>Units</h2>
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
</template>


<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";
import { BFormGroup, BFormSelect, BFormInput, BButton } from "bootstrap-vue-3";

export default {
  name: "DevFuncUnits",
  components: {
    SideNav,
    AppHeader,
    BFormGroup,
    BFormSelect,
    BFormInput,
    BButton,
  },
  data() {
    return {
      units: [],
      sites: [],
      isLoading: false,
      errorMessage: null,
      viewMode: "grid",
      searchQuery: "",
      sortBy: "name",
      viewFilter: "active",
      selectedSite: null,
      unitNumberFilter: "",
      unitTypeFilter: "",
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
    siteOptions() {
      return this.sites
        .map((site) => ({
          value: site.id,
          text: site.name,
        }))
        .sort((a, b) => a.text.localeCompare(b.text)); // Sort options alphabetically
    },
  },
  methods: {
    getPictureUrl(picture) {
      return `http://localhost:8000${picture}`;
    },
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
            location: this.constructLocation(site),
            floors: site.floors || [],
            units: site.units || [],
          }));
        }
      } catch (error) {
        console.error("Error fetching sites:", error.response || error);
        this.errorMessage = "Failed to load sites.";
      } finally {
        this.isLoading = false;
      }
    },
    constructLocation(site) {
      const addressParts = [site.province, site.municipality, site.barangay];
      return addressParts.filter(Boolean).join(", ");
    },
    openFloorManagement(site) {
      this.$router.push({
        name: "DevUnitManagement",
        params: { siteId: site.id },
      });
    },
    updateFloorAndUnitCounts() {
      this.totalFloors = this.sites.reduce(
        (sum, site) => sum + (site.floors?.length || 0),
        0
      );
    },
    async fetchUnits() {
      if (!this.selectedSite) {
        this.errorMessage = "Please select a site before searching.";
        return;
      }

      try {
        this.isLoading = true;
        const params = {
          siteId: this.selectedSite,
          unitNumber: this.unitNumberFilter,
          unitType: this.unitTypeFilter,
        };

        const response = await axios.get(
          "http://localhost:8000/developer/units/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            params,
          }
        );

        this.units = response.data.data || [];
      } catch (error) {
        console.error("Error fetching units data:", error);
        this.errorMessage = "Failed to load units.";
      } finally {
        this.isLoading = false;
      }
    },
    searchUnits() {
      if (!this.selectedSite) {
        this.errorMessage = "Please select a site before searching.";
        return;
      }

      this.fetchUnits();
    },
  },
  mounted() {
    this.fetchSites();
  },
};
</script>

<style scoped>
html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.main-page {
  display: flex;
  min-height: 100vh;
  background-color: #e8f0fa;
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

.nav-tabs .nav-link {
  background: none;  /* Removes background if you want tabs without a button-like appearance */
  border: none;  /* Removes the default button border */
  color: inherit;  /* Inherits the text color */
  font-weight: bold;  /* Makes text bold */
}

.nav-tabs .nav-link.active {
  color: #000;  /* Active tab color */
  border-bottom: 2px solid #0d6efd; 
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
  width: 100%;
  max-width: 1100px;
  margin: 20px auto;
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
  padding-right: 20px;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-bar-container {
  position: relative;
  width: 100%;
  max-width: 400px;
}

.search-bar {
  width: 400px;
  padding: 8px 12px 8px 40px;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 14px;
}

.search-icon {
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
  color: #777;
  font-size: 16px;
  pointer-events: none;
}

.dropdown-container {
  position: relative;
}

.dropdown {
  padding: 8px 12px;
  height: 38px;
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
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 14px;
  width: 90%;
  max-width: 150px;
  background-color: white;
  color: #333;
}

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
  margin-left: auto;
  margin-right: auto;
}

.site-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  max-width: 1100px;
  margin: 0 auto;
}

.site-card {
  background: #fff;
  padding: 16px;
  text-align: center;
  cursor: pointer;
}

.site-card:hover {
  transform: translateY(-2px);
}

.site-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 10px;
}

.table-image {
  width: 30px;
  height: 30px;
  object-fit: cover;
  margin-right: 10px;
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
}

.site-table th {
  background-color: #f9f9f9;
  font-weight: bold;
}

.site-table th:nth-child(2),
.site-table td:nth-child(2) {
  width: 35%;
  padding-right: 60px;
}

.site-table th:nth-child(3),
.site-table td:nth-child(3) {
  width: 20%;
}

.site-table th:nth-child(4),
.site-table td:nth-child(4) {
  width: 20%;
}

.outside-headers {
  display: grid;
  grid-template-columns: 25% 35% 20% 20%;
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
}

.btn-add {
  background-color: #0560fd;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 10px;
}

.btn-cancel {
  background-color: #343a40;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 10px;
}

.filters {
  margin-bottom: 20px;
}

.filters b-form-group {
  margin-bottom: 10px;
}

.filters b-button {
  margin-top: 10px;
}
</style>
