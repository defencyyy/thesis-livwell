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
                    <h2 class="text-start">Hello, Broker!</h2>
                    <p class="text-start underline">
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
                      <div class="d-flex-grow-1"></div>
                      <router-link
                        class="text-muted"
                        to="/broker/forgot-password"
                        >Forgot Password</router-link
                      >
                      <div class="flex-grow-1"></div>
                      <router-link
                        class="text-muted"
                        to="/broker/dashboard"
                        >Back to home</router-link
                      >
                    
                    </div>

                    <div class="text-center pt-1 mb-5 pb-1">
                      <button
                        class="btn btn-warning w-100 btn-block fa-lg gradient-custom-2 mb-3"
                        type="submit"
                      >
                        Sign in
                      </button>
                    </div>

                    <p v-if="error" class="text-danger">{{ error }}</p>
                  </form>
                </div>
              </div>
              <div class="col-lg-6 d-flex align-items-center gradient-custom-2 custom-bg-color" style="border-radius: 8px;">
                <div class="text-black px-3 py-4 p-md-5 mx-md-4">
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
                  <h4 class="mb-4">DMCI HOMES INC.</h4>
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
      error: null,
    };
  },
  methods: {
    async login() {
      this.error = null; // Reset error before making the request
      if (this.username && this.password) {
        try {
          // Get the CSRF token from Django's cookies
          const csrftoken = this.getCookie("csrftoken");

          const response = await fetch("http://localhost:8000/broker/login/", {
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
            // Store the token and logged-in status
            localStorage.setItem("authToken", data.token);
            localStorage.setItem("user_role", "broker");
            localStorage.setItem("logged_in", "true");
            localStorage.setItem("broker_id", data.user.id); // Store the broker ID

            this.$router.push("/broker/dashboard");
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


 /* Add a background image to the body or container */
 .overlay {
  border-image: linear-gradient(hsla(57, 100%, 74%, 0.6), hsla(0, 0%, 61%, 0.6))
    fill 1;
}

/* bg of the main page */
.hero {
  background-image: url("https://images.unsplash.com/photo-1697229299093-c920ab53bfb1?crop=entropy&cs=srgb&fm=jpg&ixid=M3wzMjM4NDZ8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MTU2OTIzNzZ8&ixlib=rb-4.0.3&q=85");
  background-size: cover;
  background-repeat: no-repeat;

  min-block-size: 100vh;
  place-content: center;
  text-align: center;
}

.custom-bg-color {
  background-color: #D4D6CD !important;
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
