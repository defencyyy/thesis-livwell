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
        <p>No sites with available units.</p>
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
    const router = useRouter();

    const redirectToUnits = (siteId) => {
      router.push({ name: 'AvailableUnits', params: { siteId } }); 
    };

    return { redirectToUnits };
  },
  data() {
    return {
      sites: [], 
    };
  },
  mounted() {
    this.fetchAvailableSites();
  },
  methods: {
    async fetchAvailableSites() {
      try {
        const response = await axios.get('http://localhost:8000/sites/available/');
        this.sites = response.data.sites; 
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
}

.site-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.site-card img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
}
</style>
