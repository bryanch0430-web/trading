<!-- src/components/ValueTrend.vue -->
<template>
  <div class="vcard">
    <h2>Total Value Trend</h2>
    <canvas className="flex justify-center items-center" ref="trendChart"></canvas>
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
          scales: {
            x: {
              display: false,
            },
            y: {
              display: false,
            },
          },
          plugins: {
            legend: {
              display: false,
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
  
}
</style>