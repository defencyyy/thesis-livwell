<template>
  <div>
    <div :class="['sidebar']">
      <div class="sidebar-header">
        <!-- Replace company logo with a Font Awesome icon or any other icon -->
        <i class="fas fa-cogs sidebar-logo" style="color: #0560fd"></i>
        <!-- Font Awesome Icon -->
        <h4 id="sidebar-title">{{ company.name || "Company Name" }}</h4>
      </div>
      <nav class="sidebar-nav">
        <b-nav vertical pills>
          <template v-for="(item, index) in menuItems" :key="index">
            <b-nav-item v-if="!item.children" :to="item.link" exact custom>
              <i
                :class="['menu-icon', item.icon, { active: isActive(item) }]"
              ></i>
              <span :class="['item-name', { active: isActive(item) }]">
                {{ item.name }}
              </span>
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
        <div class="right-line"></div>
        <!-- The vertical line -->
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
          {
            name: "Documents",
            link: "/developer/documents",
            icon: "fas fa-folder-open",
          },
          {
            name: "Milestones",
            link: "/developer/milestones",
            icon: "fas fa-trophy",
          },
          {
            name: "Sales",
            link: "/developer/sales",
            icon: "fas fa-chart-line",
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
            icon: "fas fa-home",
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
    isActive(item) {
      return this.$route.path === item.link;
    },
  },
};
</script>

<style scoped>
.sidebar {
  position: fixed;
  width: 250px;
  background-color: #ffffff;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1); /* Adds shadow on the right */
  z-index: 2;
}

.sidebar-header {
  display: flex;
  align-items: center;
  padding: 17px;
  height: 68px;
  box-sizing: border-box;
  margin-top: 5px;
}

.sidebar-logo {
  width: 35px;
  height: 35px;
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
  color: #343a40;
  font-size: 1.2rem;
  margin: 0;
}

.menu-icon {
  width: 20px;
  text-align: center;
  margin-right: 8px;
  flex-shrink: 0;
  color: #343a40;
}

.item-name {
  color: #343a40; /* Set the text color */
  font-size: 14px; /* Customize the font size */
}

.item-name:hover {
  color: #0056b3; /* Change color on hover */
}

.active {
  color: white !important; /* Make both icon and text white when active */
}

/* Optional: Active hover effect */
.active:hover {
  color: white; /* Ensure color stays white on hover */
}

/* RESPONSIVENESS */
/* Media queries for responsive behavior */
@media (max-width: 1440px) {
  .sidebar {
    width: 220px; /* Reduce sidebar width for medium screens */
  }

  #sidebar-title {
    font-size: 1.1rem; /* Adjust font size */
  }

  .menu-icon {
    width: 18px; /* Adjust icon size */
  }

  .item-name {
    font-size: 13px; /* Adjust item font size */
  }
}

@media (max-width: 1024px) {
  .sidebar {
    width: 200px; /* Reduce sidebar width further for smaller screens */
  }

  #sidebar-title {
    font-size: 1rem;
  }

  .menu-icon {
    width: 16px;
  }

  .item-name {
    font-size: 12px;
  }
}

@media (max-width: 720px) {
  .sidebar {
    width: 60px; /* Collapse sidebar */
  }

  #sidebar-title {
    display: none; /* Hide title for small screens */
  }

  .menu-icon {
    margin-right: 0; /* Center icon without extra space */
  }

  .item-name {
    display: none; /* Hide text for small screens */
  }
}
</style>
