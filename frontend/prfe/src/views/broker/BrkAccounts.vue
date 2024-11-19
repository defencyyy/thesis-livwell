<template>
  <header>
    <HeaderLivwell />
  </header>

  <SideNav />
 
  <div class="accounts-page">
    
    <div class="content row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <div class="card mt-5">
          <div class="card-header text-center">
            <h1>Welcome to Account</h1>
            <p>Here you can manage your account</p>
          </div>
          <div class="card-body">
            <form @submit.prevent="updateAccount">
              <div class="form-group">
                <label for="username">Username:</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="username"
                  id="username"
                />
              </div>

              <div class="form-group">
                <label for="email">Email:</label>
                <input
                  type="email"
                  class="form-control"
                  v-model="email"
                  id="email"
                />
              </div>

              <div class="form-group">
                <label for="contactNumber">Contact Number:</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="contactNumber"
                  id="contactNumber"
                />
              </div>

              <div class="form-group">
                <label for="password">Password:</label>
                <input
                  type="password"
                  class="form-control"
                  v-model="password"
                  id="password"
                />
              </div>
              <button type="submit" class="btn btn-primary btn-block">
                Update Account
              </button>
            </form>

            <p v-if="error" class="text-danger">{{ error }}</p>
            <p v-if="successMessage">{{ successMessage }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import HeaderLivwell from "@/components/HeaderLivwell.vue";

export default {
  name: "BrkAccounts",
  components: {
    SideNav,
    HeaderLivwell,
  },
  data() {
    return {
      username: "",
      email: "",
      contactNumber: "",
      password: "",
      error: null,
      successMessage: null,
    };
  },

  methods: {
    async updateAccount() {
      // Validate password on client-side
      if (this.password) {
        if (this.password.length < 8) {
          this.error = "Password must be at least 8 characters long.";
          this.successMessage = null;
          return;
        }
        if (!/[A-Z]/.test(this.password)) {
          this.error = "Password must contain at least one uppercase letter.";
          this.successMessage = null;
          return;
        }
        if (!/[a-z]/.test(this.password)) {
          this.error = "Password must contain at least one lowercase letter.";
          this.successMessage = null;
          return;
        }
        if (!/\d/.test(this.password)) {
          this.error = "Password must contain at least one number.";
          this.successMessage = null;
          return;
        }
        if (!/[!@#$%^&*(),.?":{}|<>]/.test(this.password)) {
          this.error = "Password must contain at least one special character.";
          this.successMessage = null;
          return;
        }
      }

      const brokerId = localStorage.getItem("broker_id");
      if (brokerId) {
        try {
          const response = await fetch(
            `http://localhost:8000/broker/manage-account/${brokerId}/`,
            {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("authToken")}`,
              },
              body: JSON.stringify({
                username: this.username || undefined,
                email: this.email || undefined,
                contact_number: this.contactNumber || undefined,
                password: this.password || undefined,
              }),
            }
          );

          if (!response.ok) {
            const errorData = await response.json();
            this.error = errorData.message || "Failed to update account.";
            this.successMessage = null;
            return;
          }

          const data = await response.json();
          if (data.success) {
            this.successMessage = "Account updated successfully!";
            this.error = null;
          } else {
            this.error = data.message || "Failed to update account.";
            this.successMessage = null;
          }
        } catch (error) {
          console.error("Error updating account:", error);
          this.error = "An error occurred while updating your account.";
          this.successMessage = null;
        }
      } else {
        this.error = "No broker ID found in localStorage.";
      }
    },
  },
};
</script>

<style scoped>
/* .content {
 
  text-align: center;
  display: flex;
}

.accounts-page {
  display: flex;
}

.sidebar {
  width: 250px;
  transition: width 0.5s;
  background-color: gray;
  height: 96%;
}

 */


/* Ensure the whole page content is centered */
/* Center the account page horizontally, but push content higher */
.accounts-page {
  display: flex;
  justify-content: center; /* Center horizontally */
  align-items: flex-start; /* Align to the top of the page */
  min-height: 80vh;
  padding: 20px;
  padding-top: 50px; /* Optional: add space from the top of the screen */
}

/* Adjust the content inside the account page */
.content {
  display: flex;
  justify-content: center;
  padding-left: 10%;
  width: 100%;
}

/* Modify the card width to make it wider */
.card {
  width: 100%;
  max-width: 700px; /* Set maximum width for the card */
  min-height: 500px; /* Set a minimum height to make it longer */
  border-radius: 8px; /* Optional: Add rounded corners to the card */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Add shadow to the card */
  background-color: white; /* Ensure the background is white */
}



/* Add padding inside the card */
.card-body {
  padding: 30px; /* More padding to make the form appear longer */
}

/* Space above the button */
button[type="submit"] {
  margin-top: 20px; /* Adds space between the form fields and the button */
}

/* Additional spacing for form fields */
.form-group {
  margin-bottom: 20px; /* Adds space between each form input */
}

/* Optional: Add responsiveness for smaller screens */
@media (max-width: 768px) {
  .card {
    max-width: 90%; /* On smaller screens, make the card take more width */
  }

  .card-body {
    padding: 20px; /* Adjust padding on smaller screens */
  }
}

</style>
