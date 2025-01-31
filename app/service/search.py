import os
from openai import OpenAI
from dotenv import load_dotenv
import json

dotenv_path = './app/.env'

load_dotenv()
api_key = os.getenv('API_KEY')

def search_gpt(query):
    client = OpenAI(
        api_key=api_key,
    )
    first_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {
                "role": "system",
                "content": "Ты — помощник, который анализирует тексты и отвечает 'Да' или 'Нет' на вопрос, есть ли в тексте условия для экспериментов."
            },
            {
                "role": "user",
                "content":
                    "В вопросе есть варианты ответа. Напиши мне ответ в формате json. Где в ключе answer ты напишешь числовое значение - вариант правильного ответа. В ключе reasoning  ты напишешь объяснение или дополнительную информацию по запросу (например откуда ты узнал эту информацию) и что ответ дан моделью gpt-4o-mini. В ключе sources ты напишешь список ссылок на источники информации."
                    f"Вот запрос: {query}"
            }
        ],
        response_format={ "type": "json_object" }
    )
    response = first_response.choices[0].message.content

    print("Response content:", response)
    if response:
        try:
            result = json.loads(response.replace("'", '"').replace('\'', '\"').replace('\\', '\\\\').strip("'<>() "))
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            print("Response content:", response)
            return None
        return result
    else:
        return None
