<template>
  <section class="hero overlay">
    <div class="container h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-md-8 col-lg-6 col-xl-5">
          <!-- Ensure responsive centering -->
          <div class="card rounded-3 text-black">
            <div class="card-body p-md-5 mx-md-4">
              <form @submit.prevent="login">
                <br />
                <h2 class="text-start">Hello, Broker!</h2>
                <p class="text-start underline">
                  Welcome back! Please enter your details.
                </p>
                <br />

                <div class="form-outline mb-4 text-start">
                  <label class="form-label" for="username">Username</label>
                  <input
                    type="text"
                    id="username"
                    v-model="username"
                    class="form-control"
                    required
                  />
                </div>

                <div class="form-outline mb-4 text-start">
                  <label class="form-label" for="password">Password</label>
                  <input
                    type="password"
                    id="password"
                    v-model="password"
                    class="form-control"
                    required
                  />
                </div>

                <div
                  class="d-flex justify-content-between align-items-center mb-4"
                >
                  <router-link class="text-muted" to="/broker/forgot-password"
                    >Forgot Password</router-link
                  >
                  <router-link class="text-muted" to="/home"
                    >Back to home</router-link
                  >
                </div>

                <div class="text-center pt-1 mb-5 pb-1">
                  <button
                    class="btn btn-primary w-100 btn-block fa-lg gradient-custom-2 mb-3 pt-4 pb-4"
                    :disabled="loading"
                    type="submit"
                  >
                    Log In
                  </button>
                </div>

                <p v-if="error" class="text-danger">{{ error }}</p>
              </form>

              <div class="text-center mt-4">
                <router-link
                  to="/developer/login"
                  class="btn btn-outline-primary"
                >
                  Switch to Developer
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
import { mapActions } from "vuex";

export default {
  data() {
    return {
      username: "",
      password: "",
      error: null,
      loading: false,
    };
  },
  methods: {
    ...mapActions(["login"]),
    async login() {
      this.error = null;
      this.loading = true;

      if (this.username && this.password) {
        try {
          const response = await fetch(
            "${process.env.vue_app_api_url}/broker/login/",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                username: this.username,
                password: this.password,
              }),
            }
          );

          const data = await response.json();

          if (response.ok && data.tokens) {
            // Store JWT tokens in localStorage
            localStorage.setItem("accessToken", data.tokens.access);
            localStorage.setItem("refreshToken", data.tokens.refresh);

            // Assuming the response contains user details and company info
            const user = {
              id: data.user.id,
              user_role: data.user.user_role,
              company_id: data.user.company_id,
              company: data.user.company, // Assuming the company data is included in the response
            };

            // Dispatch login action to Vuex store
            this.$store.dispatch("login", {
              user: user,
              token: data.tokens.access,
            });

            // Redirect to the broker dashboard
            this.$router.push("/broker/dashboard");
          } else {
            this.error = data.message || "Login failed. Please try again.";
          }
        } catch (error) {
          console.error("Login error:", error);
          this.error = "An error occurred during login.";
        } finally {
          this.loading = false;
        }
      } else {
        this.error = "Please fill in both fields.";
        this.loading = false;
      }
    },
  },
};
</script>

<style>
.overlay {
  background-color: linear-gradient(
      to bottom,
      rgba(113, 113, 113, 0.4),
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
  width: 100%; /* Makes card fit the container */
  max-width: 500px; /* Limits the maximum width */
}

.form-control {
  font-size: 1rem; /* Adjust font size for inputs */
}
</style>
