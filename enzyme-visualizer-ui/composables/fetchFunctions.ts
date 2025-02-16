import { useFetch } from '@vueuse/core';
import { Mutation, ParentSequenceData } from '../models/models';

const baseUrl = import.meta.env.VITE_API_BASE_URL;

// Fetch mutation data
export const fetchMutationData = async (): Promise<Mutation[]> => {
  const { data, error } = await useFetch<Mutation[]>(`${baseUrl}/visualizer/variants`).json();
  
  if (error.value) {
    console.error('Error fetching mutation data:', error.value);
    throw new Error('Error fetching mutation data');
  }
  
  return data.value || [];
};

// Fetch parent sequence data
export const fetchParentSequenceData = async (): Promise<ParentSequenceData> => {
  const { data, error } = await useFetch<ParentSequenceData>(`${baseUrl}/visualizer/parent-sequence`).json();
  
  if (error.value) {
    console.error('Error fetching parent sequence data:', error.value);
    throw new Error('Error fetching parent sequence data');
  }
  
  return data.value || { sequence: '' }; // Return empty sequence if there's an error
};
