<template>
  <!-- Show loading spinner while data is being fetched -->
  <div v-if="loading" class="loading-spinner">
    <p>Loading assets...</p>
    <!-- Add a spinner or animation here -->
  </div>

  <div v-else class="container">
    <h1>User Assets</h1>
    
    <!-- Only render asset distribution components if assetDistribution exists -->
    <div v-if="assetDistribution && userValueTrend">
      <TotalValue :totalValue="assetDistribution.total_value" />
      
      <!-- Responsive layout for ValueTrend and TypeDistribution -->
      <div class="charts-container">
        <ValueTrend :trendData="userValueTrend" />
        <TypeDistribution :distributionData="assetDistribution.asset_type_values" />
      </div>
    </div>
    <div v-else>
      <p>No asset distribution data available</p>
    </div>

    <!-- Show assets once data is loaded -->
    <h3 class="asset-card-title">Asset Details</h3>

    <div class="assets-list">
      <AssetCard v-for="asset in assets" :key="asset.id" :asset="asset" />
    </div>
    
    <!-- Button to open the funds modal -->
    <div class="funds-control">
      <button @click="showModal = true" class="manage-funds-button">Manage Funds</button>
    </div>

    <!-- Modal pop out window for deposit and withdraw actions -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2>Manage Funds</h2>

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

        <!-- Use the same structure and classes as the sell and buy buttons -->
        <div class="button-group">
          <button class="sell-button" @click="handleWithdraw" :disabled="!isValidAmount">Withdraw</button>
          <button class="buy-button" @click="handleDeposit" :disabled="!isValidAmount" >Deposit</button>
        </div>

        <!-- Optionally display an error message -->
        <p v-if="errorMsg" class="alert">{{ errorMsg }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import TotalValue from '../components/TotalValue.vue';
import ValueTrend from '../components/ValueTrend.vue';
import TypeDistribution from '../components/TypeDistribution.vue';
import AssetCard from '../components/AssetCard.vue';
import { useUserStore } from '../store/userStore';
import { useAssetStore } from '../store/assetStore';
import transactionAPI from '../api/transactionAPI';

const useStore = useUserStore();
const assetStore = useAssetStore();

onMounted(async () => {
  await useStore.fetchUserAssets();
  await assetStore.calculateUserAsset();
  await useStore.ShowUserValueTrend();
});

const assetDistribution = computed(() => assetStore.getAssetDistribution);
const assets = computed(() => useStore.userAsset);
const userValueTrend = computed(() => useStore.getValueTrend);
const loading = computed(() => useStore.loading);
const isValidAmount = computed(() => amount.value > 0);

// Modal and input states
const showModal = ref(false);
const amount = ref(0);
const errorMsg = ref(null);
const processing = ref(false);

// Function to close modal and reset states
const closeModal = () => {
  showModal.value = false;
  amount.value = 0;
  errorMsg.value = null;
};

// Handle deposit action
async function handleDeposit() {
  processing.value = true;
  errorMsg.value = null;
  
  const payload = { 
    amount: amount.value,
    deposit_pricing: 1.0,
    user_id: "2fb3c95f-0250-4c9c-8194-0e22bdf1ae32"


   };
  try {
    const transaction = await transactionAPI.depositTransaction(payload);
    console.log('Deposit transaction:', transaction);
    closeModal();
  } catch (error) {
    errorMsg.value = error.message || 'Deposit failed. Please try again.';
  } finally {
    processing.value = false;
  }
}

// Handle withdraw action
async function handleWithdraw() {
  processing.value = true;
  errorMsg.value = null;
  
  const payload = {
     amount: amount.value,
         user_id: "2fb3c95f-0250-4c9c-8194-0e22bdf1ae32"
};
  try {
    const transaction = await transactionAPI.withdrawTransaction(payload);
    console.log('Withdraw transaction:', transaction);
    closeModal();
  } catch (error) {
    errorMsg.value = error.message || 'Withdrawal failed. Please try again.';
  } finally {
    processing.value = false;
  }
}
</script>

<style scoped>
.container {
  padding: 24px;
}

h1 {
  color: var(--color-primary);
  margin-bottom: 24px;
}

/* Flex layout for charts */
.charts-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
  justify-content: center;
}

.charts-container > * {
  flex: 1 1 300px;
  max-height: 400px;
  min-width: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.assets-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background-color: var(--color-panel);
  padding: 24px;
  border-radius: var(--border-radius);
  width: 90%;
  max-width: 400px;
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

/* Button Group Styles */
.button-group {
  display: flex;
  gap: 16px;
}

/* Use the same button styling as seen in the trading section */
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

/* Deposit (Buy) button style */
.buy-button {
  background-color: #28a745; /* Green */
}

/* Withdraw (Sell) button style */
.sell-button {
  background-color: #dc3545; /* Red */
}

.buy-button:disabled,
.sell-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

/* Additional style for the funds control button container */
.funds-control {
  margin: 24px 0;
  text-align: center;
}

/* Optional style override for the manage funds button */
.manage-funds-button {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  background-color: var(--color-panel);
  color: var(--color-primary);
  cursor: pointer;
  font-size: 16px;
}
.asset-card-title {
  font-size: 1.15rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #BB86FC;
}
/* Responsive adjustments for smaller screens */
@media (max-width: 768px) {
  .charts-container > * {
    flex: 1 1 100%;
  }
}
</style>