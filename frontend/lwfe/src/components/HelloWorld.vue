<template>
  <header>
  <nav class="nav">
      <div class="logo">
        <img src="" alt="" id="poisonous" />
        <h1>LIVWELL</h1>
      </div>
      <div>
        <ul class="nav-links">
          <!-- <li><a href="#about">Sign In</a></li>
          <li><a href="#skills">Join</a></li>
          <li><a href="#projects">Projects</a></li> -->
          <li><a href="#SignIn">SignIn</a></li>
          <li><a href="#join">Join</a></li>
        </ul>
      </div>
    </nav>
  </header>

    <body>
      <section id = "content">
        <div class="searchbar">
          <h1>Find the Perfect Apartment</h1>
          <input type="type">
          <button type="button">Search</button>
          <div class="popular">
            <h2>Popular:</h2>
            <h3>Apartment</h3>
            <h3>Condo</h3>
            <button type="onclick">do</button>
          </div>
        </div>
        <div class="sidepic">
          <img src="https://t3.ftcdn.net/jpg/04/74/05/94/360_F_474059464_qldYuzxaUWEwNTtYBJ44VN89ARuFktHW.jpg" alt="">
        </div>

      </section>

    </body>








<!-- 

  <nav>
    <div>
    <ul class = "navr">
   
      <li class="navr"><a href="">HOME</a></li>
      <li class="navr">ABOUT</li>
      <li class="navr">CONTACTS</li>
      <li class="navr">SWITCH</li>
      <li class="navr"> SIGN IN/OUT</li>
    </ul>
  </div>
  </nav> -->






<!-- 
  <div class="hello">
    <div>
      <p>Find The Perfect Apartment Space For Your School</p>
    </div>

    <div>
      <p>picture</p>
    </div> -->
    <!-- <h1>{{ msg }}</h1>
    <p>
      For a guide and recipes on how to configure / customize this project,<br>
      check out the
      <a href="https://cli.vuejs.org" target="_blank" rel="noopener">vue-cli documentation</a>.
    </p>
    <h3>Installed CLI Plugins</h3>
    <ul>
      <li><a href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-babel" target="_blank" rel="noopener">babel</a></li>
      <li><a href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-eslint" target="_blank" rel="noopener">eslint</a></li>
    </ul>
    <h3>Essential Links</h3>
    <ul>
      <li><a href="https://vuejs.org" target="_blank" rel="noopener">Core Docs</a></li>
      <li><a href="https://forum.vuejs.org" target="_blank" rel="noopener">Forum</a></li>
      <li><a href="https://chat.vuejs.org" target="_blank" rel="noopener">Community Chat</a></li>
      <li><a href="https://twitter.com/vuejs" target="_blank" rel="noopener">Twitter</a></li>
      <li><a href="https://news.vuejs.org" target="_blank" rel="noopener">News</a></li>
    </ul>
    <h3>Ecosystem</h3>
    <ul>
      <li><a href="https://router.vuejs.org" target="_blank" rel="noopener">vue-router</a></li>
      <li><a href="https://vuex.vuejs.org" target="_blank" rel="noopener">vuex</a></li>
      <li><a href="https://github.com/vuejs/vue-devtools#vue-devtools" target="_blank" rel="noopener">vue-devtools</a></li>
      <li><a href="https://vue-loader.vuejs.org" target="_blank" rel="noopener">vue-loader</a></li>
      <li><a href="https://github.com/vuejs/awesome-vue" target="_blank" rel="noopener">awesome-vue</a></li>
    </ul> -->
  <!-- </div> -->
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
.nav-links {
  display: flex;
  align-items: center;
  background-color: rgb(253, 204, 113);
 
  
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
