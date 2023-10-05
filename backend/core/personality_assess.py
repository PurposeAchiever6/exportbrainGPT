import json
from repository.personality.personality import personality

results = json.load(open("personality_result_sample.json"))

# traits = ['Extraversion', 'Neuroticism', 'Conscientiousness']

# number = {trait: 0 for trait in traits}
# total_score = {trait: 0 for trait in traits}

# for result in results:
#     number[result["trait"]] += 1
#     if result["positive"]:
#         total_score[result["trait"]] += result["answer"]
#     else:
#         total_score[result["trait"]] += (4 - result["answer"])

# personality_score = {trait: int(0.999 * total_score[trait] / max(1, number[trait])) for trait in traits}
# print(personality_score)

print(personality(results))

