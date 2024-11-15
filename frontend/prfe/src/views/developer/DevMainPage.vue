<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
    <div class="content">
      <h1>Welcome, Dev! You Are Logged In!</h1>
      <p>This is the main page for developers.</p>
      <button @click="logout">Logout</button>
    </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";

export default {
  name: "DevMainPage",
  components: {
    SideNav, AppHeader
  },
  methods: {
    async logout() {
      try {
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
          localStorage.removeItem("user_id");
          localStorage.removeItem("user_role");
          localStorage.removeItem("logged_in");

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

.SideNav {
  width: 250px; /* Set fixed width for the sidebar */
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #343a40;
  z-index: 1;
}

.AppHeader {
  width: 100%;
  height: 60px; /* Adjust height as needed */
  background-color: #343a40;
  display: flex;
  align-items: center;
  padding-left: 10px;
}

.main-content {
  display: flex;
  margin-left: 250px; /* Set margin equal to sidebar width */
  flex-direction: column;
  /* Stack header and content vertically */
  flex: 1;
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
