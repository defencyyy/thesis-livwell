<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="dashboard-container"></div>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "DevMainPage",
  components: {
    SideNav,
    AppHeader,
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId || null,
      userType: (state) => state.userType || null,
      companyId: (state) => state.companyId || null,
      loggedIn: (state) => state.loggedIn, // Use Vuex loggedIn state
    }),
    localStorageUserId() {
      return localStorage.getItem("user_id");
    },
    localStorageCompanyId() {
      return localStorage.getItem("company_id");
    },
  },
  mounted() {
    if (!this.loggedIn || this.userType !== "developer" || !this.companyId) {
      this.redirectToLogin();
    }
    this.setupAxiosInterceptor();
  },
  watch: {
    loggedIn(newVal) {
      if (!newVal) {
        this.redirectToLogin(); // Handle redirect to login page if logged out
      }
    },
    userType(newVal) {
      if (newVal !== "developer") {
        this.redirectToLogin(); // Prevent access if the user is not a developer
      }
    },
    companyId(newVal) {
      if (!newVal) {
        this.redirectToLogin(); // Prevent access if no company ID
      }
    },
  },
  methods: {
    async logout() {
      try {
        // Notify backend about logout
        await axios.post(
          "http://localhost:8000/api/token/devlogout/", // Update URL to match Django endpoint
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        // Clear localStorage and Vuex state
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("developer_id");
        localStorage.removeItem("company_id");

        // Call Vuex mutation to reset user state
        this.$store.commit("clearUser");

        // Redirect to login page
        this.redirectToLogin();
      } catch (error) {
        console.error("Error during logout:", error);
        alert("Logout failed. Please try again.");
      }
    },

    redirectToLogin() {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      this.$store.commit("clearUser");
      this.$router.push({ name: "Home" });
    },
    // Handle token refresh logic here
    async refreshToken() {
      const refreshToken = localStorage.getItem("refreshToken");
      if (!refreshToken) {
        this.handleTokenRefreshFailure(); // Handle missing refresh token
        return;
      }

      try {
        const response = await axios.post(
          "http://localhost:8000/api/token/refresh/",
          { refresh: refreshToken }
        );
        const { access } = response.data;

        // Store the new access token in Vuex and localStorage
        this.$store.commit("setAuthToken", access);
        localStorage.setItem("accessToken", access); // Update localStorage
        return access;
      } catch (error) {
        console.error("Token refresh failed", error);
        this.handleTokenRefreshFailure();
        throw error;
      }
    },
    handleTokenRefreshFailure() {
      alert("Session expired. Please log in again.");
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      this.$store.commit("clearUser"); // Clear Vuex state
      this.redirectToLogin(); // Redirect to the login page
    },

    setupAxiosInterceptor() {
      axios.interceptors.request.use(
        (config) => {
          const token = localStorage.getItem("accessToken");
          if (token) {
            config.headers["Authorization"] = `Bearer ${token}`;
          }
          return config;
        },
        (error) => Promise.reject(error)
      );

      axios.interceptors.response.use(
        (response) => response,
        async (error) => {
          if (error.response && error.response.status === 401) {
            const detail = error.response.data.detail;
            if (detail === "Token expired") {
              try {
                // Attempt to refresh the token
                await this.refreshToken();

                // Retry the original request after refreshing the token
                error.config.headers[
                  "Authorization"
                ] = `Bearer ${localStorage.getItem("accessToken")}`;
                return axios(error.config);
              } catch (refreshError) {
                // If token refresh fails, handle it
                this.handleTokenRefreshFailure();
              }
            } else {
              // For any other 401 error, log out the user
              this.handleTokenRefreshFailure();
            }
          }
          return Promise.reject(error);
        }
      );
    },
  },
};
</script>

<style scoped>
.main-page {
  display: flex;
  height: 100vh;
  background-color: #f6f6f6;
}

.SideNav {
  width: 250px;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #343a40;
  z-index: 1;
}

.AppHeader {
  width: 100%;
  height: 60px;
  background-color: #343a40;
  display: flex;
  align-items: center;
  padding-left: 10px;
  color: #ffffff;
}

.main-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  margin-top: 60px;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}
</style>
