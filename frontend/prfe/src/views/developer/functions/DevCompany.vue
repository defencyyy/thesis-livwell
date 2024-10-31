<template>
  <div class="developer-company-page">
    <SideNav />
    <div class="content">
      <h1>Edit Company</h1>
      <textarea
        v-model="company.description"
        placeholder="Enter description"
      ></textarea>
      <img :src="company.logo" alt="Company Logo" v-if="company.logo" />
      <input type="file" @change="onFileChange" />
      <button @click="updateCompany">Update Company</button>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";

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
    fetchCompany() {
      const token = localStorage.getItem("authToken");

      fetch("http://localhost:8000/api/companies/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
      })
        .then((response) => {
          if (!response.ok) throw new Error("Failed to fetch company data");
          return response.json();
        })
        .then((data) => {
          if (data.length === 0) throw new Error("No company found"); // Handle empty response
          this.company = data[0]; // Assume the first company is the developer's
        })
        .catch((error) => {
          console.error("Error fetching company:", error);
        });
    },

    updateCompany() {
      const formData = new FormData();
      formData.append("description", this.company.description);
      if (this.newLogo) {
        formData.append("logo", this.newLogo);
      }

      const token = localStorage.getItem("authToken");

      fetch(`http://localhost:8000/api/companies/${this.company.id}/`, {
        // Use dynamic ID
        method: "PUT",
        body: formData,
        headers: {
          Accept: "application/json", // Allow FormData
          Authorization: `Token ${token}`,
        },
      })
        .then((response) => {
          if (!response.ok) throw new Error("Failed to update company");
          return response.json();
        })
        .then((data) => {
          console.log("Company updated:", data);
          this.company = data; // Refresh the company data
        })
        .catch((error) => {
          console.error("Error updating company:", error);
        });
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
