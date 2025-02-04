<template>
  <div class="container">
    <button class="button" @click="$router.back()">Back</button>

    <!-- Asset Details -->
    <h1 v-if="asset?.name">{{ asset.name }} Details</h1>

    <div v-if="loading" class="loading">Loading asset details...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="asset && !loading && !error" class="asset-details">
      <p><strong>Current Price:</strong> ${{ asset.current_price }}</p>
      <p><strong>Market Cap:</strong> ${{ asset.market_cap }}</p>
      <p><strong>24h Volume:</strong> ${{ asset.volume }}</p>
      <p v-if="asset.change24h !== undefined">
        <strong>Change (24h):</strong> {{ asset.change24h }}%
      </p>
    </div>

    <!-- Trading Section -->
    <div class="trading-section">
      <h2>Trade {{ asset?.name }}</h2>
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

<script setup>
import { onMounted, computed, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAssetStore } from '../store/assetStore';
import { useTransactionStore } from '../store/transactionStore';

const transactionStore = useTransactionStore();
const assetStore = useAssetStore();
const route = useRoute();
const router = useRouter();
const amount = ref(0);
const message = ref('');
const messageType = ref('');
const loading = computed(() => assetStore.loading);
const error = computed(() => assetStore.error);
const asset = computed(() => assetStore.getcurrentAsset);

const isValidAmount = computed(() => amount.value > 0);
const assetId = route.params.id;

// Lifecycle hook to fetch asset details on mount
onMounted(async () => {
  console.log('route.params:', route.params);
  console.log('Fetching asset with ID:', assetId);
  if (assetId) {
    try {
      await assetStore.getAssetPrice(assetId);
    } catch (err) {
      console.error('Failed to fetch asset:', err);
    }
  } else {
    assetStore.error = 'Invalid asset ID.';
  }
});

const buyAsset = async () => {
  if (!isValidAmount.value) return;
  
  const payload = {
    buy_target_asset_id: assetId,
    amount: amount.value,
    user_id: "2fb3c95f-0250-4c9c-8194-0e22bdf1ae32"
  };
  console.log(payload)
  try {
    const transaction = await transactionStore.makeBuy(payload);
    
    // Check if there was an error inside the store (if not thrown)
    if (transactionStore.error) {
      console.error('Buy transaction failed:', transactionStore.error);
      message.value = "Buy transaction failed!";
      messageType.value = "error";
    } else {
      console.log('Buy transaction successful:', transaction);
      message.value = "Buy transaction successful!";
      messageType.value = "success";
      
      // Route to '/assets' after successful transaction
      router.push('/assets');
    }
  } catch (err) {
    console.error('Buy transaction encountered an error:', err);
    message.value = "Buy transaction encountered an error!";
    messageType.value = "error";
  }
};

const sellAsset = async () => {
  if (!isValidAmount.value) return;
  
  const payload = {
    sell_target_asset_id: assetId,
    amount: amount.value,
    user_id: "2fb3c95f-0250-4c9c-8194-0e22bdf1ae32"
  };
  
  try {
    const transaction = await transactionStore.makeSell(payload);
    
    if (transactionStore.error) {
      console.error('Sell transaction failed:', transactionStore.error);
      message.value = "Sell transaction failed!";
      messageType.value = "error";
    } else {
      console.log('Sell transaction successful:', transaction);
      message.value = "Sell transaction successful!";
      messageType.value = "success";
      
      // Route to '/assets' after successful transaction
      router.push('/assets');
    }
  } catch (err) {
    console.error('Sell transaction encountered an error:', err);
    message.value = "Sell transaction encountered an error!";
    messageType.value = "error";
  }
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