<!-- src/views/AssetDisplayPage.vue -->
<template>
    <div class="container">
      <button class="button" @click="$router.back()">Back</button>
      <h1>{{ asset.name }} Details</h1>
      <div class="asset-details">
        <p><strong>Current Price:</strong> ${{ asset.currentPrice }}</p>
        <p><strong>Market Cap:</strong> ${{ asset.marketCap }}</p>
        <p><strong>24h Volume:</strong> ${{ asset.volume24h }}</p>
        <p><strong>Change (24h):</strong> {{ asset.change24h }}%</p>
        <!-- Add more details as needed -->
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AssetDisplayPage',
    props: ['id'],
    data() {
      return {
        asset: {},
      };
    },
    created() {
      // Fetch asset details based on the ID
      // For now, use mock data
      const mockAssets = {
        1: {
          name: 'Bitcoin',
          currentPrice: 45000,
          marketCap: 850000000000,
          volume24h: 35000000000,
          change24h: 2.5,
        },
        2: {
          name: 'Ethereum',
          currentPrice: 3000,
          marketCap: 350000000000,
          volume24h: 20000000000,
          change24h: -1.2,
        },
        // Add more assets as needed
      };
      this.asset = mockAssets[this.id] || {};
    },
  };
  </script>
  
  <style scoped>
  .container {
    padding: 24px;
  }
  h1 {
    color: var(--color-primary);
    margin: 16px 0;
  }
  .asset-details {
    background-color: var(--color-panel);
    border-radius: 12px;
    padding: 16px;
  }
  .button {
    margin-bottom: 16px;
  }
  </style>