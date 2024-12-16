<template>
  <div>
    <div :class="['sidebar']">
      <div class="sidebar-header">
        <img
          v-if="tempLogo"
          :src="tempLogo"
          class="sidebar-logo"
          alt="Company Logo"
        />
        <i v-else class="fas fa-cogs sidebar-logo" style="color: #0560fd"></i>
        <h4 id="sidebar-title">{{ tempCompanyName || "Company Name" }}</h4>
      </div>

      <nav class="sidebar-nav">
        <b-nav vertical pills>
          <template v-for="(item, index) in menuItems" :key="index">
            <!-- Normal menu item with icon and name -->
            <b-nav-item v-if="!item.children" :to="item.link" exact custom>
              <i
                :class="['menu-icon', item.icon, { active: isActive(item) }]"
              ></i>
              <span :class="['item-name', { active: isActive(item) }]">
                {{ item.name }}
              </span>
            </b-nav-item>

            <!-- Parent menu item with icon and name -->
            <div v-else>
              <b-nav-item
                :to="item.link"
                exact
                custom
                class="parent-item"
                :class="{ active: isActive(item) }"
              >
                <i
                  :class="['menu-icon', item.icon, { active: isActive(item) }]"
                ></i>
                <span :class="['item-name', { active: isActive(item) }]">
                  {{ item.name }}
                </span>
              </b-nav-item>

              <!-- Child menu items with icon and name -->
              <div class="child-menu">
                <b-nav-item
                  v-for="(child, idx) in item.children"
                  :key="idx"
                  :to="child.link"
                  exact
                  custom
                  :class="{
                    active: isActive(child),
                    'active-child': isChildActive(child),
                  }"
                >
                  <i
                    :class="[
                      'menu-icon',
                      child.icon,
                      { active: isActive(child) },
                    ]"
                  ></i>
                  <span :class="['item-name', { active: isActive(child) }]">
                    {{ child.name }}
                  </span>
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
      tempLogo: null, // Variable to store the logo temporarily
      tempCompanyName: null, // Variable to store the company name temporarily
    };
  },
  created() {
    this.setMenuItems();
    this.setTemporaryLogo(); // Set the temporary logo
    this.setTemporaryCompanyName(); // Set the temporary company name
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
    setTemporaryLogo() {
      // Try to fetch logo from localStorage if it was previously set
      const storedLogo = localStorage.getItem("company_logo");
      if (storedLogo) {
        this.tempLogo = storedLogo;
      } else if (this.company?.logo) {
        this.tempLogo = `http://localhost:8000${this.company.logo}`;
        localStorage.setItem("company_logo", this.tempLogo); // Store for future page refreshes
      }
    },
    setTemporaryCompanyName() {
      // Try to fetch company name from localStorage if it was previously set
      const storedName = localStorage.getItem("company_name");
      if (storedName) {
        this.tempCompanyName = storedName;
      } else if (this.company?.name) {
        this.tempCompanyName = this.company.name;
        localStorage.setItem("company_name", this.tempCompanyName); // Store for future page refreshes
      }
    },
    setMenuItems() {
      if (this.userRole === "developer") {
        this.menuItems = [
          {
            name: "Dashboard",
            link: "/developer/dashboard",
            icon: "fas fa-chart-pie",
          },
          {
            name: "View Customers",
            link: "/developer/customers",
            icon: "fas fa-users",
          },

          {
            name: "Manage Brokers",
            link: "/developer/brokers",
            icon: "fas fa-user-tie",
          },

          {
            name: "Manage Sites",
            link: "/developer/sites",
            icon: "fas fa-map-marker-alt",
          },
          {
            name: "Manage Units",
            link: "/developer/units",
            icon: "fas fa-home",
            children: [
              {
                name: "Unit Templates",
                link: "/developer/units/templates",
                icon: "fas fa-chevron-right",
              },
              {
                name: "Unit Types",
                link: "/developer/units/types",
                icon: "fas fa-chevron-right",
              },
            ],
          },
          {
            name: "Manage Sales",
            link: "/developer/sales",
            icon: "fas fa-chart-line",
          },
          {
            name: "Manage Doc-Types",
            link: "/developer/documents",
            icon: "fas fa-folder-open",
          },
          {
            name: "Manage Milestones",
            link: "/developer/milestones",
            icon: "fas fa-trophy",
          },

          {
            name: "Manage Company",
            link: "/developer/company",
            icon: "fas fa-building",
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
            name: "Reserve Units",
            link: "/broker/affiliated-units",
            icon: "fas fa-home",
          },
          {
            name: "Manage Sales",
            link: "/broker/manage-sales",
            icon: "fas fa-chart-line",
          },
          {
            name: "Add Customers",
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

    // Check if the current child item is active
    isChildActive(child) {
      return this.$route.path === child.link;
    },

    // Toggle the visibility of child items (for parent items with children)
    toggleChildMenu(item) {
      // If the item has children, toggle its 'active' state
      if (item.children) {
        item.active = !item.active;
      }
    },
  },
  watch: {},
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

/* Child menu styling when the parent is active */
.parent-item.active + .child-menu {
  background-color: #f3f8ff; /* Light blue background for active child items */
  border-radius: 8px; /* Add rounded corners to the child menu */
}

/* Remove extra padding for children */
.child-menu {
  padding-left: 22px; /* Ensure no padding for children */
}

/* Style for individual child items */
.child-menu b-nav-item {
  padding-left: 0; /* Remove extra padding for child nav items */
}

/* Optional: Styling for hover on child items */
.child-menu b-nav-item:hover {
  background-color: #f0f0f0; /* Light gray background for hover state */
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

  /* Remove extra padding for children */
  .child-menu {
    padding-left: 10px; /* Ensure no padding for children */
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
  /* Remove extra padding for children */
  .child-menu {
    padding-left: 0; /* Ensure no padding for children */
  }

  /* Style for individual child items */
  .child-menu b-nav-item {
    padding-left: 0 !important; /* Remove extra padding for child nav items */
  }
}
</style>
