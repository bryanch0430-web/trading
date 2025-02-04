<template>
  <div class="container">
    <h1>User Transactions</h1>

    <div class="transaction-item">
    <div class="transaction-content">
      <div>
        <strong :class="typeClass">Transaction type</strong>
      </div>
      <div>
        <strong>Asset Name</strong> 
      </div>
      <div><strong>Transaction Amount</strong></div>
      <div><strong>Price(USD)</strong></div>
      <div><strong>Time</strong></div>
    </div>
  </div>

    <!-- Show loading spinner while data is being fetched -->
    <div v-if="loading" class="loading-spinner">
      <p>Loading transactions...</p>
      <!-- Add a spinner or animation here -->
    </div>

    <!-- Show transactions once data is loaded -->
    <div v-else>
      <div v-if="transactions?.length">
        <div v-for="transaction in transactions" :key="transaction.id">
          <TransactionItem :transaction="transaction" />
        </div>
      </div>
      <div v-else>
        <p>No transactions found.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useTransactionStore } from '../store/transactionStore';
import TransactionItem from '../components/TransactionItem.vue';

// Use the Pinia store
const transactionStore = useTransactionStore();

// Fetch transactions when the component is mounted
onMounted(async() => {
  await transactionStore.fetchUserTransactions();
});

// Compute transactions and loading state from the store
const transactions = computed(() => transactionStore.allTransactions);
const loading = computed(() => transactionStore.loading); // Get the loading state
</script>


<style scoped>
.container {
  padding: 24px;
}
h1 {
  color: var(--color-primary);
  margin-bottom: 24px;
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
