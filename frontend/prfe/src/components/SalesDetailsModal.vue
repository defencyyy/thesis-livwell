<template>
  <div class="modal" v-if="isVisible">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h3>Sold Dates</h3>
      <ul>
        <li v-for="date in soldDates" :key="date">{{ date }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isVisible: Boolean,
    soldDates: Array,
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: white;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  cursor: pointer;
  float: right;
  font-size: 28px;
}
</style>
