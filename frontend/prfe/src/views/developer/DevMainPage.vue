<template>
  <div class="main-page">
    <SideNav />
    <div class="content">
      <h1>Welcome, Dev! You Are Logged In!</h1>
      <p>This is the main page for developers.</p>
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";

export default {
  name: "DevMainPage",
  components: {
    SideNav,
  },
  methods: {
    logout() {
      // Clear the local storage
      localStorage.removeItem("authToken");
      localStorage.removeItem("logged_in");
      localStorage.removeItem("user_role");

      // Redirect to the login page for developers
      this.$router.push({ path: "/home" });
    },
  },
};
</script>

<style scoped>
.main-page {
  display: flex;
  height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}

h1 {
  color: #42b983;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #ff1a1a;
}
</style>
