<template>
  <div class="container">
    <h1>User Transactions</h1>
    <div v-if="transactions.length">
      <div v-for="transaction in transactions" :key="transaction.id">
        <TransactionItem :transaction="transaction" />
      </div>
    </div>
    <div v-else>
      <p>No transactions found.</p>
    </div>
  </div>
</template>

<script>
import { onMounted, computed } from 'vue';
import { useTransactionStore } from '../store/transactionStore'; 
import TransactionItem from '../components/TransactionItem.vue';

export default {
  components: {
    TransactionItem,
  },
  setup() {
    const transactionStore = useTransactionStore();

    const transactions = computed(() => transactionStore.allTransactions);

    onMounted(() => {
      transactionStore.fetchUserTransactions();
    });

    return {
      transactions,
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