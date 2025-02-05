<template>
  <div class="container">
    <div class="header-row">
      <h1>All Assets</h1>
      <button class="manage-funds-button" @click="openModal">Add Asset</button>
    </div>

    <div class="assets-list">
      <div
        v-for="asset in assets"
        :key="asset.id"
        class="asset-item"
        @click="goToAsset(asset.id)"
      >
        <h2>{{ asset.name }}</h2>
        <p><strong>Label:</strong> {{ asset.label }}</p>
        <p><strong>Asset Type:</strong> {{ asset.asset_type }}</p>
        <p><strong>Asset Name:</strong> {{ asset.name }}</p>
      </div>
    </div>
  </div>

  <!-- Create Asset Modal (Label as in Yahoo Finance)-->
  <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
    <div class="modal">
      <h2>Create Asset</h2>
      <p class="info-text">Note: The asset label refers to the label used at Yahoo Finance.</p>
      <div class="input-group">
        <label for="asset-label">Asset Label:</label>
        <input
          id="asset-label"
          v-model="assetLabel"
          type="text"
          placeholder="Enter asset label"
        />
      </div>
      <!-- Display error message if asset creation fails -->
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div class="button-group">
        <button class="sell-button" @click="closeModal">Cancel</button>
        <button class="buy-button" @click="handleCreateAsset" :disabled="!assetLabel">
          Create
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAssetStore } from '../store/assetStore';

const assetStore = useAssetStore();
const router = useRouter();
const currentUserId = localStorage.getItem('userId');

// Reactive state for assets, modal visibility, asset label and error message
const assets = computed(() => assetStore.allAssets);
const showModal = ref(false);
const assetLabel = ref("");
const errorMessage = ref("");

// Fetch assets on component mount
onMounted(async () => {
  await assetStore.fetchAllAssets(currentUserId);
});

// Navigation to a single asset details page
const goToAsset = (id) => {
  router.push({ name: 'AssetDisplay', params: { id } });
};

// Modal control functions
const openModal = () => {
  errorMessage.value = "";
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  assetLabel.value = "";
  errorMessage.value = "";
};

// Handle asset creation with error handling
const handleCreateAsset = async () => {
  try {
    await assetStore.createAsset(assetLabel.value);
    await assetStore.fetchAllAssets(currentUserId);
    await sleep(1000); 
    closeModal();
  } catch (error) {
    console.error("Error creating asset:", error);
    // Optionally, you could check for specific error details here
    errorMessage.value = error?.response?.data?.message || "Failed to create asset. Please try again.";
  }
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

.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}
.manage-funds-button {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  background-color: var(--color-primary);
  color: #fff;
  cursor: pointer;
  font-size: 16px;
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

@media (max-width: 768px) {
  .assets-list {
    flex-direction: column;
  }
}

.error-message {
  color: red;
  margin-bottom: 1rem;
}

.info-text {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 1rem;
}
</style>

