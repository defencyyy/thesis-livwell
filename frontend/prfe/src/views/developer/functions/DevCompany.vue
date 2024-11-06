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
import { jwtDecode } from "jwt-decode"; // Use named import for jwtDecode

// Function to check if the token is valid
function checkTokenValidity() {
  const token = localStorage.getItem("authToken");

  if (!token) {
    console.error("No token found!");
    return false;
  }

  try {
    const decoded = jwtDecode(token); // Use jwtDecode here
    const currentTime = Date.now() / 1000; // Current time in seconds

    if (decoded.exp < currentTime) {
      console.error("Token has expired!");
      return false;
    } else {
      console.log("Token is valid");
      return true;
    }
  } catch (error) {
    console.error("Invalid token", error);
    return false;
  }
}

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
    const isValidToken = checkTokenValidity();
    if (isValidToken) {
      this.fetchCompany();
    } else {
      alert("Your session has expired. Please log in again.");
      this.$router.push({ name: "login" }); // Redirect to login page
    }
  },
  methods: {
    async fetchCompany() {
      const token = localStorage.getItem("authToken");
      try {
        const response = await fetch(
          "http://localhost:8000/developer/company/",
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        const data = await response.json();
        if (response.ok) {
          this.company = data; // Update company data if the response is successful
        } else {
          console.error("Error fetching company data:", data);
          if (data.detail === "Authentication credentials were not provided.") {
            alert("Session expired. Please log in again.");
            this.$router.push({ name: "login" });
          }
        }
      } catch (error) {
        console.error("Error fetching company data:", error);
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
        const token = localStorage.getItem("authToken");
        const response = await axios.put(
          `http://localhost:8000/developer/company/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: `Bearer ${token}`,
            },
          }
        );
        console.log("Update response:", response);
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
