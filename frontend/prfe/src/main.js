import { createApp } from "vue";
import App from "./App.vue";
import SideNav from "./components/SideNav.vue";
import router from "./router";
import store from "./store";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import "bootstrap-vue-3/dist/bootstrap-vue-3.css";

// Create the app instance
const app = createApp(App);

// Register the SideNav component globally
app.component("SideNav", SideNav);

// Use router and store, then mount the app
app.use(router).use(store).mount("#app");
