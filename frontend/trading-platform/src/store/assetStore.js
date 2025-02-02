import { defineStore } from 'pinia';
import { ListAsset } from '../api/assetAPI';

export const useAssetStore = defineStore('asset', {
    state: () => ({
      assets: null,
      loading: false,
      error: null,
    }),
    getters: {
      allAssets: (state) => state.assets,
      getAssetById: (state) => (id) => state.assets.find((asset) => asset.id === id),
    },
    actions: {
      async fetchAllAssets() {
        this.loading = true;
        this.error = null;
        try {
          const data = await ListAsset();
          console.log(data);
          
          // **Transform Data Here**
  
          // If `data` is an object with numeric keys
          if (typeof data === 'object' && !Array.isArray(data)) {
            this.assets = Object.values(data);
          } else if (Array.isArray(data)) {
            // If it's a sparse array, filter out `undefined` items
            this.assets = data.filter(asset => asset != null);
          } else {
            this.assets = data; // Fallback
          }
        } catch (error) {
          this.error = 'Failed to fetch assets.';
        } finally {
          this.loading = false;
        }
      },
    },
  });
  
  export default useAssetStore;