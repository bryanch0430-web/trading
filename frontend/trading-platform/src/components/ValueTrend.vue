<template>
  <div class="vcard">
    <h2 class="text-center">Total Value Trend</h2>
    <div class="chart-container">
      <canvas class="canvas-size" ref="trendChart"></canvas>
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default {
  name: 'ValueTrend',
  props: {
    trendData: {
      type: Array,
      required: true, // Array of { time: '...', value: number }
    },
  },
  setup(props) {
    const trendChart = ref(null);

    onMounted(() => {
      new Chart(trendChart.value, {
        type: 'line',
        data: {
          labels: props.trendData.map((d) => d.time),
          datasets: [
            {
              label: 'Total Value',
              data: props.trendData.map((d) => d.value),
              borderColor: '#C9A0FF',
              backgroundColor: 'rgba(201, 160, 255, 0.2)',
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false, // Ensures the chart adapts to the container
          scales: {
            x: {
              display: true, // Show x-axis for context
            },
            y: {
              display: true, // Show y-axis for context
            },
          },
          plugins: {
            legend: {
              display: true,
              position: 'top', // Position the legend
            },
          },
        },
      });
    });

    return {
      trendChart,
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
  overflow: hidden; /* Ensures content stays inside */
}

.chart-container {
  position: relative;
  width: 100%;
  height: 300px; /* Adjust height for a responsive chart */
}

.canvas-size {
  width: 100%; /* Full width of the container */
  height: 100%; /* Full height of the container */
}
</style>