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

<section>
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
</section>


<section class="features-icons bg-light text-center">
          <p class="fs-1">FEATURES</p>
            <div class="container">
                <div class="row">
                    <div class="col-lg-4">
                        <div class="features-icons-item mx-auto mb-5 mb-lg-0 mb-lg-3">
                            <div class="features-icons-icon d-flex"><i class="bi-window m-auto text-primary"></i></div>
                            <img src="../assets/instagram.png" alt="instagram" style="width: 30%; height: 30%; padding-bottom: 20px;">
                            <h3>Fully Responsive</h3>
                            <p class="lead mb-0">This theme will look great on any device, no matter the size!</p>
                        </div>
                    </div>
                    <div class="col-lg-4">
                        <div class="features-icons-item mx-auto mb-5 mb-lg-0 mb-lg-3">
                            <div class="features-icons-icon d-flex"><i class="bi-layers m-auto text-primary"></i></div>
                            <img src="../assets/instagram.png" alt="instagram" style="width: 30%; height: 30%; padding-bottom: 20px;">
                            <h3>Bootstrap 5 Ready</h3>
                            <p class="lead mb-0">Featuring the latest build of the new Bootstrap 5 framework!</p>
                        </div>
                    </div>
                    <div class="col-lg-4">
                        <div class="features-icons-item mx-auto mb-0 mb-lg-3">
                            <div class="features-icons-icon d-flex"><i class="bi-terminal m-auto text-primary"></i></div>
                            <img src="../assets/instagram.png" alt="instagram" style="width: 30%; height: 30%; padding-bottom: 20px;">
                            <h3>Easy to Use</h3>
                            <p class="lead mb-0">Ready to use with your own content, or customize the source files!</p>
                        </div>
                    </div>
                </div>
            </div>
</section>

<section class="showcase">
            <div class="container-fluid p-0">
                <div class="row g-0">
                    <div class="col-lg-6 order-lg-2 text-white showcase-img" style="background-image: url('https://i.pinimg.com/originals/a5/4a/49/a54a49b134fb37f98478d7d029feac14.jpg'); background-size: cover; background-position: center; background-repeat: no-repeat;"></div>
                    <div class="col-lg-6 order-lg-1 my-auto showcase-text ">
                        <h2 style="padding-top: 125px;">Fully Responsive Design</h2>
                        <p class="lead mb-0" style="padding-top: 25px; margin: 0px 60px; text-align: left;">When you use a theme created by Start Bootstrap, you know that the theme will look great on any device, whether it's a phone, tablet, or desktop the page will behave responsively!</p>
                    </div>
                </div>
                <div class="row g-0">
                    <div class="col-lg-6 text-white showcase-img" style="background-image: url('https://i.pinimg.com/originals/a5/4a/49/a54a49b134fb37f98478d7d029feac14.jpg'); background-size: cover; background-position: center; background-repeat: no-repeat;"></div>
                    <div class="col-lg-6 my-auto showcase-text">
                        <h2 style="padding-top: 125px;">Updated For Bootstrap 5</h2>
                        <p class="lead mb-0" style="padding-top: 25px;">Newly improved, and full of great utility classes, Bootstrap 5 is leading the way in mobile responsive web development! All of the themes on Start Bootstrap are now using Bootstrap 5!</p>
                    </div>
                </div>
                <div class="row g-0">
                    <div class="col-lg-6 order-lg-2 text-white showcase-img" style="background-image: url('https://i.pinimg.com/originals/a5/4a/49/a54a49b134fb37f98478d7d029feac14.jpg'); background-size: cover; background-position: center; background-repeat: no-repeat;"></div>
                    <div class="col-lg-6 order-lg-1 my-auto showcase-text">
                        <h2 style="padding-top: 125px;">Easy to Use & Customize</h2>
                        <p class="lead mb-0" style="padding-top: 25px; margin: 0px 60px; text-align: left;">Landing Page is just HTML and CSS with a splash of SCSS for users who demand some deeper customization options. Out of the box, just add your content and images, and your new landing page will be ready to go!</p>
                    </div>
                </div>
            </div>
        </section>


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

.features-icons
{
  padding-top: 50px;
}

.fs-1
{
  font-family:Verdana, Geneva, Tahoma, sans-serif;
}

.col-lg-6
{
  height: 480px;
}
</style>
