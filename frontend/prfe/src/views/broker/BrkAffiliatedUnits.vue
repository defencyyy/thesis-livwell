<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <h1 class="display-5 fw-bolder text-capitalize">
        Available units
        </h1>
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
                    />
                    <i class="fa fa-search search-icon"></i>
                  </div>

                  <!-- Sort Dropdown -->
                  <select v-model="sortBy" class="dropdown">
                    <option value="name">Sort: Name</option>
                    <option value="status">Sort: Status</option>
                  </select>
        </div>
        </div>
        </div>
        </div>
        </div>
        
        <div v-if="sites.length" class="site-sales">
          <div class="site-card-container">
            <div
              v-for="site in sites"
              :key="site.id"
              class="site-card"
              @click="() => redirectToUnits(site.id)"
            >
              <img :src="site.picture" alt="Site Picture" />
              <h2 class="display-6 fw-bolder text-capitalize">
                {{ site.name }}
              </h2>
              <p class="text-start">{{ site.description }}</p>
              <p class="text-start"><b>Location: </b> {{ site.location }}</p>
            </div>
          </div>
        </div>
        <div v-else>
          <p>No sites with available units.</p>
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
      sites: [],
      loading: true,
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId,
      userType: (state) => state.userType,
      companyId: (state) => state.companyId,
    }),
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
  background-color: #ebebeb; /* Gray background */
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

.site-sales {
  margin-top: 20px;
}

.site-card-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin: 0 auto;
}

.site-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  cursor: pointer;
  transition: box-shadow 0.3s;
  background-color: rgb(253, 253, 253);
}

.site-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  background: rgb(230, 230, 230);
}

.site-card img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
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

</style>
