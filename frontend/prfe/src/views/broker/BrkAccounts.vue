<template>
  <div class="accounts-page">
    <SideNav />
    <div class="content">
      <h1>Accounts</h1>
      <p>Here you can manage your accounts.</p>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue"; // Importing the SideNav component

export default {
  name: "BrkAccounts",
  components: {
    SideNav, // Registering the SideNav component
  },
};
</script>

<style scoped>
.accounts-page {
  display: flex; /* Aligns SideNav and content side by side */
  height: 100vh; /* Full height of the viewport */
}

.content {
  flex: 1; /* Fills remaining space */
  padding: 20px; /* Adds some padding */
  text-align: center; /* Center text in the content area */
}
</style>
