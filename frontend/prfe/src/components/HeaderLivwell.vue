<!-- src/components/Header.vue -->
<template>
    <nav class="navbar navbar-expand-lg navbar-black ">
      <div class="container">
        <a class="navbar-brand" href="#">MyApp</a>
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
              <a class="nav-link" href="#">Services</a>
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
    background-color: #42b983;
 }
  </style>
  