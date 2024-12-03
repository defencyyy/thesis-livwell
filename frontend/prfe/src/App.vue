<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  methods: {
    async refreshAccessToken() {
      try {
        const refreshToken = localStorage.getItem("refreshToken");
        const response = await axios.post(
          "http://localhost:8000/api/token/refresh/",
          {
            refresh: refreshToken,
          }
        );
        if (response.status === 200) {
          const { access } = response.data;
          localStorage.setItem("accessToken", access);
          return access;
        }
      } catch (error) {
        console.error("Error refreshing token:", error);
        this.handleTokenRefreshFailure();
      }
    },

    handleTokenRefreshFailure() {
      alert("Session expired. Redirecting to home.");
      localStorage.clear();
      this.$store.dispatch("logout");
      this.$router.push({ name: "Home" });
    },

    setupAxiosInterceptors() {
      axios.interceptors.response.use(
        (response) => response,
        async (error) => {
          if (error.response?.status === 401) {
            const refreshedToken = await this.refreshAccessToken();
            if (refreshedToken) {
              error.config.headers[
                "Authorization"
              ] = `Bearer ${refreshedToken}`;
              return axios(error.config);
            }
          }
          return Promise.reject(error);
        }
      );
    },
  },
  mounted() {
    this.setupAxiosInterceptors();
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
