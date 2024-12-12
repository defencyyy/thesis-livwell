<template>
  <section class="hero overlay">
    <div class="container h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-md-8 col-lg-6 col-xl-5">
          <div class="card rounded-3 text-black">
            <div class="card-body p-md-5 mx-md-4">
              <h2 class="text-start">Reset Your Password</h2>
              <p class="text-start underline">Please enter a new password for your account, {{ username }}.</p>
              <form @submit.prevent="resetPassword">
                <div class="form-outline mb-4">
                  <label class="form-label" for="new-password">New Password</label>
                  <input
                    type="password"
                    id="new-password"
                    v-model="newPassword"
                    class="form-control"
                    required
                  />
                </div>

                <div class="form-outline mb-4">
                  <label class="form-label" for="confirm-password">Confirm New Password</label>
                  <input
                    type="password"
                    id="confirm-password"
                    v-model="confirmPassword"
                    class="form-control"
                    required
                  />
                </div>

                <div class="text-center pt-1 mb-5 pb-1">
                  <button
                    class="btn btn-primary w-100 btn-block fa-lg gradient-custom-2 mb-3 pt-4 pb-4"
                    :disabled="loading"
                    type="submit"
                  >
                    Reset Password
                  </button>
                </div>

                <p v-if="error" class="text-danger">{{ error }}</p>
                
                <!-- Success/Error Modal -->
                <b-modal v-model="showMessage" :title="'Password Reset Status'" hide-footer>
                  <div>
                    <p>{{ modalMessage }}</p>
                    <b-button @click="closeModal">Close</b-button>
                  </div>
                </b-modal>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { BModal, BButton } from "bootstrap-vue-3";  // Import necessary Bootstrap Vue components

export default {
  components: {
    BModal,
    BButton
  },
  data() {
    return {
      newPassword: "",
      confirmPassword: "",
      error: null,
      loading: false,
      username: "", // You can fetch the username based on the token if needed
      token: this.$route.params.token, // Get the token from the route params
      showMessage: false, // For showing the modal
      modalMessage: "", // Message to display in the modal
    };
  },
  created() {
    // You can fetch user data based on the token if needed to verify user
    this.username = "User"; // You can update this based on your logic
  },
  methods: {
    async resetPassword() {
      this.error = null;
      this.loading = true;

      if (this.newPassword === this.confirmPassword) {
        try {
          const response = await fetch(`http://localhost:8000/reset-password/${this.token}/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              new_password: this.newPassword,
            }),
          });

          const data = await response.json();

          if (response.ok) {
            this.modalMessage = "Password reset successfully! You can now log in with your new password.";
            this.showMessage = true;
            setTimeout(() => {
              this.$router.push("/login"); // Redirect to login page after password reset
            }, 9000); // Delay to show the modal before redirecting
          } else {
            this.modalMessage = data.message || "An error occurred. Please try again.";
            this.showMessage = true;
          }
        } catch (error) {
          console.error("Request error:", error);
          this.modalMessage = "An error occurred during the password reset request.";
          this.showMessage = true;
        } finally {
          this.loading = false;
        }
      } else {
        this.error = "Passwords do not match.";
        this.loading = false;
      }
    },
    closeModal() {
      this.showMessage = false; // Close the modal
      this.$router.push("/login"); // Redirect to login page when modal is closed
    }
  },
};
</script>

<style scoped>
/* Add styles for the modal if needed */
</style>
