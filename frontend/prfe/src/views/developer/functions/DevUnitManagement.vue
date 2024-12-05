<template>
  <div class="unit-types">
    <!-- Actions -->
    <div class="actions" v-if="!isLoading && !errorMessage">
      <button @click="redirectToUnits">Manage Units</button>
      <button @click="redirectToUnitTemplates">Manage Unit Templates</button>
      <button @click="redirectToUnitTypes">Manage Unit Types</button>
    </div>
    <h1>Unit Types Management</h1>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-else>
      <div class="unit-type-form">
        <h2>Create New Unit Type</h2>
        <form @submit.prevent="createUnitType">
          <div>
            <label for="unitTypeName">Unit Type Name:</label>
            <input
              v-model="newUnitType.name"
              id="unitTypeName"
              type="text"
              placeholder="Enter Unit Type"
              required
            />
          </div>
          <button type="submit">Create Unit Type</button>
        </form>
      </div>

      <div class="unit-types-list">
        <h2>Existing Unit Types</h2>
        <ul>
          <li v-for="unitType in unitTypes" :key="unitType.id">
            {{ unitType.name }}
            <button @click="archiveUnitType(unitType.id)">Archive</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      loading: true,
      unitTypes: [],
      newUnitType: {
        name: "",
      },
    };
  },
  methods: {
    redirectToUnits() {
      this.$router.push({ name: "DevFuncUnits" });
    },

    redirectToUnitTemplates() {
      this.$router.push({ name: "DevUnitTemplates" });
    },

    redirectToUnitTypes() {
      this.$router.push({ name: "DevUnitTypes" });
    },
    // Fetch existing unit types
    fetchUnitTypes() {
      axios
        .get("/api/unit-types/") // Assuming API URL to fetch unit types
        .then((response) => {
          this.unitTypes = response.data.data; // Adjust based on your API response format
          this.loading = false;
        })
        .catch((error) => {
          console.error("Error fetching unit types:", error);
          this.loading = false;
        });
    },

    // Create new unit type
    createUnitType() {
      const data = {
        name: this.newUnitType.name,
        is_custom: true, // Assuming this is for custom unit types
      };

      axios
        .post("/api/unit-types/", data)
        .then((response) => {
          this.unitTypes.push(response.data.data); // Add the new unit type to the list
          this.newUnitType.name = ""; // Clear input
        })
        .catch((error) => {
          console.error("Error creating unit type:", error);
        });
    },

    // Archive a unit type
    archiveUnitType(unitTypeId) {
      axios
        .put(`/api/unit-types/${unitTypeId}/archive/`) // Adjust the API endpoint for archiving
        .then(() => {
          // Update the local list after archiving
          const unitTypeIndex = this.unitTypes.findIndex(
            (type) => type.id === unitTypeId
          );
          if (unitTypeIndex !== -1) {
            this.unitTypes[unitTypeIndex].is_archived = true;
          }
        })
        .catch((error) => {
          console.error("Error archiving unit type:", error);
        });
    },
  },
  created() {
    this.fetchUnitTypes(); // Fetch the unit types when the component is created
  },
};
</script>

<style scoped>
.unit-types {
  padding: 20px;
}

.unit-types-list {
  margin-top: 20px;
}

.unit-type-form {
  margin-bottom: 20px;
}

.loading {
  font-size: 18px;
  color: #888;
}

button {
  margin-left: 10px;
  padding: 5px 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

input {
  padding: 8px;
  font-size: 14px;
  margin-right: 10px;
}
</style>
