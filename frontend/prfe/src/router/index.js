import { createRouter, createWebHistory } from "vue-router";

import Home from "@/views/HomeView.vue";
import NotFoundComponent from "@/components/NotFoundComponent.vue";

// Developers
import DevLogin from "@/views/developer/DevLogin.vue";
import DevForgotPass from "@/views/developer/DevForgotPass.vue";
import DevResetPass from "@/views/developer/DevResetPass.vue";
import DevMainPage from "@/views/developer/DevMainPage.vue";

// Dev Functions
import DevFuncAccount from "@/views/developer/functions/DevAccount.vue";
import DevFuncBroker from "@/views/developer/functions/DevBrokers.vue";
import DevFuncCompany from "@/views/developer/functions/DevCompany.vue";
import DevFuncSites from "@/views/developer/functions/DevSites.vue";
import DevFuncUnits from "@/views/developer/functions/DevUnits.vue";
import DevUnitTemplates from "@/views/developer/functions/DevUnitTemplates.vue";
import DevUnitManagement from "@/views/developer/functions/DevUnitManagement.vue";
import DevUnitTypes from "@/views/developer/functions/DevUnitTypes.vue";
import DevFuncCustomers from "@/views/developer/functions/DevCustomers.vue";
import DevFuncDocuments from "@/views/developer/functions/DevDocuments.vue";
import DevFuncMilestones from "@/views/developer/functions/DevMilestones.vue";
import DevFuncSales from "@/views/developer/functions/DevSales.vue";

// Brokers
import BrkLogin from "@/views/broker/BrkLogin.vue";
import BrkForgotPass from "@/views/broker/BrkForgotPass.vue";
import BrkResetPass from "@/views/broker/BrkResetPass.vue";
import BrkMainPage from "@/views/broker/BrkMainPage.vue";

// Broker Functions
import AffiliatedUnits from "@/views/broker/BrkAffiliatedUnits.vue";
import BrkManageCustomers from "@/views/broker/BrkManageCustomers.vue";
import BrkMilestones from "@/views/broker/BrkMilestones.vue";
import BrkAccounts from "@/views/broker/BrkAccounts.vue";
import BrkManageSales from "@/views/broker/BrkManageSales.vue";
import AvailableUnits from "@/components/AvailableUnits.vue"; // Adjust the path as necessary
import SalesDetailsPage from "@/components/SalesDetailsPage.vue";
import BrkTest from "@/views/broker/BrkTest.vue";
import ReservePage from "@/components/ReservePage.vue";
import PaymentPlan from '@/components/PaymentPlan.vue';



const routes = [
  { path: "/home", name: "Home", component: Home },

  // Developer Routes
  {
    path: "/developer/login",
    name: "DevLogin",
    component: DevLogin,
  },
  {
    path: "/developer/forgot-password",
    name: "DevForgotPass",
    component: DevForgotPass,
  },
  {
    path: "/developer/reset-pass/:uid/:token",
    name: "DevResetPass",
    component: DevResetPass,
  },
  {
    path: "/developer/dashboard",
    name: "DevMain",
    component: DevMainPage,
    meta: { requiresAuth: true, role: "developer" },
  },
  {
    path: "/developer/account",
    name: "DevFuncAccount",
    component: DevFuncAccount,
    meta: { requiresAuth: true, role: "developer" },
  },
  {
    path: "/developer/brokers",
    name: "DevFuncBroker",
    component: DevFuncBroker,
    meta: { requiresAuth: true, role: "developer" },
  },
  {
    path: "/developer/company",
    name: "DevFuncCompany",
    component: DevFuncCompany,
    meta: { requiresAuth: true, role: "developer" },
  },
  {
    path: "/developer/sites",
    name: "DevFuncSites",
    component: DevFuncSites,
    meta: { requiresAuth: true, role: "developer" },
  },
  {
    path: "/developer/units",
    name: "DevFuncUnits",
    component: DevFuncUnits,
    meta: { requiresAuth: true, role: "developer" },
  },
  {
    path: "/developer/units/templates",
    name: "DevUnitTemplates",
    component: DevUnitTemplates,
    meta: { requiresAuth: true, role: "developer" },
  },
  {
    path: "/developer/units/types",
    name: "DevUnitTypes",
    component: DevUnitTypes,
    meta: { requiresAuth: true, role: "developer" },
  },
  {
    path: "/developer/units/management/:siteId",
    name: "DevUnitManagement",
    component: DevUnitManagement,
    props: true,
    meta: { requiresAuth: true, role: "developer" },
  },

  {
    path: "/developer/customers",
    name: "DevFuncCustomers",
    component: DevFuncCustomers,
    meta: { requiresAuth: true, role: "developer" },
  },
  {
    path: "/developer/documents",
    name: "DevFuncDocuments",
    component: DevFuncDocuments,
    meta: { requiresAuth: true, role: "developer" },
  },
  {
    path: "/developer/milestones",
    name: "DevFuncMilestones",
    component: DevFuncMilestones,
    meta: { requiresAuth: true, role: "developer" },
  },
  {
    path: "/developer/sales",
    name: "DevFuncSales",
    component: DevFuncSales,
    meta: { requiresAuth: true, role: "developer" },
  },

  // Broker Routes
  {
    path: "/broker/login",
    name: "BrkLogin",
    component: BrkLogin,
  },
  {
    path: "/broker/forgot-password",
    name: "BrkForgotPass",
    component: BrkForgotPass,
  },
  {
    path: "/broker/reset-pass/:uid/:token",
    name: "BrkResetPass",
    component: BrkResetPass,
  },
  {
    path: "/broker/dashboard",
    name: "BrkMain",
    component: BrkMainPage,
    meta: { requiresAuth: true, role: "broker" },
  },
  {
    path: "/broker/affiliated-units",
    name: "AffiliatedUnits",
    component: AffiliatedUnits,
    meta: { requiresAuth: true, role: "broker" },
  },

  // other routes
  {
    path: "/units/:siteId",
    name: "AvailableUnits",
    component: AvailableUnits,
  },
  {
    path: '/payment-plan/:unitId',
    name: 'PaymentPlan',
    component: PaymentPlan,

  },
  {
    path: "/broker/manage-sales",
    name: "ManageSales",
    component: BrkManageSales,
    meta: { requiresAuth: true, role: "broker" },
  },
  {
    path: "/sales-details/:id", // Dynamic route using :id for the sales detail ID
    name: "SalesDetails",
    component: SalesDetailsPage,
    props: true, // Pass route params as props to the component
  },
  {
    path: "/broker/manage-customer",
    name: "ManageCustomers",
    component: BrkManageCustomers,
    meta: { requiresAuth: true, role: "broker" },
  },
  {
    path: "/broker/milestones",
    name: "BrkMilestones",
    component: BrkMilestones,
    meta: { requiresAuth: true, role: "broker" },
  },
   {
    path: "/reserve",
    name: "ReservePage",
    component: ReservePage,
  },

  {
    path: "/broker/account",
    name: "BrkAccounts",
    component: BrkAccounts,
    meta: { requiresAuth: true, role: "broker" },
  },

  {
    path: "/broker/test",
    name: "BrkTest",
    component: BrkTest,
    meta: { requiresAuth: true, role: "broker" },
  },
  { path: "/", redirect: "/home" },
  { path: "/:catchAll(.*)", component: NotFoundComponent },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem("logged_in") === "true";
  const userRole = localStorage.getItem("user_role");

  // Handle routes that require authentication
  if (to.meta.requiresAuth) {
    if (!isLoggedIn) {
      return next({ path: "/home" }); // Redirect to home if not logged in
    }

    // Check if the user role matches the required role
    if (to.meta.role && to.meta.role !== userRole) {
      if (userRole === "developer") {
        return next({ path: "/developer/dashboard" });
      } else if (userRole === "broker") {
        return next({ path: "/broker/dashboard" });
      }
    }
  }

  // Handle login routes; if logged in, redirect to appropriate dashboard
  if ((to.name === "DevLogin" || to.name === "BrkLogin") && isLoggedIn) {
    if (userRole === "developer") {
      return next({ path: "/developer/dashboard" });
    } else if (userRole === "broker") {
      return next({ path: "/broker/dashboard" });
    }
  }

  // If no conditions are met, continue to the next route
  next();
});

export default router;
