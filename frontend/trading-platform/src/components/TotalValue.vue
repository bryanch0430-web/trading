<!-- src/components/TotalValue.vue -->
<template>
  <div class="card">
    <h2>Total Value</h2>
    <p>${{ totalValue }}</p>
  </div>
</template>

<script>
export default {
  name: 'TotalValue',
  props: {
    totalValue: {
      type: Number,
      required: true,
    },
  },
};
</script>

<style scoped>
.card {
  background-color: var(--color-panel);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  text-align: center;
}
</style>