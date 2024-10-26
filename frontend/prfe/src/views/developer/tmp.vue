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
    async logout() {
      try {
        // Send a logout request to the server
        const response = await fetch(
          "http://localhost:8000/developer/logout/",
          {
            method: "POST",
            credentials: "include", // Include cookies for proper logout
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        if (data.success) {
          // Clear all localStorage items related to the user
          localStorage.removeItem("user_id");
          localStorage.removeItem("user_role");
          localStorage.removeItem("logged_in");

          // Redirect to the home page (login)
          this.$router.push({ path: "/home" });
        } else {
          console.error("Logout failed:", data.message);
        }
      } catch (error) {
        console.error("Logout request failed:", error);
      }
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
