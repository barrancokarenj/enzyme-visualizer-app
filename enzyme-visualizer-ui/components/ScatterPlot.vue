<template>
  <v-container>
    <!-- ECharts component to show scatter plot -->
    <div ref="chartContainer" style="height: 400px; width: 100%;"></div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';
import { useMutationData } from '../composables/useMutationData';
import * as echarts from 'echarts';
import type { MutationChartData, MutationInfo } from '../models/models';

// Destructure the necessary data from the useMutationData composable
const { 
  properties, 
  selectedProperty, 
  getDataForSelectedProperty, 
  parentSequence
} = useMutationData();

// Reference for the chart container
const chartContainer = ref<HTMLElement | null>(null);

let chart: echarts.ECharts | null = null;

// Colors for amino acids
const aminoAcidColors: Record<string, string> = {
  'A': '#A5AA9C', 'V': '#A5AA9C', 'L': '#A5AA9C', 'I': '#A5AA9C', 'M': '#A5AA9C', 'P': '#A5AA9C',
  'F': '#7350F2', 'Y': '#7350F2', 'W': '#7350F2',
  'S': '#93F1F1', 'T': '#93F1F1', 'C': '#93F1F1', 'N': '#93F1F1', 'Q': '#93F1F1',
  'K': '#F3B4B4', 'R': '#F3B4B4', 'H': '#F3B4B4',
  'D': '#E16D63', 'E': '#E16D63',
};

// Define the prop to accept selectedProperty from the parent
const props = defineProps({
  newSelectedProperty: {
    type: String,  
    required: true,
  }
});

const emit = defineEmits<{
  (event: 'onPropertiesLoaded', items: MutationInfo): void;
}>();

// Fetch data when the component is mounted
onMounted(() => {
  handleUpdateChart();
});

// Watch for changes in selected property to update the chart
watch(selectedProperty, () => {
  handleUpdateChart();
});

// Watch for changes in the newSelectedProperty prop to update the chart
watch(() => props.newSelectedProperty, (value: string) => {
  selectedProperty.value = value;
  handleUpdateChart();
});

// Function to update the chart
const updateChart = (): void => {
  if (chartContainer.value) {
    if (chart) {
      chart.dispose();
    }

    chart = echarts.init(chartContainer.value);

    // Get data for the selected property
    const data = getDataForSelectedProperty();
    const positions = data.map((mutationData : MutationChartData) => mutationData.mutationPosition);
    const values = data.map((mutationData : MutationChartData) => Number(mutationData.value));
    const mutatedAminoAcids: string[] = data.map((mutationData : MutationChartData) => mutationData.mutatedAminoAcid[0]);
    const originalAminoAcids = data.map((mutationData : MutationChartData) => mutationData.originalAminoAcid);

    // Parent sequence data (X position is amino acid index, Y is baseline 0)
    const parentSequenceData = parentSequence.value.split('').map((aminoAcid: string, index: number) => ({
      value: [index, 0],  // Position on X (index), baseline value of 0 on Y
      symbolSize: 10,
      itemStyle: {
        color: aminoAcidColors[aminoAcid] || '#000000', // Default to black if no color is found
      },
      tooltip: {
        formatter: `Position: ${index + 1}<br>Amino Acid: ${aminoAcid}`,
      }
    }));

    // ECharts options configuration
    const option = {
      tooltip: {
        trigger: 'item',
        formatter: (params: any) => {
          
          const { seriesName, dataIndex } = params;

          if (seriesName === 'Mutations') {
            return `Position: ${positions[dataIndex]}<br>Original: ${originalAminoAcids[dataIndex]} → Mutated: ${mutatedAminoAcids[dataIndex]}<br>Property Value: ${values[dataIndex]}`;
          }
          if (seriesName === 'Parent Sequence') {
            return `Position: ${params.dataIndex + 1}<br>Amino Acid: ${parentSequence[params.dataIndex]}`;
          }
          return '';
        }
      },
      xAxis: {
        type: 'category',
        data: parentSequence.value.split('').map((_, i) => `${i + 300}`),  // Position of the amino acids as X labels
        name: 'Position',
        axisLabel: {
          formatter: (value: string, index: number) => {
            const aminoAcid = parentSequence.value[index];
            return `${aminoAcid}${value}`; // Display amino acid and its position
          },
        },
        nameLocation: 'middle',
        nameGap: 50,
        onZero: false
      },
      yAxis: {
        type: 'value',
        name: selectedProperty.value,
        nameLocation: 'middle',
        nameGap: 50
      },
      series: [
        {
          name: 'Parent Sequence',
          data: parentSequenceData, // Parent sequence points as baseline
          type: 'scatter',
          symbol: 'circle',
        },
        {
          name: 'Mutations',
          data: values.map((value: number, index: number) => ({
            value: [positions[index], value],
            symbolSize: 10,
            itemStyle: {
              color: aminoAcidColors[mutatedAminoAcids[index]] || '#FF5733', // Color for mutations
            },
          })),
          type: 'scatter',
        },
      ],
    };

    // Apply the options to the chart
    chart.setOption(option);

  }
};

const handleUpdateChart = ():void => {
  updateChart(); // Update the chart when the selected property changes
  emit('onPropertiesLoaded', {'properties': properties, 'selectedProperty': selectedProperty});
};

// Cleanup the chart instance when the component is unmounted
onBeforeUnmount(() => {
  if (chart) {
    chart.dispose(); // Dispose the chart instance
  }
});
</script>