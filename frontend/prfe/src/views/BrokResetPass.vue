<template>
  <section>
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-xl-10">
          <div class="card rounded-3 text-black">
            <div class="card-body p-md-5 mx-md-4">
              <h3>Set a New Password</h3>
              <p>Enter your new password below.</p>
              <form @submit.prevent="resetPassword">
                <div class="form-outline mb-4">
                  <label for="new_password" class="form-label">New Password</label>
                  <input
                    type="password"
                    id="new_password"
                    v-model="newPassword"
                    class="form-control"
                    required
                  />
                </div>

                <button type="submit" class="btn btn-primary w-100">
                  Reset Password
                </button>

                <p v-if="message" class="text-success mt-3">{{ message }}</p>
                <p v-if="error" class="text-danger mt-3">{{ error }}</p>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      newPassword: "",
      message: "",
      error: ""
    };
  },
  methods: {
    async resetPassword() {
      try {
        const response = await fetch(`http://localhost:8000/reset-password-confirm/${this.$route.params.uid}/${this.$route.params.token}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ new_password: this.newPassword }),
        });

        if (response.ok) {
          const data = await response.json();
          this.message = "Password reset successfully!";
          this.error = "";
        } else {
          const data = await response.json();
          this.error = data.message || "Failed to reset password.";
          this.message = "";
        }
      } catch (error) {
        this.error = "An error occurred while resetting the password.";
        this.message = "";
      }
    },
  },
};
</script>

<style>
/* Add your styles here */
</style>
