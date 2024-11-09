<template>
  <div class="developer-company-page">
    <SideNav />
    <div class="content">
      <h2>Edit Company</h2>
      <div class="user-info">
        <p><strong>User ID:</strong> {{ userId }}</p>
        <p><strong>User Role:</strong> {{ userType }}</p>
        <p><strong>Company ID:</strong> {{ companyId }}</p>
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
  },
  mounted() {
    this.fetchCompany();
  },
  methods: {
    async fetchCompany() {
      if (!this.userId || !this.companyId) {
        alert("Developer or Company ID not found. Please log in.");
        this.$router.push({ name: "DevLogin" });
        return;
      }

      try {
        const response = await axios.get(
          "http://localhost:8000/developer/company/",
          {
            headers: {
              "Developer-ID": this.userId,
              "Company-ID": this.companyId,
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
    getLogoUrl(logoPath) {
      return `http://localhost:8000${logoPath}`;
    },
    onFileChange(event) {
      this.newLogo = event.target.files[0];
    },
    async updateCompany() {
      if (!this.userId || !this.companyId) {
        alert("Developer or Company ID not found. Please log in.");
        this.$router.push({ name: "DevLogin" });
        return;
      }

      this.company.description = this.draftDescription;

      try {
        const formData = new FormData();
        formData.append("description", this.company.description);
        if (this.newLogo) {
          formData.append("logo", this.newLogo);
        }

        const response = await axios.put(
          "http://localhost:8000/developer/company/",
          formData,
          {
            headers: {
              "Developer-ID": this.userId,
              "Company-ID": this.companyId,
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
