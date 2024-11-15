<template>
  <div class="developer-sites-page">
    <SideNav />
    <div class="content">
      <h1>Company Site Management</h1>
      <div class="toolbar">
        <select v-model="sortBy">
          <option value="name">Sort: Name</option>
          <option value="status">Sort: Status</option>
        </select>
        <input type="text" v-model="searchQuery" placeholder="Search Site" />
        <button @click="addSite">Add</button>
      </div>
      <div class="site-grid">
        <div
          v-for="site in filteredSites"
          :key="site.id"
          class="site-card"
          @click="viewSite(site)"
        >
          <img :src="site.picture" alt="Site Picture" class="site-image" />
          <h2>{{ site.name }}</h2>
        </div>
      </div>

      <!-- Site Details Modal -->
      <div v-if="selectedSite" class="site-details">
        <button @click="selectedSite = null">Back</button>
        <div class="site-header">
          <h2>{{ selectedSite.name }}</h2>
          <button @click="editSite(selectedSite)">Edit</button>
          <button @click="deleteSite(selectedSite)">Delete</button>
        </div>
        <div class="site-info">
          <img
            :src="selectedSite.picture"
            alt="Site Picture"
            class="site-image-large"
          />
          <div class="site-details-info">
            <p><strong>Site Name:</strong> {{ selectedSite.name }}</p>
            <p><strong>Address:</strong> {{ selectedSite.location }}</p>
            <p><strong>Total Units:</strong> 100 units</p>
            <p><strong>Available Units:</strong> 80 units</p>
            <p><strong>Sold Units:</strong> 20 units</p>
            <p><strong>Status:</strong> {{ selectedSite.status }}</p>
            <p><strong>Assigned Brokers:</strong> Team A</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";

export default {
  name: "DevFuncSites",
  components: {
    SideNav,
  },
  data() {
    return {
      sortBy: "name",
      searchQuery: "",
      selectedSite: null,
      sites: [
        {
          id: 1,
          picture: "path/to/picture1.jpg",
          name: "COMPANY SITE 1",
          description: "Description for Company Site 1",
          location: "Manila City, Philippines",
          status: "preselling",
        },
        {
          id: 2,
          picture: "path/to/picture2.jpg",
          name: "COMPANY SITE 2",
          description: "Description for Company Site 2",
          location: "Quezon City, Philippines",
          status: "ongoing",
        },
        {
          id: 3,
          picture: "path/to/picture3.jpg",
          name: "COMPANY SITE 3",
          description: "Description for Company Site 3",
          location: "Cebu City, Philippines",
          status: "completed",
        },
        {
          id: 4,
          picture: "path/to/picture4.jpg",
          name: "COMPANY SITE 4",
          description: "Description for Company Site 4",
          location: "Davao City, Philippines",
          status: "sold_out",
        },
        // Additional dummy sites as needed
      ],
    };
  },
  computed: {
    filteredSites() {
      return this.sites
        .filter((site) =>
          site.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        )
        .sort((a, b) => {
          if (this.sortBy === "name") {
            return a.name.localeCompare(b.name);
          } else if (this.sortBy === "status") {
            return a.status.localeCompare(b.status);
          }
          return 0;
        });
    },
  },
  methods: {
    viewSite(site) {
      this.selectedSite = site;
    },
    editSite(site) {
      alert(`Editing ${site.name}`);
    },
    deleteSite(site) {
      alert(`Deleting ${site.name}`);
    },
    addSite() {
      alert("Add a new site");
    },
  },
};
</script>

<style scoped>
.developer-sites-page {
  display: flex;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.site-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.site-card {
  border: 1px solid #ccc;
  padding: 10px;
  cursor: pointer;
  text-align: center;
}

.site-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.site-details {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20px;
  overflow-y: auto;
}

.site-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.site-image-large {
  width: 100%;
  height: auto;
  max-width: 400px;
  margin: 20px 0;
}

.site-details-info {
  text-align: left;
}
</style>
