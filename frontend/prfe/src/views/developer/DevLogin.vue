<template>
  <section>
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
                    <p class="text-start">
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
                      <div class="flex-grow-1"></div>
                      <router-link
                        class="text-muted"
                        to="/developer/forgot-password"
                      >
                        Forgot Password
                      </router-link>
                    </div>

                    <div class="text-center pt-1 mb-5 pb-1">
                      <button
                        class="btn btn-primary w-100 btn-block fa-lg gradient-custom-2 mb-3"
                        :disabled="loading"
                        type="submit"
                      >
                        Sign in
                      </button>
                    </div>

                    <p v-if="error" class="text-danger">{{ error }}</p>
                  </form>
                </div>
              </div>
              <div class="col-lg-6 d-flex align-items-center gradient-custom-2">
                <div class="text-white px-3 py-4 p-md-5 mx-md-4">
                  <div
                    style="
                      width: 120px;
                      height: 120px;
                      background-color: white;
                      border-radius: 50%;
                      margin: 0 auto 20px;
                    "
                  ></div>
                  <h4 class="mb-4">Company Name</h4>
                  <p class="small mb-0">
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

    getCookie(name) {
      const cookieArr = document.cookie.split(";");
      for (let cookie of cookieArr) {
        const [key, value] = cookie.split("=");
        if (key.trim() === name) return decodeURIComponent(value);
      }
      return null;
    },

    async login() {
      this.error = null;
      this.loading = true;

      if (this.username && this.password) {
        try {
          const csrftoken = this.getCookie("csrftoken");
          if (!csrftoken) {
            this.error =
              "CSRF token not found. Please try refreshing the page.";
            this.loading = false;
            return;
          }

          const response = await fetch(
            "http://localhost:8000/developer/login/",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
              },
              body: JSON.stringify({
                username: this.username,
                password: this.password,
              }),
              credentials: "include",
            }
          );

          if (!response.ok) {
            const errorData = await response.json();
            this.error = errorData.message || "Invalid username or password.";
            this.loading = false;
            return;
          }

          const data = await response.json();
          if (data.success) {
            // Store auth token and user data in localStorage
            localStorage.setItem("authToken", data.tokens.access);
            localStorage.setItem("user_role", "developer");
            localStorage.setItem("logged_in", "true");
            localStorage.setItem("developer_id", data.user.id);
            localStorage.setItem("company_id", data.user.company_id); // Add company_id to localStorage
            console.log(
              "Developer ID stored:",
              localStorage.getItem("developer_id")
            );
            console.log(
              "Company ID stored:",
              localStorage.getItem("company_id")
            );
            console.log(
              "Developer ID (from localStorage):",
              this.localStorageUserId
            );
            console.log(
              "Company ID (from localStorage):",
              this.localStorageCompanyId
            );

            // Dispatch login action to Vuex store
            const user = data.user;
            const token = data.tokens.access;
            this.$store.dispatch("login", { user, token });

            // Redirect to the developer dashboard
            this.$router.push("/developer/dashboard");
          } else {
            this.error = data.message || "Invalid username or password.";
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
.gradient-custom-2 {
  background: red;
}

.form-label {
  text-align: left !important;
  display: block;
}
</style>
