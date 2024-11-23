<template>
  <div class="main-page">
    <SideNav />
    <div class="content">
      <h1>Hi, {{ brokerName }}</h1>
      <p>{{ brokerEmail }}</p>
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";

export default {
  name: "BrkMainPage",
  components: {
    SideNav,
  },
  data() {
    return {
      brokerName: '',   // To store the broker's full name
      brokerEmail: '',  // To store the broker's email
    };
  },
  created() {
    this.fetchBrokerInfo();
  },
  methods: {
    // Fetch the broker info from the backend API
    async fetchBrokerInfo() {
      const brokerId = localStorage.getItem('broker_id');  // Retrieve the logged-in broker's ID from localStorage
      try {
        const response = await fetch(`http://localhost:8000/brokers/${brokerId}/`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`,  // Pass token for authentication
          },
        });
        const data = await response.json();
        if (data.success !== false) {
          this.brokerName = `${data.f_name} ${data.l_name}`;  // Combine first name and last name
          this.brokerEmail = data.email;  // Set email
        } else {
          console.error('Broker info not found or error:', data.message);
        }
      } catch (error) {
        console.error('Error fetching broker info:', error);
      }
    },

    logout() {
      localStorage.removeItem("authToken");
      localStorage.removeItem("logged_in");
      localStorage.removeItem("user_role");
      localStorage.removeItem("user_id");
      localStorage.removeItem("company_id");

      this.$router.push({ path: "/home" });
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

h1 {
  color: #42b983;
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
