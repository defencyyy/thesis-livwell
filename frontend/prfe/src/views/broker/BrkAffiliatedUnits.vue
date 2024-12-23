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
        
        <div>
          <div class="outside-headers">
            <span class="header-item">Name</span>
            <span class="header-item">Location</span>
            <span class="header-item">Actions</span>
          </div>

          <div v-if = "filteredSites.length">
            <div
              v-for="site in paginatedSites"
              :key="site.id || index"
              class="card border-0 rounded-1 mx-auto card-hover"
              style="
              max-width: 1100px;
              box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            "
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
                      <td>
                        <div class="broker-actions d-flex">
                          <button  @click="() => redirectToUnits(site.id)" style="
                              border: none;
                              background-color: transparent;
                              color: #343a40;
                              cursor: pointer;
                              font-size: 18px;
                            ">
                            <i class="fas fa-eye"></i>
                          </button>
                      </div>
                    </td>
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
    <nav aria-label="Page navigation example">
      <ul class="pagination">
        <li :class="['page-item', { disabled: currentPage === 1 }]">
          <a 
            class="page-link" 
            href="#" 
            @click.prevent="goToPage(currentPage - 1)"
            aria-label="Previous"
          >
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        <li 
          v-for="page in totalPages" 
          :key="page" 
          :class="['page-item', { active: page === currentPage }]"
        >
          <a 
            class="page-link" 
            href="#" 
            @click.prevent="goToPage(page)"
          >
            {{ page }}
          </a>
        </li>
        <li :class="['page-item', { disabled: currentPage === totalPages }]">
          <a 
            class="page-link" 
            href="#" 
            @click.prevent="goToPage(currentPage + 1)"
            aria-label="Next"
          >
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
        </nav>
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
      itemsPerPage: 15, // Number of customers per page

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
  padding: 0;
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

.main-page {
  display: flex;
  min-height: 100vh;
  background-color: #e8f0fa;
}

.main-content {
  display: flex;
  flex-direction: column;
  margin-top: 80px;
  margin-left: 250px;
  flex: 1;
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

.site-image {
  width: 100%; 
  height: 150px; 
  object-fit: cover; 
  border-radius: 12px;
  margin-bottom: 10px; 
}

.site-name {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 5px; 
}

.site-location {
  font-size: 14px;
  color: #777;
}

.table-image {
  width: 30px;
  height: 30px;
  object-fit: cover;
  margin-right: 10px;
}

.site-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 14px;
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

.site-table th:nth-child(1),
.site-table td:nth-child(1) {
  width: 40%;
}

.site-table th:nth-child(2),
.site-table td:nth-child(2) {
  width: 50%;
}

.site-table th:nth-child(3),
.site-table td:nth-child(3) {
  width: 10%;
}

.outside-headers {
  display: grid;
  grid-template-columns: 40% 50% 10%;
  padding: 0px 18px;
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
  margin-left: auto;
  margin-right: auto;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: -15px; /* Reduce margin */
  padding-right: 40px; /* Reduce padding */
  font-size: 14px; /* Smaller font size */
  line-height: 1.2; /* Adjust line height for compactness */
}

.page-item {
  margin: 0 2px; /* Reduce spacing between buttons */
}

.page-link {
  padding: 4px 8px; /* Smaller button padding */
  font-size: 14px; /* Match font size for consistency */
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