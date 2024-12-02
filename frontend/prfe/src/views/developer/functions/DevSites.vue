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
            <div
              class="view-icon"
              :class="{ active: viewMode === 'grid' }"
              @click="viewMode = 'grid'"
            >
              <i class="fa fa-th"></i>
              <!-- Grid Icon -->
            </div>
            <div class="separator"></div>
            <div
              class="view-icon"
              :class="{ active: viewMode === 'table' }"
              @click="viewMode = 'table'"
            >
              <i class="fa fa-list"></i>
              <!-- Table Icon -->
            </div>
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
                    />
                    <i class="fa fa-search search-icon"></i>
                  </div>

                  <!-- Sort Dropdown -->
                  <select v-model="sortBy" class="dropdown">
                    <option value="name">Sort: Name</option>
                    <option value="status">Sort: Status</option>
                  </select>

                  <select v-model="sortBy" class="dropdown2">
                    <option value="name">View: Archive</option>
                    <option value="status">View: Active</option>
                  </select>
                </div>

                <div class="right-section">
                  <!-- Filter Button -->
                  <button
                    @click="toggleArchived"
                    :class="['btn-secondary', { active: showArchived }]"
                    class="filter-button"
                  >
                    {{ showArchived ? "View Archived" : "View Active" }}
                  </button>

                  <!-- Add Site Button -->
                  <button
                    @click="showAddModal = true"
                    class="btn-primary add-button"
                  >
                    Add Site
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Grid View -->
        <div v-if="viewMode === 'grid'" class="site-grid">
          <div
            v-for="(site, index) in filteredSites"
            :key="site.id || index"
            class="site-card"
            @click="openEditModal(site)"
          >
            <!-- Site Image -->
            <img
              :src="site.picture || require('@/assets/home.png')"
              alt="Site Image"
              class="site-image"
            />

            <!-- Site Name -->
            <h2 class="site-name">
              {{ site.name || "Unknown" }}
            </h2>

            <!-- Site Location -->
            <p class="site-location">
              {{ site.location || "Location unavailable" }}
            </p>
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
          <div
            v-for="(site, index) in filteredSites"
            :key="site.id || index"
            class="card border-0 rounded-1 mx-auto"
            style="
              max-width: 1100px;
              box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <div class="card-body">
              <table class="site-table">
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
                    <td>{{ site.status || "Status unavailable" }}</td>
                    <td>
                      <!-- Edit Button -->
                      <button
                        @click.stop="openEditModal(site)"
                        style="
                          border: none;
                          background-color: transparent;
                          color: #343a40;
                          cursor: pointer;
                          font-size: 18px;
                        "
                      >
                        <i class="fas fa-edit"></i>
                      </button>

                      <!-- Manage Floors Button -->
                      <button
                        @click.stop="openFloorModal(site)"
                        style="
                          border: none;
                          background-color: transparent;
                          color: #343a40;
                          cursor: pointer;
                          font-size: 18px;
                        "
                      >
                        <i class="fas fa-layer-group"></i>
                      </button>

                      <!-- Archive/Unarchive Buttons -->
                      <button
                        v-if="!site.archived"
                        @click.stop="archiveSite(site)"
                        class="btn btn-sm btn-warning"
                        style="
                          border: none;
                          background-color: transparent;
                          color: #343a40;
                          cursor: pointer;
                          font-size: 18px;
                        "
                      >
                        <i class="fas fa-archive"></i>
                      </button>

                      <button
                        v-else
                        @click.stop="unarchiveSite(site)"
                        class="btn btn-sm btn-success"
                      >
                        <i class="fas fa-undo"></i> Unarchive
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <b-modal
          v-model="showAddModal"
          hide-header
          hide-footer
          centered
          size="lg"
        >
          <div class="modal-title p-3">
            <h5 class="mb-0">New Site</h5>
          </div>
          <div class="p-3">
            <form @submit.prevent="addSite">
              <div class="row">
                <!-- Left Side (Site Name to Status) -->
                <div class="col-md-6">
                  <!-- Site Name -->
                  <div class="form-group mb-3">
                    <label for="siteName" class="form-label">Site Name</label>
                    <input
                      type="text"
                      v-model="newSite.name"
                      id="siteName"
                      class="form-control"
                      required
                    />
                  </div>

                  <!-- Location -->
                  <div class="row mb-3">
                    <!-- Region Dropdown -->
                    <div class="col-md-6">
                      <label for="region" class="form-label">Region</label>
                      <select
                        v-model="selectedRegion"
                        id="region"
                        class="form-select"
                        @change="loadProvinceData(selectedRegion)"
                      >
                        <option
                          v-for="region in regionOptions"
                          :key="region"
                          :value="region"
                        >
                          {{ region }}
                        </option>
                      </select>
                    </div>

                    <!-- Province Dropdown -->
                    <div class="col-md-6">
                      <label for="province" class="form-label">Province</label>
                      <select
                        v-model="selectedProvince"
                        id="province"
                        class="form-select"
                        @change="loadMunicipalityData(selectedProvince)"
                      >
                        <option
                          v-for="province in provinceOptions"
                          :key="province"
                          :value="province"
                        >
                          {{ province }}
                        </option>
                      </select>
                    </div>
                  </div>

                  <!-- Municipality Dropdown -->
                  <div class="form-group mb-3">
                    <label for="municipality" class="form-label"
                      >Municipality</label
                    >
                    <select
                      v-model="selectedMunicipality"
                      id="municipality"
                      class="form-select"
                      @change="loadBarangayData(selectedMunicipality)"
                    >
                      <option
                        v-for="municipality in municipalityOptions"
                        :key="municipality"
                        :value="municipality"
                      >
                        {{ municipality }}
                      </option>
                    </select>
                  </div>

                  <div class="form-group mb-3">
                    <label for="barangay" class="form-label">Barangay</label>
                    <select
                      v-model="newSite.barangay"
                      id="barangay"
                      class="form-select"
                      required
                    >
                      <option
                        v-for="barangay in barangayOptions"
                        :key="barangay"
                        :value="barangay"
                      >
                        {{ barangay }}
                      </option>
                    </select>
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label for="postalCode" class="form-label"
                        >Postal Code</label
                      >
                      <input
                        type="text"
                        v-model="newSite.postalCode"
                        id="postalCode"
                        class="form-control"
                      />
                    </div>

                    <div class="col-md-6">
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
                  </div>
                </div>

                <!-- Right Side (Photo Upload with Preview) -->
                <div class="col-md-6">
                  <!-- Image Upload Section -->
                  <div class="form-group mb-3">
                    <label for="sitePicture" class="form-label"
                      >Upload Photo</label
                    >
                    <input
                      type="file"
                      @change="handlePictureUpload"
                      id="sitePicture"
                      class="form-control"
                      accept="image/*"
                    />
                  </div>

                  <!-- Image Preview Section -->
                  <div v-if="imagePreview" class="text-center">
                    <h6>Image Preview</h6>
                    <img
                      :src="imagePreview"
                      alt="Image Preview"
                      class="img-fluid"
                      style="max-height: 200px; object-fit: cover"
                    />
                  </div>
                </div>
              </div>

              <!-- Add Floors -->
              <div class="form-group mb-3">
                <label for="numberOfFloors">Number of Floors</label>
                <input
                  type="number"
                  v-model="newSite.number_of_floors"
                  id="numberOfFloors"
                  class="form-control"
                  placeholder="Enter the number of floors"
                  min="1"
                  required
                />
              </div>

              <!-- Buttons -->
              <div
                class="d-flex justify-content-end gap-2 mt-3"
                style="padding-top: 15px"
              >
                <button type="submit" class="btn-add" style="width: 150px">
                  Add New Site
                </button>
                <button
                  type="button"
                  @click="showAddModal = false"
                  class="btn-cancel"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </b-modal>

        <!-- Detail Modal -->
        <b-modal
          v-model="showEditModal"
          title="Site Details / Edit"
          hide-header
          hide-footer
          centered
          size="lg"
        >
          <div class="modal-title p-3">
            <h5 class="mb-0">Site Details / Edit</h5>
          </div>
          <div class="p-3">
            <form @submit.prevent="manageSite">
              <div class="row">
                <!-- Left Side (Site Name to Status) -->
                <div class="col-md-6">
                  <!-- Site Name (Read-Only) -->
                  <div class="form-group mb-3">
                    <label for="editSiteName" class="form-label"
                      >Site Name</label
                    >
                    <input
                      type="text"
                      v-model="editSite.name"
                      id="editSiteName"
                      class="form-control"
                      readonly
                    />
                  </div>

                  <!-- Location (Read-Only) -->
                  <div class="row mb-3">
                    <!-- Region -->
                    <div class="col-md-6">
                      <label for="editRegion" class="form-label">Region</label>
                      <input
                        type="text"
                        v-model="editSite.region"
                        id="editRegion"
                        class="form-control"
                        readonly
                      />
                    </div>

                    <!-- Province -->
                    <div class="col-md-6">
                      <label for="editProvince" class="form-label"
                        >Province</label
                      >
                      <input
                        type="text"
                        v-model="editSite.province"
                        id="editProvince"
                        class="form-control"
                        readonly
                      />
                    </div>
                  </div>

                  <!-- Municipality -->
                  <div class="form-group mb-3">
                    <label for="editMunicipality" class="form-label"
                      >Municipality</label
                    >
                    <input
                      type="text"
                      v-model="editSite.municipality"
                      id="editMunicipality"
                      class="form-control"
                      readonly
                    />
                  </div>

                  <!-- Barangay -->
                  <div class="form-group mb-3">
                    <label for="editBarangay" class="form-label"
                      >Barangay</label
                    >
                    <input
                      type="text"
                      v-model="editSite.barangay"
                      id="editBarangay"
                      class="form-control"
                      readonly
                    />
                  </div>

                  <!-- Postal Code -->
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label for="editPostalCode" class="form-label"
                        >Postal Code</label
                      >
                      <input
                        type="text"
                        v-model="editSite.postalCode"
                        id="editPostalCode"
                        class="form-control"
                        readonly
                      />
                    </div>

                    <!-- Status (Editable) -->
                    <div class="col-md-6">
                      <label for="editSiteStatus" class="form-label"
                        >Status</label
                      >
                      <select
                        v-model="editSite.status"
                        id="editSiteStatus"
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
                  </div>
                </div>

                <!-- Right Side (Image Upload with Preview) -->
                <div class="col-md-6">
                  <!-- Display Current Picture (if any) -->
                  <div class="mb-3">
                    <label for="current-picture" class="form-label"
                      >Current Picture</label
                    >
                    <div v-if="editSite.picture">
                      <img
                        :src="getPictureUrl(editSite.picture)"
                        alt="Current Site Picture"
                        class="img-fluid rounded shadow-sm"
                        style="max-width: 150px; max-height: 150px"
                      />
                    </div>
                    <div v-else>
                      <p>No current picture available.</p>
                    </div>
                  </div>

                  <!-- Upload New Picture -->
                  <div class="mb-3">
                    <label for="picture" class="form-label"
                      >Upload New Picture</label
                    >
                    <input
                      type="file"
                      class="form-control"
                      id="picture"
                      accept="image/*"
                      @change="handlePictureUpload($event, 'edit')"
                    />
                  </div>

                  <!-- Preview of Uploaded Picture -->
                  <div class="mb-3">
                    <strong>Preview:</strong>
                    <div v-if="imagePreview">
                      <img
                        :src="imagePreview"
                        alt="Site Picture Preview"
                        class="img-fluid rounded shadow-sm"
                        style="max-width: 150px; max-height: 150px"
                      />
                    </div>
                    <p v-else>No picture selected</p>
                  </div>
                </div>
              </div>

              <!-- Buttons -->
              <div
                class="d-flex justify-content-end gap-2 mt-3"
                style="padding-top: 15px"
              >
                <button
                  type="submit"
                  class="btn btn-success"
                  style="width: 150px"
                >
                  Save Changes
                </button>
                <button type="button" @click="cancelEdit" class="btn-cancel">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </b-modal>

        <!-- Floor Modal -->
        <b-modal
          v-model="showFloorModal"
          title="Manage Floors"
          hide-footer
          centered
          size="lg"
        >
          <div class="modal-title p-3">
            <h5 class="mb-0">
              <strong>Site Name:</strong> {{ currentSite.name }}
            </h5>
          </div>
          <div class="p-3">
            <!-- Floor Information -->
            <div class="mb-3">
              <strong>Floor Information</strong>
              <p>
                <strong>Total Floors:</strong> {{ currentSite.floors.length }}
              </p>
            </div>

            <!-- Add Floors -->
            <div class="mb-3">
              <h6>Add Floors</h6>
              <div class="d-flex gap-2">
                <input
                  type="number"
                  v-model="newFloorCount"
                  class="form-control"
                  placeholder="Enter number of floors"
                  min="1"
                  max="99"
                />
                <button @click="addFloors" class="btn btn-primary">
                  Add Floors
                </button>
              </div>
              <small class="text-muted">
                Enter the number of floors to add (Max 99).
              </small>
            </div>

            <!-- Existing Floors -->
            <div class="mb-3">
              <h6>Existing Floors</h6>
              <div v-if="currentSite.floors.length">
                <table class="table">
                  <thead>
                    <tr>
                      <th>Floor Number</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="floor in currentSite.floors"
                      :key="floor.floor_number"
                    >
                      <td>Floor {{ floor.floor_number }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p v-else>No floors available for this site.</p>
            </div>

            <!-- Buttons -->
            <div class="d-flex justify-content-end gap-2">
              <button @click="closeFloorModal" class="btn btn-secondary">
                Close
              </button>
              <button @click="saveSite" class="btn btn-primary">
                Save Floors
              </button>
            </div>
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
      statusOptions: [],
      newSite: {
        name: "",
        status: "",
        region: "",
        province: "",
        municipality: "",
        barangay: "",
        description: "",
        picture: "",
        number_of_floors: 0, // Set number of floors here
      },
      editSite: {
        id: "",
        name: "",
        status: "",
        region: "",
        province: "",
        municipality: "",
        barangay: "",
        description: "",
        picture: "",
        floors: [], // This would be populated with existing floors
        number_of_floors: 0,
      },
      showFloorModal: false,
      currentSite: {
        id: "",
        name: "",
        status: "",
        region: "",
        province: "",
        municipality: "",
        barangay: "",
        description: "",
        picture: "",
        floors: [], // This would be populated with existing floors
        number_of_floors: 0,
      },
      totalFloors: 0, // Total number of floors for the site
      newFloorNumber: null, // For adding a new floor
      newFloorCount: null,
      sites: [],
      archivedSites: [],
      regionOptions: [], // Stores regions like 'REGION I', 'REGION II', etc.
      provinceOptions: [], // Stores provinces in the selected region
      municipalityOptions: [], // Stores municipalities in the selected province
      barangayOptions: [], // Stores barangays in the selected municipality
      selectedRegion: null, // Selected region from dropdown
      selectedProvince: null, // Selected province from dropdown
      selectedMunicipality: null, // Selected municipality from dropdown
      selectedBarangay: null, // Selected barangay from dropdown
      newPictureFile: null,
      imagePreview: null,
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
      const sitesToFilter = this.showArchived ? this.archivedSites : this.sites;
      return sitesToFilter
        .filter(
          (site) =>
            site.name &&
            site.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        )
        .sort((a, b) =>
          this.sortBy === "name"
            ? (a.name || "").localeCompare(b.name || "")
            : (a.status || "").localeCompare(b.status || "")
        );
    },
  },
  methods: {
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
      this.$store.dispatch("logout");
      this.$router.push({ name: "DevLogin" });
    },
    async fetchSiteDetails() {
      try {
        const response = await axios.get(
          `http://localhost:8000/developer/sites/${this.siteId}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.data.success) {
          this.currentSite = response.data.data; // This should include floors
        }
      } catch (error) {
        console.error("Error fetching site details:", error);
      }
    },
    async fetchSites() {
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
          this.sites = response.data.data.map((site) => ({
            ...site,
            location: this.constructLocation(site), // Dynamically build location
            isArchived: site.isArchived ?? false,
            floors: site.floors || [], // Ensure floors is always an array
          }));
        }
      } catch (error) {
        console.error("Error fetching sites:", error.response || error);
      }
    },
    async fetchArchivedSites() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/sites/archived/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        if (response.status === 200) {
          this.archivedSites = response.data.data.map((site) => ({
            ...site,
            location: this.constructLocation(site), // Build location dynamically
          }));
          console.log("Archived sites fetched:", this.archivedSites);
        }
      } catch (error) {
        if (error.response?.status === 401) {
          const refreshedToken = await this.refreshAccessToken();
          if (refreshedToken) {
            this.fetchArchivedSites(); // Retry fetching archived sites
          }
        } else {
          console.error(
            "Error fetching archived sites:",
            error.response || error
          );
        }
      }
    },
    async archiveSite(site) {
      const siteId = site.id; // Get the site ID
      console.log("Archiving site with ID:", siteId);

      if (confirm("Are you sure you want to archive this site?")) {
        try {
          const response = await axios.put(
            `http://localhost:8000/developer/sites/${siteId}/`, // Correct endpoint for updating the site
            {
              name: site.name, // Pass the existing name or other required fields
              description: site.description,
              region: site.region,
              province: site.province,
              municipality: site.municipality,
              barangay: site.barangay,
              postal_code: site.postal_code,
              picture: site.picture, // If you want to keep the picture
              status: site.status,
              archived: true, // If you need to update the archive status
            },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
              params: { action: "archive" }, // Send action=archive as query parameter
            }
          );

          if (response.status === 200) {
            console.log("Site archived successfully.");
            this.fetchSites();
            this.fetchArchivedSites();
          }
        } catch (error) {
          console.error("Error archiving site:", error.response?.data || error);
        }
      }
    },
    async unarchiveSite(site) {
      const siteId = site.id; // Get the site ID
      console.log("Unarchiving site with ID:", siteId);

      if (confirm("Are you sure you want to unarchive this site?")) {
        try {
          const response = await axios.put(
            `http://localhost:8000/developer/sites/${siteId}/`, // Correct endpoint for updating the site
            {
              name: site.name, // Pass the existing name or other required fields
              description: site.description,
              region: site.region,
              province: site.province,
              municipality: site.municipality,
              barangay: site.barangay,
              postal_code: site.postal_code,
              picture: site.picture, // If you want to keep the picture
              status: site.status,
              archived: false, // Update the archived status to false (unarchive)
            },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
              params: { action: "unarchive" }, // Send action=unarchive as query parameter
            }
          );

          if (response.status === 200) {
            console.log("Site unarchived successfully.");
            this.fetchSites(); // Refresh the site list
            this.fetchArchivedSites(); // Refresh the archived site list
          }
        } catch (error) {
          console.error(
            "Error unarchiving site:",
            error.response?.data || error
          );
        }
      }
    },
    toggleArchived() {
      this.showArchived = !this.showArchived;
      console.log("Toggled archived view:", this.showArchived);

      if (this.showArchived && this.archivedSites.length === 0) {
        // Fetch archived sites only when switching to archived view
        this.fetchArchivedSites();
      }
    },
    toggleView() {
      this.viewMode = this.viewMode === "grid" ? "table" : "grid";
    },
    constructLocation(site) {
      const addressParts = [
        site.region,
        site.province,
        site.municipality,
        site.barangay,
        site.postal_code ? `Postal Code: ${site.postal_code}` : null,
      ];
      return addressParts.filter(Boolean).join(", "); // Join non-empty parts
    },
    async loadRegionData() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/sites/locations/"
        );
        console.log("Region Data fetched:", response.data);
        this.regionData = response.data; // Store region data for further processing

        // Sort region options: non-numeric values at the top, followed by numeric ones in ascending order
        this.regionOptions = Object.keys(this.regionData).sort((a, b) => {
          // Check if the keys are numeric
          const isANumeric = !isNaN(parseInt(a));
          const isBNumeric = !isNaN(parseInt(b));

          // If both are numeric or both are non-numeric, sort numerically or lexicographically
          if (isANumeric && isBNumeric) {
            return parseInt(a) - parseInt(b); // Numeric sorting
          } else if (!isANumeric && !isBNumeric) {
            return a.localeCompare(b); // Non-numeric sorting (lexicographically)
          } else {
            // If one is numeric and the other is non-numeric, non-numeric goes first
            return isANumeric ? 1 : -1;
          }
        });
      } catch (error) {
        console.error("Error loading region data:", error);
      }
    },

    loadProvinceData(regionCode) {
      if (!regionCode) {
        console.error("No region selected.");
        return;
      }

      const region = this.regionData[regionCode]; // Get the region using selectedRegion
      if (region) {
        this.provinceOptions = Object.keys(region.province_list); // Map available provinces from province_list

        // Set the region to newSite
        this.newSite.region = regionCode;

        // Clear previous municipality and barangay options
        this.municipalityOptions = [];
        this.barangayOptions = [];
        this.newSite.province = ""; // Reset province in newSite
        this.newSite.municipality = ""; // Reset municipality in newSite
        this.newSite.barangay = ""; // Reset barangay in newSite
      } else {
        console.error("Invalid region selected.");
      }
    },

    loadMunicipalityData(provinceName) {
      if (!this.newSite.region) {
        console.error("No region selected.");
        return;
      }
      if (!provinceName) {
        console.error("No province selected.");
        return;
      }

      const region = this.regionData[this.newSite.region]; // Get the region using newSite.region
      if (region) {
        const province = region.province_list[provinceName]; // Get the province using provinceName
        if (province) {
          this.municipalityOptions = Object.keys(province.municipality_list); // Map available municipalities from municipality_list

          // Set the province to newSite
          this.newSite.province = provinceName;

          // Clear barangay options when a new province is selected
          this.barangayOptions = [];
          this.newSite.municipality = ""; // Reset municipality in newSite
          this.newSite.barangay = ""; // Reset barangay in newSite
        } else {
          this.municipalityOptions = []; // Clear if no province found
          this.barangayOptions = []; // Clear barangay options if no province is found
        }
      }
    },

    loadBarangayData(municipalityName) {
      if (!municipalityName) {
        console.error("No municipality selected.");
        return;
      }

      const region = this.regionData[this.newSite.region]; // Get the region using newSite.region
      if (region) {
        const province = region.province_list[this.newSite.province]; // Get the province using newSite.province
        if (province) {
          const municipality = province.municipality_list[municipalityName]; // Get municipality using municipalityName
          if (municipality) {
            this.barangayOptions = municipality.barangay_list || []; // Map available barangays from barangay_list

            // Set the municipality to newSite
            this.newSite.municipality = municipalityName;
          }
        }
      }
    },
    handlePictureUpload(event, mode) {
      const file = event.target.files[0];
      if (file) {
        // Set the image preview to the file's URL for preview
        this.imagePreview = URL.createObjectURL(file);

        // Only update the current image if you want to save it
        if (mode === "edit") {
          // Don't overwrite the current picture unless you're saving the change
          this.newPictureFile = file; // Update for edit mode only when confirmed
        } else if (mode === "add") {
          this.newSite.picture = file; // Set for add mode
        }
      } else {
        this.imagePreview = null; // Clear preview if no file is selected
      }
    },
    // Function to get the picture URL (for the current image)
    getPictureUrl(picture) {
      return `http://localhost:8000${picture}`; // Adjust the URL path as needed
    },
    // Open the modal to manage floors for the current site
    openFloorModal(site) {
      this.currentSite = site; // Set the current site to the selected site
      this.showFloorModal = true;
    },
    // Close the modal
    closeFloorModal() {
      this.showFloorModal = false;
    },
    addFloors() {
      if (!this.newFloorCount || this.newFloorCount < 1) {
        alert("Please enter a valid number of floors.");
        return;
      }

      const currentFloorCount = this.currentSite.floors.length;
      const totalFloors = currentFloorCount + this.newFloorCount;

      if (totalFloors > 99) {
        alert("Cannot add more than 99 floors in total.");
        return;
      }

      const newFloors = [];
      const currentMaxFloor =
        currentFloorCount > 0
          ? Math.max(
              ...this.currentSite.floors.map((floor) => floor.floor_number)
            )
          : 0;

      for (let i = 1; i <= this.newFloorCount; i++) {
        newFloors.push({
          floor_number: currentMaxFloor + i,
        });
      }

      // Push the new floors into the current site
      this.currentSite.floors.push(...newFloors);

      // Update the number_of_floors with the total number of floors
      this.currentSite.number_of_floors = this.currentSite.floors.length;

      this.newFloorCount = 0; // Reset the floor count input
    },

    async saveSite() {
      const formData = new FormData();
      formData.append("companyId", this.vuexCompanyId);
      formData.append("name", this.currentSite.name);
      formData.append("description", this.currentSite.description || "");
      formData.append("region", this.currentSite.region);
      formData.append("province", this.currentSite.province);
      formData.append("municipality", this.currentSite.municipality);
      formData.append("barangay", this.currentSite.barangay);
      formData.append("status", this.currentSite.status);

      // Debugging - log the company and floor data
      console.log("Company ID being sent:", this.vuexCompanyId);
      console.log("Floor data being sent:", this.currentSite.number_of_floors);

      if (this.currentSite.floors && this.currentSite.floors.length > 0) {
        this.currentSite.floors.forEach((floor) => {
          formData.append("floors[]", JSON.stringify(floor)); // Sending as simple objects in array
        });
      }

      // Append the floors to the formData
      if (this.currentSite.floors && this.currentSite.floors.length > 0) {
        this.currentSite.floors.forEach((floor, index) => {
          formData.append(
            `floors[${index}][floorNumber]`,
            floor.floor_number || "" // Correcting the key to match the property in floors
          );
        });
      }

      try {
        const response = await axios.put(
          `http://localhost:8000/developer/sites/${this.currentSite.id}/`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.status === 200) {
          this.showFloorModal = false;
          this.fetchSites();
          console.log("Site updated successfully!");
        }
      } catch (error) {
        console.error("Error saving site:", error.response || error);
        // Display generic error message in case of failure
        alert("Failed to save site. Please try again.");
      }
    },
    // Save the new site including floor details
    async addSite() {
      const formData = new FormData();
      formData.append("companyId", this.vuexCompanyId);
      formData.append("name", this.newSite.name);
      formData.append("description", this.newSite.description || "");
      formData.append("region", this.newSite.region);
      formData.append("province", this.newSite.province);
      formData.append("municipality", this.newSite.municipality);
      formData.append("barangay", this.newSite.barangay);
      formData.append("status", this.newSite.status);
      formData.append("number_of_floors", this.newSite.number_of_floors);

      // Append the floors to the formData
      if (this.newSite.floors && this.newSite.floors.length > 0) {
        this.newSite.floors.forEach((floor, index) => {
          formData.append(
            `floors[${index}][floorNumber]`,
            floor.floorNumber || ""
          );
        });
      }

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
          // Reset form data after adding the site
          this.newSite = {
            name: "",
            status: "",
            region: "",
            province: "",
            municipality: "",
            barangay: "",
            description: "",
            picture: null,
            number_of_floors: 0,
            floors: [], // Ensure floors are cleared
          };
          this.imagePreview = null;
          this.showAddModal = false;
          this.fetchSites();
        }
      } catch (error) {
        console.error("Error adding site:", error.response || error);
        // Provide user feedback
        this.$toast.error("Failed to add site. Please try again.");
      }
    },
    // Save edited site including floor details
    async manageSite() {
      const formData = new FormData();
      formData.append("name", this.editSite.name);
      formData.append("region", this.editSite.region);
      formData.append("province", this.editSite.province);
      formData.append("municipality", this.editSite.municipality);
      formData.append("barangay", this.editSite.barangay);
      formData.append("status", this.editSite.status);
      formData.append("description", this.editSite.description || "");

      if (this.newPictureFile) {
        formData.append("picture", this.newPictureFile);
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
          if (index !== -1) {
            this.sites[index] = response.data;
          }
          this.showEditModal = false;
          this.fetchSites();
        }
      } catch (error) {
        console.error("Error updating site:", error.response || error);
      }
    },
    openEditModal(site) {
      this.editSite = { ...site, floors: site.floors || [] }; // Ensure floors is initialized
      this.showEditModal = true;
    },
    cancelEdit() {
      this.resetPicturePreview();
      this.showEditModal = false;
    },
    resetPicturePreview() {
      this.newPictureFile = null;
      this.imagePreview = null;
    },
    async fetchStatusOptions() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/sites/status-options/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.statusOptions = Object.keys(response.data.status_options); // Extract keys (the stored values)
      } catch (error) {
        console.error("Error fetching status options:", error);
      }
    },
  },
  mounted() {
    console.log("Component mounted, fetching sites...");
    this.fetchSites();
    this.loadRegionData();
    if (this.showArchived) {
      this.fetchArchivedSites();
    }
  },
  watch: {
    showArchived() {},
  },
  created() {
    this.fetchStatusOptions(); // Fetch the status options when the component is created
  },
};
</script>

<style scoped>
html,
body {
  height: 100%;
  margin: 0; /* Removes default margin */
  padding: 0; /* Removes default padding */
}

/* Ensure .main-page fills the available space */
.main-page {
  display: flex;
  min-height: 100vh; /* Ensures it spans the full viewport height */
  background-color: #ebebeb; /* Gray background */
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
  background-color: #343a40;
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
  border-radius: 3px;
  overflow: hidden;
  background-color: #f6f6f6;
}

.view-icon {
  flex: 1;
  padding: 6px;
  text-align: center;
  cursor: pointer;
  font-size: 15px;
  color: #343a40;
  transition: background-color 0.3s, color 0.3s;
}

.view-icon.active {
  background-color: #343a40;
  color: #f6f6f6;
}

.separator {
  width: 1px;
  background-color: #f6f6f6;
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
  padding: 16px;
  text-align: center;
  cursor: pointer;
  /* transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; */
}

.site-card:hover {
  transform: translateY(-2px);
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
  padding: 0px 18px;
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
  color: #6c757d;
  /* Adjust the value to your preferred size */
}

.btn-add {
  background-color: #42b983; /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px; /* Adjust the border radius */
  padding: 10px;
}

.btn-cancel {
  background-color: #343a40; /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px; /* Adjust the border radius */
  padding: 10px;
}
</style>
