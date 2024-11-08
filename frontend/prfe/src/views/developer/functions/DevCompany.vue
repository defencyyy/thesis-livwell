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
      userType: (state) => state.userType,
      companyId: (state) => state.companyId,
    }),
  },
  mounted() {
    this.fetchCompany(); // Fetch the company data immediately without token check
  },
  methods: {
    async fetchCompany() {
      const userId = localStorage.getItem("user_id");
      const companyId = localStorage.getItem("company_id");

      if (!userId || !companyId) {
        alert("Developer or Company ID not found. Please log in.");
        this.$router.push({ name: "DevLogin" });
        return;
      }

      try {
        console.log(userId);
        console.log(companyId);
        const response = await axios.get(
          "http://localhost:8000/developer/company/",
          {
            headers: {
              "Developer-ID": userId, // Pass the developer ID in the headers
              "Company-ID": companyId, // Pass the company ID in the headers
              "Content-Type": "application/json",
            },
          }
        );

        if (response.status === 200) {
          this.company = response.data;
        } else {
          alert("Error fetching company data.");
        }
      } catch (error) {
        console.error("Error fetching company data:", error);
        alert("Error fetching company data.");
      }
    },
    onFileChange(event) {
      this.newLogo = event.target.files[0];
    },

    async updateCompany() {
      console.log("Attempting to update company...");
      try {
        const formData = new FormData();
        formData.append("description", this.company.description);
        if (this.newLogo) {
          formData.append("logo", this.newLogo);
        }

        const response = await axios.put(
          `http://localhost:8000/developer/company/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              "Developer-ID": this.userId, // Include developer ID
              "Company-ID": this.companyId, // Include company ID
            },
          }
        );

        console.log("Update response:", response);
        alert("Company updated successfully!");
      } catch (error) {
        console.error("Error updating company:", error);
        alert("Error updating company. Please try again.");
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
