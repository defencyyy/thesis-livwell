<template>
  <div class="developer-sites-page">
    <SideNav />
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
              <button @click.stop="deleteSite(site)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Add and Edit Modals using b-modal -->
      <b-modal v-model="showAddModal" title="Add New Site" hide-footer>
        <form @submit.prevent="addSite">
          <div class="form-group">
            <label for="siteName">Site Name:</label>
            <input type="text" v-model="newSite.name" id="siteName" required />
          </div>

          <div class="form-group">
            <label for="siteLocation">Location:</label>
            <input
              type="text"
              v-model="newSite.location"
              id="siteLocation"
              required
            />
          </div>

          <div class="form-group">
            <label for="siteStatus">Status:</label>
            <select v-model="newSite.status" id="siteStatus" required>
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
            <label for="sitePicture">Picture URL:</label>
            <input type="text" v-model="newSite.picture" id="sitePicture" />
          </div>

          <button type="submit">Save</button>
          <button type="button" @click="showAddModal = false">Cancel</button>
        </form>
      </b-modal>

      <b-modal v-model="showEditModal" title="Edit Site" hide-footer>
        <form @submit.prevent="confirmEdit">
          <div class="form-group">
            <label for="editSiteName">Site Name:</label>
            <input
              type="text"
              v-model="editSite.name"
              id="editSiteName"
              required
            />
          </div>

          <div class="form-group">
            <label for="editSiteLocation">Location:</label>
            <input
              type="text"
              v-model="editSite.location"
              id="editSiteLocation"
              required
            />
          </div>

          <div class="form-group">
            <label for="editSiteStatus">Status:</label>
            <select v-model="editSite.status" id="editSiteStatus" required>
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
            <label for="editSitePicture">Picture URL:</label>
            <input
              type="text"
              v-model="editSite.picture"
              id="editSitePicture"
            />
          </div>

          <button type="submit">Save Changes</button>
          <button type="button" @click="showEditModal = false">Cancel</button>
        </form>
      </b-modal>

      <!-- Site Details Modal -->
      <b-modal v-model="selectedSiteModal" title="Site Details" hide-footer>
        <div v-if="selectedSite">
          <h2>{{ selectedSite.name }}</h2>
          <p><strong>Location:</strong> {{ selectedSite.location }}</p>
          <p><strong>Status:</strong> {{ selectedSite.status }}</p>
          <img
            :src="selectedSite.picture || '/default-image-large.jpg'"
            alt="Site Picture"
            class="site-image-large"
          />
        </div>
        <button class="btn-primary" @click="selectedSiteModal = false">
          Close
        </button>
      </b-modal>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import { BModal } from "bootstrap-vue-3";
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "DevSites",
  components: {
    SideNav,
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
      newSite: { name: "", location: "", status: "", picture: "" },
      editSite: {},
      statusOptions: ["Preselling", "Ongoing", "Completed", "Sold Out"],
      sites: [],
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
        .sort((a, b) =>
          this.sortBy === "name"
            ? a.name.localeCompare(b.name)
            : a.status.localeCompare(b.status)
        );
    },
  },
  methods: {
    async fetchSites() {
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
        if (response.status === 200) {
          this.sites = response.data;
        }
      } catch (error) {
        console.error("Error fetching sites:", error);
      }
    },
    toggleView() {
      this.viewMode = this.viewMode === "grid" ? "table" : "grid";
    },
    async addSite() {
      try {
        const response = await axios.post(
          "http://localhost:8000/developer/sites/add",
          this.newSite,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 201) {
          this.sites.push(response.data);
          this.showAddModal = false;
          this.newSite = { name: "", location: "", status: "", picture: "" };
        }
      } catch (error) {
        console.error("Error adding site:", error);
      }
    },
    openEditModal(site) {
      this.editSite = { ...site };
      this.showEditModal = true;
    },
    async confirmEdit() {
      try {
        const response = await axios.put(
          `http://localhost:8000/developer/sites/${this.editSite.id}/`,
          this.editSite,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
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
        console.error("Error editing site:", error);
      }
    },
    async deleteSite(site) {
      try {
        const response = await axios.delete(
          `http://localhost:8000/developer/sites/${site.id}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 204) {
          this.sites = this.sites.filter((s) => s.id !== site.id);
        }
      } catch (error) {
        console.error("Error deleting site:", error);
      }
    },
    viewSite(site) {
      this.selectedSite = site;
      this.selectedSiteModal = true;
    },
  },
  mounted() {
    this.fetchSites();
  },
};
</script>

<style scoped>
/* Refined Styles */
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
