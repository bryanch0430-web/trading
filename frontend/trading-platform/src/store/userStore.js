import { defineStore } from 'pinia';
import userAPI from '../api/userAPI';

export const useUserStore = defineStore('user', {
  state: () => ({
    userAsset: [],
    loading: false, // Add a loading state
  }),
  getters: {
    allAsset(state) {
      return state.userAsset;
    },
  },
  actions: {
    async fetchUserAssets(user_id = '2fb3c95f-0250-4c9c-8194-0e22bdf1ae32') {
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
  },
});

export default useUserStore;
