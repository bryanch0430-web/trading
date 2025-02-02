ListAsset

import { defineStore } from 'pinia';
import { ListAsset } from '../api/assetAPI';

export const useAssetStore = defineStore('transaction', {
  state: () => ({
    assets: [],
  }),
  getters: {
    allAssets(state) {
      return state.assets;
    },
  },
  actions: {
    async ListALLAsset() {
      try {
        const response = await ListAsset();
        this.assets = response; // Adjust based on actual response
      } catch (error) {
        console.error('Error fetching transactions:', error);
      }
    },
  },
});

export default useAssetStore;