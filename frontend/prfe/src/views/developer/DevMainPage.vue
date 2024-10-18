<template>
  <div>
    <h1>Welcome, Dev! You Are Logged In!</h1>
    <p>This is the main page.</p>
    <button
      class="btn btn-primary w-100 btn-block fa-lg gradient-custom-2 mb-3"
      @click.prevent="logout"
    >
      Logout
    </button>
  </div>
</template>

<script>
export default {
  name: "MainPage",
  methods: {
    logout() {
      // Clear local data (optional)
      localStorage.clear();
      sessionStorage.clear();
      // Redirect to the login page
      this.$router.push("/developer/login");
    },
  },
};
</script>

<style scoped>
h1 {
  color: #42b983;
}
</style>
