<template>
  <NavLWFE/>
  <AboutLWFE msg="Welcome"/>
  <SearchLWFE/>
  <HelloWorld msg="Welcome to Your Vue.js App"/>
  <FooterLWFE/>

  


</template>

<script>

import AboutLWFE from './components/AboutLWFE.vue';
import HelloWorld from './components/HelloWorld.vue';
import NavLWFE from './components/NavLWFE.vue';
import SearchLWFE from './components/SearchLWFE.vue';
import FooterLWFE from './components/FooterLWFE.vue';






export default {
  name: 'App',
  components: {
    HelloWorld, 
    AboutLWFE,
    NavLWFE,
    SearchLWFE,
    FooterLWFE
   
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
