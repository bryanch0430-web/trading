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
        <p><strong>Label:</strong> {{ asset.label }}</p>
        <p><strong>Asset Type:</strong> {{ asset.asset_type }}</p>
        <p><strong>Asset Name:</strong> {{ asset.name }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAssetStore } from '../store/assetStore'; // Adjust the path based on your project structure
//        @click="goToAsset(asset.id)"
const assetStore = useAssetStore();
const router = useRouter();
const currentUserId = localStorage.getItem('userId');

// Access the reactive state directly
const assets =computed(()=> assetStore.allAssets);

// Fetch assets when the component is mounted
onMounted(async () => {
  await assetStore.fetchAllAssets(currentUserId);
});

  const goToAsset = (id) => {
    router.push({ name: 'AssetDisplay', params: { id } });
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

