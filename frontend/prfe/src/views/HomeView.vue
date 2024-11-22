<template>
  <div class="home">
    <img alt="Vue logo" src="@/assets/logo.png" />
    <h1>Welcome to LivWell!</h1>
    <p>Explore listings or manage your properties with ease.</p>

    <div class="button-container">
      <button @click="goToDeveloperLogin">Developer Login</button>
      <button @click="goToBrokerLogin">Broker Login</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  methods: {
    goToDeveloperLogin() {
      this.$router.push("/developer/login");
    },
    goToBrokerLogin() {
      this.$router.push("/broker/login");
    },
  },
};
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}

.button-container {
  margin-top: 20px;
}

button {
  margin: 0 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  background-color: #4caf50;
  color: white;
  border-radius: 5px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #45a049;
}
</style>
