<template>
  <div>
    <div :class="['sidebar']">
      <div class="sidebar-header">
        <img
          src="https://via.placeholder.com/150"
          alt="Logo"
          class="sidebar-logo"
        />
        <h4 id="sidebar-title" class="text-white">Company Name</h4>
      </div>
      <nav class="sidebar-nav">
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
          { name: "Dashboard", link: "/developer/dashboard" },
          { name: "Company", link: "/developer/company" },
          { name: "Brokers", link: "/developer/brokers" },
          { name: "Sites", link: "/developer/sites" },
          { name: "Units", link: "/developer/units" },
          { name: "Customers", link: "/developer/customers" },
          { name: "Payment Schedules", link: "/developer/payment-schedule" },
        ];
      } else if (this.userRole === "broker") {
        this.menuItems = [
          { name: "Dashboard", link: "/broker/dashboard" },
          { name: "Units", link: "/broker/affiliated-units" },
          { name: "Manage Sales ", link: "/broker/manage-sales" },
          { name: "Manage Customer", link: "/broker/manage-customer" },
          { name: "Milestones", link: "/broker/milestones" },
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
.sidebar {
  width: 250px;
  background-color: #343a40;
  height: 100vh;
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
}
.sidebar-nav {
  text-align: left; /* Align all items in the sidebar to the left */
  margin-left: 8px;
  margin-top: 15px;
}

.sidebar h4 {
  display: inline;
}

.parent-item {
  font-weight: bold;
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

.sidebar .b-nav-item.active,
.sidebar .b-nav-item:focus,
.sidebar .b-nav-item:hover {
  background-color: #007bff;
  color: white;
}
</style>
