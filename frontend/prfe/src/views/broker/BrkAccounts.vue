<template>
<div>    
  <AppHeaderLivwell />
  <div class = "broker-account-page">
    <SideNav />
  <div class = "main-content">
    <div class = "content">
      <div class = "title-wrapper">
        <div class = "title-icon"></div>
        <div class = "edit-title">Account Settings</div>
      </div>
      <div class="card shadow-lg border-0 rounded-1 mx-auto" style="max-width: 900px">
        <div class = "card-body">
          <form @submit.prevent="updateAccount">
            <div class = "row">
              <!-- Personal Information Section -->
              <div class = "col-md-6">
                <h5 class="mb-4">Personal Information</h5>
                  <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input
                      type="email"
                      id="email"
                      v-model="email"
                      class="form-control"
                      :placeholder="placeholderEmail"

                    />
                  </div>
                  <div class="mb-3">
                    <label for="contactNumber" class="form-label"
                      >Phone Number</label
                    >
                    <input
                      type="text"
                      id="contactNumber"
                      v-model="contactNumber"
                      class="form-control"
                      :placeholder="placeholderContactNumber"

                    />
                  </div>
                  <div class="mb-3">
                    <label for="username" class="form-label"
                      >Username</label
                    >
                    <input
                      type="text"
                      id="username"
                      v-model="username"
                      class="form-control"
                      :placeholder="placeholderUsername"

                    />
                  </div>
              </div>

              <!-- Password Settings Section -->            
              <div class="col-md-6">
                <h5 class="mb-4">Password Settings</h5>
                <div class="mb-3">
                  <label for="currentPassword" class="form-label"
                    >Current Password</label
                  >
                  <input
                    type="password"
                    id="currentPassword"
                    v-model="currentPassword"
                    class="form-control"
                  />
                </div>
                <div class="mb-3">
                  <label for="newPassword" class="form-label"
                    >New Password</label
                  >
                  <input
                    type="password"
                    id="password"
                    v-model="password"
                    class="form-control"
                  />
                </div>
                <div class="mb-3">
                  <label for="confirmNewPassword" class="form-label"
                    >Confirm New Password</label
                  >
                  <input
                    type="password"
                    id="confirmNewPassword"
                    v-model="confirmNewPassword"
                    class="form-control"
                  />
                </div>
              </div>
            </div>
            <div class="d-flex justify-content-end gap-2 mt-4">
              <button type="submit" class="btn-update" :disabled="loading">
                {{ loading ? "Updating..." : "Update" }}
              </button>
              <button type="button" class="btn-cancel" @click="cancelUpdate">
                Cancel
              </button>
            </div>
          </form>
          <b-modal
              v-model="showModal"
              :title="isSuccess ? 'Success' : 'Error'"
              @hide="closeModal"
              centered
              hide-footer
              :modal-class="isSuccess ? 'modal-success' : 'modal-error'"
            >
              <p>{{ modalMessage }}</p>
              <div class="buttons-container">
                <button @click="closeModal" class="btn btn-primary">OK</button>
              </div>
            </b-modal>
        </div>
      </div>
    </div>
  </div>
  </div>
</div>
</template>

<script>
import { mapGetters } from "vuex";
import SideNav from "@/components/SideNav.vue";
import AppHeaderLivwell from "@/components/Header.vue";
import { BModal } from "bootstrap-vue-3"; 

export default {
  name: "BrkAccounts",
  components: {
    SideNav,
    BModal,
    AppHeaderLivwell,
  },
  mounted() {
    this.fetchBrokerData();
  },
  data() {
    return {
      username: "",
      email: "",
      contactNumber: "",
      password: "",
      modalMessage: "", // Message to display in the modal
      showModal: false, // Modal visibility
      isSuccess: false,
      loading: false, // For showing loading state
      placeholderUsername: "",
      placeholderEmail: "",
      placeholderContactNumber: "",
    };
  },
  computed: {
    ...mapGetters(["getUserId", "getAuthToken"]),
  },
  methods: {
      closeModal() {
      this.showModal = false; // Hide the modal
      this.modalMessage = ""; // Clear the message
    },
    async fetchBrokerData() {
      const brokerId = this.getUserId;
      const authToken = this.getAuthToken;
      try {
        const response = await fetch(
          `http://localhost:8000/broker/manage-accounts/${brokerId}/`,
          {
            headers: {
              Authorization: `Bearer ${authToken}`,
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          // Assign placeholders from fetched data
          this.placeholderUsername = data.username;
          this.placeholderEmail = data.email;
          this.placeholderContactNumber = data.contact_number;
        } else {
          this.showModalWithMessage("Failed to fetch broker data.", false);

        }
      } catch (error) {
        console.error("Error fetching broker data:", error);
        this.showModalWithMessage("An error occurred while fetching broker data.", false);

      }
    },
async updateAccount() {
      const brokerId = this.getUserId;
      if (this.username === ""&&this.email===""&&this.contactNumber===""&&this.password==="") {
        this.showModalWithMessage("No changes found.", false);
        return;
      }
  // Validate password on client-side
 if (this.password) {
  // Ensure current password is provided when trying to change the password
  if (!this.currentPassword) {
    this.showModalWithMessage(
      "You must provide your current password to change your password.",
      false
    );
    return;
  }

  // Define a regex to validate all password criteria
  const passwordRegex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/;

  if (!passwordRegex.test(this.password)) {
    this.showModalWithMessage(
      "Password must be at least 8 characters long and include an uppercase letter, a lowercase letter, a number, and a special character.",
      false
    );
    return;
  }

  if (this.password !== this.confirmNewPassword) {
    this.showModalWithMessage("New passwords do not match.", false);
    return;
  }
}

  if (brokerId) {
    try {
      const response = await fetch(`http://localhost:8000/broker/manage-account/${brokerId}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        },
        body: JSON.stringify({
          current_password: this.currentPassword || undefined, // Only include if provided
          username: this.username || undefined,
          email: this.email || undefined,
          contact_number: this.contactNumber || undefined,
          password: this.password || undefined,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        this.showModalWithMessage(errorData.message || "Failed to update account.", false);
        return;
      }

      const data = await response.json();
      if (data.success) {
        this.showModalWithMessage("Account updated successfully!", true);
        // Optionally clear sensitive fields like current password
        this.currentPassword = "";
        this.password = "";
        this.confirmNewPassword = "";
      } else {
        const errorData = await response.json();
        this.showModalWithMessage(errorData.message || "Failed to update account.", false);
      }
    } catch (error) {
      console.error("Error updating account:", error);
      this.showModalWithMessage("An error occurred while updating your account.", false);

    }
  } else {
    this.error = "No broker ID found in localStorage.";
  }
    },
 showModalWithMessage(message, isSuccess) {
      this.modalMessage = message;
      this.isSuccess = isSuccess;
      this.showModal = true;
    },
  },
};
</script>

<style scoped>
html,
body {
  height: 100%;
  margin: 0;
  /* Removes default margin */
  padding: 0;
  /* Removes default padding */
}

/* Ensure .main-page fills the available space */
.broker-account-page {
  display: flex;
  min-height: 100vh;
  /* Ensures it spans the full viewport height */
  background-color: #e8f0fa;
  /* Gray background */
}

.SideNav {
  width: 250px;
  /* Set fixed width for the sidebar */
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #343a40;
  z-index: 1;
}

.AppHeader {
  width: 100%;
  height: 60px;
  /* Adjust height as needed */
  background-color: #343a40;
  display: flex;
  align-items: center;
  padding-left: 10px;
}

.main-content {
  display: flex;
  flex-direction: column;
  margin-top: 80px;
  margin-left: 250px;
  /* Offset for header height */
  flex: 1;
  /* margin-left: 250px; */
  /* Set margin equal to sidebar width */
}

.card {
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
}

.card-body {
  padding: 2.5rem;
}

.title-wrapper {
  display: flex;
  /* Align line and title horizontally */
  align-items: center;
  width: 100%;
  max-width: 900px;

  /* Ensure the title width matches the card's width */
  margin-left: auto;
  margin-right: auto;
  margin-top: 20px;
  /* Center the wrapper */
}

.edit-title {
  color: #000000;
  margin-bottom: 0.8rem;
  text-align: left;
  /* Align the text to the left */
}

.title-icon {
  width: 15px;
  /* Short horizontal line */
  height: 5px;
  /* Thin line */
  background-color: #343a40;
  /* Line color */
  border-radius: 5px;
  /* Rounded corners */
  margin-right: 10px;
  /* Space between the icon and the title */
  margin-bottom: 15px;
}

.row {
  display: flex;
  justify-content: space-between;
  /* Ensures there's space between the columns */
}

.col-md-6 {
  width: 47%; /* You can tweak the width to suit your design */
  margin-bottom: 20px; /* Spacing between sections */
  padding-right: 10px; /* Optional: add some padding to prevent overlap */
}

h5 {
  text-align: left;
  margin-bottom: 1rem; /* Adjust spacing below the title */
  font-size: 1.1rem; /* Optional: Adjust font size if needed */
  font-style: italic; /* Italicize the titles */
}

.form-label {
  font-size: 0.9rem;
  color: #6c757d;
  /* Adjust the value to your preferred size */
}

.btn-update {
  background-color: #42b983; /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px; /* Adjust the border radius */
  padding: 10px; /* Adjust the padding at the bottom */
  width: 100px;
}

.btn-cancel {
  background-color: #343a40; /* Button primary color */
  color: #fff;
  border: none;
  border-radius: 3px; /* Adjust the border radius */
  padding: 10px;
}
</style>
