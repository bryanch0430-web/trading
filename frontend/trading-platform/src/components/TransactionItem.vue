<template>
  <div class="transaction-item">
    <div class="transaction-content">
      <div>
      <strong :class="typeClass">{{ transaction.transaction_type }}</strong>
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
      if (this.transaction.transaction_type === 'buy') {
        return 'text-blue';
      } else if (this.transaction.transaction_type === 'sell') {
        return 'text-red';
      } else if (this.transaction.transaction_type === 'withdraw') {
        return 'text-yellow';
      } else if (this.transaction.transaction_type === 'deposit') {
        return 'text-green';
      }
      return '';
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
.text-yellow {
  color: #ffd700; /* Yellow */
}

.text-green {
  color: #32cd32; /* Lime green */
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