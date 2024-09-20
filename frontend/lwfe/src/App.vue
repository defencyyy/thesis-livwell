<template>
  <NavLWFE/>
  <AboutLWFE msg="Welcome"/>
  <SearchLWFE/>
  <HelloWorld msg="Welcome to Your Vue.js App"/>

  


</template>

<script>

import AboutLWFE from './components/AboutLWFE.vue';
import HelloWorld from './components/HelloWorld.vue';
import NavLWFE from './components/NavLWFE.vue';
import SearchLWFE from './components/SearchLWFE.vue';






export default {
  name: 'App',
  components: {
    HelloWorld, 
    AboutLWFE,
    NavLWFE,
    SearchLWFE
   
  }
}
</script>

<style>

* {
  margin: 0;
  padding: 0;
  text-decoration: none;
}
</style>
