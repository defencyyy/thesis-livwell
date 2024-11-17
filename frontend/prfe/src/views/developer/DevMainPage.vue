<template>
  <div class="main-page">
    <SideNav />
    <div class="main-content">
      <AppHeader />
      <div class="content">
        <div class="dashboard-container">
          <!-- Top Row -->
          <div class="card shadow-lg border-0 rounded-3 mx-auto dashboard-box">
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
          </div>

          <!-- Large Center Box -->
          <div class="card shadow-lg border-0 rounded-3 mx-auto large-box">
            <div class="card-body">
              <h5 class="card-title">Overview</h5>
            </div>
          </div>

          <!-- Bottom Row -->
          <div class="card shadow-lg border-0 rounded-3 mx-auto dashboard-box">
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
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import AppHeader from "@/components/Header.vue";
import { mapState } from "vuex";


export default {
  name: "DevMainPage",
  components: {
    SideNav, AppHeader
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId || null,
      userType: (state) => state.userType || null,
      companyId: (state) => state.companyId || null,
    }),
    localStorageUserId() {
      return localStorage.getItem("developer_id");
    },
    localStorageCompanyId() {
      return localStorage.getItem("company_id");
    },
  },
  mounted() {
    if (!this.userId || !this.userType || !this.companyId) {
      // Reload the page to ensure state is synced
      this.$router.push({ name: "DevLogin" });
    }
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
          localStorage.removeItem("authToken");
          localStorage.removeItem("user_id");
          localStorage.removeItem("user_role");
          localStorage.removeItem("logged_in");
          localStorage.removeItem("company_id");
          localStorage.removeItem("developer_id");

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
  margin-left: 250px;
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
