<template>
  <section
    class="vh-100 vw-100 d-flex align-items-center justify-content-center"
  >
    <div class="container">
      <div class="row gy-4 align-items-center">
        <div class="col-12 col-md-6 col-xl-7">
          <div class="d-flex justify-content-center">
            <div class="col-12 col-xl-9 text-start">
              <img
                class="img-fluid rounded mb-4"
                loading="lazy"
                width="245"
                height="80"
                alt="Logo of Company"
              />
              <hr class="border mb-4" />
              <h2 class="h1 mb-4 text-black">Welcome to PLMP</h2>
              <p class="lead mb-5">
                Property Listing Management Platform <br />
                <br /><br /><br />
                Log in Page
              </p>
            </div>
          </div>
        </div>

        <div class="col-12 col-md-6 col-xl-5">
          <div class="card border-0 rounded-4">
            <div class="card-body p-3 p-md-4 p-xl-5">
              <div class="row">
                <div class="col-12">
                  <div class="mb-4">
                    <h2 class="h3">Log In</h2>
                    <h3 class="fs-6 fw-normal text-secondary m-0">
                      Welcome back! Please enter your details.
                    </h3>
                  </div>
                </div>
              </div>
              <form @submit.prevent="login">
                <div class="row gy-3 overflow-hidden">
                  <div class="col-12">
                    <div class="form-floating mb-3">
                      <input
                        type="text"
                        id="username"
                        v-model="username"
                        class="form-control"
                        placeholder="Username"
                        required
                      />
                      <label for="username">Username</label>
                    </div>
                  </div>

                  <div class="col-12">
                    <div class="form-floating mb-3">
                      <input
                        type="password"
                        id="password"
                        v-model="password"
                        class="form-control"
                        placeholder="Password"
                        required
                      />
                      <label for="password">Password</label>
                    </div>
                  </div>

                  <div class="col-12">
                    <div class="d-grid">
                      <button
                        class="btn btn-primary btn-lg"
                        :disabled="loading"
                        type="submit"
                      >
                        Log In
                      </button>
                    </div>
                  </div>
                </div>
                <p v-if="error" class="text-danger mt-3">{{ error }}</p>
              </form>

              <div class="row">
                <div class="col-12">
                  <div
                    class="d-flex gap-2 gap-md-4 flex-column flex-md-row justify-content-md-center mt-4"
                  >
                    <router-link
                      to="/forgot-password"
                      class="link-secondary text-decoration-none"
                    >
                      Forgot Password
                    </router-link>
                  </div>
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
          let response = await fetch("http://localhost:8000/broker/login/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password,
            }),
          });

          const data = await response.json();

          if (response.ok && data.tokens) {
            this.handleLogin(data, "broker");
          } else {
            response = await fetch(
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

            const datas = await response.json();

            if (response.ok && datas.tokens) {
              this.handleLogin(datas, "developer");
            } else {
              this.error =
                data.message || "Login failed. Please check your credentials.";
            }
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

    handleLogin(data, role) {
      localStorage.setItem("accessToken", data.tokens.access);
      localStorage.setItem("refreshToken", data.tokens.refresh);

      const user = {
        id: data.user.id,
        user_role: data.user.user_role,
        company_id: data.user.company_id,
        company: data.user.company,
      };

      this.$store.dispatch("login", {
        user: user,
        token: data.tokens.access,
      });

      this.$router.push(`/${role}/dashboard`);
    },
  },
};
</script>

<style>
section {
  background-color: rgb(41, 176, 254);
}

.bg-primary {
  background-color: #007bff;
  color: white;
}
.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.form-control {
  font-size: 1rem;
  padding: 1rem;
}
</style>
