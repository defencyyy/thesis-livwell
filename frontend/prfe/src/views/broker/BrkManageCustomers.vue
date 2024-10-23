<template>
  <div class="manage-customers-page">
    <SideNav />
    <div class="content">
      <h1>Manage Customers</h1>
      <p>Here you can view and manage your customers.</p>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue"; // Importing the SideNav component

export default {
  name: "ManageCustomers",
  components: {
    SideNav, // Registering the SideNav component
  },
};
</script>

<style scoped>
.manage-customers-page {
  display: flex; /* Aligns SideNav and content side by side */
  height: 100vh; /* Full height of the viewport */
}

.content {
  flex: 1; /* Fills remaining space */
  padding: 20px; /* Adds some padding */
  text-align: center; /* Center text in the content area */
}
</style>
