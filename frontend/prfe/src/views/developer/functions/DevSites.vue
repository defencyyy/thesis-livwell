<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="title-wrapper">
          <div class="title-left">
            <div class="title-icon"></div>
            <div class="edit-title">Company Site Management</div>
          </div>

          <div class="view-switch">
            <div class="view-icon" :class="{ active: viewMode === 'grid' }" @click="viewMode = 'grid'">
              <i class="fa fa-th"></i> <!-- Grid Icon -->
            </div>
            <div class="separator"></div>
            <div class="view-icon" :class="{ active: viewMode === 'table' }" @click="viewMode = 'table'">
              <i class="fa fa-list"></i> <!-- Table Icon -->
            </div>
          </div>

          <!-- <button @click="toggleView">
                  Switch to {{ viewMode === "grid" ? "Table" : "Grid" }} View
                </button> -->
        </div>

        <div class="card shadow-lg border-0 rounded-3 mx-auto" style="max-width: 1100px">
          <div class="card-body">
            <div class="row">
              <!-- Toolbar -->
              <div class="toolbar">
                <div class="left-section">
                  <div class="search-bar-container">
                    <input type="text" v-model="searchQuery" placeholder="Search Site" class="search-bar" />
                    <i class="fa fa-search search-icon"></i>
                  </div>
                  <select v-model="sortBy" class="dropdown">
                    <option value="name">Sort: Name</option>
                    <option value="status">Sort: Status</option>
                  </select>
                </div>
                <div class="right-section">
                  <button @click="showAddModal = true" class="btn-primary add-button">
                    Add Site
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Grid View -->
        <div v-if="viewMode === 'grid'" class="site-grid">
          <div v-for="site in filteredSites" :key="site.id" class="site-card" @click="viewSite(site)">
            <!-- Site Image -->
            <img :src="site.picture || require('@/assets/home.png')" alt="Site Image" class="site-image" />

            <!-- Site Name -->
            <h2 class="site-name">{{ site.name }}</h2>

            <!-- Site Location -->
            <p class="site-location">{{ site.location }}</p>
          </div>
        </div>

        <!-- Table View -->
        <div v-if="viewMode === 'table'">
          <!-- Headers outside the card -->
          <div class="outside-headers">
            <span class="header-item">Name</span>
            <span class="header-item">Location</span>
            <span class="header-item">Status</span>
            <span class="header-item">Actions</span>
          </div>

          <!-- Table inside the card -->
          <div v-for="site in filteredSites" :key="site.id" class="card shadow-lg border-0 rounded-3 mx-auto"
            style="max-width: 1100px">
            <div class="card-body">
              <table class="site-table">
                <tbody>
                  <tr>
                    <td>
                      <div class="site-info">
                        <img :src="site.picture || require('@/assets/home.png')" alt="Site Image" class="table-image" />
                        <span class="site-name">{{ site.name }}</span>
                      </div>
                    </td>
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
            </div>
          </div>
        </div>

        <!-- Add and Edit Modals using b-modal -->
        <!-- <b-modal v-model="showAddModal" title="Add New Site" hide-footer>
          <form @submit.prevent="addSite">
            <div class="form-group">
              <label for="siteName">Site Name:</label>
              <input type="text" v-model="newSite.name" id="siteName" required />
            </div>

            <div class="form-group">
              <label for="siteLocation">Location:</label>
              <input type="text" v-model="newSite.location" id="siteLocation" required />
            </div>

            <div class="form-group">
              <label for="siteStatus">Status:</label>
              <select v-model="newSite.status" id="siteStatus" required>
                <option v-for="status in statusOptions" :key="status" :value="status">
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
        </b-modal> -->

        <b-modal v-model="showAddModal" hide-header hide-footer>
          <div class="modal-title p-3">
            <h5 class="mb-0">New Site</h5>
          </div>
          <div class="p-3">
            <form @submit.prevent="addSite">
              <!-- Site Name -->
              <div class="form-group mb-3">
                <label for="siteName" class="form-label">Site Name</label>
                <input type="text" v-model="newSite.name" id="siteName" class="form-control" required />
              </div>

              <!-- Location -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="region" class="form-label">Region</label>
                  <select v-model="newSite.region" id="region" class="form-select" required>
                    <option v-for="region in regionOptions" :key="region" :value="region">
                      {{ region }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label for="province" class="form-label">Province</label>
                  <select v-model="newSite.province" id="province" class="form-select" required>
                    <option v-for="province in provinceOptions" :key="province" :value="province">
                      {{ province }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="city" class="form-label">City</label>
                  <select v-model="newSite.city" id="city" class="form-select" required>
                    <option v-for="city in cityOptions" :key="city" :value="city">
                      {{ city }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label for="postalCode" class="form-label">Postal Code</label>
                  <input type="text" v-model="newSite.postalCode" id="postalCode" class="form-control" required />
                </div>
              </div>
              <div class="form-group mb-3">
                <label for="otherAddress" class="form-label">Barangay, Street Name, Building No.</label>
                <input type="text" v-model="newSite.otherAddress" id="otherAddress" class="form-control" required />
              </div>

              <!-- Status -->
              <div class="form-group mb-3">
                <label for="siteStatus" class="form-label">Status</label>
                <select v-model="newSite.status" id="siteStatus" class="form-select" required>
                  <option v-for="status in statusOptions" :key="status" :value="status">
                    {{ status }}
                  </option>
                </select>
              </div>

              <!-- Picture URL -->
              <div class="form-group mb-3">
        <label for="siteStatus" class="form-label">Status</label>
        <select
          v-model="newSite.status"
          id="siteStatus"
          class="form-select"
          required
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

      <!-- Modern Photo Upload -->
      <div class="form-group mb-3">
        <label for="sitePicture" class="form-label">Upload Photo</label>
        <input
          type="file"
          @change="handleFileUpload"
          id="sitePicture"
          class="form-control"
          accept="image/*"
        />
      </div>


              <!-- Buttons -->
              <div class="d-flex justify-content-end gap-3">
                <button type="submit" class="btn btn-primary">Save</button>
                <button type="button" @click="showAddModal = false" class="btn btn-secondary">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </b-modal>



        <b-modal v-model="showEditModal" title="Edit Site" hide-footer>
          <form @submit.prevent="confirmEdit">
            <!-- Site Name -->
            <div class="form-group mb-3">
              <label for="editSiteName" class="form-label">Site Name:</label>
              <input type="text" v-model="editSite.name" id="editSiteName" class="form-control" required />
            </div>

            <!-- Location -->
            <div class="form-group mb-3">
              <label for="editSiteLocation" class="form-label">Location:</label>
              <input type="text" v-model="editSite.location" id="editSiteLocation" class="form-control" required />
            </div>

            <!-- Status -->
            <div class="form-group mb-3">
              <label for="editSiteStatus" class="form-label">Status:</label>
              <select v-model="editSite.status" id="editSiteStatus" class="form-select" required>
                <option v-for="status in statusOptions" :key="status" :value="status">
                  {{ status }}
                </option>
              </select>
            </div>

            <!-- Picture URL -->
            <div class="form-group mb-3">
              <label for="editSitePicture" class="form-label">Picture URL:</label>
              <input type="text" v-model="editSite.picture" id="editSitePicture" class="form-control" />
            </div>

            <!-- Buttons -->
            <div class="d-flex justify-content-end gap-3">
              <button type="submit" class="btn btn-success">Save Changes</button>
              <button type="button" @click="showEditModal = false" class="btn btn-secondary">Cancel</button>
            </div>
          </form>
        </b-modal>

        <b-modal v-model="showEditModal" title="Edit Site" hide-footer>
          <form @submit.prevent="confirmEdit">
            <div class="form-group">
              <label for="editSiteName">Site Name:</label>
              <input type="text" v-model="editSite.name" id="editSiteName" required />
            </div>

            <div class="form-group">
              <label for="editSiteLocation">Location:</label>
              <input type="text" v-model="editSite.location" id="editSiteLocation" required />
            </div>

            <div class="form-group">
              <label for="editSiteStatus">Status:</label>
              <select v-model="editSite.status" id="editSiteStatus" required>
                <option v-for="status in statusOptions" :key="status" :value="status">
                  {{ status }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="editSitePicture">Picture URL:</label>
              <input type="text" v-model="editSite.picture" id="editSitePicture" />
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
            <img :src="selectedSite.picture || '/default-image-large.jpg'" alt="Site Picture"
              class="site-image-large" />
          </div>
          <button class="btn-primary" @click="selectedSiteModal = false">
            Close
          </button>
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

.title-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  /* Push items to opposite sides */
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
  background-color: #6c757d;
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
  border-radius: 8px;
  overflow: hidden;
  background-color: #f9f9f9;
}

.view-icon {
  flex: 1;
  padding: 6px;
  text-align: center;
  cursor: pointer;
  font-size: 15px;
  color: #777;
  transition: background-color 0.3s, color 0.3s;
}

.view-icon.active {
  background-color: #7d7d7d;
  color: #fff;
}

.view-icon:hover {
  background-color: #e0e0e0;
}

.separator {
  width: 1px;
  background-color: #ccc;
  height: 100%;
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
  border-radius: 4px;
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
  border-radius: 4px;
  font-size: 14px;
  width: 80%;
  max-width: 150px;
  background-color: white;
  color: #333;
}


/* Button Styles */
.btn-primary.add-button {
  padding: 8px 12px;
  border: 1px solid #007bff;
  border-radius: 4px;
  font-size: 14px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary.add-button:hover {
  background-color: #0056b3;
}

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  margin-top: 0;
  max-width: 1100px;
  /* Ensures the card and grid align */
  margin-left: auto;
  /* Centers the card */
  margin-right: auto;
}


/* .search-bar {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
} */

.site-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  max-width: 1100px;
  /* Matches the max-width of the card */
  margin: 0 auto;
  /* Centers the grid within the parent */
}

.site-card {
  background: #fff;
  border: 1px solid #ffffff;
  border-radius: 16px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.site-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

.site-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  /* Ensures the image is cropped to fit the area */
  border-radius: 12px;
  margin-bottom: 10px;
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

.site-info {
  flex-direction: row;
}

.site-name {
  font-size: 15px;
  font-weight: bold;
  margin-top: 10px;
}

.site-location {
  font-size: 14px;
  color: #777;
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

.site-table th:nth-child(2),
.site-table td:nth-child(2) {
  /* Location column */
  width: 35%;
  padding-right: 60px;
}

.site-table th:nth-child(3),
.site-table td:nth-child(3) {
  /* Status column */
  width: 20%;
}

.site-table th:nth-child(4),
.site-table td:nth-child(4) {
  /* Actions column */
  width: 20%;
}


.outside-headers {
  display: grid;
  /* Change to grid layout */
  grid-template-columns: 25% 35% 20% 20%;
  /* Match the column widths */
  padding: 0px 20px;
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

.form-group .form-label,
.row .form-label {
  font-size: 0.9rem;
  /* Adjust the value to your preferred size */
}
</style>