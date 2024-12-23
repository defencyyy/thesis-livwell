<template>
  <div class="top-bar">
    <div class="welcome-text">
      Welcome, <b>{{ roleName }}!</b>
    </div>
    <div class="d-flex align-items-center">
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
              <i class="bi bi-person me-2"></i> {{ roleName }}
            </span>
          </li>
          <li>
            <hr class="dropdown-divider" />
          </li>
          <li v-for="(option, index) in dropdownOptions" :key="index">
            <router-link class="dropdown-item" :to="option.link">
              <i :class="option.icon + ' me-2'"></i> {{ option.name || "User" }}
            </router-link>
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
      firstName: localStorage.getItem("first_name") || "Guest", // Get first_name from localStorage
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
        this.roleName = `${this.firstName}`;
        this.profilePicture = "/assets/account.png"; // Example custom image
        this.dropdownOptions = [
          {
            name: "Account Settings",
            link: "/developer/account",
            icon: "bi bi-gear",
          },
        ];
      } else if (this.userRole === "broker") {
        this.roleName = `${this.firstName}`;
        this.profilePicture = "/assets/broker-profile.png";
        this.dropdownOptions = [
          {
            name: "Account Settings",
            link: "/broker/account",
            icon: "bi bi-gear",
          },
        ];
      } else {
        this.roleName = `${this.firstName}`;
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
        localStorage.removeItem("company_logo"); // Remove company logo
        localStorage.removeItem("company_name"); // Remove company name

        if (this.userRole === "developer") {
          this.redirectToLogin("MainLogin");
        } else if (this.userRole === "broker") {
          this.redirectToLogin("MainLogin");
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

/* Media queries for responsiveness */
@media (max-width: 1440px) {
  .top-bar {
    left: 220px; /* Adjust for the narrower sidebar */
    width: calc(100% - 220px);
  }

  .welcome-text {
    font-size: 16px; /* Adjust font size */
  }

  .profile-icon {
    font-size: 20px; /* Scale down icon */
  }

  .dropdown-menu {
    width: 200px; /* Adjust dropdown width */
  }
}

@media (max-width: 1024px) {
  .top-bar {
    left: 200px; /* Adjust for smaller sidebar */
    width: calc(100% - 200px);
    padding: 10px 20px; /* Adjust padding */
  }

  .welcome-text {
    font-size: 15px; /* Scale down text */
  }

  .profile-icon {
    font-size: 18px;
  }
}

@media (max-width: 720px) {
  .top-bar {
    left: 60px; /* Adjust for collapsed sidebar */
    width: calc(100% - 60px);
    padding: 8px 15px; /* Minimal padding */
  }

  .welcome-text {
    display: none; /* Hide welcome text for small screens */
  }

  .profile-icon {
    font-size: 16px;
  }

  .d-flex .dropdown {
    margin-left: 10px; /* Reduce spacing */
  }
}
</style>
