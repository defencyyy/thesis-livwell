<template>
  <section class="hero overlay">
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-md-8 col-lg-6 col-xl-5">
          <!-- Adjusted column width to center the form -->
          <div class="card rounded-3 text-black">
            <div class="card-body p-md-5 mx-md-4">
              <form @submit.prevent="login">
                <br />
                <h2 class="text-start">Hello, Developer!</h2>
                <p class="text-start underline">
                  Welcome back! Please enter your details.
                </p>
                <br />

                <div class="form-outline mb-4">
                  <label class="form-label" for="username">Username</label>
                  <input
                    type="text"
                    id="username"
                    v-model="username"
                    @input="error = null"
                    class="form-control"
                    required
                  />
                </div>

                <div class="form-outline mb-4">
                  <label class="form-label" for="password">Password</label>
                  <input
                    type="password"
                    id="password"
                    v-model="password"
                    @input="error = null"
                    class="form-control"
                    required
                  />
                </div>

                <div
                  class="d-flex justify-content-between align-items-center mb-4"
                >
                  <router-link
                    class="text-muted"
                    to="/developer/forgot-password"
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

              <!-- Add the Switch to Broker button -->
              <div class="text-center mt-4">
                <router-link to="/broker/login" class="btn btn-outline-primary">
                  Switch to Broker
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
            "${process.env.vue_app_api_url}/api/token/developer/",
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

            // Redirect to the developer dashboard
            this.$router.push("/developer/dashboard");
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
      rgba(55, 55, 55, 0.4),
      rgba(44, 171, 255, 0.7)
    )
    fill 1;
}

/* bg of the main page */
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

@layer general-styling {
  html {
    color-scheme: dark light;
    font-family: system-ui;
    line-height: 1.6;
  }

  body {
    font-size: 2rem;
    margin: 1rem;
  }

  h1 {
    line-height: 1;
  }
}
</style>
