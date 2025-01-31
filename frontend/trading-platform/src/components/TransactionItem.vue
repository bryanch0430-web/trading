<template>
  <div class="transaction-item">
    <div class="transaction-content">
      <div>
      <strong :class="typeClass">{{ transaction.type }}</strong>
    </div>

      <div>
        <strong>{{ transaction.assetName }}</strong> 
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
    typeClass() {
      return this.transaction.type === 'Buy' ? 'text-blue' : 'text-red';
    },
  },
};
</script>

<style scoped>

.text-blue {
  color: #addfff;
}

.text-red {
  color: #ff7f7f;
}
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