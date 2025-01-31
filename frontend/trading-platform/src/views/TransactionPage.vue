<!-- src/views/TransactionPage.vue -->
<template>
    <div class="container">
      <h1>User Transactions</h1>
      <div v-for="transaction in transactions" :key="transaction.id">
        <TransactionItem :transaction="transaction" />
      </div>
    </div>
  </template>
  
  <script>
  import TransactionItem from '../components/TransactionItem.vue';
  
  export default {
    name: 'TransactionPage',
    components: {
      TransactionItem,
    },
    data() {
      return {
        transactions: [
          // Mock data
          {
            id: 1,
            assetName: 'Bitcoin',
            type: 'Buy',
            time: '2023-08-01T10:00:00Z',
            amount: 0.5,
          },
          {
            id: 2,
            assetName: 'Ethereum',
            type: 'Sell',
            time: '2023-08-02T14:30:00Z',
            amount: 2,
          },
          // Add more transactions as needed
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  .container {
    padding: 24px;
  }
  h1 {
    color: var(--color-primary);
    margin-bottom: 24px;
  }
  </style>