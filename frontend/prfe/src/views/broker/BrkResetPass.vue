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
                  <label for="new_password" class="form-label"
                    >New Password</label
                  >
                  <input
                    type="password"
                    id="new_password"
                    v-model="newPassword"
                    class="form-control"
                    required
                  />
                </div>
                <div class="form-outline mb-4">
                  <label for="confirm_password" class="form-label"
                    >Confirm Password</label
                  >
                  <input
                    type="password"
                    id="confirm_password"
                    v-model="confirmPassword"
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
      confirmPassword: "",
      message: "",
      error: "",
    };
  },
  methods: {
  async resetPassword() {
    // Client-side password validation
    const password = this.newPassword;
    const confirmPassword = this.confirmPassword;

    // Check if passwords match
    if (password !== confirmPassword) {
      this.error = "Passwords do not match.";
      this.message = "";
      return;
    }

    // Validate password strength on the client-side
    const passwordRequirements = [
      { regex: /.{8,}/, message: "Password must be at least 8 characters long." },
      { regex: /[A-Z]/, message: "Password must contain at least one uppercase letter." },
      { regex: /[a-z]/, message: "Password must contain at least one lowercase letter." },
      { regex: /\d/, message: "Password must contain at least one number." },
      { regex: /[!@#$%^&*(),.?":{}|<>]/, message: "Password must contain at least one special character." },
    ];

    for (const rule of passwordRequirements) {
      if (!rule.regex.test(password)) {
        this.error = rule.message;
        this.message = "";
        return;
      }
    }

    // Proceed with the password reset request if validation passes
    try {
      const response = await fetch(
        `http://localhost:8000/broker/reset-pass/${this.$route.params.uid}/${this.$route.params.token}/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ new_password: password }),
        }
      );

      if (response.ok) {
        this.message = "Password reset successfully!";
        this.error = "";
      } else {
        const errorData = await response.json();
        this.error = errorData.message || "Failed to reset password.";
        this.message = "";
      }
    } catch (error) {
      this.error = "An error occurred while resetting the password.";
      this.message = "";
    }
  },
}
};
</script>

<style>
/* Add any styles here */
</style>
