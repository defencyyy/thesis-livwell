<template>
  <div class="top-bar">
    <div class="welcome-text">Welcome Back, {{ roleName }}!</div>
    <div class="d-flex align-items-center">
      <button class="btn btn-link text-white">
        <i class="bi bi-bell"></i>
      </button>
      <div class="dropdown">
        <a
          href="#"
          class="d-flex align-items-center text-white text-decoration-none dropdown-toggle"
          id="dropdownUser"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <img
            :src="profilePicture"
            alt="profile"
            class="rounded-circle"
            width="35"
            height="35"
            style="margin-right: 5px"
          />
        </a>
        <ul
          class="dropdown-menu dropdown-menu-end text-small"
          aria-labelledby="dropdownUser"
        >
          <li>
            <span class="dropdown-item disabled">
              <i class="bi bi-person me-2"></i>{{ roleName }}
            </span>
          </li>
          <li>
            <hr class="dropdown-divider" />
          </li>
          <li v-for="(option, index) in dropdownOptions" :key="index">
            <a class="dropdown-item" :href="option.link">
              <i :class="option.icon + ' me-2'"></i> {{ option.name }}
            </a>
          </li>
          <li>
            <hr class="dropdown-divider" />
          </li>
          <li>
            <a class="dropdown-item" href="#" @click.prevent="logout">
              <i class="bi bi-box-arrow-right me-2"></i> Sign Out
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AppHeader",
  data() {
    return {
      userRole: localStorage.getItem("user_role") || "guest",
      roleName: "",
      profilePicture: "https://via.placeholder.com/40", // Default profile picture
      dropdownOptions: [],
    };
  },
  created() {
    this.setHeaderContent();
  },
  methods: {
    setHeaderContent() {
      if (this.userRole === "developer") {
        this.roleName = "Developer";
        this.profilePicture = "/assets/developer-profile.png"; // Example custom image
        this.dropdownOptions = [
          {
            name: "Account Settings",
            link: "/developer/account",
            icon: "bi bi-gear",
          },
          {
            name: "Display Settings",
            link: "/developer/display-settings",
            icon: "bi bi-moon",
          },
          {
            name: "Help & Support",
            link: "/developer/help",
            icon: "bi bi-question-circle",
          },
        ];
      } else if (this.userRole === "broker") {
        this.roleName = "Broker";
        this.profilePicture = "/assets/broker-profile.png";
        this.dropdownOptions = [
          {
            name: "Manage Sales",
            link: "/broker/manage-sales",
            icon: "bi bi-bar-chart",
          },
          {
            name: "Account Settings",
            link: "/broker/account",
            icon: "bi bi-gear",
          },
          {
            name: "Help & Support",
            link: "/broker/help",
            icon: "bi bi-question-circle",
          },
        ];
      } else {
        this.roleName = "Guest";
        this.profilePicture = "https://via.placeholder.com/40";
        this.dropdownOptions = [
          { name: "Home", link: "/home", icon: "bi bi-house" },
          { name: "About", link: "/about", icon: "bi bi-info-circle" },
        ];
      }
    },
    async logout() {
      try {
        // Notify backend about logout
        await axios.post(
          "http://localhost:8000/api/token/devlogout/",
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
.top-bar {
  background-color: #343a40;
  color: #fff;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: fixed;
  top: 0;
  left: 250px; /* Sidebar width */
  width: calc(100% - 250px);
  z-index: 2;
}

.welcome-text {
  font-size: 1.2rem;
}

.d-flex {
  display: flex;
}

.d-flex .btn i {
  font-size: 20px;
  color: #fff;
}

.d-flex .dropdown {
  margin-left: 20px;
  margin-right: 10px;
}

.dropdown-menu {
  padding: 12px 5px !important;
  width: 210px;
  transform: translateY(40px) !important;
}
</style>