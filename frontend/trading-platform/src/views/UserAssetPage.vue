<template>
  <div v-if="loading" class="loading-spinner">
    <p>Loading assets...</p>
  </div>

  <div v-else class="container">
    <h1>User Assets</h1>
    
    <div v-if="assetDistribution && userValueTrend">
      <TotalValue :totalValue="assetDistribution.total_value" />
      
      <div class="charts-container">
        <ValueTrend :trendData="userValueTrend" />
        <TypeDistribution :distributionData="assetDistribution.asset_type_values" />
      </div>
    </div>
    <div v-else>
      <p>No asset distribution data available</p>
    </div>

    <h3 class="asset-card-title">Holding Asset Details</h3>

    <div class="assets-list">
      <AssetCard v-for="asset in assets" :key="asset.id" :asset="asset" />
    </div>
    
    <!-- Button to open the funds modal -->
    <div class="funds-control">
      <button @click="showModal = true" class="manage-funds-button">Manage Funds</button>
    </div>

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

        <div class="button-group">
          <button class="sell-button" @click="handleWithdraw" :disabled="!isValidAmount">Withdraw</button>
          <button class="buy-button" @click="handleDeposit" :disabled="!isValidAmount" >Deposit</button>
        </div>

        <!--  display error message -->
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
const currentUserId = localStorage.getItem('userId');

onMounted(async () => {
  await useStore.fetchUserAssets(currentUserId);
  await assetStore.calculateUserAsset(currentUserId);
  await useStore.ShowUserValueTrend(currentUserId);
});

const assetDistribution = computed(() => assetStore.getAssetDistribution);
const assets = computed(() => useStore.userAsset);
const userValueTrend = computed(() => useStore.getValueTrend);
const loading = computed(() => useStore.loading);
const isValidAmount = computed(() => amount.value > 0);
const showModal = ref(false);
const amount = ref(0);
const errorMsg = ref(null);
const processing = ref(false);

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
    user_id: currentUserId

   };
  try {
    const transaction = await transactionAPI.depositTransaction(payload);
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
     user_id: currentUserId
};
  try {
    const transaction = await transactionAPI.withdrawTransaction(payload);
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
  /* background-color: var(--color-background); */
  padding: 24px;
  /* border: 1px solid #ccc; */
  /* border-radius: var(--border-radius); */
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
  background-color: #28a745; 
}

.sell-button {
  background-color: #dc3545;
}

.buy-button:disabled,
.sell-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.funds-control {
  margin: 24px 0;
  text-align: center;
}

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

@media (max-width: 768px) {
  .charts-container > * {
    flex: 1 1 100%;
  }
}
</style>

