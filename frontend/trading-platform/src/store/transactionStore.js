import { defineStore } from 'pinia';
import transactionAPI from '../api/transactionAPI';

export const useTransactionStore = defineStore('transaction', {
  state: () => ({
    transactions: [],
    loading: false,
  }),
  getters: {
    allTransactions(state) {
      return state.transactions;
    },
  },
  actions: {
    async fetchUserTransactions(user_id = '2fb3c95f-0250-4c9c-8194-0e22bdf1ae32') {
      this.loading = true;
      try {
        const response = await transactionAPI.fetchTransactions(user_id);
        this.transactions = response;
      } catch (error) {
        console.error('Error fetching transactions:', error);
      } finally {
        this.loading = false; 
      }
    },
  },
});
export default useTransactionStore;
