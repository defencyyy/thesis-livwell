<template>
  <section>
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-xl-10">
          <div class="card rounded-3 text-black">
            <div class="card-body p-md-5 mx-md-4">
              <h3>Developer Password Reset</h3>
              <p>Please enter your email to receive a password reset link.</p>
              <form @submit.prevent="sendDevResetLink">
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
    async sendDevResetLink() {
      try {
        const response = await fetch(
          "http://localhost:8000/developer/reset-password/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: this.email }),
          }
        );

        if (response.ok) {
          this.message = "Password reset link sent to your email.";
          this.error = "";
        } else {
          const data = await response.json();
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
