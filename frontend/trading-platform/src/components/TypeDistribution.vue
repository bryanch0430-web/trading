<template>
  <div class="vcard">
    <h2 class="text-center">Type Distribution</h2>
    <div class="chart-container">
      <canvas class="canvas-size" ref="distributionChart"></canvas>
    </div>
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
          maintainAspectRatio: true, // Prevent chart distortion
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
.vcard {
  background-color: var(--color-panel);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  text-align: center;
  overflow: hidden; /* Ensure content stays inside */
}

.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.canvas-size {
  width: 200px; /* Adjust the width */
  height: 200px; /* Adjust the height */
  max-width: 100%; /* Ensure responsiveness */
}
</style>