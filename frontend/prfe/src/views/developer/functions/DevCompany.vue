<template>
  <div class="developer-company-page">
    <SideNav />
    <div class="content">
      <!-- Main Company Details -->
      <h2>Company Details</h2>
      <div class="company-info">
        <p><strong>Company Name:</strong> {{ company.name || "" }}</p>
        <p>
          <strong>Company Description:</strong> {{ company.description || "" }}
        </p>
        <div>
          <strong>Company Logo:</strong>
          <img
            v-if="company.logo"
            :src="getLogoUrl(company.logo)"
            alt="Company Logo"
            width="100"
          />
          <span v-else>No Logo Available</span>
        </div>
      </div>

      <!-- Edit Company Section -->
      <h3>Edit Company</h3>
      <form @submit.prevent="updateCompany">
        <div>
          <label for="description">Description:</label>
          <textarea v-model="draftDescription"></textarea>
        </div>
        <div>
          <label for="logo">Logo:</label>
          <input type="file" @change="onFileChange" />
          <img
            v-if="company.logo"
            :src="getLogoUrl(company.logo)"
            alt="Company Logo"
            width="100"
          />
        </div>
        <button type="submit">Save Changes</button>
      </form>

      <!-- Debugging Information -->
      <h3>Debugging Information</h3>
      <div class="debug-info">
        <p><strong>Vuex User ID:</strong> {{ vuexUserId }}</p>
        <p><strong>Vuex Company ID:</strong> {{ vuexCompanyId }}</p>
        <p><strong>LocalStorage User ID:</strong> {{ localStorageUserId }}</p>
        <p>
          <strong>LocalStorage Company ID:</strong> {{ localStorageCompanyId }}
        </p>
        <p><strong>User Role:</strong> {{ userType }}</p>
      </div>
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
      company: {},
      draftDescription: "",
      newLogo: null,
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
    localStorageUserId() {
      return localStorage.getItem("developer_id");
    },
    localStorageCompanyId() {
      return localStorage.getItem("company_id");
    },
  },
  mounted() {
    this.fetchCompany();
  },
  methods: {
    // Method to fetch company details
    async fetchCompany() {
      const userId = this.userId || localStorage.getItem("developer_id");
      const companyId = this.companyId || localStorage.getItem("company_id");

      if (!userId || !companyId) {
        alert("Developer or Company ID not found. Please log in.");
        this.$router.push({ name: "DevLogin" });
        return;
      }

      try {
        const response = await axios.get(
          "http://localhost:8000/developer/company/",
          {
            headers: {
              "Developer-ID": userId,
              "Company-ID": companyId,
              "Content-Type": "application/json",
            },
          }
        );

        if (response.status === 200) {
          this.company = {
            name: response.data.company_name,
            description: response.data.company_description,
            logo: response.data.company_logo,
          };
          this.draftDescription = this.company.description;
        } else {
          alert("Error fetching company data.");
        }
      } catch (error) {
        console.error("Error fetching company data:", error);
        alert("Error fetching company data.");
      }
    },

    // Method to get logo URL
    getLogoUrl(logoPath) {
      return `http://localhost:8000${logoPath}`;
    },

    // Method to handle logo file change
    onFileChange(event) {
      this.newLogo = event.target.files[0];
    },

    // Method to update company details
    async updateCompany() {
      try {
        const formData = new FormData();
        formData.append("description", this.draftDescription);

        if (this.newLogo) {
          formData.append("logo", this.newLogo);
        }

        const response = await axios.put(
          "http://localhost:8000/developer/company/edit/",
          formData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
              "Developer-ID": localStorage.getItem("developer_id"),
              "Company-ID": localStorage.getItem("company_id"),
            },
          }
        );

        if (response.status === 200) {
          alert("Company updated successfully!");
        } else {
          alert("Error updating company.");
        }
      } catch (error) {
        console.error("Error updating company:", error);
        if (error.response) {
          console.error(error.response.data);
          console.error(error.response.status);
        }
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
