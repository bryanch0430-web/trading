<!-- src/components/TransactionItem.vue -->
<template>
  <div class="transaction-item">
    <div class="transaction-content">
      <div>
        <strong>{{ transaction.assetName }}</strong> ({{ transaction.type }})
      </div>
      <div>{{ transaction.amount }}</div>
      <div>{{ formattedTime }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TransactionItem',
  props: {
    transaction: {
      type: Object,
      required: true,
    },
  },
  computed: {
    formattedTime() {
      const date = new Date(this.transaction.time);
      return date.toLocaleString();
    },
  },
};
</script>

<style scoped>
.transaction-item {
  background-color: var(--color-panel);
  border-radius: 12px; /* Rounded square */
  padding: 16px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.transaction-content {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.transaction-content > div {
  flex: 1;
  text-align: center;
}
</style>