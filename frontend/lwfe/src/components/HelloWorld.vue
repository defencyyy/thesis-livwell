<template>
  <header>
   <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
    <div class="container">
      <a href="" class="navbar-brand">LIVWELL</a>
      
      
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collape" data-bs-targer="#navmenu">
        <span class="navbar-toggler-icon"></span>
      </button>


      <div class="collapse navbar-collapse" id="navmenu">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item ">
            <a href="" class="nav-link">About</a>
          </li>
          <li class="nav-item">
            <a href="" class="nav-link">About</a>
          </li>
          <li class="nav-item">
            <a href="" class="nav-link">About</a>
          </li>
        </ul>
      </div>
    </div>
    
   </nav>
  </header>

    <body>
      
      <div class="p-3 mb-2 bg-primary-subtle text-primary-emphasis" style="width: 100%; height: 100%;"></div>

    </body>









</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->


<style>
@import url("https://fonts.googleapis.com/css2?family=Francois+One&display=swap");



nav,
.logo,
.nav-links{
  /* display: flex;
  align-items: center; */
  /* background-color: rgb(253, 204, 113); */
  
  
}








body
{
  background-color: rgb(189, 189, 189);
  width: 100%;
  height: 100%;
}
.logo{
  padding-right: 20%;
  font-family: "Francois One", sans-serif;
  font-size: larger;
}
nav {
  justify-content: space-around;
  height: 10vh;
  margin-bottom: 0.5in;
}

.nav-links {
  padding-left: 20%;
  gap: 5rem;
  list-style: none;
  font-size: 1.5rem;
}

#content
{
  display: flex;
  gap: 30rem;
  justify-content: center;
  padding-top: 3%;
  
}

#content h1
{
  font-family: "Francois One", sans-serif;
  font-weight: 400;
  font-style: normal;
  font-size: 40px
  
}

input
{
  width: 100%;
  height: 10%;
  border: none;

}

button
{
  background-color: green;
  color: black;
  border: none;
  width: 25%;
  height: 15%;
  font-family: "Francois One", sans-serif;
  font-weight: 400;
  font-style: normal;
  font-size: large;
  cursor: pointer;
}

.popular
{
  display: flex;
  padding-top: 20px;
  gap: 2rem;
}

h3
{
  border: 1px solid rgb(0, 0, 0);
  padding: 3px 3px 3px 3px;
}

/* .hello
{
  display: flex;
}
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
} */
</style>
