import { createStore } from "vuex";

export default createStore({
  state: {
    userId: localStorage.getItem("user_id") || null,
    userType: localStorage.getItem("user_role") || null,
    companyId: localStorage.getItem("company_id") || null,
    loggedIn: localStorage.getItem("logged_in") === "true",
  },
  getters: {
    isLoggedIn: (state) => state.loggedIn,
    getUserType: (state) => state.userType,
    getUserId: (state) => state.userId,
    getCompanyId: (state) => state.companyId,
  },
  mutations: {
    setUser(state, user) {
      state.userId = user.id;
      state.userType = user.user_role;
      state.companyId = user.company_id;
      state.loggedIn = true;

      // Store in localStorage
      localStorage.setItem("user_id", user.id);
      localStorage.setItem("user_role", user.user_role);
      localStorage.setItem("company_id", user.company_id);
      localStorage.setItem("logged_in", "true");
    },
    clearUser(state) {
      state.userId = null;
      state.userType = null;
      state.companyId = null;
      state.loggedIn = false;

      // Clear from localStorage
      localStorage.removeItem("user_id");
      localStorage.removeItem("user_role");
      localStorage.removeItem("company_id"); // Clear companyId
      localStorage.setItem("logged_in", "false");
    },
  },
  actions: {
    login({ commit }, user) {
      commit("setUser", user);
    },
    logout({ commit }) {
      commit("clearUser");
    },
  },
  modules: {},
});
