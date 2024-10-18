import { createRouter, createWebHashHistory } from "vue-router";

// Landing views

// Broker views
import BrkLogin from "@/views/broker/BrkLogin.vue";
import BrkMainPage from "@/views/broker/BrkMainPage.vue";
import BrkForgotPass from "@/views/broker/BrkForgotPass.vue";
import BrkResetPass from "@/views/broker/BrkResetPass.vue";

// Developer views
import DevLogin from "@/views/developer/DevLogin.vue";
import DevMainPage from "@/views/developer/DevMainPage.vue";
import DevForgotPass from "@/views/developer/DevForgotPass.vue";
import DevResetPass from "@/views/developer/DevResetPass.vue";

// Layout components
import BrokerLayout from "@/components/BrokerLayout.vue";
import DeveloperLayout from "@/components/DeveloperLayout.vue";

const routes = [
  // Broker routes
  {
    path: "/broker",
    name: "Broker",
    component: BrokerLayout,
    children: [
      { path: "login", name: "BrkLogin", component: BrkLogin },
      { path: "main", name: "BrkMain", component: BrkMainPage },
      { path: "forgotpass", name: "BrkForgotPass", component: BrkForgotPass },
      {
        path: "resetpass/:uid/:token",
        name: "BrkResetPass",
        component: BrkResetPass,
      },
    ],
  },

  // Developer routes
  {
    path: "/developer",
    name: "Developer",
    component: DeveloperLayout,
    children: [
      { path: "login", name: "DevLogin", component: DevLogin },
      { path: "main", name: "DevMain", component: DevMainPage },
      { path: "forgotpass", name: "DevForgotPass", component: DevForgotPass },
      {
        path: "resetpass/:uid/:token",
        name: "DevResetPass",
        component: DevResetPass,
      },
    ],
  },

  // Redirect root to broker login *MAKE HOME PAGE
  { path: "/", redirect: "/broker/login" },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
