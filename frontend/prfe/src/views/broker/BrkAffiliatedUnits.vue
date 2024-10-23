<template>
  <div class="affiliated-units-page">
    <SideNav />
    <div class="content">
      <h1>Welcome to Affiliated Units</h1>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue"; // Importing the SideNav component

export default {
  name: "AffiliatedUnits",
  components: {
    SideNav, // Registering the SideNav component
  },
};
</script>

<style scoped>
.affiliated-units-page {
  display: flex; /* Aligns SideNav and content side by side */
  height: 100vh; /* Full height of the viewport */
}

.content {
  flex: 1; /* Fills remaining space */
  padding: 20px; /* Adds some padding */
  text-align: center; /* Center text in the content area */
}
</style>
