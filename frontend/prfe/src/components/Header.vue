<template>
  <div class="top-bar">
    <div class="welcome-text">Welcome Back, <b>{{ roleName }}!</b></div>
    <div class="d-flex align-items-center">
      <button class="btn-bell">
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
          <i class="bi bi-person-circle profile-icon"></i>
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
            <a class="dropdown-item" href="#" @click="logout">
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
        this.profilePicture = "/assets/account.png"; // Example custom image
        this.dropdownOptions = [
          {
            name: "Account Settings",
            link: "/developer/account",
            icon: "bi bi-gear",
          },
          // {
          //   name: "Display Settings",
          //   link: "/developer/display-settings",
          //   icon: "bi bi-moon",
          // },
          // {
          //   name: "Help & Support",
          //   link: "/developer/help",
          //   icon: "bi bi-question-circle",
          // },
        ];
      } else if (this.userRole === "broker") {
        this.roleName = "Broker";
        this.profilePicture = "/assets/broker-profile.png";
        this.dropdownOptions = [
          {
            name: "Account Settings",
            link: "/broker/account",
            icon: "bi bi-gear",
          },
          // {
          //   name: "Help & Support",
          //   link: "/broker/help",
          //   icon: "bi bi-question-circle",
          // },
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
        let logoutEndpoint = "";

        // Determine the logout endpoint based on userRole
        if (this.userRole === "developer") {
          logoutEndpoint = "http://localhost:8000/api/token/devlogout/";
        } else if (this.userRole === "broker") {
          logoutEndpoint = "http://localhost:8000/api/token/brklogout/";
        } else {
          throw new Error("Unsupported user role.");
        }

        await axios.post(
          logoutEndpoint,
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("user_id");
        localStorage.removeItem("user_role");
        localStorage.removeItem("company_id");

        if (this.userRole === "developer") {
          this.redirectToLogin("Home");
        } else if (this.userRole === "broker") {
          this.redirectToLogin("Home");
        }
      } catch (error) {
        console.error("Error during logout:", error);
        alert("Logout failed. Please try again.");
      }
    },
    redirectToLogin(pageName) {
      this.$router.push({ name: pageName });
    },
  },
};
</script>

<style scoped>
.top-bar {
  background-color: #eff4fb;
  color: #343a40;
  padding: 12px 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: fixed;
  top: 0;
  left: 250px; /* Sidebar width */
  width: calc(100% - 250px);
  z-index: 1;
  height: 68px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* Adds a shadow at the bottom */
}

.welcome-text {
  font-size: 18px;
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

.profile-icon {
  font-size: 22px; /* Matches the size of the original image */
  color: #343a40;
  margin-right: 5px; /* Space between icon and dropdown */
}

.btn-bell {
  background: none;
  border: none;
  color: #343a40; /* Match profile icon color */
  font-size: 20px;
  cursor: pointer;
  padding: 0;
}

.dropdown-menu {
  padding: 12px 5px !important;
  width: 210px;
  transform: translateY(40px) !important;
}

.dropdown-toggle::after {
  display: inline-block;
  margin-left: 0.25em;
  vertical-align: 0.255em;
  content: "";
  border-top: 0.3em solid #343a40; /* Match profile icon color */
  border-right: 0.3em solid transparent;
  border-left: 0.3em solid transparent;
}
</style>
