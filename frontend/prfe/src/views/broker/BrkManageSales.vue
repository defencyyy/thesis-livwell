<template>
  <header>
    <HeaderLivwell/>
  </header>
  <div class="manage-sales-page">
    <SideNav />
    <div class="content">
        <h1>Welcome to the Manage Sales Page</h1>
        <p>This is where you can manage sales data for brokers and developers.</p>
    </div>
  </div>
</template>

<script>
import HeaderLivwell from "@/components/HeaderLivwell.vue";
import SideNav from "@/components/SideNav.vue";

export default {
    name: "ManageSales",
    components: {
    SideNav, HeaderLivwell
  },
};
</script>

<style scoped>
.manage-sales-page {
  display: flex;
  height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}
</style>
