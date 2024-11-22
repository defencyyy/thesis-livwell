<template>
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
          {
            name: "Dashboard",
            link: "/developer/dashboard",
            icon: "fa-solid fa-chart-line",
          },
          {
            name: "Company",
            link: "/developer/company",
            icon: "fa-solid fa-building",
          },
          {
            name: "Brokers",
            link: "/developer/brokers",
            icon: "fa-solid fa-user-tie",
          },
          {
            name: "Sites",
            link: "/developer/sites",
            icon: "fa-solid fa-map-marker-alt",
            // children: [{ name: "Units", link: "/developer/units" }],
          },
          {
            name: "Payment Schedules",
            link: "/developer/payment-schedule",
            icon: "fa-solid fa-calendar-check",
          },
          // { name: "Account", link: "/developer/account", icon: "fa-solid fa-chart-line" },
        ];
      } else if (this.userRole === "broker") {
        this.menuItems = [
          { name: "Dashboard", link: "/broker/dashboard" },
          { name: "Units", link: "/broker/affiliated-units" },
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

.sidebar-header {
  display: flex;
  align-items: center;
  padding: 20px;
  background-color: #23272b;
  border-bottom: 1px solid #444;
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
</style>
