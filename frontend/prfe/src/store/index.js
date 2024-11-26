// store/index.js
import { createStore } from "vuex";

export default createStore({
  state: {
    userId: localStorage.getItem("user_id") || null,
    userType: localStorage.getItem("user_role") || null,
    companyId: localStorage.getItem("company_id") || null,
    loggedIn: localStorage.getItem("logged_in") === "true",
    authToken: localStorage.getItem("authToken") || null, // Store auth token
  },
  getters: {
    isLoggedIn: (state) => state.loggedIn,
    getUserType: (state) => state.userType,
    getUserId: (state) => state.userId,
    getCompanyId: (state) => state.companyId,
    getAuthToken: (state) => state.authToken,
  },
  mutations: {
    setUser(state, user) {
      state.userId = user.id;
      state.userType = user.user_role;
      state.companyId = user.company_id;
      state.loggedIn = true;

      // Store in localStorage and Vuex
      localStorage.setItem("user_id", user.id);
      localStorage.setItem("user_role", user.user_role);
      localStorage.setItem("company_id", user.company_id);
      localStorage.setItem("logged_in", "true");
    },
    setAuthToken(state, authToken) {
      state.authToken = authToken;
      localStorage.setItem("authToken", authToken); // Store authToken in localStorage
    },
    clearUser(state) {
      state.userId = null;
      state.userType = null;
      state.companyId = null;
      state.loggedIn = false;
      state.authToken = null;

      localStorage.removeItem("user_id");
      localStorage.removeItem("user_role");
      localStorage.removeItem("company_id");
      localStorage.removeItem("authToken");
      localStorage.setItem("logged_in", "false");
    },
  },
  actions: {
    login({ commit }, { user, token }) {
      commit("setUser", user);
      commit("setAuthToken", token);
    },
    logout({ commit }) {
      commit("clearUser");
    },
  },
});
