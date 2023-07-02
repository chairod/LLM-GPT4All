from constants import *
from custom_gpt4all import pyllmodel
from langchain.prompts import PromptTemplate

model_path = f'{LLM_MODEL_PATH}\\{LLM_MODEL_NAME}'
llm = pyllmodel.LLModel()
llm.load_model(model_path=model_path)



print()
print()
while True:
    user_message = input('Input score,question:')
    user_message = user_message.strip()
    if user_message == '':
        continue
    if user_message == 'exit':
        break

    score_value, question = user_message.split(',')
    prompt = PromptTemplate(
    template=
"""
recommendation:
score value is {score_value}
if score value more than or equals 1 just answer "i dont' know will provide answer when score value less than 1"

question: {question}
""",
    input_variables=['score_value', 'question']
    )
    prompt = prompt.format(score_value=score_value, question=question)

    print()
    print('Try to test chatbot if you input "score_value" more than 1 just get answer "I\'dont know" ')
    print(f'score_value: {score_value}, question: {question}')
    print()
    print(f'Your prompt:\n{prompt}')
    llm.generate(prompt=prompt, streaming=True)

