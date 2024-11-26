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
          class="card shadow-lg border-0 rounded-3 mx-auto"
          style="max-width: 1100px"
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

                  <!-- Filter Button -->
                  <button
                    @click="toggleArchived"
                    :class="['btn-secondary', { active: showArchived }]"
                    class="filter-button"
                  >
                    {{ showArchived ? "View Archived" : "View Active" }}
                  </button>
                </div>

                <div class="right-section">
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
            @click="viewSite(site)"
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
            class="card shadow-lg border-0 rounded-3 mx-auto"
            style="max-width: 1100px"
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
                      <!-- View Button as Icon (Yellow) -->
                      <button
                        @click.stop="viewSite(site)"
                        style="
                          border: none;
                          background-color: transparent;
                          cursor: pointer;
                          padding: 8px;
                          font-size: 18px;
                        "
                      >
                        <i class="fas fa-eye" style="color: black"></i>
                        <!-- GINAWA KO GANTO PUTI SAKIN - Cy -->
                      </button>

                      <!-- Edit Button as Icon (Blue) -->
                      <button
                        @click.stop="openEditModal(site)"
                        style="
                          border: none;
                          background-color: transparent;
                          cursor: pointer;
                          padding: 8px;
                          font-size: 18px;
                        "
                      >
                        <i class="fas fa-edit" style="color: black"></i>
                        <!-- GINAWA KO GANTO PUTI SAKIN - Cy -->
                      </button>

                      <!-- Delete Button as Icon (Red) -->
                      <button
                        @click.stop="deleteSite(site)"
                        style="
                          border: none;
                          background-color: transparent;
                          cursor: pointer;
                          padding: 8px;
                          font-size: 18px;
                        "
                      >
                        <i class="fas fa-trash" style="color: black"></i>
                        <!-- GINAWA KO GANTO PUTI SAKIN - Cy -->
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <b-modal v-model="showAddModal" hide-header hide-footer size="lg">
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

              <!-- Buttons -->
              <div class="d-flex justify-content-end gap-2 mt-3">
                <button
                  type="submit"
                  class="btn btn-primary"
                  style="width: 150px"
                >
                  Add New Site
                </button>
                <button
                  type="button"
                  @click="showAddModal = false"
                  class="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </b-modal>

        <b-modal
          v-model="showEditModal"
          title="Edit Site"
          hide-header
          hide-footer
          size="lg"
        >
          <div class="modal-title p-3">
            <h5 class="mb-0">Edit Site</h5>
          </div>
          <div class="p-3">
            <form @submit.prevent="manageSite">
              <div class="row">
                <!-- Left Side (Site Name to Status) -->
                <div class="col-md-6">
                  <!-- Site Name -->
                  <div class="form-group mb-3">
                    <label for="editSiteName" class="form-label"
                      >Site Name</label
                    >
                    <input
                      type="text"
                      v-model="editSite.name"
                      id="editSiteName"
                      class="form-control"
                      required
                    />
                  </div>

                  <!-- Location -->
                  <div class="row mb-3">
                    <!-- Region Dropdown -->
                    <div class="col-md-6">
                      <label for="editRegion" class="form-label">Region</label>
                      <select
                        v-model="editSite.region"
                        id="editRegion"
                        class="form-select"
                        @change="loadProvinceData(editSite.region)"
                        required
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
                      <label for="editProvince" class="form-label"
                        >Province</label
                      >
                      <select
                        v-model="editSite.province"
                        id="editProvince"
                        class="form-select"
                        @change="loadMunicipalityData(editSite.province)"
                        required
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
                    <label for="editMunicipality" class="form-label"
                      >Municipality</label
                    >
                    <select
                      v-model="editSite.municipality"
                      id="editMunicipality"
                      class="form-select"
                      @change="loadBarangayData(editSite.municipality)"
                      required
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

                  <!-- Barangay -->
                  <div class="form-group mb-3">
                    <label for="editBarangay" class="form-label"
                      >Barangay</label
                    >
                    <select
                      v-model="editSite.barangay"
                      id="editBarangay"
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
                      <label for="editPostalCode" class="form-label"
                        >Postal Code</label
                      >
                      <input
                        type="text"
                        v-model="editSite.postalCode"
                        id="editPostalCode"
                        class="form-control"
                      />
                    </div>

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

                <!-- Right Side (Photo Upload with Preview) -->
                <div class="col-md-6">
                  <!-- Image Upload Section -->
                  <div class="form-group mb-3">
                    <label for="editSitePicture" class="form-label"
                      >Upload Photo</label
                    >
                    <input
                      type="file"
                      @change="handlePictureUpload"
                      id="editSitePicture"
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

              <!-- Buttons -->
              <div class="d-flex justify-content-end gap-2 mt-3">
                <button
                  type="submit"
                  class="btn btn-success"
                  style="width: 150px"
                >
                  Save Changes
                </button>
                <button
                  type="button"
                  @click="showEditModal = false"
                  class="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </b-modal>

        <b-modal
          v-model="selectedSiteModal"
          title="Site Details"
          hide-header
          hide-footer
          size="lg"
        >
          <div class="modal-title p-3">
            <h5 class="mb-0">Site Details</h5>
          </div>
          <div class="p-3">
            <div class="row">
              <!-- Left Side (Text Details) -->
              <div class="col-md-6">
                <!-- Site Name -->
                <div class="form-group mb-3">
                  <label for="siteName" class="form-label">Site Name:</label>
                  <p>{{ selectedSite.name }}</p>
                </div>

                <!-- Location -->
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="region" class="form-label">Region:</label>
                    <p>{{ selectedSite.region }}</p>
                  </div>
                  <div class="col-md-6">
                    <label for="province" class="form-label">Province:</label>
                    <p>{{ selectedSite.province }}</p>
                  </div>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="municipality" class="form-label"
                      >Municipality:</label
                    >
                    <p>{{ selectedSite.municipality }}</p>
                  </div>
                  <div class="col-md-6">
                    <label for="postalCode" class="form-label"
                      >Postal Code:</label
                    >
                    <p>{{ selectedSite.postalCode }}</p>
                  </div>
                </div>

                <div class="form-group mb-3">
                  <label for="barangay" class="form-label">Barangay:</label>
                  <p>{{ selectedSite.barangay }}</p>
                </div>

                <!-- Status -->
                <div class="form-group mb-3">
                  <label for="siteStatus" class="form-label">Status:</label>
                  <p>{{ selectedSite.status }}</p>
                </div>
              </div>

              <!-- Right Side (Image Preview) -->
              <div class="col-md-6">
                <!-- Image Preview Section -->
                <div class="text-center">
                  <h6>Site Photo</h6>
                  <img
                    :src="selectedSite.picture || '/default-image-large.jpg'"
                    alt="Site Picture"
                    class="img-fluid"
                    style="max-height: 200px; object-fit: cover"
                  />
                </div>
              </div>
            </div>

            <!-- Close Button -->
            <div class="d-flex justify-content-end gap-3 mt-3">
              <button
                type="button"
                @click="selectedSiteModal = false"
                class="btn btn-secondary"
              >
                Close
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
        region: "", // Region selection
        province: "", // Province selection
        municipality: "", // municipality selection
        barangay: "", // Barangay selection
        description: "",
        picture: "",
      },
      editSite: {},
      sites: [],
      regionOptions: [], // Stores regions like 'REGION I', 'REGION II', etc.
      provinceOptions: [], // Stores provinces in the selected region
      municipalityOptions: [], // Stores municipalities in the selected province
      barangayOptions: [], // Stores barangays in the selected municipality
      selectedRegion: null, // Selected region from dropdown
      selectedProvince: null, // Selected province from dropdown
      selectedMunicipality: null, // Selected municipality from dropdown
      selectedBarangay: null, // Selected barangay from dropdown
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
      return this.sites
        .filter(
          (site) =>
            site &&
            site.name &&
            site.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        )
        .filter((site) => this.showArchived || !site.isArchived)
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
        console.log("Sites fetched:", response.data); // Debug API response
        if (response.status === 200) {
          this.sites = response.data.data.map((site) => ({
            ...site,
            location: this.constructLocation(site), // Dynamically build location
            isArchived: site.isArchived ?? false,
          }));
          console.log("Processed Sites:", this.sites); // Debug processed sites
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
    toggleView() {
      this.viewMode = this.viewMode === "grid" ? "table" : "grid";
    },
    toggleArchived() {
      this.showArchived = !this.showArchived;
      console.log("Show archived:", this.showArchived);
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
        // Set the imagePreview to the file's URL
        this.imagePreview = URL.createObjectURL(file);

        // Continue with your logic to handle the file...
        if (mode === "add") {
          this.newSite.picture = file;
        } else if (mode === "edit") {
          this.editSite.picture = file;
        }
      }
    },
    async addSite() {
      const formData = new FormData();
      formData.append("companyId", this.vuexCompanyId);
      formData.append("name", this.newSite.name);
      formData.append("description", this.newSite.description || ""); // Optional description field
      formData.append("region", this.newSite.region);
      formData.append("province", this.newSite.province);
      formData.append("municipality", this.newSite.municipality);
      formData.append("barangay", this.newSite.barangay);
      formData.append("status", this.newSite.status);

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
          // Clear form and modal
          this.newSite = {
            name: "",
            region: "",
            province: "",
            municipality: "",
            barangay: "",
            status: "",
            description: "",
            picture: "",
          };
          this.showAddModal = false;

          // Re-fetch the sites
          this.fetchSites();
        }
      } catch (error) {
        console.error("Error adding site:", error.response || error);
      }
    },
    async manageSite() {
      // Create FormData and log it
      const formData = new FormData();
      formData.append("name", this.editSite.name);
      formData.append("region", this.editSite.region); // Sending region
      formData.append("province", this.editSite.province); // Sending province
      formData.append("municipality", this.editSite.municipality); // Sending municipality
      formData.append("barangay", this.editSite.barangay); // Sending barangay
      formData.append("status", this.editSite.status);
      formData.append("description", this.editSite.description || ""); // Optional description field

      // Check if picture is being added
      if (this.editSite.picture) {
        console.log("Picture being uploaded:", this.editSite.picture);
        formData.append("picture", this.editSite.picture);
      }

      // Log the FormData contents (for debugging purposes)
      for (let pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
      }

      try {
        const token = localStorage.getItem("accessToken");
        if (!token) {
          console.error("No token found. Cannot proceed with the request.");
          return;
        }
        console.log("Using Authorization token:", token); // Log the token (be cautious in production)

        const response = await axios.put(
          `http://localhost:8000/developer/sites/${this.editSite.id}/`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        // Log the response from the API
        console.log("API Response:", response);

        if (response.status === 200) {
          const index = this.sites.findIndex(
            (site) => site.id === this.editSite.id
          );
          if (index !== -1) {
            // Update the site in the list with the new data from the response
            this.sites[index] = response.data;
          }
          this.showEditModal = false;
          this.fetchSites();
        }
      } catch (error) {
        console.error("Error saving site:", error.response || error);
      }
    },
    async archiveSite(site) {
      try {
        console.log("Archiving site:", site);

        const response = await axios.put(
          `http://localhost:8000/developer/sites/${site.id}/`,
          { ...site, isArchived: true },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        if (response.status === 200) {
          // Update sites array
          this.sites = this.sites.map((s) =>
            s.id === site.id ? { ...s, isArchived: true } : s
          );
          console.log("Site archived successfully.");
        }
      } catch (error) {
        console.error("Error archiving site:", error.response?.data || error);
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
  /* margin-left: 250px; */
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
