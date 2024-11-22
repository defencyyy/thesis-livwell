
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
            <a href="#" class="d-flex align-items-center text-white text-decoration-none dropdown-toggle" id="dropdownUser" data-bs-toggle="dropdown" aria-expanded="false">
                <img src="https://via.placeholder.com/40" alt="profile" class="rounded-circle" width="35" height="35"  style="margin-right: 5px;">
            </a>
            <ul class="dropdown-menu dropdown-menu-end text-small " aria-labelledby="dropdownUser">
                <li><span class="dropdown-item disabled"><i class="bi bi-person me-2"></i>Developer Name</span></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#"><i class="bi bi-gear me-2"></i> Account Settings</a></li>
                <li><a class="dropdown-item" href="#"><i class="bi bi-moon me-2"></i> Display Settings</a></li>
                <li><a class="dropdown-item" href="#"><i class="bi bi-question-circle me-2"></i> Help & Support</a></li>
            </ul>
        </div>
    </div>
</div>
</template>

<script>
    export default {
    name: "AppHeader"
};
</script>

<style>
.top-bar {
        background-color: #333;
        color: #fff;
        padding: 10px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .welcome-text {
        font-size: 1.2rem;
    }
    .d-flex {
        display: flex;
    }
    .d-flex .btn i {
        font-size: 20px; /* Ensures the bell icon is large enough */
        color: #fff; /* Makes sure the icon is white */
    }
    .d-flex .dropdown {
        margin-left: 20px; /* Adds space on the left side of the dropdown */
        margin-right: 10px; /* Adds space on the right side of the dropdown */
    }
    .dropdown-menu {
        padding: 12px 5px !important; /* Adjust padding as needed */
        width: 210px;
        transform: translateY(40px) !important; /* Moves the dropdown 10px down */
    }
 
</style> 