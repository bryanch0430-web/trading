<!-- src/components/AssetCard.vue -->
<template>
  <div class="asset-card" @click="navigateToAsset">
    <h3>{{ asset.asset_name }}</h3>
    <p>Amount: {{ asset.total_value }}</p>
    <p>Buy Price: ${{ asset.average_price }} </p>
  </div>
</template>

<script>
export default {
  name: 'AssetCard',
  props: {
    asset: {
      type: Object,
      required: true,
    },
  },
  methods: {
    navigateToAsset() {
      this.$router.push({ name: 'AssetDisplay', params: { id: this.asset.asset_id } });
    },
  },
};
</script>

<style scoped>
.asset-card {
  background-color: var(--color-panel);
  border-radius: 12px; /* Rounded rectangle */
  padding: 16px;
  margin: 12px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.asset-card:hover {
  background-color: var(--color-secondary);
}

.asset-card h3 {
  margin: 0 0 8px 0;
}

.asset-card p {
  margin: 4px 0;
}
</style>