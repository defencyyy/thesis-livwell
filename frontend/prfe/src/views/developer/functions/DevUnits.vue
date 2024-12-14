<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="dashboard-container">
          <!-- Loading and Error Message -->
          <div v-if="isLoading" class="loading-indicator">Loading...</div>
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <!-- Sites Section -->
          <div class="title-wrapper">
            <div class="title-left">
              <div class="title-icon"></div>
              <div class="edit-title">Sites</div>
            </div>
          </div>

          <!-- Search and Filter Section -->
          <div
            class="card border-0 rounded-1 mx-auto"
            style="
              max-width: 1100px;
              box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <div class="card-body">
              <div class="row">
                <div class="toolbar">
                  <div class="left-section">
                    <div class="search-bar-container">
                      <input
                        type="text"
                        v-model="searchQuery"
                        placeholder="Search Site Name"
                        class="search-bar"
                      />
                      <i class="fa fa-search search-icon"></i>
                    </div>
                    <!-- Sort Dropdown -->
                    <select v-model="sortBy" class="dropdown">
                      <option value="name">Name</option>
                      <option value="created_at">Date Created</option>
                      <option value="status">Status</option>
                      <option value="sections">Sections</option>
                    </select>
                    <select v-model="sortOrder" class="dropdown">
                      <option value="asc">Ascending</option>
                      <option value="desc">Descending</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Sites Table -->
          <div v-if="viewMode === 'table'">
            <div class="outside-headers">
              <span class="header-item">Name</span>
              <span class="header-item">Location</span>
              <span class="header-item">Status</span>
              <span class="header-item">Sections</span>
              <span class="header-item">Units</span>
              <span class="header-item">Available Units</span>
              <span class="header-item">Actions</span>
            </div>
            <div v-for="site in filteredSites" :key="site.id" class="card">
              <div class="card-body">
                <table class="site-table">
                  <tbody>
                    <tr>
                      <td>{{ site.name || "Unknown" }}</td>
                      <td>{{ site.location || "Location unavailable" }}</td>
                      <td>
                        {{ site.status.toUpperCase() || "Status unavailable" }}
                      </td>
                      <td>{{ site.sections?.length || "None" }}</td>
                      <td>{{ site.total_units || "None" }}</td>
                      <td>{{ site.available_units || "None" }}</td>
                      <td>
                        <button
                          @click.stop="openSectionManagement(site)"
                          class="btn-manage"
                        >
                          Manage Sections
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
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
  components: {
    SideNav,
    AppHeader,
  },
  data() {
    return {
      units: [],
      sites: [],
      isLoading: false,
      errorMessage: null,
      viewMode: "table",
      searchQuery: "", // Search query for site name
      sortBy: "name", // Default sorting option
      sortOrder: "asc", // Default sorting order (Ascending)
    };
  },
  computed: {
    filteredSites() {
      return this.sites
        .filter((site) =>
          site.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        )
        .sort((a, b) => this.compareSites(a, b));
    },
    siteOptions() {
      return this.sites
        .map((site) => ({ value: site.id, text: site.name }))
        .sort((a, b) => a.text.localeCompare(b.text)); // Sort options alphabetically
    },
  },
  methods: {
    compareSites(a, b) {
      let comparison = 0;
      if (this.sortBy === "name") comparison = a.name.localeCompare(b.name);
      if (this.sortBy === "created_at")
        comparison = new Date(a.created_at) - new Date(b.created_at);
      if (this.sortBy === "status")
        comparison = a.status.localeCompare(b.status);
      if (this.sortBy === "sections")
        comparison = a.sections.length - b.sections.length;
      return this.sortOrder === "asc" ? comparison : -comparison;
    },
    getPictureUrl(picture) {
      return `http://localhost:8000${picture}`;
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
            sections: site.sections || [],
            units: site.units || [],
            total_units: site.sections.reduce(
              (sum, section) => sum + section.total_units,
              0
            ),
            available_units: site.sections.reduce(
              (sum, section) => sum + section.available_units,
              0
            ),
          }));
        }
      } catch (error) {
        this.errorMessage = "Failed to load sites.";
        console.error("Error fetching sites:", error.response || error);
      } finally {
        this.isLoading = false;
      }
    },
    constructLocation(site) {
      const addressParts = [site.province, site.municipality, site.barangay];
      return addressParts.filter(Boolean).join(", ");
    },
    openSectionManagement(site) {
      this.$router.push({
        name: "DevUnitManagement",
        params: { siteId: site.id },
      });
    },
    updateSectionAndUnitCounts() {
      this.totalSections = this.sites.reduce(
        (sum, site) => sum + (site.sections?.length || 0),
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
        const response = await axios.get(
          "http://localhost:8000/developer/units/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            params: {
              siteId: this.selectedSite,
              unitNumber: this.unitNumberFilter,
              unitType: this.unitTypeFilter,
            },
          }
        );
        this.units = response.data.data || [];
      } catch (error) {
        this.errorMessage = "Failed to load units.";
        console.error("Error fetching units data:", error);
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
  background: none; /* Removes background if you want tabs without a button-like appearance */
  border: none; /* Removes the default button border */
  color: inherit; /* Inherits the text color */
  font-weight: bold; /* Makes text bold */
  font-size: 14px;
}

.nav-tabs .nav-link.active {
  color: #000; /* Active tab color */
  border-bottom: 2px solid #0d6efd;
  font-size: 14px;
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

.dropdown {
  appearance: none;
  padding: 8px 12px;
  height: 38px;
  /* Explicitly set height */
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  width: 100%;
  max-width: 150px;
  background-color: white;
  color: #333;
  padding-right: 30px;
  background-image: url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"%3E%3Cpath d="M7 10l5 5 5-5z"/%3E%3C/svg%3E');
  background-position: right 10px center;
  background-repeat: no-repeat;
  background-size: 14px;
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
  text-align: left;
  background: #fff;
  font-size: 14px;
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
  width: 25%;
  padding-right: 10px;
}

.site-table th:nth-child(3),
.site-table td:nth-child(3) {
  width: 12%;
}

.site-table th:nth-child(4),
.site-table td:nth-child(4) {
  width: 12%;
}

.site-table th:nth-child(5),
.site-table td:nth-child(5) {
  width: 12%;
}

.site-table th:nth-child(6),
.site-table td:nth-child(6) {
  width: 12%;
}
.site-table th:nth-child(7),
.site-table td:nth-child(7) {
  width: 7%;
}

.outside-headers {
  display: grid;
  grid-template-columns: 20% 25% 12% 12% 12% 12% 7%;
  padding: 0px 15px;
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

.btn-manage {
  background-color: #8b8b8b;
  /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px;
  /* Adjust the border radius */
  padding: 8px;
  font-size: 12px;
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

.button-bottom-right {
  padding: 10px 15px; /* Optional: Adjust padding for button size */
  background-color: #007bff; /* Optional: Change button color */
  color: white; /* Button text color */
  border: none; /* Remove border */
  border-radius: 4px; /* Rounded corners */
  cursor: pointer; /* Add pointer cursor */
}

.button-bottom-right:hover {
  background-color: #0056b3; /* Optional: Change color on hover */
}
</style>
