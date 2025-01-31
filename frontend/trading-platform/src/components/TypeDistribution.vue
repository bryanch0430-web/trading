<!-- src/components/TypeDistribution.vue -->
<template>
  <div class="card">
    <h2>Type Distribution</h2>
    <canvas ref="distributionChart"></canvas>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default {
  name: 'TypeDistribution',
  props: {
    distributionData: {
      type: Object,
      required: true, // { type1: count1, type2: count2, ... }
    },
  },
  setup(props) {
    const distributionChart = ref(null);

    onMounted(() => {
      new Chart(distributionChart.value, {
        type: 'pie',
        data: {
          labels: Object.keys(props.distributionData),
          datasets: [
            {
              data: Object.values(props.distributionData),
              backgroundColor: ['#C9A0FF', '#B6B5D8', '#5790FC', '#E06DB9'],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom',
            },
          },
        },
      });
    });

    return {
      distributionChart,
    };
  },
};
</script>

<style scoped>
.card {
  background-color: var(--color-panel);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}
</style>