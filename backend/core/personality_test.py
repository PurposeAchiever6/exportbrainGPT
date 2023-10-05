import json
from dotenv import load_dotenv
from repository.personality.personality_question import generate_question_all

load_dotenv()

USER_COLOR = "\033[32m"  # green
QUESTION_COLOR = "\033[35m"  # purple
RESET_COLOR = "\033[0m"  # reset

responsiveness = ["Disagree Strongly", "Disagree a little", "Neither agree nor disagree", "Agree a little", "Agree strongly"]

if __name__ == '__main__':
    results = []
    questions = generate_question_all(question_number=4)
    print("This is personality assess question")
    for question in questions:
        print('\n' + QUESTION_COLOR + "Question: " + RESET_COLOR + question["question"] + '\n\n' + 'The options for the respondent are:')
        for index, agent in enumerate(responsiveness, start=1):
            print(f"{index}. {agent}")
        # print(USER_COLOR + "You: ")
        while True:
            op_index = input('\n' + "Choose a number" + '\n' + USER_COLOR + '\n' + "You: " + RESET_COLOR)
            try:
                op = int(op_index) - 1
                if op >= 0 and op < 5:
                    question["answer"] = op
                    results.append(question)
                    break
                else: 
                    print("Input 1 ~ 5")
            except:
                continue
    print(results[0])
    f = open ('personality.json', 'w')
    json.dump(results, f)
    f.close()
