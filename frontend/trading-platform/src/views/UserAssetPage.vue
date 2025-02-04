<template>
  <!-- Show loading spinner while data is being fetched -->
  <div v-if="loading" class="loading-spinner">
    <p>Loading assets...</p>
    <!-- Add a spinner or animation here -->
  </div>

  <div v-else class="container">
    <h1>User Assets</h1>
    
    <!-- Only render asset distribution components if assetDistribution exists -->
    <div v-if="assetDistribution">
      <TotalValue :totalValue="assetDistribution.total_value" />
      
      <!-- Responsive layout for ValueTrend and TypeDistribution -->
      <div class="charts-container">
        <ValueTrend :trendData="trendData" />
        <TypeDistribution :distributionData="assetDistribution.asset_type_values" />
      </div>
    </div>
    <div v-else>
      <p>No asset distribution data available</p>
    </div>

    <!-- Show assets once data is loaded -->
    <div class="assets-list">
      <AssetCard v-for="asset in assets" :key="asset.id" :asset="asset" />
    </div>
  </div>
</template>

<script setup>
import TotalValue from '../components/TotalValue.vue';
import ValueTrend from '../components/ValueTrend.vue';
import TypeDistribution from '../components/TypeDistribution.vue';
import AssetCard from '../components/AssetCard.vue';
import { onMounted, computed } from 'vue';
import { useUserStore } from '../store/userStore';
import { useAssetStore } from '../store/assetStore';

// Sample mock data for other components
const trendData = [
  { time: 'Jan', value: 10000 },
  { time: 'Feb', value: 11000 },
  { time: 'Mar', value: 12000 },
  { time: 'Apr', value: 13000 },
  { time: 'May', value: 15000 },
];

const useStore = useUserStore();
const assetStore = useAssetStore();

// Fetch assets when the component is mounted
onMounted(async () => {
  await useStore.fetchUserAssets();
  await assetStore.calculateUserAsset();
});

// Compute assets and loading state from the store
const assetDistribution = computed(() => assetStore.getAssetDistribution);
const assets = computed(() => useStore.userAsset);
const loading = computed(() => useStore.loading); // Get the loading state
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
  justify-content: center; /* Center the charts horizontally */
}

/* Style for individual chart components */
.charts-container > * {
  flex: 1 1 300px; /* Allow charts to shrink for smaller screens */
  max-height: 400px; /* Limit height for better layout */
  min-width: 300px; /* Ensure charts fit neatly on small screens */
  display: flex;
  justify-content: center;
  align-items: center;
}

.assets-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

/* Responsive adjustments for smaller screens */
@media (max-width: 768px) {
  .charts-container > * {
    flex: 1 1 100%; /* Stack charts vertically on small screens */
  }
}
</style>
