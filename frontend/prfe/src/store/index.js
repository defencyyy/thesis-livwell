import { createStore } from "vuex";

export default createStore({
  state: {
    userId: localStorage.getItem("user_id") || null,
    userType: localStorage.getItem("user_role") || null,
    firstName: localStorage.getItem("first_name") || null, // Store first_name in state
    companyId: localStorage.getItem("company_id") || null,
    company: {}, // Add company to the state
    loggedIn: localStorage.getItem("logged_in") === "true",
    authToken: localStorage.getItem("authToken") || null,
  },
  getters: {
    isLoggedIn: (state) => state.loggedIn,
    getUserType: (state) => state.userType,
    getUserId: (state) => state.userId,
    getFirstName: (state) => state.firstName,
    getCompanyId: (state) => state.companyId,
    getAuthToken: (state) => state.authToken,
    getCompany: (state) => state.company,
    getCompanyName: (state) => state.company.name || null,
    getCompanyLogo: (state) => state.company.logo || null,
  },
  mutations: {
    setUser(state, user) {
      state.userId = user.id;
      state.userType = user.user_role;
      state.companyId = user.company_id;
      state.company = user.company; // Store company objec
      state.loggedIn = true;

      // Store in localStorage and Vuex
      localStorage.setItem("user_id", user.id);
      localStorage.setItem("user_role", user.user_role);
      localStorage.setItem("first_name", user.first_name); // Store first_name
      localStorage.setItem("company_id", user.company_id);
      localStorage.setItem("company", JSON.stringify(user.company)); // Store entire company object
      localStorage.setItem("logged_in", "true");
    },
    setCompany(state, company) {
      state.company = company; // Store company in Vuex
    },
    setAuthToken(state, authToken) {
      state.authToken = authToken;
      localStorage.setItem("authToken", authToken);
    },
    clearUser(state) {
      state.userId = null;
      state.userType = null;
      state.companyId = null;
      state.loggedIn = false;
      state.authToken = null;
      state.company = {}; // Clear company data
      localStorage.removeItem("user_id");
      localStorage.removeItem("user_role");
      localStorage.removeItem("first_name");
      localStorage.removeItem("company_id");
      localStorage.removeItem("company"); // Remove entire company object
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
      // Clear everything from localStorage and Vuex
      commit("clearUser");
      localStorage.removeItem("refreshToken");
      this.$router.push({ name: "Home" }); // Redirect to home or login page
    },
    setCompany({ commit }, company) {
      console.log("Setting company in Vuex:", company); // Log the company data
      commit("setCompany", company); // Set company data
    },
  },
});
