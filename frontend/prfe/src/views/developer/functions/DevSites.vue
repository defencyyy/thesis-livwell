<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <h1>Company Site Management</h1>

        <!-- Toolbar -->
        <div class="toolbar">
          <button @click="toggleView">
            Switch to {{ viewMode === "grid" ? "Table" : "Grid" }} View
          </button>
          <select v-model="sortBy">
            <option value="name">Sort: Name</option>
            <option value="status">Sort: Status</option>
          </select>
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search Site"
            class="search-bar"
          />
          <button @click="showAddModal = true" class="btn-primary">
            Add Site
          </button>
          <!-- Button to toggle archived sites visibility -->
          <button @click="toggleArchived" class="btn-secondary">
            {{ showArchived ? "Hide Archived Sites" : "Show Archived Sites" }}
          </button>
        </div>

        <!-- Grid View -->
        <div v-if="viewMode === 'grid'" class="site-grid">
          <div
            v-for="site in filteredSites"
            :key="site.id"
            class="site-card"
            @click="viewSite(site)"
          >
            <img :src="site.picture || '/default-image.jpg'" alt="Site Image" />
            <h2>{{ site.name }}</h2>
          </div>
        </div>

        <!-- Table View -->
        <table v-if="viewMode === 'table'" class="site-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Location</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="site in filteredSites" :key="site.id">
              <td>{{ site.name }}</td>
              <td>{{ site.location }}</td>
              <td>{{ site.status }}</td>
              <td>
                <button @click.stop="viewSite(site)">View</button>
                <button @click.stop="openEditModal(site)">Edit</button>
                <button @click.stop="archiveSite(site)">Archive</button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Add and Edit Modals using b-modal -->
        <!-- Add Site Modal -->
        <b-modal v-model="showAddModal" title="Add New Site" hide-footer>
          <!-- Add Site Form -->
        </b-modal>

        <!-- Edit Site Modal -->
        <b-modal v-model="showEditModal" title="Edit Site" hide-footer>
          <!-- Edit Site Form -->
        </b-modal>

        <!-- Site Details Modal -->
        <b-modal v-model="selectedSiteModal" title="Site Details" hide-footer>
          <!-- Site Details Content -->
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { BModal } from "bootstrap-vue-3";
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "DevSites",
  components: {
    SideNav,
    AppHeader,
    BModal,
  },
  data() {
    return {
      viewMode: "table",
      sortBy: "name",
      searchQuery: "",
      showAddModal: false,
      showEditModal: false,
      selectedSite: null,
      selectedSiteModal: false,
      newSite: {
        name: "",
        location: "",
        status: "",
        picture: "",
        description: "",
      }, // Added description
      editSite: {},
      statusOptions: ["Preselling", "Ongoing", "Completed", "Sold Out"],
      sites: [],
      showArchived: false, // State to control archived sites visibility
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId,
      userType: (state) => state.userType,
      companyId: (state) => state.companyId,
    }),
    vuexUserId() {
      return this.userId;
    },
    vuexCompanyId() {
      return this.companyId;
    },
    filteredSites() {
      return this.sites
        .filter((site) =>
          site.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        )
        .filter((site) => this.showArchived || !site.isArchived) // Show or hide archived sites
        .sort((a, b) =>
          this.sortBy === "name"
            ? a.name.localeCompare(b.name)
            : a.status.localeCompare(b.status)
        );
    },
  },
  methods: {
    async fetchSites() {
      console.log("Fetching sites...");

      const companyId = this.vuexCompanyId;
      if (!companyId) {
        alert("Company ID not found. Please log in.");
        this.$router.push({ name: "DevLogin" });
        return;
      }

      try {
        const response = await axios.get(
          "http://localhost:8000/developer/sites/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        console.log("Sites fetched:", response.data);
        if (response.status === 200) {
          this.sites = response.data; // Fetch both active and archived sites
        }
      } catch (error) {
        if (error.response?.status === 401) {
          const refreshedToken = await this.refreshAccessToken();
          if (refreshedToken) {
            this.fetchSites(); // Retry after refreshing
          }
        } else {
          console.error("Error fetching sites:", error.response || error);
        }
      }
    },

    async refreshAccessToken() {
      try {
        const refreshToken = localStorage.getItem("refreshToken");
        const response = await axios.post(
          "http://localhost:8000/api/token/refresh/",
          { refresh: refreshToken }
        );
        if (response.status === 200) {
          const { access } = response.data;
          localStorage.setItem("accessToken", access);
          return access;
        } else {
          this.handleTokenRefreshFailure();
        }
      } catch (error) {
        this.handleTokenRefreshFailure();
      }
    },

    handleTokenRefreshFailure() {
      alert("Session expired. Please log in again.");
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      this.$router.push({ name: "DevLogin" });
    },

    toggleView() {
      this.viewMode = this.viewMode === "grid" ? "table" : "grid";
    },
    toggleArchived() {
      this.showArchived = !this.showArchived;
    },
    async addSite() {
      console.log("Adding site with data:", this.newSite);

      const formData = new FormData();
      formData.append("name", this.newSite.name);
      formData.append("location", this.newSite.location);
      formData.append("status", this.newSite.status || "Preselling");
      formData.append("companyId", this.vuexCompanyId);
      formData.append("userId", this.vuexUserId);
      formData.append("description", this.newSite.description || ""); // Optional description field

      if (this.newSite.picture) {
        formData.append("picture", this.newSite.picture);
      }

      try {
        const response = await axios.post(
          "http://localhost:8000/developer/sites/",
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );
        if (response.status === 201) {
          this.sites.push(response.data);
          this.showAddModal = false;
          this.newSite = {
            name: "",
            location: "",
            status: "",
            picture: "",
            description: "",
          }; // Clear the form
        }
      } catch (error) {
        console.error("Error adding site:", error.response || error);
      }
    },
    async archiveSite(site) {
      console.log("Archiving site:", site);
      site.isArchived = true; // Mark as archived

      try {
        const response = await axios.put(
          `http://localhost:8000/developer/sites/${site.id}/`,
          site,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          this.sites = this.sites.filter((s) => s.id !== site.id); // Remove from UI
        }
      } catch (error) {
        console.error("Error archiving site:", error.response || error);
      }
    },
    viewSite(site) {
      this.selectedSite = site;
      this.selectedSiteModal = true;
    },
    openEditModal(site) {
      this.editSite = { ...site };
      this.showEditModal = true;
    },
  },
  mounted() {
    this.fetchSites();
  },
};
</script>

<style scoped>
.main-page {
  display: flex;
  height: 100vh;
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

.toolbar {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.search-bar {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.site-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.site-card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.site-card img {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.site-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
}

.site-table th,
.site-table td {
  padding: 10px;
  border: 1px solid #ddd;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
