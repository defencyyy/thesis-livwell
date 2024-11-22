<template>
 
    <nav class="navbar navbar-expand-lg navbar-light fixed-top mask-custom shadow-0">
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
                <!-- <div class="col-md-6 text-center text-md-end py-1">
                    <ul class="nav justify-content-center justify-content-md-end list-unstyled footer-link-01 m-0">
                        <li class="p-0 mx-3 ms-md-0 me-md-3"><a href="#" class="text-white text-opacity-75">Privace &amp; Policy</a></li>
                        <li class="p-0 mx-3 ms-md-0 me-md-3"><a href="#" class="text-white text-opacity-75">Faq's</a></li>
                        <li class="p-0 mx-3 ms-md-0 me-md-3"><a href="#" class="text-white text-opacity-75">Get a Quote</a></li>
                    </ul>
                </div> -->
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
