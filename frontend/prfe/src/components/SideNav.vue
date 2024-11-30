<!-- <template>
  <div>
    <div :class="['sidebar']">
      <div class="sidebar-header">
        <img
          src="https://via.placeholder.com/150"
          alt="Logo"
          class="sidebar-logo"
        />
        <h4 id="sidebar-title">Company Name</h4>
      </div>
      <nav class="sidebar-nav">
        <div class="sidebar-menu-title">MAIN MENU</div>
        <b-nav vertical>
          <template v-for="(item, index) in menuItems" :key="index">
            <b-nav-item v-if="!item.children" :to="item.link" exact custom >
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
          { name: "Documents", link: "/developer/documents" },
          { name: "Milestones", link: "/developer/milestones" },
          { name: "Sales", link: "/developer/sales" },
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
  position: fixed;
  width: 250px;
  background-color: #ffffff;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
}

.sidebar-menu-title {
  font-size: 11px; /* Adjust font size */
  font-weight: bold;
  color: #909090; /* Text color */
  padding-left: 16px; /* Align with sidebar items */
  padding-bottom: 15px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  padding: 17px; /* Add space around the header */
  border-bottom: 2px solid #f6f6f6; /* Add a line below the header */
  height: 68px; /* Match the height of the header */
  box-sizing: border-box; /* Includes padding in height calculation */
}

.sidebar-logo {
  width: 40px; /* Adjust the size as needed */
  height: 40px; /* Ensures the image remains square */
  border-radius: 50%; /* Makes the image circular */
  margin-right: 10px; /* Space between the logo and the text */
  margin-left: 5px; /* Space between the logo and the text */
  object-fit: cover; /* Ensures the image fits within the circle */
}

.sidebar-nav {
  text-align: left; /* Align all items in the sidebar to the left */
  margin-top: 15px;
  padding-left: 13px !important; /* Remove padding from the sidebar container */
}

#sidebar-title {
  color: #343a40; /* Make the text color black */
  font-size: 1.2rem; /* Adjust the font size */
  margin: 0; /* Remove unnecessary margins */
}

.menu-icon {
  width: 20px; /* Set a fixed width for the icons */
  text-align: center; /* Center-align the icon within its width */
  margin-right: 8px; /* Space between the icon and the text */
  flex-shrink: 0; /* Prevent the icon from shrinking */
  color: #343a40;
}
</style> -->

<template>
  <div>
    <div :class="['sidebar']">
      <div class="sidebar-header">
        <!-- Display the company logo dynamically -->
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
import axios from "axios"; // Import axios for API calls

export default {
  name: "SideNav",
  components: { BNav, BNavItem },
  data() {
    return {
      userRole: localStorage.getItem("user_role") || "guest",
      menuItems: [],
      company: {}, // Object to store company data
    };
  },
  created() {
    this.setMenuItems();
    this.fetchCompany(); // Fetch the company details on component creation
  },
  methods: {
    setMenuItems() {
      if (this.userRole === "developer") {
        this.menuItems = [
          {
            name: "Dashboard",
            link: "/developer/dashboard",
            icon: "fas fa-chart-line",
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
            icon: "fas fa-user-tie",
          },
          {
            name: "Sites",
            link: "/developer/sites",
            icon: "fas fa-map-marker-alt",
          },
          { name: "Units", link: "/developer/units", icon: "fas fa-home" },
          { name: "Documents", link: "/developer/documents" },
          { name: "Milestones", link: "/developer/milestones" },
          { name: "Sales", link: "/developer/sales" },
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
            icon: "fas fa-chart-line",
          },
          {
            name: "Units",
            link: "/broker/affiliated-units",
            icon: "fas fa-chart-line",
          },
          {
            name: "Manage Sales",
            link: "/broker/manage-sales",
            icon: "fas fa-dollar-sign",
          },
          {
            name: "Manage Customer",
            link: "/broker/manage-customer",
            icon: "fas fa-users",
          },
          {
            name: "Milestones",
            link: "/broker/milestones",
            icon: "fas fa-flag-checkered",
          },
        ];
      } else {
        this.menuItems = [
          { name: "Home", link: "/home" },
          { name: "About", link: "/about" },
        ];
      }
    },

    async fetchCompany() {
      try {
        const response = await axios.get(
          "http://localhost:8000/developer/company/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (response.status === 200) {
          this.company = response.data; // Store company data in the `company` object
        } else {
          console.error("Error fetching company details.");
        }
      } catch (error) {
        console.error("Error fetching company data:", error);
      }
    },

    getLogoUrl(logoPath) {
      return `http://localhost:8000${logoPath}`; // Return the full URL of the logo
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
}

.sidebar-menu-title {
  font-size: 11px; /* Adjust font size */
  font-weight: bold;
  color: #909090; /* Text color */
  padding-left: 16px; /* Align with sidebar items */
  padding-bottom: 15px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  padding: 17px; /* Add space around the header */
  border-bottom: 2px solid #f6f6f6; /* Add a line below the header */
  height: 68px; /* Match the height of the header */
  box-sizing: border-box; /* Includes padding in height calculation */
}

.sidebar-logo {
  width: 40px; /* Adjust the size as needed */
  height: 40px; /* Ensures the image remains square */
  border-radius: 50%; /* Makes the image circular */
  margin-right: 10px; /* Space between the logo and the text */
  margin-left: 5px; /* Space between the logo and the text */
  object-fit: cover; /* Ensures the image fits within the circle */
}

.sidebar-nav {
  text-align: left; /* Align all items in the sidebar to the left */
  margin-top: 15px;
  padding-left: 13px !important; /* Remove padding from the sidebar container */
}

#sidebar-title {
  color: #343a40; /* Make the text color black */
  font-size: 1.2rem; /* Adjust the font size */
  margin: 0; /* Remove unnecessary margins */
}

.menu-icon {
  width: 20px; /* Set a fixed width for the icons */
  text-align: center; /* Center-align the icon within its width */
  margin-right: 8px; /* Space between the icon and the text */
  flex-shrink: 0; /* Prevent the icon from shrinking */
  color: #343a40;
}
</style>
