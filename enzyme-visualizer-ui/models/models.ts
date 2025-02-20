// Define the types for the fetched data
export interface Mutation {
  mutation: string;
  properties: Record<string, number>;
}

/// Parent sequence string
export interface ParentSequenceData {
  sequence: string;
}

//Properties and selected property received from the Scatter Plot
export interface MutationInfo {
  selectedProperty:  Ref<string>;
  properties: Ref<string[]>; 
}

//Mutation Data 
export interface MutationChartData {
  mutationPosition: number,
  value: number,
  mutatedAminoAcid: string[],
  originalAminoAcid: string
}