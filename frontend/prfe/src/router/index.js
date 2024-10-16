import { createRouter, createWebHashHistory } from "vue-router";

// Broker views
import BrokLogin from "@/views/broker/BrokLogin.vue";
import BrokMainPage from "@/views/broker/BrokMainPage.vue";
import BrokForgotPass from "@/views/broker/BrokForgotPass.vue";
import BrokResetPass from "@/views/broker/BrokResetPass.vue";

// Developer views
import DevLogin from "@/views/developer/DevLogin.vue";
import DevMainPage from "@/views/developer/DevMainPage.vue";
import DevForgotPass from "@/views/developer/DevForgotPass.vue";
import DevResetPass from "@/views/developer/DevResetPass.vue";

const routes = [
  // Broker routes
  { path: "/broklogin", name: "BrokLogin", component: BrokLogin },
  { path: "/brokmain", name: "BrokMain", component: BrokMainPage },
  {
    path: "/brokforgotpass",
    name: "BrokForgotPass",
    component: BrokForgotPass,
  },
  {
    path: "/brokresetpass/:uid/:token",
    name: "BrokResetPass",
    component: BrokResetPass,
  },

  // Developer routes
  { path: "/devlogin", name: "DevLogin", component: DevLogin },
  { path: "/devmain", name: "DevMain", component: DevMainPage },
  { path: "/devforgotpass", name: "DevForgotPass", component: DevForgotPass },
  {
    path: "/devresetpass/:uid/:token",
    name: "DevResetPass",
    component: DevResetPass,
  },

  // Redirect root to broker login
  { path: "/", redirect: "/broklogin" },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
