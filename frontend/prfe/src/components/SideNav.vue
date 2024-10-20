<template>
  <div>
    <b-button @click="toggleSidebar">{{
      isCollapsed ? "UnCollapse" : "Collapse"
    }}</b-button>
    <div :class="['sidebar', { collapsed: isCollapsed }]">
      <h4 id="sidebar-title">Company Name and Logo</h4>
      <nav class="mb-3">
        <b-nav vertical>
          <b-nav-item
            v-for="(item, index) in menuItems"
            :key="index"
            :to="item.link"
            exact
            custom
          >
            {{ item.name }}
          </b-nav-item>
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
      isCollapsed: false, // State to manage sidebar collapse
    };
  },
  created() {
    console.log("User Role:", this.userRole);
    this.setMenuItems();
    console.log("Menu Items:", this.menuItems);
  },
  methods: {
    setMenuItems() {
      if (this.userRole === "developer") {
        this.menuItems = [{ name: "Dashboard", link: "/developer/dashboard" }];
      } else if (this.userRole === "broker") {
        this.menuItems = [{ name: "Dashboard", link: "/broker/dashboard" }];
      } else {
        this.menuItems = [
          { name: "Home", link: "/home" },
          { name: "About", link: "/about" },
        ];
      }
    },
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed; // Toggle the collapsed state
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 250px; /* Set your desired width */
  transition: width 0.3s;
  /* Add other styles for the sidebar here */
}

.sidebar.collapsed {
  width: 60px; /* Adjust width when collapsed */
  overflow: hidden; /* Prevent content from overflowing */
}

.sidebar h4 {
  display: inline; /* Keep title inline for collapsed view */
}

.sidebar .b-nav-item {
  white-space: nowrap; /* Prevent text from wrapping */
  display: inline-block; /* Keep items inline in collapsed view */
  transition: opacity 0.3s;
}

.sidebar.collapsed .b-nav-item {
  opacity: 0; /* Hide items in collapsed view */
  pointer-events: none; /* Prevent click events */
}

.sidebar:not(.collapsed) .b-nav-item {
  opacity: 1; /* Show items when expanded */
  pointer-events: auto; /* Allow click events */
}
</style>
