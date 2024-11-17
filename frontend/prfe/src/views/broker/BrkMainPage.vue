<template>
  <HeaderLivwell />
  <div class="main-page">
    <SideNav />
    <div class="content">
      <div>
        <h1>Gwynn Rafer Cujardo</h1>
        <h5>@gwynncujardo</h5>
        <p>This is the main page for brokers.</p>
        <button @click="logout">Logout</button>
      </div>

      <div class="contentpage py-5 mx-2" style="width: 100%; height: 80%">
        <div>
          <div class="content1" style="height: 30%"><h2>Total Sales:</h2></div>
          <div class="content2" style="height: 30%">
            <h2>Milestones Achieved:</h2>
          </div>
          <div class="content4">
            <h2>Broker of the Month</h2>
            <div>
              <img
                src="https://th.bing.com/th/id/OIP.2nSUJDGTSglEgp0sQw_R8AHaKu?rs=1&pid=ImgDetMain"
                alt=""
                width="250px"
                height="200px"
              />
            </div>
          </div>
        </div>
        <div>
          <div class="content3"><h2>Analytics</h2></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
// import AppHeader from "@/components/Header.vue";
import HeaderLivwell from "@/components/HeaderLivwell.vue";
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "BrkMainPage",
  components: {
    SideNav,
    HeaderLivwell,
    // AppHeader,
  },
  computed: {
    ...mapState({
      userId: (state) => state.userId || null,
      userType: (state) => state.userType || null,
      companyId: (state) => state.companyId || null,
      loggedIn: (state) => state.loggedIn, // Use Vuex loggedIn state
    }),
    localStorageUserId() {
      return localStorage.getItem("user_id");
    },
    localStorageCompanyId() {
      return localStorage.getItem("company_id");
    },
  },
  mounted() {
    if (!this.loggedIn || this.userType !== "broker" || !this.companyId) {
      this.redirectToLogin();
    }
  },
  watch: {
    loggedIn(newVal) {
      if (!newVal || this.userType !== "broker" || !this.companyId) {
        this.redirectToLogin();
      }
    },
    userType(newVal) {
      if (newVal !== "broker" || !this.companyId) {
        this.redirectToLogin();
      }
    },
    companyId(newVal) {
      if (!newVal || this.userType !== "broker") {
        this.redirectToLogin();
      }
    },
  },
  methods: {
    async logout() {
      try {
        // Notify backend about logout
        await axios.post(
          "http://localhost:8000/api/token/brklogout/", // Update URL to match backend endpoint
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        // Clear localStorage and Vuex state
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("broker_id");
        localStorage.removeItem("company_id");

        // Call Vuex mutation to reset user state
        this.$store.commit("clearUser");

        // Redirect to login page
        this.redirectToLogin();
      } catch (error) {
        console.error("Error during logout:", error);
        alert("Logout failed. Please try again.");
      }
    },

    redirectToLogin() {
      this.$router.push({ name: "BrkLogin" });
    },
  },
};
</script>

<style scoped>
.main-page {
  display: flex;
  height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}
.contentpage {
  border: 1px solid black;
}
.content h1,
h5 {
  color: black;
  text-align: left;
  padding-left: 50px;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}

.content1,
.content2 {
  text-align: left;
  background-color: #d9d9d9;
  height: 30%;
  border-radius: 10px;
  padding-left: 10px;
  margin-bottom: 20px;
  margin-right: 20px;
  margin-left: 50px;
}
.content1 h2,
.content2 h2 {
  padding-right: 30px;
}
.content3 {
  text-align: center;
  background-color: #d9d9d9;
  border-radius: 10px;
  padding-left: 10px;
  margin-bottom: 20px;
  margin-right: 20px;
  margin-left: 20px;
  height: 60%;
  width: 500%;
}
.content3 h2 {
  text-align: center;
  padding-top: 20px;
}

.content4 {
  background-color: #d9d9d9;
  border-radius: 10px;
  height: 40%;
  width: 200%;
  margin-bottom: 20px;
  margin-right: 20px;
  margin-left: 50px;
  padding-left: 20px;
  text-align: start;
}
.content img {
  margin-left: 10px;
}
.contentpage {
  display: flex;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #ff1a1a;
}
</style>
