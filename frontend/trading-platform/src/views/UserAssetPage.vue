<template>
  <div class="container">
    <h1>User Assets</h1>
    <TotalValue :totalValue="totalValue" />
    
    <!-- Responsive layout for ValueTrend and TypeDistribution -->
    <div class="charts-container">
      <ValueTrend :trendData="trendData" />
      <TypeDistribution :distributionData="distributionData" />
    </div>

    <div class="assets-list">
      <AssetCard v-for="asset in assets" :key="asset.id" :asset="asset" />
    </div>
  </div>
</template>

<script>
import TotalValue from '../components/TotalValue.vue';
import ValueTrend from '../components/ValueTrend.vue';
import TypeDistribution from '../components/TypeDistribution.vue';
import AssetCard from '../components/AssetCard.vue';

export default {
  name: 'UserAssetPage',
  components: {
    TotalValue,
    ValueTrend,
    TypeDistribution,
    AssetCard,
  },
  data() {
    return {
      totalValue: 15000, // Mock total value
      trendData: [
        { time: 'Jan', value: 10000 },
        { time: 'Feb', value: 11000 },
        { time: 'Mar', value: 12000 },
        { time: 'Apr', value: 13000 },
        { time: 'May', value: 15000 },
      ],
      distributionData: {
        Bitcoin: 40,
        Ethereum: 30,
        Litecoin: 20,
        Ripple: 10,
      },
      assets: [
        {
          id: 1,
          name: 'Bitcoin',
          amount: 2,
          buyPrice: 4000,
        },
        {
          id: 2,
          name: 'Ethereum',
          amount: 5,
          buyPrice: 2000,
        },
      ],
    };
  },
};
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
}

/* Style for individual chart components */
.charts-container > * {
  flex: 1 1; /* Two columns on wider screens */
  max-height: 1000px; /* Limit height for better layout */
  min-width: 700px; /* Ensure charts are readable on smaller screens */
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