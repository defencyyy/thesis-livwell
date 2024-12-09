<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />  
      <div class="content">
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title"><strong>Available Sites</strong></div>
          </div>

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
        </div>

        <div
          class="card border-0 rounded-1 mx-auto"
          style="max-width: 1100px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)"
        >
          <div class="card-body">
            <div class="row">
              <!-- Toolbar -->
              <div class="toolbar">
                <div class="left-section">
                  <!-- Search Bar -->
                  <div class="search-bar-container">
                    <input
                      type="text"
                      v-model="searchQuery"
                      placeholder="Search Site"
                      class="search-bar"
                      @input="filterSites"
                    />
                    <i class="fa fa-search search-icon"></i>
                  </div>

                  <!-- Sort Dropdown -->
                  <select v-model="sortBy" @change="sortSites" class="dropdown">
                    <option value="site_asc">Site (A-Z)</option>
                    <option value="site_desc">Site (Z-A)</option>
                    <option value="status_pre">Status (Preselling)</option>
                    <option value="status_comp">Status (Complete)</option>
                    <option value="status_on">Status (On Going)</option>
                  </select>
        </div>
        </div>
        </div>
        </div>
        </div>
        
        <!-- Grid View -->
        <div v-if="viewMode === 'grid'">
          <div v-if="filteredSites.length" class="site-grid">
            <div
              v-for="site in paginatedSites"
              :key="site.id || index"
              class="site-card"
              @click="() => redirectToUnits(site.id)"
            >
              <!-- Site Image -->
              <img
                :src="site.picture || require('@/assets/home.png')"
                alt="Site Image"
                class="site-image"
              />

              <!-- Site Name -->
              <h2 class="site-name">
                {{ site.name || "Unknown" }}
              </h2>

              <!-- Site Location -->
              <p class="site-location">
                {{ site.location || "Location unavailable" }}
              </p>
            </div>
          </div>
          <div v-else>
            <p>No sites with available units.</p>
          </div>
        </div>


        <div v-if="viewMode === 'table'">
          <div class="outside-headers">
            <span class="header-item">Name</span>
            <span class="header-item">Location</span>
          </div>
          <div v-if = "filteredSites.length">
            <div
              v-for="site in paginatedSites"
              :key="site.id || index"
              class="card border-0 rounded-1 mx-auto card-hover"
              style="
              max-width: 1100px;
              box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
              cursor: 'pointer';
            "
              @click="() => redirectToUnits(site.id)"
            >
              <div class = "card-body">
                <table class = "site-table">
                  <tbody>
                    <tr>
                      <td>
                        <div class="site-info">
                          <img
                            :src="site.picture || require('@/assets/home.png')"
                            alt="Site Image"
                            class="table-image"
                          />
                          <span class="site-name">
                            {{ site.name || "Unknown" }}
                          </span>
                        </div>
                      </td>
                      <td>{{ site.location || "Location unavailable" }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <div v-else>
            <p>No sites with available units.</p>
          </div>
        </div>

    <!-- Pagination Controls -->
    <div class="pagination-controls">
      <button
        @click="goToPage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="page-button"
      >
        Previous
      </button>
      <span v-for="page in totalPages" :key="page">
        <button
          @click="goToPage(page)"
          :class="{ active: page === currentPage }"
          class="page-button"
        >
          {{ page }}
        </button>
      </span>
      <button
        @click="goToPage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="page-button"
      >
        Next
      </button>
    </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from "@/components/Header.vue";
import SideNav from "@/components/SideNav.vue"; // Importing the SideNav component
import axios from "axios"; // Ensure you have axios installed
import { useRouter } from "vue-router"; // Import useRouter
import { mapState } from "vuex";

export default {
  name: "AffiliatedUnits",
  components: {
    SideNav,
    AppHeader, // Registering the SideNav component
  },
  setup() {
    const router = useRouter();

    const redirectToUnits = (siteId) => {
      router.push({ name: "AvailableUnits", params: { siteId } });
    };

    return { redirectToUnits };
  },
  data() {
    return {
      viewMode: "table",
      sites: [],
      loading: true,
      sortBy: "site_asc",
      searchQuery: "", // New property for search input
      filteredSites: [],
      currentPage: 1, // Current page number
      itemsPerPage: 5, // Number of customers per page

    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId,
      userType: (state) => state.userType,
      companyId: (state) => state.companyId,
    }),
     // Filter and sort sites dynamically
    filteredAndSortedSites() {
      // Filter by search query
      const query = this.searchQuery.toLowerCase();
      const filtered = this.sites.filter((site) => {
        const siteName = site.name.toLowerCase();
        return !query || siteName.includes(query);
      });

      // Sort based on selected option
      return filtered.sort((a, b) => {
        switch (this.sortBy) {
          case "site_asc":
            return a.name.localeCompare(b.name);
          case "site_desc":
            return b.name.localeCompare(a.name);
          case "status_pre":
            return a.status === "preselling" ? -1 : b.status === "preselling" ? 1 : 0;
          case "status_comp":
            return a.status === "completed" ? -1 : b.status === "completed" ? 1 : 0;
          case "status_on":
            return a.status === "on going" ? -1 : b.status === "on going" ? 1 : 0;
          default:
            return 0;
        }
      });
    },

    // Paginate filtered and sorted sites
    paginatedSites() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.filteredAndSortedSites.slice(startIndex, endIndex);
    },

    // Total pages based on filtered and sorted sites
    totalPages() {
      return Math.ceil(this.filteredAndSortedSites.length / this.itemsPerPage);
    },
  },
  vuexUserId() {
    return this.userId;
  },
  vuexCompanyId() {
    return this.companyId;
  },
  mounted() {
    this.fetchAvailableSites();
  },
  methods: {
      goToPage(pageNumber) {
      if (pageNumber > 0 && pageNumber <= this.totalPages) {
        this.currentPage = pageNumber;
      }
    },

    toggleView() {
      this.viewMode = this.viewMode === "grid" ? "table" : "grid";
    },
    
    async fetchAvailableSites() {
      try {
        console.log("Fetching sites for company ID:", this.companyId);
        const response = await axios.get(
          `http://localhost:8000/sites/available/`,
          {
            params: {
              company_id: this.companyId, // Pass the company ID of the logged-in broker
            },
          }
        );
        this.sites = response.data.sites;
        this.filteredSites = this.sites; // Initialize filtered sites

        if (!this.sites.length) {
          console.warn("No sites with available units found.");
        }
      } catch (error) {
        console.error(
          "Error fetching available sites:",
          error.response || error.message
        );
      } finally {
        this.loading = false;
      }
    },
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

/* Ensure .main-page fills the available space */
.main-page {
  display: flex;
  min-height: 100vh;
  /* Ensures it spans the full viewport height */
  background-color: #e8f0fa;
  /* Gray background */
}

.main-content {
  display: flex;
  flex-direction: column;
  margin-top: 80px;
  margin-left: 250px;
  /* Offset for header height */
  flex: 1;
  /* margin-left: 250px; */
  /* Set margin equal to sidebar width */
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

/* Ensure the container takes the full width available */
.site-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  max-width: 1100px;
  /* Matches the max-width of the card */
  margin: 0 auto;
  /* Centers the grid within the parent */
}


/* Site card settings */
.site-card {
  background: #fff;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  box-sizing: border-box; /* Ensure padding is included in width/height */
  transition: transform 0.2s ease; /* Smooth hover effect */
}

/* Hover effect */
.site-card:hover {
  transform: translateY(-2px); /* Lift effect on hover */
}

/* Image within the card */
.site-image {
  width: 100%; /* Fill the width of the card */
  height: 150px; /* Fixed height for consistency */
  object-fit: cover; /* Crop and maintain aspect ratio */
  border-radius: 12px;
  margin-bottom: 10px; /* Space between image and text */
}

/* Site name styling */
.site-name {
  font-size: 15px;
  font-weight: bold;
  margin-bottom: 5px; /* Space below the site name */
}

/* Site location styling */
.site-location {
  font-size: 14px;
  color: #777;
}

/* Optional: Add a max-height to the cards if the image/content is too large */
.site-card {
  height: 300px; /* Optional: Fix card height to prevent overflow */
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Space out the content */
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

.site-table th:nth-child(1),
.site-table td:nth-child(1) {
  /* Status column */
  width: 50%;
}

.site-table th:nth-child(2),
.site-table td:nth-child(2) {
  /* Actions column */
  width: 50%;
}

.outside-headers {
  display: grid;
  /* Change to grid layout */
  grid-template-columns: 50% 50%;
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

.card-hover {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.card-hover:hover {
  transform: translateY(-5px); /* Slight lift effect */
  box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.2); /* Increase shadow on hover */
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
  border: 1px solid #42b983;
  border-radius: 3px;
  font-size: 14px;
  background-color: #42b983;
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

/* Custom pagination styles */
.pagination-controls {
  display: flex;
  justify-content: flex-end; /* Align to the right */
  margin-top: 20px; /* Add spacing from the content above */
  gap: 10px; /* Spacing between buttons */
  padding-right: 20px; /* Add padding to push it away from the edge */
}

.page-button {
  padding: 5px 10px;
  font-size: 12px; /* Slightly smaller font */
  border: 1px solid #ddd;
  background-color: #fff;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.page-button.active {
  background-color: #007bff;
  color: white;
}

.page-button:disabled {
  cursor: not-allowed;
  background-color: #f5f5f5;
}

.page-button:hover:not(:disabled) {
  background-color: #e9ecef; /* Light gray */
}


@media (max-width: 1440px) {
  .site-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
}

@media (max-width: 1080px) {
  .site-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
}

@media (max-width: 720px) {
  .site-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }

  .site-card {
    height: auto; /* Adjust for smaller screens */
  }

  .pagination-controls {
    flex-direction: column; /* Stack pagination for smaller viewports */
    align-items: center;
  }
}

@media (max-width: 720px) {
  body {
    font-size: 14px; /* Smaller font for smaller screens */
  }

  .site-name {
    font-size: 14px;
  }

  .site-location {
    font-size: 12px;
  }
}


</style>
