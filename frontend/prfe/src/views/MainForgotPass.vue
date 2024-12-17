<template>
  <section class="hero overlay">
    <div class="container h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-md-8 col-lg-6 col-xl-5">
          <div class="card rounded-3 text-black">
            <div class="card-body p-md-5 mx-md-4">
              <form @submit.prevent="requestPasswordReset">
                <br />
                <h2 class="text-start">Forgot Password?</h2>
                <p class="text-start underline">
                  Please enter your username and email to reset your password.
                </p>
                <br />

                <div class="form-outline mb-4">
                  <label class="form-label" for="username">Username</label>
                  <input
                    type="text"
                    id="username"
                    v-model="username"
                    class="form-control"
                    required
                  />
                </div>

                <div class="form-outline mb-4">
                  <label class="form-label" for="email">Email</label>
                  <input
                    type="email"
                    id="email"
                    v-model="email"
                    class="form-control"
                    required
                  />
                </div>

                <div class="text-center pt-1 mb-5 pb-1">
                  <button
                    class="btn btn-primary w-100 btn-block fa-lg gradient-custom-2 mb-3 pt-4 pb-4"
                    :disabled="loading"
                    type="submit"
                  >
                    Submit
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <div v-if="successMessage" class="modal-overlay">
      <div class="modal-content">
        <p>{{ successMessage }}</p>
        <button @click="successMessage = null" class="btn btn-primary">OK</button>
      </div>
    </div>

    <!-- Error Modal -->
    <div v-if="error" class="modal-overlay">
      <div class="modal-content">
        <p>{{ error }}</p>
        <button @click="error = null" class="btn btn-danger">OK</button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      email: "",
      error: null,
      successMessage: null,  // To hold the success message for the pop-up
      loading: false,
    };
  },
  methods: {
    async requestPasswordReset() {
      this.error = null;
      this.successMessage = null;  // Clear any previous messages
      this.loading = true;

      if (this.username && this.email) {
        try {
          const response = await fetch("http://localhost:8000/forgot-password/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              username: this.username.toLowerCase(),
              email: this.email,
            }),
          });

          const data = await response.json();

          if (response.ok) {
            this.successMessage = "Password reset email sent successfully.";
            setTimeout(() => {
              this.successMessage = null;  // Hide the message after 5 seconds
            }, 5000);  // 5 seconds delay before hiding
          } else {
            this.error = data.message || "An error occurred. Please try again.";
          }
        } catch (error) {
          console.error("Request error:", error);
          this.error = "An error occurred during the password reset request.";
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

<style scoped>
/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

/* Modal Content */
.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: 300px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}

/* Button Style */
.modal-content button {
  margin-top: 10px;
}
</style>
