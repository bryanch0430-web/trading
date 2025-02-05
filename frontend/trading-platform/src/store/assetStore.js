import { defineStore } from 'pinia';
import assetAPI from '../api/assetAPI';

export const useAssetStore = defineStore('asset', {
    state: () => ({
      assets: null,
      loading: false,
      error: null,
      currentAsset:null,
      assetDistribution: null
    }),
    getters: {
      allAssets: (state) => state.assets,
      getAssetById: (state) => (id) => state.assets.find((asset) => asset.id === id),
      getcurrentAsset: (state) => state.currentAsset, // Corrected here
      getAssetDistribution: (state) => state.assetDistribution
    },
    actions: {
      async fetchAllAssets() {
        this.loading = true;
        this.error = null;
        try {
          const data = await assetAPI.ListAsset();
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
      async getAssetPrice(assetId) {
        this.loading = true;
        this.error = null;
        try {
          const data = await assetAPI.ListAssetPrice(assetId);
          this.currentAsset = data;
          
          console.log(`Fetched price for asset ID ${assetId}:`, this.currentAsset);

        } catch (error) {
          console.error('Error in fetchAssetPrice:', error);
          this.error = 'Failed to fetch asset price.';
        } finally {
          this.loading = false;
        }
      },
      async fetchUserAssets(userId) {
        this.loading = true;
        this.error = null;
        try {
          const data = await assetAPI.getUserAssets(userId);
          console.log(`Fetched assets for user ${userId}:`, data);
  
          if (Array.isArray(data)) {
            this.assets = data;
          } else if (typeof data === 'object') {
            this.assets = Object.values(data);
          } else {
            this.assets = [data];
          }
        } catch (error) {
          console.error("Error in fetchUserAssets:", error);
          this.error = 'Failed to fetch user assets.';
        } finally {
          this.loading = false;
        }
      },
      
      async calculateUserAsset(userId) {
        this.loading = true;
        this.error = null;
        try {
          const data = await assetAPI.calculateUserAsset(userId);
          console.log('API Response:', data);
          this.assetDistribution = data;
        } catch (error) {
          console.error('Error in calculateUserAsset:', error);
          this.error = 'Failed to calculate user asset distribution.';
        } finally {
          this.loading = false;
        }
      },
      
    },
  });
  
  export default useAssetStore;

