<template class="all">
 
    <nav class="navbar navbar-expand-lg  fixed-top mask-custom shadow-0 ">
        <div class="container">
            <a class="navbar-brand" href="./HomeView.vue"><span style="color: black;">Liv</span><span style="color: #fff;">Well</span></a>
            <button class="navbar-toggler" type="button" data-mdb-toggle="collapse"
                data-mdb-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                aria-label="Toggle navigation">
                <i class="fas fa-bars"></i>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
            </div>
        </div>
    </nav>

<section class="home-section">
    <div class="d-flex justify-content-evenly align-items-center bg-secondary home-container">
        <div class="home text-white">
            <p class="mt-5 fs-3 text-uppercase">Go to</p>
            <h1 class="display-1 fw-bolder text-capitalize">DEVELOPER</h1>
            <div class="button-container">
            <button @click="goToDeveloperLogin" class="text-uppercase">Developer Login</button>
            </div>
        </div>
        <div class="home text-white">
            <p class="mt-5 fs-3 text-uppercase">Go to</p>
            <h1 class="display-1 fw-bolder text-capitalize">BROKER</h1>
            <div class="button-container">
            <button @click="goToBrokerLogin" class="text-uppercase">Broker Login</button>
            </div>
        </div>
    </div>
</section>


<footer class="bg-dark footer">
    <div class="footer-top py-8">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 text-start">
                    <h1 class="text-white footer-title-01 fs-5">LivWell</h1>
                    <div>
                        <p class="fs-sm text-white text-opacity-75">Official Website of LivWell</p>
                    </div>
                </div>
                <div class="col-lg-8 text-start ">
                    <div class="row gy-5">
                        <div class="col-6 col-lg-4 text-start ">
                            <h5 class="text-white footer-title-01">Contact Us</h5>
                            <ul class="list-unstyled footer-link-01 m-0 pb-2">
                                <h6 class="text-white text-opacity-75"><b>Email:</b> LivWell@gmail.com</h6>
                             
                            </ul>
                            <ul class="list-unstyled footer-link-01 m-0">
                                <h6 class="text-white text-opacity-75"><b>Phone:</b> 092-2421-432</h6>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="footer-bottom small py-3 border-top border-white border-opacity-10">
        <div class="container">
            <div class="row">
                <div class="col-md-6 text-center text-md-start py-1">
                    <p class="m-0 text-white text-opacity-75">© Copyright. All Rights Reserved <a class="text-reset" href="#">Livwell</a></p>
                </div>
            </div>
        </div>
    </div>
</footer>


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
/* NAVBAR SECTION  */
.navbar{ 
  background-color: rgb(131, 255, 131);
}
.navbar a{
    font-size: 20px;
}
/* NAVBAR SECTION  */

/* HOME SECTION */

    .home-container {
        background-image:  linear-gradient(to bottom, rgba(255, 255, 255, 0.4), rgba(0, 0, 0, 0.7)), 
        url('https://i.pinimg.com/originals/fc/ac/19/fcac194ad03f8af8dfaf702db8db5b0f.jpg');
        background-size: cover;
        background-position: center;
        min-height: 75vh; /* Ensure the container takes up at least full viewport height */
        position: relative;
        padding: 0; /* Adjust padding as needed */
    }

    /* Optional: Dark overlay to improve text readability */
    .home-container.bg-secondary {
        background-color: rgba(0, 0, 0, 0.5); /* Dark overlay for contrast */
    }

    /* Ensure text and buttons are above the background */
    .home {
        position: relative;
        z-index: 2;
    }

    .home-container .home p,
    .home-container .home h1,
    .home-container .button-container {
        position: relative;
        z-index: 2;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7); 
    }

    /* HOME BUTTON */
    .button-container button {
        background-color:rgb(131, 255, 131);
        color: #000;
        border: none;
        padding: 10px 25px;  /* Adjust the padding for top/bottom and left/right */
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
        transition: background-color 0.3s ease;  /* Optional: smooth hover effect */
        margin-top: 20px;
    }

    .button-container button:hover {
        background-color: #ddd; /* Change color on hover */
    }
/* HOME SECTION */




/* footer */
.wrapper>* {
     flex: 0 0 auto;
 }

 a {
     text-decoration: none;
     background-color: transparent;
 }

 .py-8 {
     padding-top: 3.5rem !important;
     padding-bottom: 3.5rem !important;
 }

 .footer-title-01 {
     font-size: 10px;
     margin: 0 0 20px;
     font-weight: 600;
 }

 .footer-title-01 {
     font-size: 16px;
     margin: 0 0 20px;
     font-weight: 600
 }
/* footer */



</style>

