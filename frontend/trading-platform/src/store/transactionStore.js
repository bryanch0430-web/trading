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
    async makeDeposit(depositData) {
      this.loading = true;
      this.error = null;
      try {
        const transaction = await transactionAPI.depositTransaction(depositData);
        // Optionally, update the state by adding the new transaction to the transactions list
        //this.transactions.push(transaction);
        return transaction;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async makeWithdraw(withdrawData) {
      this.loading = true;
      this.error = null;
      try {
        const transaction = await transactionAPI.withdrawTransaction(withdrawData);
                //this.transactions.push(transaction);

        return transaction;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async makeBuy(buyData) {
      this.loading = true;
      this.error = null;
      try {
        const transaction = await transactionAPI.buyTransaction(buyData);
                //this.transactions.push(transaction);

        return transaction;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async makeSell(sellData) {
      this.loading = true;
      this.error = null;
      try {
        const transaction = await transactionAPI.sellTransaction(sellData);

          //this.transactions.push(transaction);

        return transaction;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
  },
});
export default useTransactionStore;

