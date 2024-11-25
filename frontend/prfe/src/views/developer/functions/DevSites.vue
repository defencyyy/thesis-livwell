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

        <!-- Add Site Modal -->
        <b-modal v-model="showAddModal" title="Add New Site" hide-footer>
          <form @submit.prevent="addSite">
            <div class="form-group">
              <label for="siteName">Name</label>
              <input
                v-model="newSite.name"
                type="text"
                id="siteName"
                placeholder="Enter site name"
                class="form-control"
              />
            </div>
            <div class="form-group">
              <label for="siteLocation">Location</label>
              <input
                v-model="newSite.location"
                type="text"
                id="siteLocation"
                placeholder="Enter location"
                class="form-control"
              />
            </div>
            <div class="form-group">
              <label for="siteStatus">Status</label>
              <select
                v-model="newSite.status"
                id="siteStatus"
                class="form-control"
              >
                <option
                  v-for="status in statusOptions"
                  :key="status"
                  :value="status"
                >
                  {{ status }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="siteDescription">Description</label>
              <textarea
                v-model="newSite.description"
                id="siteDescription"
                placeholder="Enter description"
                class="form-control"
              ></textarea>
            </div>
            <div class="form-group">
              <label for="sitePicture">Picture</label>
              <input
                type="file"
                id="sitePicture"
                @change="handlePictureUpload($event, 'add')"
                class="form-control"
              />
            </div>

            <div class="form-group">
              <button type="submit" class="btn-primary">Add Site</button>
            </div>
          </form>
        </b-modal>

        <!-- Edit Site Modal -->
        <b-modal v-model="showEditModal" title="Edit Site" hide-footer>
          <form @submit.prevent="saveEditSite">
            <div class="form-group">
              <label for="editSiteName">Name</label>
              <input
                v-model="editSite.name"
                type="text"
                id="editSiteName"
                class="form-control"
              />
            </div>
            <div class="form-group">
              <label for="editSiteLocation">Location</label>
              <input
                v-model="editSite.location"
                type="text"
                id="editSiteLocation"
                class="form-control"
              />
            </div>
            <div class="form-group">
              <label for="editSiteStatus">Status</label>
              <select
                v-model="editSite.status"
                id="editSiteStatus"
                class="form-control"
              >
                <option
                  v-for="status in statusOptions"
                  :key="status"
                  :value="status"
                >
                  {{ status }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="editSiteDescription">Description</label>
              <textarea
                v-model="editSite.description"
                id="editSiteDescription"
                class="form-control"
              ></textarea>
            </div>
            <div class="form-group">
              <label for="editSitePicture">Picture</label>
              <input
                type="file"
                id="editSitePicture"
                @change="handlePictureUpload($event, 'edit')"
                class="form-control"
              />
            </div>

            <div class="form-group">
              <button type="submit" class="btn-primary">Save Changes</button>
            </div>
          </form>
        </b-modal>

        <!-- Site Details Modal -->
        <b-modal v-model="selectedSiteModal" title="Site Details" hide-footer>
          <div v-if="selectedSite">
            <img
              :src="selectedSite.picture || '/default-image.jpg'"
              alt="Site Image"
              class="img-fluid mb-3"
            />
            <h2>{{ selectedSite.name }}</h2>
            <p><strong>Location:</strong> {{ selectedSite.location }}</p>
            <p><strong>Status:</strong> {{ selectedSite.status }}</p>
            <p><strong>Description:</strong> {{ selectedSite.description }}</p>
            <button @click="selectedSiteModal = false" class="btn-secondary">
              Close
            </button>
          </div>
          <div v-else>
            <p>Loading site details...</p>
          </div>
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
      selectedSite: {}, // Prevent null reference issues
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
      if (!Array.isArray(this.sites)) return [];
      return this.sites
        .filter((site) =>
          site.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        )
        .filter((site) => this.showArchived || !site.isArchived)
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
    handlePictureUpload(event, mode) {
      const file = event.target.files[0];
      if (file) {
        if (mode === "add") {
          this.newSite.picture = file;
        } else if (mode === "edit") {
          this.editSite.picture = file;
        }
      }
    },
    async saveEditSite() {
      console.log("Saving site:", this.editSite);

      const formData = new FormData();
      formData.append("name", this.editSite.name);
      formData.append("location", this.editSite.location);
      formData.append("status", this.editSite.status);
      formData.append("description", this.editSite.description || "");

      if (this.editSite.picture) {
        formData.append("picture", this.editSite.picture);
      }

      try {
        const response = await axios.put(
          `http://localhost:8000/developer/sites/${this.editSite.id}/`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );
        if (response.status === 200) {
          const index = this.sites.findIndex(
            (site) => site.id === this.editSite.id
          );
          this.sites[index] = response.data;
          this.showEditModal = false;
        }
      } catch (error) {
        console.error("Error saving site:", error.response || error);
      }
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
      if (site) {
        this.selectedSite = site;
        this.selectedSiteModal = true;
      } else {
        console.error("Attempted to view a null or undefined site.");
      }
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
