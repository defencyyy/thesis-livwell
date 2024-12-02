<template>
  <div>
    <div :class="['sidebar']">
      <div class="sidebar-header">
        <!-- Use company logo from Vuex -->
        <img
          v-if="company.logo"
          :src="getLogoUrl(company.logo)"
          alt="Company Logo"
          class="sidebar-logo"
        />
        <h4 id="sidebar-title">{{ company.name || "Company Name" }}</h4>
      </div>
      <nav class="sidebar-nav">
        <div class="sidebar-menu-title">MAIN MENU</div>
        <b-nav vertical>
          <template v-for="(item, index) in menuItems" :key="index">
            <b-nav-item v-if="!item.children" :to="item.link" exact custom>
              <i :class="item.icon" class="menu-icon"></i>
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
import { mapState } from "vuex";

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
  computed: {
    // Map company data from Vuex store
    ...mapState({
      userId: (state) => state.userId,
      userType: (state) => state.userType,
      companyId: (state) => state.companyId,
      company: (state) => state.company, // Company details are now in Vuex
    }),
  },
  methods: {
    setMenuItems() {
      if (this.userRole === "developer") {
        this.menuItems = [
          {
            name: "Dashboard",
            link: "/developer/dashboard",
            icon: "fas fa-chart-pie",
          },
          {
            name: "Company",
            link: "/developer/company",
            icon: "fas fa-building",
          },
          {
            name: "Brokers",
            link: "/developer/brokers",
            icon: "fas fa-user-tie",
          },
          {
            name: "Customers",
            link: "/developer/customers",
            icon: "fas fa-users",
          },
          {
            name: "Sites",
            link: "/developer/sites",
            icon: "fas fa-map-marker-alt",
          },
          { name: "Units", link: "/developer/units", icon: "fas fa-home" },
          { name: "Documents", link: "/developer/documents", icon: "fas fa-folder-open", },
          { name: "Milestones", link: "/developer/milestones", icon: "fas fa-trophy", },
          { name: "Sales", link: "/developer/sales", icon: "fas fa-chart-line", },
          {
            name: "Payment Schedules",
            link: "/developer/payment-schedule",
            icon: "fas fa-calendar-alt",
          },
        ];
      } else if (this.userRole === "broker") {
        this.menuItems = [
          {
            name: "Dashboard",
            link: "/broker/dashboard",
            icon: "fas fa-chart-pie",
          },
          {
            name: "Units",
            link: "/broker/affiliated-units",
            icon: "fas fa-home"
          },
          {
            name: "Sales",
            link: "/broker/manage-sales",
            icon: "fas fa-chart-line",
          },
          {
            name: "Customers",
            link: "/broker/manage-customer",
            icon: "fas fa-users",
          },
          {
            name: "Milestones",
            link: "/broker/milestones",
            icon: "fas fa-trophy",
          },
          
        ];
      } else {
        this.menuItems = [
          { name: "Home", link: "/home" },
          { name: "About", link: "/about" },
        ];
      }
    },
    getLogoUrl(logoPath) {
      return `http://localhost:8000${logoPath}`;
    },
  },
};
</script>

<style scoped>
.sidebar {
  position: fixed;
  width: 250px;
  background-color: #343a40;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
}

.sidebar-menu-title {
  font-size: 11px;
  font-weight: bold;
  color: #acacac;
  padding-left: 16px;
  padding-bottom: 15px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  padding: 17px;
  border-bottom: 2px solid #acacac;
  height: 68px;
  box-sizing: border-box;
}

.sidebar-logo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  margin-left: 5px;
  object-fit: cover;
}

.sidebar-nav {
  text-align: left;
  margin-top: 15px;
  padding-left: 13px !important;
}

#sidebar-title {
  color: #ffffff;
  font-size: 1.2rem;
  margin: 0;
}

.menu-icon {
  width: 20px;
  text-align: center;
  margin-right: 8px;
  flex-shrink: 0;
  color: #ffffff;
}
</style>
