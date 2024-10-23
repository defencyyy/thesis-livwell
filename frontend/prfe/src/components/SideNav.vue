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
          { name: "Units", link: "/developer/units" },
          { name: "Broker Accounts", link: "/developer/broker-accounts" },
          { name: "Payment Schedules", link: "/developer/payment-schedules" },
          { name: "Manage Company", link: "/developer/manage-company" },
          { name: "Manage Affiliations", link: "/developer/manage-affiliations" },
          { name: "Manage Sites", link: "/developer/manage-sites" },
          { name: "Manage Account", link: "/developer/manage-account" },
        ];
      } else if (this.userRole === "broker") {
        this.menuItems = [
          { name: "Dashboard", link: "/broker/dashboard" },
          { name: "Affiliated Units", link: "/broker/affiliated-units" }, 
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
</style>
