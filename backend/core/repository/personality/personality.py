traits = ['extraversion', 'neuroticism', 'conscientiousness']
extraversion_list = ["Wallflower", "Lone Wolf", "Social Butterfly", "Life of the Party"]
neuroticism_list = ["Zen Master", "Stoic", "Dramatic", "Nervous Wreck"]
conscientiousness_list = ["Absent", "Free Spirit", "Organized Assistant", "Rigid Perfectionist"]
description_list = [extraversion_list, neuroticism_list, conscientiousness_list]


def personality(results):
    number = {trait: 0 for trait in traits}
    total_score = {trait: 0 for trait in traits}

    for result in results:
        number[result.trait] += 1
        if result.positive:
            total_score[result.trait] += result.answer
        else:
            total_score[result.trait] += (4 - result.answer)

    personality_score = {trait: int(0.999 * total_score[trait] / max(1, number[trait])) for trait in traits}

    # personality = {trait: {"score": personality_score[trait], "description": description_list[index][personality_score[trait]]} for index, trait in enumerate(traits)}
    personality = {"score": personality_score, "description": {trait: description_list[index][personality_score[trait]] for index, trait in enumerate(traits)}}
    
    return personality