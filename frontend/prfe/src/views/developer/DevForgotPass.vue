<template>
  <section class="hero overlay">
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-md-8 col-lg-6 col-xl-5">
          <div class="card rounded-3 text-black">
            <div class="card-body p-md-5 mx-md-4">
              <h2 class="text-start">Forgot Password?</h2>
              <p class="text-start">
                Enter your email address and we’ll send you a link to reset your password.
              </p>
              <br />

              <form @submit.prevent="sendResetLink">
                <div class="form-outline mb-4">
                  <label for="email" class="form-label">Email Address</label>
                  <input
                    type="email"
                    id="email"
                    v-model="email"
                    @input="error = null"
                    class="form-control"
                    required
                  />
                </div>

                <div class="text-center pt-1 mb-5 pb-1">
                  <button
                    type="submit"
                    class="btn btn-primary w-100 btn-block fa-lg gradient-custom-2 mb-3 pt-4 pb-4"
                    :disabled="loading"
                  >
                    Send Reset Link
                  </button>
                </div>

                <p v-if="message" class="text-success">{{ message }}</p>
                <p v-if="error" class="text-danger">{{ error }}</p>
              </form>

              <div class="text-center mt-4">
                <router-link to="/developer/login" class="btn btn-outline-primary">
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
      loading: false,
    };
  },
  methods: {
    async sendResetLink() {
      this.error = null;
      this.message = null;
      this.loading = true;

      try {
        const response = await fetch("http://localhost:8000/developer/reset-password/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email: this.email }),
        });

        if (response.ok) {
          this.message = "Password reset link sent to your email.";
        } else {
          const data = await response.json();
          this.error = data.message || "Failed to send the reset link.";
        }
      } catch (error) {
        this.error = "An error occurred while sending the reset link.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
.overlay {
  background: linear-gradient(
      to bottom,
      rgba(25, 128, 255, 0.4),
      rgba(44, 171, 255, 0.7)
    )
    fill 5;
}

/* Background of the main page */
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