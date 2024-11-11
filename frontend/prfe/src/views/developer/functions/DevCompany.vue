<template>
  <div class="developer-company-page">
    <SideNav />
    <div class="content">
      <h2>Edit Company</h2>

      <!-- Display user information -->
      <div class="user-info">
        <p><strong>User ID:</strong> {{ userId }}</p>
        <p><strong>User Role:</strong> {{ userType }}</p>
        <p><strong>Company ID:</strong> {{ companyId }}</p>
      </div>

      <!-- Debug: Display company data -->
      <div class="company-data">
        <h3>Company Data (Debug)</h3>
        <pre>{{ company }}</pre>
      </div>

      <form @submit.prevent="updateCompany">
        <div>
          <label for="description">Description:</label>
          <textarea v-model="company.description"></textarea>
        </div>
        <div>
          <label for="logo">Logo:</label>
          <input type="file" @change="onFileChange" />
          <img
            v-if="company.logo"
            :src="company.logo"
            alt="Company Logo"
            width="100"
          />
        </div>
        <button type="submit">Save Changes</button>
      </form>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import axios from "axios";
import { mapState } from "vuex";

export default {
  name: "DevCompany",
  components: { SideNav },
  data() {
    return {
      company: {}, // Holds company data
      newLogo: null, // Stores the new logo file
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId,
      userType: (state) => state.userType, // Corrected from userRole to userType
      companyId: (state) => state.companyId,
    }),
  },
  mounted() {
    console.log("Company ID from Vuex store:", this.companyId); // Debugging line
    this.fetchCompany();
  },

  methods: {
    async fetchCompany() {
      try {
        const token = localStorage.getItem("authToken");
        console.log("Using company ID:", this.companyId); // Debugging line
        const response = await axios.get(`/developer/company/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        this.company = response.data;
      } catch (error) {
        console.error("Error fetching company data:", error);
      }
    },
    onFileChange(event) {
      this.newLogo = event.target.files[0];
    },
    async updateCompany() {
      console.log("Attempting to update company..."); // Add this line
      try {
        const formData = new FormData();
        formData.append("description", this.company.description);
        if (this.newLogo) {
          formData.append("logo", this.newLogo);
        }
        const token = localStorage.getItem("authToken");
        const response = await axios.put(`/developer/company/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`,
          },
        });
        console.log("Update response:", response); // Log the response
        alert("Company updated successfully!");
      } catch (error) {
        console.error("Error updating company:", error);
      }
    },
  },
};
</script>

<style scoped>
.developer-company-page {
  display: flex;
}
.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}
.user-info {
  margin-bottom: 20px;
  text-align: left;
}
</style>
