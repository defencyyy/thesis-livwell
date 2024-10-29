<template>
  <div class="developer-account-page">
    <SideNav />
    <div class="content">
      <h1>title</h1>
      <p>desc</p>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";

export default {
  name: "DevFuncAccount",
  components: {
    SideNav,
  },
};
</script>

<style scoped>
.milestones-page {
  display: flex;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}
</style>
