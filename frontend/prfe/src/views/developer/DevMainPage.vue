<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="dashboard-container">
          <!-- Top Row -->
          <!-- <div class="card shadow-lg border-0 rounded-3 mx-auto dashboard-box">
            <div class="card-body">
              <h5 class="card-title">Total Number of Units</h5>
            </div>
          </div>
          <div class="card shadow-lg border-0 rounded-3 mx-auto dashboard-box">
            <div class="card-body">
              <h5 class="card-title">Available Units</h5>
            </div>
          </div>
          <div class="card shadow-lg border-0 rounded-3 mx-auto dashboard-box">
            <div class="card-body">
              <h5 class="card-title">Sold Units</h5>
            </div>
          </div> -->

          <!-- Large Center Box -->
          <!-- <div class="card shadow-lg border-0 rounded-3 mx-auto large-box">
            <div class="card-body">
              <h5 class="card-title">Overview</h5>
            </div>
          </div> -->

          <!-- Bottom Row -->
          <!-- <div class="card shadow-lg border-0 rounded-3 mx-auto dashboard-box">
            <div class="card-body">
              <h5 class="card-title">BROKER of the MONTH!</h5>
            </div>
          </div>
          <div class="card shadow-lg border-0 rounded-3 mx-auto dashboard-box">
            <div class="card-body">
              <h5 class="card-title">Achievements</h5>
            </div>
          </div>
          <div class="card shadow-lg border-0 rounded-3 mx-auto dashboard-box">
            <div class="card-body">
              <h5 class="card-title">Upcoming Goals</h5>
            </div>
          </div> -->

        </div>
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
    // Check if the user is logged in, has a developer role, and belongs to the correct company
    if (!this.loggedIn || this.userType !== "developer" || !this.companyId) {
      this.redirectToLogin();
    }
  },
  watch: {
    loggedIn(newVal) {
      if (!newVal || this.userType !== "developer" || !this.companyId) {
        this.redirectToLogin();
      }
    },
    userType(newVal) {
      if (newVal !== "developer" || !this.companyId) {
        this.redirectToLogin();
      }
    },
    companyId(newVal) {
      if (!newVal || this.userType !== "developer") {
        this.redirectToLogin();
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
      this.$router.push({ name: "DevLogin" });
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
