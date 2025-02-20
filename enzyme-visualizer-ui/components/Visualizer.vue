<template>
  <v-container>
    <v-select
      v-model="selectedPropertyFromChild"
      :items="itemsFromChild"
      label="Select Property"
      outlined
    ></v-select>
    <scatter-plot :newSelectedProperty=selectedPropertyFromChild  @onPropertiesLoaded="handlePropertiesLoaded"/>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { MutationInfo } from '../models/models'; 

const itemsFromChild = ref<string[]>([]);
const selectedPropertyFromChild = ref<string>('');

const handlePropertiesLoaded = (items: MutationInfo) => {
  itemsFromChild.value = items.properties.value; // Store the data received from the child component
  selectedPropertyFromChild.value = items.selectedProperty.value;
};
</script>