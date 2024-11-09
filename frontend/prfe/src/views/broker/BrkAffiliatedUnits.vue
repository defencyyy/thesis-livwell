<template>
  <header>
    <HeaderLivwell/>
  </header>
  <div class="affiliated-units-page">
    <SideNav />
    <div class="content">
      <h1>Welcome to Affiliated Units</h1>
      <div v-if="sites.length" class="site-sales">
        <div class="site-card-container">
          <div 
            v-for="site in sites" 
            :key="site.id" 
            class="site-card" 
            @click="() => redirectToUnits(site.id)"  
          >
            <img :src="site.picture" alt="Site Picture" />
            <h2>{{ site.name }}</h2>
            <p>{{ site.description }}</p>
            <p>Location: {{ site.location }}</p>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No sites available.</p>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderLivwell from "@/components/HeaderLivwell.vue";
import SideNav from "@/components/SideNav.vue"; // Importing the SideNav component
import axios from 'axios'; // Ensure you have axios installed
import { useRouter } from 'vue-router'; // Import useRouter

export default {
  name: "AffiliatedUnits",
  components: {
    SideNav, HeaderLivwell // Registering the SideNav component
  },
  setup() {
    const router = useRouter(); // Use router for navigation

    const redirectToUnits = (siteId) => {
      router.push({ name: 'AvailableUnits', params: { siteId } }); // Redirect with site ID
    };

    return { redirectToUnits };
  },
  data() {
    return {
      sites: [], // Array to hold site data
    };
  },
  mounted() {
    this.fetchAvailableSites();
  },
  methods: {
    async fetchAvailableSites() {
      try {
        const response = await axios.get('http://localhost:8000/sites/available/');
        this.sites = response.data.sites; // Store the sites in the component's state
      } catch (error) {
        console.error("Error fetching available sites:", error);
      }
    },
  },
};
</script>

<style scoped>
.affiliated-units-page {
  display: flex;
  height: 100vh;
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
  display: grid; /* Use grid layout */
  grid-template-columns: repeat(3, 1fr); /* Three cards per row */
  gap: 20px; /* Space between cards */
  margin: 0 auto; /* Center the container */
}

.site-card {
  border: 1px solid #ccc; /* Optional: Add a border */
  border-radius: 8px; /* Optional: Add rounded corners */
  padding: 10px; /* Optional: Add padding */
  text-align: center;
  cursor: pointer; /* Indicate that the card is clickable */
  transition: box-shadow 0.3s; /* Smooth transition for hover effect */
}

.site-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Add a shadow on hover */
}

.site-card img {
  width: 100%; /* Make image take full width of the card */
  height: 150px; /* Set a fixed height for the image */
  object-fit: cover; /* Maintain aspect ratio and cover the area */
  border-radius: 4px; /* Optional: Add rounded corners to the image */
}
</style>
