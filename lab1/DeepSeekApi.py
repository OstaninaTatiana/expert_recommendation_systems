import requests

def request_ds(prompt, rapidApiKey):
    """Запрос к модели DeepSeek r1 distill on qwen 32b"""
    # Подготовка данных
    payload = {
        "model": "deepseek/deepseek-r1-distill-qwen-32b",
        "messages": [{"role": "user", "content": prompt}]
    }

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "deepseek-r1-distill-qwen-32b.p.rapidapi.com",
        "x-rapidapi-key": rapidApiKey
    }

    url = "https://deepseek-r1-distill-qwen-32b.p.rapidapi.com/api/v1/chat/completions"

    # Отправка запроса
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # вызовет исключение при 4xx/5xx
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        exit(1)

    # пытаемся извлечь ответ
    try:
        choice = data["choices"][0]
        content = choice["message"]["content"]
        return content.strip()
    except (KeyError, IndexError, TypeError) as e:
        print(data)
        raise e