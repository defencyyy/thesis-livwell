<template>
  <div class="developer-company-page">
    <SideNav />
    <div class="content">
      <h1>Edit Company</h1>
      <p>Description: {{ company.description }}</p>
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
  components: {
    SideNav,
  },
  data() {
    return {
      company: {},
      newLogo: null, // To hold the new logo file
    };
  },
  mounted() {
    const token = localStorage.getItem("token"); // Adjust this to where you store your token
    fetch("http://localhost:8000/api/companies/1/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`, // or 'Bearer ' if you're using Bearer tokens
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        this.company = data;
      })
      .catch((error) => {
        console.error("Error fetching company:", error);
      });
  },
  methods: {
    onFileChange(event) {
      // Handle file input change
      this.newLogo = event.target.files[0];
    },
    updateCompany() {
      const formData = new FormData();
      formData.append("description", this.company.description); // Assume you want to update description
      if (this.newLogo) {
        formData.append("logo", this.newLogo); // Append new logo if provided
      }

      // Make a PUT request to update the company
      fetch(`http://localhost:8000/api/companies/1/`, {
        method: "PUT",
        body: formData,
        headers: {
          // You may need to set the content type to application/json depending on your backend setup
          Accept: "application/json",
          // 'Content-Type': 'application/json' // Uncomment if sending JSON; remove if sending FormData
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          console.log("Company updated:", data);
          // Optionally, redirect or show success message
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
