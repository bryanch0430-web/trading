<!-- src/views/AssetDisplayPage.vue -->
<template>
  <div class="container">
    <button class="button" @click="$router.back()">Back</button>
    <h1>{{ asset.name }} Details</h1>
    <div class="asset-details">
      <p><strong>Current Price:</strong> ${{ asset.currentPrice.toLocaleString() }}</p>
      <p><strong>Market Cap:</strong> ${{ asset.marketCap.toLocaleString() }}</p>
      <p><strong>24h Volume:</strong> ${{ asset.volume24h.toLocaleString() }}</p>
      <p><strong>Change (24h):</strong> {{ asset.change24h }}%</p>
      <!-- Add more details as needed -->
    </div>

    <!-- Trading Section -->
    <div class="trading-section">
      <h2>Trade {{ asset.name }}</h2>
      <div class="input-group">
        <label for="amount">Amount:</label>
        <input
          v-model.number="amount"
          id="amount"
          type="number"
          min="0"
          placeholder="Enter amount"
        />
      </div>
      <div class="button-group">
        <button class="buy-button" @click="buyAsset" :disabled="!isValidAmount">
          Buy
        </button>
        <button class="sell-button" @click="sellAsset" :disabled="!isValidAmount">
          Sell
        </button>
      </div>
      <div v-if="message" :class="['message', messageType]">
        {{ message }}
      </div>
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
      amount: 0,
      message: '',
      messageType: '', // 'success' or 'error'
    };
  },
  computed: {
    isValidAmount() {
      return this.amount > 0;
    },
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
  methods: {
    buyAsset() {
      // Placeholder for buy functionality
      // In a real application, you'd integrate with a backend or wallet service
      if (this.isValidAmount) {
        // Example: Calculate total cost
        const totalCost = this.amount * this.asset.currentPrice;
        this.message = `Successfully bought ${this.amount} ${this.asset.name} for $${totalCost.toLocaleString()}.`;
        this.messageType = 'success';
        this.amount = 0; // Reset amount
      } else {
        this.message = 'Please enter a valid amount to buy.';
        this.messageType = 'error';
      }
    },
    sellAsset() {
      // Placeholder for sell functionality
      // In a real application, you'd integrate with a backend or wallet service
      if (this.isValidAmount) {
        // Example: Calculate total revenue
        const totalRevenue = this.amount * this.asset.currentPrice;
        this.message = `Successfully sold ${this.amount} ${this.asset.name} for $${totalRevenue.toLocaleString()}.`;
        this.messageType = 'success';
        this.amount = 0; // Reset amount
      } else {
        this.message = 'Please enter a valid amount to sell.';
        this.messageType = 'error';
      }
    },
  },
};
</script>

<style scoped>
.container {
  padding: 24px;
  max-width: 600px;
  margin: 0 auto;
}

h1 {
  color: var(--color-primary);
  margin: 16px 0;
}

.asset-details {
  background-color: var(--color-panel);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 24px;
}

.trading-section {
  background-color: var(--color-panel);
  border-radius: 12px;
  padding: 16px;
}

.input-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
}

.input-group label {
  margin-bottom: 8px;
  font-weight: bold;
}

.input-group input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.button-group {
  display: flex;
  gap: 16px;
}

.buy-button,
.sell-button {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
  font-size: 16px;
}

.buy-button {
  background-color: #28a745; /* Green for Buy */
}

.sell-button {
  background-color: #dc3545; /* Red for Sell */
}

.buy-button:disabled,
.sell-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.message {
  margin-top: 16px;
  padding: 12px;
  border-radius: 4px;
  font-weight: bold;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
}

.button {
  margin-bottom: 16px;
  padding: 10px 16px;
  background-color: #007bff;
  border: none;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
}

.button:hover {
  background-color: #0056b3;
}
</style>