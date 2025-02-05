import { defineStore } from 'pinia';
import userAPI from '../api/userAPI';

export const useUserStore = defineStore('user', {
  state: () => ({
    userAsset: [],
    valueTrend:[],
    loading: false, // Add a loading state
  }),
  getters: {
    allAsset(state) {
      return state.userAsset;
    },
    getValueTrend(state) {
      return state.valueTrend;
    },
  },
  actions: {
    async fetchUserAssets(user_id) {
      this.loading = true; // Set loading to true when fetching starts
      try {
        const response = await userAPI.ListUserAsset(user_id);
        this.userAsset = response;
      } catch (error) {
        console.error('Error fetching transactions:', error);
      } finally {
        this.loading = false; // Set loading to false when fetching ends
      }
    },

    async ShowUserValueTrend(user_id) {
      this.loading = true; // Set loading to true when fetching starts
      try {
        const response = await userAPI.ShowUserValueTrend(user_id);
        this.valueTrend = response;
      } catch (error) {
        console.error('Error fetching transactions:', error);
      } finally {
        this.loading = false; // Set loading to false when fetching ends
      }
    },
  },
});

export default useUserStore;
