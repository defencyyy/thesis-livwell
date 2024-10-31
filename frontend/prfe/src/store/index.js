import { createStore } from "vuex";

export default createStore({
  state: {
    userId: localStorage.getItem("user_id") || null, // Changed from userId to user_id
    userType: localStorage.getItem("user_role") || null, // Changed from userType to user_role
    loggedIn: localStorage.getItem("logged_in") === "true", // Changed from loggedIn to logged_in
  },
  getters: {
    isLoggedIn: (state) => state.loggedIn,
    getUserType: (state) => state.userType,
    getUserId: (state) => state.userId,
  },
  mutations: {
    setUser(state, user) {
      state.userId = user.id;
      state.userType = user.user_role; // Changed from user_type to user_role
      state.loggedIn = true;

      // Store in localStorage
      localStorage.setItem("user_id", user.id); // Changed from userId to user_id
      localStorage.setItem("user_role", user.user_role); // Changed from userType to user_role
      localStorage.setItem("logged_in", "true"); // Changed from loggedIn to logged_in
    },
    clearUser(state) {
      state.userId = null;
      state.userType = null;
      state.loggedIn = false;

      // Clear from localStorage
      localStorage.removeItem("user_id"); // Changed from userId to user_id
      localStorage.removeItem("user_role"); // Changed from userType to user_role
      localStorage.setItem("logged_in", "false"); // Changed from loggedIn to logged_in
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
