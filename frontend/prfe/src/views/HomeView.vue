<template>
 
 <nav class="navbar navbar-expand-lg navbar-light fixed-top mask-custom shadow-0">
    <div class="container">
        <a class="navbar-brand" href="#!"><span style="color: black;">Liv</span><span style="color: #fff;">Well</span></a>
        <button class="navbar-toggler" type="button" data-mdb-toggle="collapse"
            data-mdb-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
            aria-label="Toggle navigation">
            <i class="fas fa-bars"></i>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mx-auto"> <!-- Center the nav items -->
                <li class="nav-item">
                    <a class="nav-link" href="#!">Offer</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#!">Features</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#!">About</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#!">Team</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#!">Contact</a>
                </li>
            </ul>
            <ul class="navbar-nav d-flex flex-row">
                <li class="nav-item me-3 me-lg-0">
                    <a class="nav-link" href="#!">
                        <i class="fas fa-shopping-cart"></i>
                    </a>
                </li>
                <li class="nav-item me-3 me-lg-0">
                    <a class="nav-link" href="#!">
                      <img src="../assets/facebook.png" alt="facebook" style="width: 30px; height: 30px;">
                    </a>
                </li>
                <li class="nav-item me-3 me-lg-0">
                    <a class="nav-link" href="#!">
                      <img src="../assets/instagram.png" alt="instagram" style="width: 30px; height: 30px;">
                    </a>
                </li>
            </ul>
        </div>
    </div>
</nav>


  <div class="d-flex justify-content-evenly bg-secondary">

  <div class="home text-white">
    <img alt="Vue logo" src="@/assets/logo.png"/>
    
    <h1>Welcome to LivWell!</h1>
    <p>Explore listings or manage your properties with ease.</p>

    <div class="button-container">
      <button @click="goToDeveloperLogin">Developer Login</button>
    
    </div>
  </div>

  <div class="home">
    <img alt="Vue logo" src="@/assets/logo.png" />
    <h1>Welcome to LivWell!</h1>
    <p>Explore listings or manage your properties with ease.</p>

    <div class="button-container">

      <button @click="goToBrokerLogin">Broker Login</button>
    </div>
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
  margin-top: 120px;
  margin-bottom: 100px;
  
}

/* .homes
{
  display: flex;
} */
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

nav{
  background-color: #4caf50;
}
</style>
