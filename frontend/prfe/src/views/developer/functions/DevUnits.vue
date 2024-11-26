<template>
  <div class="developer-units-page">
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
  name: "DevFuncUnits",
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
