import { ref, Ref, onMounted } from 'vue';
import { fetchMutationData, fetchParentSequenceData } from './fetchFunctions';
import { Mutation } from '../models/models'; 

export const useMutationData = () => {
  // Define the reactive state with proper types
  const variants: Ref<Mutation[]> = ref([]);
  const properties: Ref<string[]> = ref([]);
  const selectedProperty: Ref<string> = ref('');
  const parentSequence: Ref<string> = ref('');
  const mutatedSequence: Ref<string> = ref('');

  // Function to fetch mutation data
  const fetchData = async () => {
    try {
      variants.value = await fetchMutationData();
      if (variants.value.length > 0) {
        properties.value = Object.keys(variants.value[0].properties);
        selectedProperty.value = properties.value[0];  // Set the default property
      }
    } catch (error) {
      console.error('Error fetching mutation data:', error);
    }
  };

  // Function to fetch parent sequence data
  const fetchParentSequence = async () => {
    try {
      const parentData = await fetchParentSequenceData();
      parentSequence.value = parentData.sequence;
      mutatedSequence.value = generateMutatedSequence();
    } catch (error) {
      console.error('Error fetching parent sequence data:', error);
    }
  };

  // Generate the mutated sequence by comparing it with the parent sequence
  const generateMutatedSequence = (): string => {
    let mutatedSeq = parentSequence.value.split(''); // Convert parent sequence to an array
    variants.value.forEach((variant:Mutation) => {
      const mutationParts = variant.mutation.split('+');
      mutationParts.forEach((mutation: string) => {
        const position = parseInt(mutation.match(/\d+/)?.[0] ?? '0') - 1; // Adjust for 0-based index
        const mutatedAminoAcid = mutation[mutation.length - 1];

        if (mutatedSeq[position] !== mutatedAminoAcid) {
          mutatedSeq[position] = mutatedAminoAcid; // Apply mutation
        }
      });
    });
    return mutatedSeq.join(''); // Return the mutated sequence as a string
  };

  // Get mutation data for the selected property
  const getDataForSelectedProperty = () => {
    return variants.value.map((variant: Mutation) => {
      const mutationParts = variant.mutation.split('+');
      const originalAminoAcid = parentSequence.value[parseInt(mutationParts[0].match(/\d+/)?.[0] ?? '0') - 1];
      return {
        mutationPosition: parseInt(mutationParts[0].match(/\d+/)?.[0] ?? '0'),
        value: variant.properties[selectedProperty.value],
        mutatedAminoAcid: mutationParts.map((mutation: string) => mutation[mutation.length - 1]),
        originalAminoAcid, // Include the original amino acid at the mutation position
      };
    });
  };

  // Call fetch functions when component is mounted
  onMounted(async () => {
    await fetchParentSequence();
    await fetchData();
  });

  return {
    variants,
    properties,
    selectedProperty,
    parentSequence,
    mutatedSequence,
    getDataForSelectedProperty,
  };
};
