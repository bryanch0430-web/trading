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
          if (typeof data === 'object' && !Array.isArray(data)) {
            this.assets = Object.values(data);
          } else if (Array.isArray(data)) {
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
          this.assetDistribution = data;
        } catch (error) {
          console.error('Error in calculateUserAsset:', error);
          this.error = 'Failed to calculate user asset distribution.';
        } finally {
          this.loading = false;
        }
      },
      async createAsset(label) {
        this.loading = true;
        this.error = null;
        try {
            const payload={
              "label":label
            }
          const data = await assetAPI.createAsset(payload);
        } catch (error) {
          console.error("Error creating asset:", error);
          this.error = "Failed to create asset.";
        } finally {
          this.loading = false;
        }
      },
      
    },
  });
  
  export default useAssetStore;



