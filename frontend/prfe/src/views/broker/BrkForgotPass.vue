<template>
  <section class="hero overlay">
    <div class="container h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-md-8 col-lg-6 col-xl-5">
          <div class="card rounded-3 text-black">
            <div class="card-body p-md-5 mx-md-4">
              <h3 class="text-center">Reset Your Password</h3>
              <p class="text-center">
                Please enter your email to receive a password reset link.
              </p>
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

              <div class="text-center mt-4">
                <router-link to="/broker/login" class="btn btn-outline-primary">
                  Back to Login
                </router-link>
              </div>
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

<style>
.overlay {
  border-image: linear-gradient(
      to bottom,
      rgba(25, 128, 255, 0.4),
      rgba(44, 171, 255, 0.7)
    )
    fill 1;
}
.hero {
 
  background-size: cover;
  background-repeat: no-repeat;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  width: 100%;
  max-width: 500px;
}

.form-control {
  font-size: 1rem;
}
</style>
