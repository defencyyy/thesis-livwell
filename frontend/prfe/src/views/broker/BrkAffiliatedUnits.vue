<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <h1 class="display-5 fw-bolder text-capitalize">Welcome to Affiliated Units</h1>
        <div v-if="sites.length" class="site-sales">
          <div class="site-card-container">
            <div
              v-for="site in sites"
              :key="site.id"
              class="site-card"
              @click="() => redirectToUnits(site.id)"
            >
              <img :src="site.picture" alt="Site Picture" />
              <h2 class="display-6 fw-bolder text-capitalize">{{ site.name }}</h2>
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
        const response = await axios.get(
          `http://localhost:8000/sites/available/`,
          {
            params: {
              company_id: this.companyId, // Pass the company ID of the logged-in broker
            },
          }
        );
        this.sites = response.data.sites;
      } catch (error) {
        console.error("Error fetching available sites:", error);
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
</style>
