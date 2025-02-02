<template>
  <div class="transaction-item">
    <div class="transaction-content">
      <div>
        <strong :class="typeClass">{{ transaction.transaction_type }}</strong>
      </div>
      <div>
        <strong>{{ transaction.asset_name }}</strong> 
      </div>
      <div>{{ transaction.amount }}</div>
      <div>{{ transaction.price }}</div>
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
      const date = new Date(this.transaction.timestamp); // Updated here
      return isNaN(date) ? 'Invalid Date' : date.toLocaleString();
    },
    typeClass() {
      const type = this.transaction.transaction_type;
      switch(type) {
        case 'buy':
          return 'text-blue';
        case 'sell':
          return 'text-red';
        case 'withdraw':
          return 'text-yellow';
        case 'deposit':
          return 'text-green';
        default:
          return '';
      }
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