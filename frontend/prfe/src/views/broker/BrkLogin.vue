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
                    <h2 class="text-start">Hello, User!</h2>
                    <p class="text-start">
                      Welcome back! Please enter your details.
                    </p>
                    <br />

                    <div class="form-outline mb-4">
                      <label class="form-label" for="form2Example11"
                        >Username</label
                      >
                      <input
                        type="text"
                        id="username"
                        v-model="username"
                        class="form-control"
                        required
                      />
                    </div>

                    <div class="form-outline mb-4">
                      <label class="form-label" for="form2Example22"
                        >Password</label
                      >
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
                      <div class="flex-grow-1"></div>
                      <router-link class="text-muted" to="/broker/forgotpass"
                        >Forgot Password</router-link
                      >
                    </div>

                    <div class="text-center pt-1 mb-5 pb-1">
                      <button
                        class="btn btn-primary w-100 btn-block fa-lg gradient-custom-2 mb-3"
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
export default {
  data() {
    return {
      username: "",
      password: "",
      error: null, // Add the error property to hold the error message
    };
  },
  methods: {
    async login() {
      this.error = null; // Reset error before making the request
      if (this.username && this.password) {
        try {
          // Get the CSRF token from Django's cookies
          const csrftoken = this.getCookie("csrftoken");

          const response = await fetch("http://localhost:8000/login/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrftoken, // Include CSRF token in the headers
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password,
            }),
          });

          const data = await response.json();
          if (data.success) {
            // Login successful, redirect to main page
            this.$router.push("/broker/main");
          } else {
            // Set the error message if login fails
            this.error = data.message;
          }
        } catch (error) {
          // Set a generic error message if the fetch fails
          this.error = "An error occurred during login.";
        }
      } else {
        // Handle empty input fields
        this.error = "Please fill in both fields.";
      }
    },

    // Function to get the CSRF token from cookies
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },
  },
};
</script>

<style>
.gradient-custom-2 {
  background: #0d6efd;
}

.form-label {
  text-align: left !important;
  display: block;
}
</style>
