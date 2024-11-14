<!-- src/components/Header.vue -->
<template class="body">

<HeaderLivwell/>

<section>
  <h1 class="p-5">hello</h1>
</section>

<footer class="bg-dark footer">
    <div class="footer-top">
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
import HeaderLivwell from './HeaderLivwell.vue';



  export default {
    name: "AboutUs",
    components: {
    HeaderLivwell,
  },
  };
  </script>
  
  <style scoped>
.body
{
  width: 100%;
  height: 100%;
}

 /* .navbar
 {
    background-color: #FAD566;
    padding-top: 10px;  
  }

 .navbar-brand{
  justify-content: flex-start
 }

 .navbar-nav
 {
  padding-left: 85%;
 }

 .nav-item
 {
  padding-right: 20px;
 } */

 
  </style>
  