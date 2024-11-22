<template class="all">
 
 <nav class="navbar navbar-expand-lg navbar-light fixed-top mask-custom shadow-0">
    <div class="container">
        <a class="navbar-brand" href="./HomeView.vue"><span style="color: black;">Liv</span><span style="color: #fff;">Well</span></a>
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
                <li class="nav-item dropdown">
                   <router-link to="/AboutUs"><a class="nav-link" href="">About</a></router-link> 
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



<section class="hero overlay">
    <div id="hero-carousel" class="carousel slide overlay" data-bs-ride="carousel">
        <div class="carousel-indicators">
            <button type="button" data-bs-target="#hero-carousel" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
            <button type="button" data-bs-target="#hero-carousel" data-bs-slide-to="1" aria-label="Slide 2"></button>
        </div>
        <div class="carousel-inner">
            <!-- First Slide -->
            <div class="carousel-item active c-item">
            <img src="https://i.pinimg.com/originals/fc/ac/19/fcac194ad03f8af8dfaf702db8db5b0f.jpg" class="d-block w-100 c-img" alt="Slide 1">
            <div class="carousel-caption top-0 mt-4">
                <p class="mt-5 fs-3 text-uppercase">Go to</p>
                <h1 class="display-1 fw-bolder text-capitalize">DEVELOPER</h1>
                <button @click="goToDeveloperLogin" class="bton btn-primary px-4 py-2 fs-5 mt-5">Developer Login</button>
            </div>
            
            
            </div>
            
            <!-- Second Slide -->
            <div class="carousel-item c-item">
            <img src="https://3.bp.blogspot.com/-QZdUc9EHQAw/VNSUfEba57I/AAAAAAAAB7k/AZhy1zYsiWI/s1600/Amenity%2BCore.jpg" class="d-block w-100 c-img" alt="Slide 2">
            <div class="carousel-caption top-0 mt-4">
                <p class="text-uppercase fs-3 mt-5">Go to</p>
                <p class="display-1 fw-bolder text-capitalize">BROKER</p>
                <button @click="goToBrokerLogin" class="bton btn-primary px-4 py-2 fs-5 mt-5" >Broker Login</button>
            </div>
            </div>
        </div>
        <!-- Carousel Controls -->
        <button class="carousel-control-prev" type="button" data-bs-target="#hero-carousel" data-bs-slide="prev">
            <span class="carousel-control-prev-icon"></span>
            <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#hero-carousel" data-bs-slide="next">
            <span class="carousel-control-next-icon"></span>
            <span class="visually-hidden">Next</span>
        </button>
    </div>
</section>

<footer class="bg-dark footer">
    <div class="footer-top py-8">
        <div class="container">
            <div class="row gy-5">
                <div class="col-lg-4 text-start">
                    <h1 class="text-white footer-title-01 fs-5">LivWell</h1>
                    <div>
                        <p class="fs-sm text-white text-opacity-75">Official Website of LivWell</p>
                    </div>
                </div>
                <div class="col-lg-8 pe-xxl-10">
                    <div class="row gy-5">
                        <div class="col-6 col-lg-4 text-start">
                            <h5 class="text-white footer-title-01">Useful Links</h5>
                            <ul class="list-unstyled footer-link-01 m-0">
                                <li><a class="text-white text-opacity-75" href="#">About Us</a></li>
                                <li><a class="text-white text-opacity-75" href="#">Gallery</a></li>
                                <li><a class="text-white text-opacity-75" href="#">Offers</a></li>
                                <li><a class="text-white text-opacity-75" href="#">FAQ'S</a></li>
                                <li><a class="text-white text-opacity-75" href="#">Features</a></li>
                            </ul>
                        </div>
                        <div class="col-6 col-lg-4 text-start">
                            <h5 class="text-white footer-title-01">About</h5>
                            <ul class="list-unstyled footer-link-01 m-0">
                                <li><a class="text-white text-opacity-75" href="#">Customer Service</a></li>
                                <li><a class="text-white text-opacity-75" href="#">Privacy Policy</a></li>
                                <li><a class="text-white text-opacity-75" href="#">Cookie Policy</a></li>
                                <li><a class="text-white text-opacity-75" href="#">Terms &amp; Conditions</a></li>
                                <li><a class="text-white text-opacity-75" href="#">Terms of Use</a></li>
                            </ul>
                        </div>
                        <div class="col-6 col-lg-4 text-start">
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
                 <div class="col-md-6 text-center text-md-end py-1">
                    <ul class="nav justify-content-center justify-content-md-end list-unstyled footer-link-01 m-0">
                        <li class="p-0 mx-3 ms-md-0 me-md-3"><a href="#" class="text-white text-opacity-75">Privace &amp; Policy</a></li>
                        <li class="p-0 mx-3 ms-md-0 me-md-3"><a href="#" class="text-white text-opacity-75">Faq's</a></li>
                        <li class="p-0 mx-3 ms-md-0 me-md-3"><a href="#" class="text-white text-opacity-75">Get a Quote</a></li>
                    </ul>
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
.home {
  text-align: center;
  margin-top: 120px;
  margin-bottom: 100px;
  
}

.button-container {
  margin-top: 20px;
}

button {
  /* margin: 0 10px; */
  /* padding: 10px 20px; */
  font-size: 16px;
  cursor: pointer;
  border: none;
  /* background-color: #FFE79E; */
  color: black;
  border-radius: 5px;
  transition: background-color 0.3s;
}

nav{
  background-color: #FFE79E;
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

.bods {
    padding-top: 5%;
    padding-bottom: 5%;
}

/* ABOUT */

.features-icons
{
    animation: fade-up 5s;
}

.showcase
{
    animation: fade-up 3s;
}


/* FEATURES */
.card-title:hover{
   cursor: pointer;
    color: #FFE79E;
}

/* FAQ */
body{margin-top:20px;}
.accordion-style .card {
    background: transparent;
    box-shadow: none;
    margin-bottom: 15px;
    margin-top: 0 !important;
    border: none;
}
.accordion-style .card:last-child {
    margin-bottom: 0;
}
.accordion-style .card-header {
    border: 0;
    background: none;
    padding: 0;
    border-bottom: none;
}
.accordion-style .btn-link {
    color: #ffffff;
    position: relative;
    background: #15395a;
    border: 1px solid #15395a;
    display: block;
    width: 100%;
    font-size: 18px;
    border-radius: 3px;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
    text-align: left;
    white-space: normal;
    box-shadow: none;
    padding: 15px 55px;
    text-decoration: none;
}
.accordion-style .btn-link:hover {
    text-decoration: none;
}
.accordion-style .btn-link.collapsed {
    background: #ffffff;
    border: 1px solid #15395a;
    color: #1e2022;
    border-radius: 3px;
}
.accordion-style .btn-link.collapsed:after {
    background: none;
    border-radius: 3px;
    content: "+";
    left: 16px;
    right: inherit;
    font-size: 20px;
    font-weight: 600;
    line-height: 26px;
    height: 26px;
    transform: none;
    width: 26px;
    top: 15px;
    text-align: center;
    background-color: #15395a;
    color: #fff;
}
.accordion-style .btn-link:after {
    background: #fff;
    border: none;
    border-radius: 3px;
    content: "-";
    left: 16px;
    right: inherit;
    font-size: 20px;
    font-weight: 600;
    height: 26px;
    line-height: 26px;
    transform: none;
    width: 26px;
    top: 15px;
    position: absolute;
    color: #15395a;
    text-align: center;
}
.accordion-style .card-body {
    padding: 20px;
    border-top: none;
    border-bottom-right-radius: 3px;
    border-bottom-left-radius: 3px;
    /* border-left: 1px solid #15395a;
    border-right: 1px solid #15395a;
    border-bottom: 1px solid #15395a; */
}
@media screen and (max-width: 767px) {
    .accordion-style .btn-link {
        padding: 15px 40px 15px 55px;
    }
}
@media screen and (max-width: 575px) {
    .accordion-style .btn-link {
        padding: 15px 20px 15px 55px;
    }
}
.card-style1 {
    box-shadow: 0px 0px 10px 0px rgb(89 75 128 / 9%);
}
.border-0 {
    border: 0!important;
}
.card {
    position: relative;
    display: flex;
    flex-direction: column;
    min-width: 0;
    word-wrap: break-word;
    background-color: #fff;
    background-clip: border-box;
    border: 1px solid rgba(0,0,0,.125);
    border-radius: 0.25rem;
}

.FAQ {
    padding: 120px 0;
    overflow: hidden;
    background: #fff;
}
.mb-2-3, .my-2-3 {
    margin-bottom: 2.3rem;
}

.section-title {
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
    position: relative;
    display: inline-block;

}
.text-primary {
    color: #ceaa4d !important;
}



/* 
footer */
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

 .footer-link-01 li+li {
     padding-top: 0.8rem;
 }

 .footer-title-01 {
     font-size: 16px;
     margin: 0 0 20px;
     font-weight: 600;
 }

 .footer-title-01 {
     font-size: 16px;
     margin: 0 0 20px;
     font-weight: 600
 }

 .footer-link-01 li+li {
     padding-top: .8rem
 }

 @media (max-width: 991.98px) {
     .footer-link-01 li+li {
         padding-top: .6rem
     }
 }

 .footer-link-01 a {
     position: relative;
     display: inline-block;
     vertical-align: top
 }

 .footer-link-01 a:after {
     content: "";
     position: absolute;
     bottom: 0;
     left: auto;
     right: 0;
     width: 0;
     height: 1px;
     transition: ease all .35s;
     background: currentColor
 }

 .footer-link-01 a:hover:after {
     left: 0;
     right: auto;
     width: 100%
 }


 /* FEATURES ANIMATION */
 @keyframes appear {
        from {
          opacity: 0;
          clip-path: inset(-100%);
        }
        to {
          opacity: 1;
          clip-path: inset(0 0 0 0);
        }
      }
  
      .logos, .imgpic, .cards {
        animation: appear linear;
        animation-timeline: view();
        animation-range: entry 0% cover 50%;
      }



/* LOGIN CSS      */
.hero {
  min-block-size: 80vh;
  place-content: center;
  text-align: center;
  animation: fade-up 1s;
}
.home
{
    animation: fade-up 2s;
}

.c-item {
  height: 780px;
}

.c-img {
  height: 100%;
  object-fit: cover;
  filter: brightness(0.6);
}
.bton{
 background-color: #FFE79E;
}
.bton:hover{
    background-color: white;
}







</style> -->

