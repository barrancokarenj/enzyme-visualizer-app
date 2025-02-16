// Define the types for the fetched data
export interface Mutation {
  mutation: string;
  properties: Record<string, number>;
}

/// Parent sequence string
export interface ParentSequenceData {
  sequence: string;
}

export interface MutationInfo {
  selectedProperty:  Ref<string>;
  properties: Ref<string[]>; 
}

export interface MutationChartData {
  mutationPosition: number,
  value: string,
  mutatedAminoAcid: string,
  originalAminoAcid: string
}