=======
<b-modal v-model="showEditModal" title="Edit Site" hide-footer centered>
  <form @submit.prevent="confirmEdit">
    <!-- Site Name -->
    <div class="form-group mb-3">
      <label for="editSiteName" class="form-label">Site Name:</label>
      <input
        type="text"
        v-model="editSite.name"
        id="editSiteName"
        class="form-control"
        required
      />
    </div>

    <!-- Location -->
    <div class="form-group mb-3">
      <label for="editSiteLocation" class="form-label">Location:</label>
      <input
        type="text"
        v-model="editSite.location"
        id="editSiteLocation"
        class="form-control"
        required
      />
    </div>

    <!-- Status -->
    <div class="form-group mb-3">
      <label for="editSiteStatus" class="form-label">Status:</label>
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

    <!-- Picture URL -->
    <div class="form-group mb-3">
      <label for="editSitePicture" class="form-label"
        >Picture URL:</label
      >
      <input
        type="text"
        v-model="editSite.picture"
        id="editSitePicture"
        class="form-control"
      />
    </div>

    <!-- Buttons -->
    <div class="d-flex justify-content-end gap-3">
      <button type="submit" class="btn btn-success">
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
</b-modal>

>>>>>>> origin/frontend_cujardo
