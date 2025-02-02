import { defineStore } from 'pinia';
import { fetchTransactions } from '../api/transactionAPI';

export const useTransactionStore = defineStore('transaction', {
  state: () => ({
    transactions: [],
  }),
  getters: {
    allTransactions(state) {
      return state.transactions;
    },
  },
  actions: {
    async fetchUserTransactions(user_id = '2fb3c95f-0250-4c9c-8194-0e22bdf1ae32') {
      try {
        const response = await fetchTransactions(user_id);
        this.transactions = response.data; // Adjust based on actual response
      } catch (error) {
        console.error('Error fetching transactions:', error);
      }
    },
  },
});

export default useTransactionStore;