<template>
  <section>
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-xl-10">
          <div class="card rounded-3 text-black">
            <div class="card-body p-md-5 mx-md-4">
              <h3>Reset Your Password</h3>
              <p>Please enter your email to receive a password reset link.</p>
              <form @submit.prevent="sendResetLink">
                <div class="form-outline mb-4">
                  <label for="email" class="form-label">Email address</label>
                  <input
                    type="email"
                    id="email"
                    v-model="email"
                    class="form-control"
                    required
                  />
                </div>

                <button type="submit" class="btn btn-primary w-100">
                  Send Reset Link
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
      email: "",
      message: "",
      error: "",
    };
  },
  methods: {
    async sendResetLink() {
      //console.log("Entered email:", this.email);
      try {
        const response = await fetch(
          "http://localhost:8000/broker/reset-password/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: this.email }),
          }
        );

        if (response.ok) {
          // No need for "data" here, since we're not using the returned data
          this.message = "Password reset link sent to your email.";
          this.error = "";
        } else {
          // No need to declare "data" unless you use it to extract a specific message
          const data = await response.json(); // Extract message if available
          this.error = data.message || "Failed to send the reset link.";
          this.message = "";
        }
      } catch (error) {
        this.error = "An error occurred while sending the reset link.";
        this.message = "";
      }
    },
  },
};
</script>

<style>
/* Add styles here */
</style>
