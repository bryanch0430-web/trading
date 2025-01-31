<!-- src/views/AllAssetsPage.vue -->
<template>
    <div class="container">
      <h1>All Assets</h1>
      <div class="assets-list">
        <div
          v-for="asset in assets"
          :key="asset.id"
          class="asset-item"
          @click="goToAsset(asset.id)"
        >
          <h2>{{ asset.name }}</h2>
          <p><strong>Price:</strong> ${{ asset.currentPrice.toLocaleString() }}</p>
          <p><strong>Market Cap:</strong> ${{ asset.marketCap.toLocaleString() }}</p>
          <p><strong>24h Change:</strong> {{ asset.change24h }}%</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AllAssetsPage',
    data() {
      return {
        assets: [],
      };
    },
    created() {
      // Fetch all assets
      // For now, use mock data
      this.assets = [
        {
          id: 1,
          name: 'Bitcoin',
          currentPrice: 45000,
          marketCap: 850000000000,
          volume24h: 35000000000,
          change24h: 2.5,
        },
        {
          id: 2,
          name: 'Ethereum',
          currentPrice: 3000,
          marketCap: 350000000000,
          volume24h: 20000000000,
          change24h: -1.2,
        },
        {
          id: 3,
          name: 'Binance Coin',
          currentPrice: 400,
          marketCap: 60000000000,
          volume24h: 5000000000,
          change24h: 1.8,
        },
      ];
    },
    methods: {
      goToAsset(id) {
        this.$router.push({ name: 'AssetDisplay', params: { id } });
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    padding: 24px;
    max-width: 800px;
    margin: 0 auto;
  }
  
  h1 {
    color: var(--color-primary);
    margin-bottom: 24px;
  }
  
  .assets-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .asset-item {
    background-color: var(--color-panel);
    border-radius: 12px;
    padding: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.3s ease;
  }
  
  .asset-item:hover {
    background-color: #f0f0f0; /* Light gray on hover */
    transform: scale(1.02);
  }
  
  .asset-item h2 {
    margin: 0 0 8px 0;
  }
  
  .asset-item p {
    margin: 4px 0;
  }
  </style>