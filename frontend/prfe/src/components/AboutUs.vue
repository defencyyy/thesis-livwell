<!-- src/components/Header.vue -->
<template class="abtus">
 <section>
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

</section>


<section class="hero overlay">
  <h1 class="display-5 fw-bolder text-capitalize">About Us</h1>
  <div>
    <div class="herop">
        <RouterLink to="/home" ><p class="textmg text-star fw-bolder text-capitalize">Home/ </p></RouterLink>
        <p class="textmg text-start fw-bolder text-capitalize"> About</p>
    
    </div>
  </div>
</section>


<section class="about">
    <div class="container">
        <div class="row">
            <!-- First Item -->
            <div class="col-12 pb-5">
                <div class="main">
                    <img src="https://th.bing.com/th/id/OIP.BCJ2MktPMdWOpYimWIw88wHaKl?w=600&h=857&rs=1&pid=ImgDetMain" alt="Image 1">
                    <div class="about-text">
                        <h1>About Us</h1>
                        <h5>Monitoring of Sites, Units, Customers, and Brokers </h5>
                        <p> Stay on top of every detail with our comprehensive monitoring tools. Our system allows you to track and manage condo sites, units, and customer data in real time. You can easily monitor the progress of each site, track available units, and keep a close eye on customer interactions. Additionally, the broker management features allow you to oversee broker performance, ensuring that each partner is aligned with your sales and marketing goals.
                        </p>
                      
                    </div>
                </div>
            </div>
            <!-- Second Item -->
            <div class="col-12 pb-5">
                <div class="main">
                    <img src="https://th.bing.com/th/id/OIP.BCJ2MktPMdWOpYimWIw88wHaKl?w=600&h=857&rs=1&pid=ImgDetMain " alt="Image 2">
                    <div class="about-text">
                        <h1>About Us</h1>
                        <h5>Management of Units to Customers</h5>
                        <p> Our intuitive platform simplifies the process of managing and assigning condo units to customers. Whether you're dealing with pre-sale, under-construction, or completed units, our system provides a clear and organized way to manage unit availability, customer preferences, and transaction histories. With real-time updates and a user-friendly interface, you can ensure smooth and timely unit allocation to customers, improving satisfaction and reducing operational delays.</p>
                     
                    </div>
                </div>
            </div>
            <!-- Third Item -->
            <div class="col-12">
                <div class="main">
                    <img src="https://th.bing.com/th/id/OIP.BCJ2MktPMdWOpYimWIw88wHaKl?w=600&h=857&rs=1&pid=ImgDetMain " alt="Image 3">
                    <div class="about-text">
                        <h1>About Us</h1>
                        <h5>Management of Sales and Commissions </h5>
                        <p>Efficiently manage sales transactions and commissions with our robust sales management tools. Track every sale from initial inquiry to closing, and seamlessly calculate commissions for brokers and agents. Our system automates commission structures, ensuring that all payouts are accurate and timely. With detailed reporting features, you can easily analyze sales performance and monitor broker productivity, enabling better decision-making and optimized business growth.</p>
                       
                    </div>
                </div>
            </div>
        </div>
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
    name: "AboutUs",
    components: {
  
  },
  };
  </script>
  

  <style scoped>
.body
{
  width: 100%;
  height: 100%;

}
.abtus
{
    height: 100%;
    width: 100%;
}

nav{
  background-color: #FFE79E;
}

.overlay {
  border-image: linear-gradient(hsla(0, 0%, 65%, 0.6), hsla(57, 100%, 75%, 0.6))
    fill 1;
}

.hero {
  background-image: url("https://images.unsplash.com/photo-1697229299093-c920ab53bfb1?crop=entropy&cs=srgb&fm=jpg&ixid=M3wzMjM4NDZ8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MTU2OTIzNzZ8&ixlib=rb-4.0.3&q=85");
  background-size: cover;
  background-repeat: no-repeat;

  min-block-size: 30vh;
  place-content: center;
  text-align: center;
}

/* .herop
{
    border-image: linear-gradient(hsla(0, 0%, 65%, 0.6), hsla(57, 100%, 75%, 0.6))
    fill 1;
    width: 100%;
    position: absolute; 
    padding-top: 15px;
    margin-top: 58px;
    padding-left: 450px;
    font-size: large;
   
    display: flex;
}

.herop p
{
    color: rgb(255, 255, 255);
} */

@layer general-styling {
  html {
    color-scheme: dark light;
    font-family: system-ui;
    line-height: 1.6;
  }

  body {
    font-size: 2rem;
    margin: 1rem;
  }

  h1 {
    line-height: 1;
  }
}


/* .textabt
{
    padding-left: 500px;
    padding-right: 500px;
}

.textabt p
{
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
} */



/* RESPONSIVENESS */



/* ROUTER-LINK */

.herop {
    border-image: linear-gradient(hsla(0, 0%, 65%, 0.6), hsla(57, 100%, 75%, 0.6)) fill 1;
    width: 100%;
    position: absolute;
    padding-top: 15px;
    margin-top: 68px;
    padding-bottom: 10px;
    font-size: large;
    display: flex;
    padding-left: 450px;
    
}


/*about*/
@import url('https://fonts.googleapis.com/css2?family=Hind&family=Poppins:ital,wght@0,200;0,300;0,400;0,500;0,600;1,200&display=swap');

* {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    font-family: 'Josefin Sans', sans-serif;
}

.about {
    width: 100%;
    padding: 78px 0;
    background-color: white;
}

.about img {
    height: 480px; /* Adjust image size to fit the container */
    width: 50%; /* Make the image responsive */
    border-radius: 15px;
    object-fit: cover; /* Ensures image covers the container proportionally */
}

.about-text {
    width: 100%;
    text-align: center;
    padding: 20px; /* Adds spacing between text and image */
}

.main {
    margin-bottom: 50px; /* Adds space between sections */
    text-align: center; /* Center content inside the main div */
}

.about-text h1 {
    color: rgb(0, 0, 0);
    font-size: 30px; /* Adjust font size for responsive design */
    text-transform: uppercase;
    margin-bottom: 20px;
}

.about-text h5 {
    color: rgb(0, 0, 0);
    font-size: 20px;
    text-transform: capitalize;
    margin-bottom: 25px;
    letter-spacing: 2px;
}

span {
    color: #ffde23;
}

.about-text p {
    /* color: rgba(0, 0, 0, 0.8);
    letter-spacing: 1px;
    line-height: 28px;
    font-size: 16px;
    margin-bottom: 45px; */
    
    color: rgba(0, 0, 0, 0.8);
    letter-spacing: 1px;
    line-height: 28px;
    font-size: 16px;
    margin-bottom: 45px;
    background-color: white; /* Set background to white */
    padding: 15px; /* Add padding to create space inside the p tag */
    border-radius: 10px; /* Round the corners of the p tag */
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); /* Add a subtle shadow */
    transition: all 0.3s ease; /* Smooth transition for hover effect */

}

button {
    background: #f9b700;
    color: rgb(0, 0, 0);
    text-decoration: none;
    border: 2px solid transparent;
    font-weight: bold;
    padding: 13px 30px;
    border-radius: 30px;
    transition: .4s;
}

button:hover {
    background: transparent;
    border: 2px solid #f9f500;
    cursor: pointer;
}

/* Bootstrap Grid Adjustments */
@media (max-width: 768px) {
    .about-text h1 {
        font-size: 24px; /* Smaller heading size on tablets */
    }

    .about-text h5 {
        font-size: 18px; /* Smaller subtitle on tablets */
    }

    .about-text p {
        font-size: 14px; /* Smaller paragraph text on tablets */
    }

    .about img {
        height: 250px; /* Adjust image size on smaller screens */
    }
}

/* For Mobile Screens */
@media (max-width: 480px) {
    .about-text h1 {
        font-size: 20px; /* Smaller heading on mobile */
    }

    .about-text h5 {
        font-size: 16px; /* Smaller subtitle on mobile */
    }

    .about-text p {
        font-size: 14px; /* Smaller paragraph on mobile */
    }

    .about img {
        height: 200px; /* Smaller image size on mobile */
    }

    .main {
        margin-bottom: 20px; /* Adjust margin between sections on mobile */
    }
}



/* 
FOOTER  */

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

  </style>
  