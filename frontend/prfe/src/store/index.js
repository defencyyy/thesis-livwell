import { createStore } from "vuex";

export default createStore({
  state: {
    userId: localStorage.getItem("user_id") || null,
    userType: localStorage.getItem("user_role") || null,
    companyId: localStorage.getItem("company_id") || null,
    loggedIn: localStorage.getItem("logged_in") === "true",
    authToken: localStorage.getItem("authToken") || null, // Store the token here
  },
  getters: {
    isLoggedIn: (state) => state.loggedIn,
    getUserType: (state) => state.userType,
    getUserId: (state) => state.userId,
    getCompanyId: (state) => state.companyId,
    getAuthToken: (state) => state.authToken, // Getter to access the token
  },
  mutations: {
    setUser(state, user) {
      console.log("Setting user in Vuex:", user); // Debugging line
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
    setAuthToken(state, token) {
      state.authToken = token;
      localStorage.setItem("authToken", token); // Store token in localStorage as well
    },
    clearUser(state) {
      state.userId = null;
      state.userType = null;
      state.companyId = null;
      state.loggedIn = false;
      state.authToken = null; // Clear the token

      // Clear from localStorage
      localStorage.removeItem("user_id");
      localStorage.removeItem("user_role");
      localStorage.removeItem("company_id");
      localStorage.removeItem("authToken"); // Remove token from localStorage
      localStorage.setItem("logged_in", "false");
    },
  },
  actions: {
    login({ commit }, { user, token }) {
      console.log("User data at login:", user); // Debugging line
      commit("setUser", user);
      commit("setAuthToken", token); // Store the token after login
    },
    logout({ commit }) {
      commit("clearUser");
    },
  },
  modules: {},
});
