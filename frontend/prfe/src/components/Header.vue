<template>
    <div class="top-bar">
      <div class="welcome-text">
        Welcome Back, User!
      </div>
      <div class="d-flex align-items-center">
        <button class="btn btn-link text-white me">
          <i class="bi bi-bell"></i> <!-- Notification bell icon -->
        </button>
        <div class="dropdown">
          <a href="#" class="d-flex align-items-center text-white text-decoration-none dropdown-toggle"
            id="dropdownUser" data-bs-toggle="dropdown" aria-expanded="false">
            <img src="https://via.placeholder.com/40" alt="profile" class="rounded-circle" width="35"
              height="35" style="margin-right: 5px;">
          </a>
          <ul class="dropdown-menu dropdown-menu-end text-small " aria-labelledby="dropdownUser">
            <li><span class="dropdown-item disabled"><i class="bi bi-person me-2"></i>Developer Name</span></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="#"><i class="bi bi-gear me-2"></i> Account Settings</a></li>
            <li><a class="dropdown-item" href="#"><i class="bi bi-moon me-2"></i> Display Settings</a></li>
            <li><a class="dropdown-item" href="#"><i class="bi bi-question-circle me-2"></i> Help & Support</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <!-- Sign Out Button with Logout -->
            <li><a class="dropdown-item" href="#" @click.prevent="logout"><i class="bi bi-box-arrow-right me-2"></i> Sign Out</a></li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "AppHeader",
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
            // Clear localStorage items
            localStorage.removeItem("authToken");
            localStorage.removeItem("user_id");
            localStorage.removeItem("user_role");
            localStorage.removeItem("logged_in");
            localStorage.removeItem("company_id");
            localStorage.removeItem("developer_id");
  
            // Redirect to the home page or login page
            this.$router.push({ path: "/home" });
          } else {
            console.error("Logout failed:", data.message);
          }
        } catch (error) {
          console.error("Logout request failed:", error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .top-bar {
    background-color: #333;
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
  