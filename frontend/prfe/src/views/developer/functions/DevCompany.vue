<template>
  <div class="developer-company-page">
    <SideNav />
    <div class="content">
      <h2>Edit Company</h2>
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

export default {
  name: "DevCompany",
  components: { SideNav },
  data() {
    return {
      company: {}, // Holds company data
      newLogo: null, // Stores the new logo file
    };
  },
  mounted() {
    this.fetchCompany();
  },
  methods: {
    async fetchCompany() {
      try {
        const token = localStorage.getItem("authToken");
        const response = await axios.get("/developer/company/", {
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
      try {
        const formData = new FormData();
        formData.append("description", this.company.description);
        if (this.newLogo) {
          formData.append("logo", this.newLogo);
        }

        await axios.put("/developer/company/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

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
</style>
