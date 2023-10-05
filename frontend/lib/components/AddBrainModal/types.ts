export type PersonalityResponse = {
    score: {
        conscientiousness: number,
        extraversion: number,
        neuroticism: number,
        // Include other properties of score if they exist
      },
    description: {
        conscientiousness: string,
        extraversion: string,
        neuroticism: string,
        // Include other properties of score if they exist
      },
  };