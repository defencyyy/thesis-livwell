<!-- src/components/Header.vue -->
<template>
    <nav class="navbar navbar-expand-lg navbar-black ">
      <div class="container">
        <a class="navbar-brand" href="#">Welcome Back, Broker!</a>
        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item active">
              <a class="nav-link" href="#">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">About</a>
            </li>
            <li class="nav-item">
              <img src="../assets/bell.png" alt="" width="25px" height="30px" href="#" type="button">
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Contact</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>

  export default {
    name: "HeaderLivwell",
  };
  </script>
  
  <style scoped>
 .navbar
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
 }
  </style>
  