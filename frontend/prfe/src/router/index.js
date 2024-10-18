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
  { path: "/devlogin", name: "DevLogin", component: DevLogin },
  { path: "/devforgotpass", name: "DevForgotPass", component: DevForgotPass },
  {
    path: "/devresetpass/:uid/:token",
    name: "DevResetPass",
    component: DevResetPass,
  },
  { path: "/devmain", name: "DevMain", component: DevMainPage },

  // Broker Routes
  { path: "/broklogin", name: "BrkLogin", component: BrkLogin },
  { path: "/brokforgotpass", name: "BrkForgotPass", component: BrkForgotPass },
  {
    path: "/brokresetpass/:uid/:token",
    name: "BrkResetPass",
    component: BrkResetPass,
  },
  { path: "/brokmain", name: "BrkMain", component: BrkMainPage },

  // Redirect
  { path: "/", redirect: "/broklogin" },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
