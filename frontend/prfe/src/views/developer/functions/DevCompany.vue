<template>
  <div class="developer-company-page">
    <SideNav /> <!-- Sidebar on the left -->
    <div class="main-content">
      <AppHeader /> <!-- Top bar aligned horizontally, after the sidebar -->
      <div class="container mt-5">
        <!-- Title aligned with the left edge of the card -->
        <div class="title-wrapper">
          <div class="title-icon"></div> 
          <div class="edit-title">Edit Company Details</div>
        </div>
        <div class="card shadow-lg border-0 rounded-3 mx-auto" style="max-width: 900px;">
          <div class="card-body">
            <div class="row">
              <!-- Left Section: Logo Upload with Preview -->
              <div class="col-md-6">
                <div class="mb-3">
                  <label for="description" class="form-label">Description</label>
                  <textarea class="form-control" id="description" v-model="company.description" rows="6"
                    placeholder="Enter company description"></textarea>
                </div>

                <div class="d-flex justify-content-end">
                  <button type="submit" class="btn btn-primary">Save Changes</button>
                </div>
              </div>

              <!-- Right Section: Description and Save Button -->
              <div class="col-md-6 d-flex flex-column align-items-center">
                <div class="mb-3">
                  <label for="logo" class="form-label">Upload Logo</label>
                  <input type="file" class="form-control" id="logo" accept="image/*" @change="onFileChange" />
                </div>
                <div class="mb-3">
                  <!-- Preview Image -->
                  <img v-if="company.logo" :src="company.logo"  alt="Company Logo" width="100" />
                  <p v-else>No logo uploaded</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- <div class="content">
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
      </div> -->
    </div>
  </div>

  <!-- <div class="developer-company-page">
    <SideNav />
    <AppHeader />
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
  </div> -->
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import axios from "axios";

export default {
  name: "DevCompany",
  components: { SideNav, AppHeader },
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
      this.company.logo = URL.createObjectURL(this.newLogo);
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
  height: 100vh;
}

.SideNav {
  width: 250px; /* Set fixed width for the sidebar */
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #343a40;
  z-index: 1;
}

.AppHeader {
  width: 100%;
  height: 60px; /* Adjust height as needed */
  background-color: #343a40;
  display: flex;
  align-items: center;
  padding-left: 10px;
}

.main-content {
  display: flex;
  margin-left: 250px; /* Set margin equal to sidebar width */
  flex-direction: column;
  /* Stack header and content vertically */
  flex: 1;
}

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 2.5rem;
}

.title-wrapper {
  display: flex; /* Align line and title horizontally */
  align-items: center; 
  width: 100%;
  max-width: 900px;
  /* Ensure the title width matches the card's width */
  margin-left: auto;
  margin-right: auto;
  /* Center the wrapper */
}

.edit-title {
  color: #000000;
  margin-bottom: 1rem;
  text-align: left;
  /* Align the text to the left */
  background-color: #fff;
  /* Match background with card */

}

.title-icon {
  width: 15px; /* Short horizontal line */
  height: 5px; /* Thin line */
  background-color: #6c757d; /* Line color */
  border-radius: 5px; /* Rounded corners */
  margin-right: 10px; /* Space between the icon and the title */
  margin-bottom: 15px;
}


/* Styling for the file input and image preview section */
input[type="file"] {
  border: 1px solid #ccc;
  border-radius: 8px;
}

img {
  object-fit: cover;
}

/* Styling for the text area */
textarea {
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
  padding: 10px;
  transition: border-color 0.3s ease;
}

textarea:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* Button Styling */
.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
  font-weight: 600;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}


/* .developer-company-page {
  display: flex;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
} */
</style>
