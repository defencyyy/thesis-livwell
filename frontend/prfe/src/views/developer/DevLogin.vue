<template>
  <section class="hero overlay">
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-xl-10">
          <div class="card rounded-3 text-black">
            <div class="row g-0">
              <div class="col-lg-6">
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
                      <div class="d-flex-grow-1"></div>
                      <router-link
                        class="text-muted"
                        to="/developer/forgot-password"
                      >Forgot Password
                      </router-link>

                      <div class="flex-grow-1"></div>
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

                  <!-- Add the Return and Switch to Broker buttons -->
                  <div class="text-center mt-4">
                    <!-- <router-link to="/home" class="btn btn-outline-secondary">
                      Return
                    </router-link> -->
                    <router-link
                      to="/broker/login"
                      class="btn btn-outline-primary"
                    >
                      Switch to Broker
                    </router-link>
                  </div>
                </div>
              </div>
              <div class="col-lg-6 d-flex align-items-center gradient-custom-2 custom-bg-color"
              style="border-radius: 8px"
              >
                <div  class="text-black px-3 py-4 p-md-5 mx-md-4">
                  <div
                    style="
                      width: 250px;
                      height: 200px;

                      background-image: url(https://sid.dmcihomes.com/images/OnlineCRF/DMCI2019.png);
                      background-size: contain; /* Ensures the image scales to fit the div without cropping */
                      background-position: center; /* Centers the image within the div */
                      background-repeat: no-repeat;

                      border-radius: 50%;
                      margin: 0 auto 0px;
                    "
                  ></div>
                  <h4 class="mb-4 text-white">Company Name</h4>
                  <p class="small mb-0 text-white">
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit,
                    sed do eiusmod tempor incididunt ut labore et dolore magna
                    aliqua.
                  </p>
                </div>
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
            "http://localhost:8000/api/token/developer/",
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
  border-image:  linear-gradient(to bottom, rgba(25, 128, 255, 0.4), rgba(44, 171, 255, 0.7)) 
    fill 1;
}

/* bg of the main page */
.hero {
  background-image: url("https://wp-assets.dotproperty-kh.com/wp-content/uploads/sites/2/2021/03/24111936/The-Seasons-Residences-Metro-Manila.jpg");
  background-size: cover;
  background-repeat: no-repeat;
  min-block-size: 100vh;
  place-content: center;
  text-align: center;
}

.custom-bg-color {
  background-color:rgb(53, 118, 202) !important;
}

/* underline after the welcome back */
.underline {
  border-bottom: 1px solid #5e5e5e;
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
