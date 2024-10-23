import { createRouter, createWebHashHistory } from "vue-router";

import Home from "@/views/HomeView.vue";
import About from "@/views/AboutView.vue";

// Developers
import DevLogin from "@/views/developer/DevLogin.vue";
import DevForgotPass from "@/views/developer/DevForgotPass.vue";
import DevResetPass from "@/views/developer/DevResetPass.vue";
import DevMainPage from "@/views/developer/DevMainPage.vue";

// Brokers
import BrkLogin from "@/views/broker/BrkLogin.vue";
import BrkForgotPass from "@/views/broker/BrkForgotPass.vue";
import BrkResetPass from "@/views/broker/BrkResetPass.vue";
import BrkMainPage from "@/views/broker/BrkMainPage.vue";

const routes = [
  { path: "/home", name: "Home", component: Home },
  { path: "/about", name: "About", component: About },

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

  // Redirect
  { path: "/", redirect: "/home" },
];

const router = createRouter({
  history: createWebHashHistory(),
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

  // Always proceed to the next route
  next();
});

export default router;
