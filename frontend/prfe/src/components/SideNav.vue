<template>
  <div>
    <div class="sidebar">
      <div class="sidebar-header">
        <img
          src="https://via.placeholder.com/150"
          alt="Logo"
          class="sidebar-logo"
        />
        <h4 id="sidebar-title" class="text-white">Company Name</h4>
      </div>
      <nav class="sidebar-nav">
        <div class="menu-title">Main Menu</div>
        <b-nav vertical>
          <template v-for="(item, index) in menuItems" :key="index">
            <b-nav-item v-if="!item.children" :to="item.link" exact custom>
              <i :class="item.icon" class="menu-icon"></i>
        {{ item.name }}
            </b-nav-item>

            <div v-else>
              <b-nav-item :to="item.link" exact custom class="parent-item">
                <i :class="item.icon" class="menu-icon"></i>
                {{ item.name }}
              </b-nav-item>
              <div class="child-menu">
                <b-nav-item
                  v-for="(child, idx) in item.children"
                  :key="idx"
                  :to="child.link"
                  exact
                  custom
                >
                  {{ child.name }}
                </b-nav-item>
              </div>
            </div>
          </template>
        </b-nav>
      </nav>
    </div>
  </div>
</template>

<script>
import { BNav, BNavItem } from "bootstrap-vue-3";

export default {
  name: "SideNav",
  components: { BNav, BNavItem },
  data() {
    return {
      userRole: localStorage.getItem("user_role") || "guest",
      menuItems: [],
    };
  },
  created() {
    this.setMenuItems();
  },
  methods: {
    setMenuItems() {
      if (this.userRole === "developer") {
        this.menuItems = [
          { name: "Dashboard", link: "/developer/dashboard", icon: "fa-solid fa-chart-line" },
          { name: "Company", link: "/developer/company", icon: "fa-solid fa-building" },
          { name: "Brokers", link: "/developer/brokers", icon: "fa-solid fa-user-tie" },
          // { name: "Affiliations", link: "/developer/affiliation", icon: "fa-solid fa-users"  },
          {
            name: "Sites",
            link: "/developer/sites", icon: "fa-solid fa-users" 
            // children: [{ name: "Units", link: "/developer/units" }],
          },
          { name: "Payment Schedules", link: "/developer/payment-schedule", icon: "fa-solid fa-calendar-check" },
          // { name: "Account", link: "/developer/account", icon: "fa-solid fa-calendar-check" },
        ];
      } else if (this.userRole === "broker") {
        this.menuItems = [
          { name: "Dashboard", link: "/broker/dashboard" },
          { name: "Affiliated Units", link: "/broker/affiliated-units" },
          { name: "Manage Sales", link: "/broker/manage-sales" },
          { name: "Manage Customer", link: "/broker/manage-customer" },
          { name: "Milestones", link: "/broker/milestones" },
          { name: "Account", link: "/broker/account" },
        ];
      } else {
        this.menuItems = [
          { name: "Home", link: "/home" },
          { name: "About", link: "/about" },
        ];
      }
    },
  },
};
</script>

<style scoped>
.menu-title {
  font-size: 9px;
  font-weight: bold;
  padding: 15px;
  color: #adb5bd;
  text-transform: uppercase;
}

.menu-icon {
  font-size: 16px;
  margin-right: 12px;
  color: #ced4da;
}

.sidebar {
  width: 250px;
  background-color: #343a40;
  height: 100vh;
  color: white;
  display: flex;
  flex-direction: column;
  position: fixed; /* Fix sidebar to the left */
  transition: width 0.3s;
}

.sidebar-header {
  display: flex;
  align-items: center;
  padding: 20px;
  background-color: #23272b;
  border-bottom: 1px solid #444;
}

.sidebar-logo {
  width: 40px;
  height: 40px;
  margin-right: 10px;
  border-radius: 50%;
}

#sidebar-title {
  font-size: 18px;
  font-weight: bold;
}

.sidebar-nav {
  padding: 0;
  text-align: left; /* Align all items in the sidebar to the left */
  margin-left: 8px;
  margin-top: 15px;
}

.sidebar .b-nav {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Align items to the left */
}

.sidebar .b-nav-item {
  width: 100%; /* Ensure items span the full width of the sidebar */
  padding: 10px 15px;
  text-align: left; /* Align text within the item to the left */
  display: block; /* Ensure full block layout */
}


.sidebar .b-nav-item:hover {
  background-color: #495057;
}

.parent-item {
  font-weight: bold;
  color: #ced4da;
}

.child-menu {
  margin-left: 20px;
}

.sidebar .b-nav-item.active,
.sidebar .b-nav-item:focus,
.sidebar .b-nav-item:hover {
  background-color: #007bff;
  color: white;
}
</style>


<!-- <template>
  <div>
    <b-button @click="toggleSidebar">{{
      isCollapsed ? "UnCollapse" : "Collapse"
    }}</b-button>
    <div :class="['sidebar', { collapsed: isCollapsed }]">
      <h4 id="sidebar-title">Company Name and Logo</h4>
      <nav class="mb-3">
        <b-nav vertical>
          <template v-for="(item, index) in menuItems" :key="index">
            <b-nav-item v-if="!item.children" :to="item.link" exact custom>
              {{ item.name }}
            </b-nav-item>

            <div v-else>
              <b-nav-item :to="item.link" exact custom class="parent-item">
                {{ item.name }}
              </b-nav-item>
              <div class="child-menu">
                <b-nav-item
                  v-for="(child, idx) in item.children"
                  :key="idx"
                  :to="child.link"
                  exact
                  custom
                >
                  {{ child.name }}
                </b-nav-item>
              </div>
            </div>
          </template>
        </b-nav>
      </nav>
    </div>
  </div>
</template>

<script>
import { BButton, BNav, BNavItem } from "bootstrap-vue-3";

export default {
  name: "SideNav",
  components: { BButton, BNav, BNavItem },
  data() {
    return {
      userRole: localStorage.getItem("user_role") || "guest",
      menuItems: [],
      isCollapsed: false,
    };
  },
  created() {
    this.setMenuItems();
  },
  methods: {
    setMenuItems() {
      if (this.userRole === "developer") {
        this.menuItems = [
          { name: "Dashboard", link: "/developer/dashboard" },
          { name: "Company", link: "/developer/company" },
          { name: "Brokers", link: "/developer/brokers" },
          { name: "Affiliations", link: "/developer/affiliation" },
          {
            name: "Sites",
            link: "/developer/sites",
            children: [{ name: "Units", link: "/developer/units" }],
          },
          { name: "Payment Schedules", link: "/developer/payment-schedule" },
          { name: "Account", link: "/developer/account" },
        ];
      } else if (this.userRole === "broker") {
        this.menuItems = [
          { name: "Dashboard", link: "/broker/dashboard" },
          { name: "Affiliated Units", link: "/broker/affiliated-units" },
          { name: "Manage Sales ", link: "/broker/manage-sales" },
          { name: "Manage Customer", link: "/broker/manage-customer" },
          { name: "Milestones", link: "/broker/milestones" },
          { name: "Account", link: "/broker/account" },
        ];
      } else {
        this.menuItems = [
          { name: "Home", link: "/home" },
          { name: "About", link: "/about" },
        ];
      }
    },
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 250px;
  transition: width 0.3s;
}

.sidebar.collapsed {
  width: 60px;
  overflow: hidden;
}

.sidebar h4 {
  display: inline;
}

.parent-item {
  font-weight: bold;
}

.child-menu {
  margin-left: 20px;
}

.sidebar .b-nav-item {
  white-space: nowrap;
  display: inline-block;
  transition: opacity 0.3s;
}

.sidebar.collapsed .b-nav-item {
  opacity: 0;
  pointer-events: none;
}

.sidebar:not(.collapsed) .b-nav-item {
  opacity: 1;
  pointer-events: auto;
}
</style> -->
