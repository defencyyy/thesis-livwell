import { createRouter, createWebHashHistory } from "vue-router";

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
  // Developer Routes
  { path: "/developer/login", name: "DevLogin", component: DevLogin },
  {
    path: "/developer/forgot-password",
    name: "DevForgotPass",
    component: DevForgotPass,
  },
  {
    path: "/developer/reset-password/:uid/:token",
    name: "DevResetPass",
    component: DevResetPass,
  },
  { path: "/developer/dashboard", name: "DevMain", component: DevMainPage },

  // Broker Routes
  { path: "/broker/login", name: "BrkLogin", component: BrkLogin },
  {
    path: "/broker/forgot-password",
    name: "BrkForgotPass",
    component: BrkForgotPass,
  },
  {
    path: "/broker/reset-password/:uid/:token",
    name: "BrkResetPass",
    component: BrkResetPass,
  },
  { path: "/broker/dashboard", name: "BrkMain", component: BrkMainPage },

  // Redirect
  { path: "/", redirect: "/broker/login" },


const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
