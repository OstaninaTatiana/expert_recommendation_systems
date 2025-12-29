import requests


def request_gem(prompt, rapidApiKey):
    """Запрос к модели GemeniPro"""
    # Подготовка данных
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "gemini-pro-ai.p.rapidapi.com",
        "x-rapidapi-key": rapidApiKey
    }

    url = "https://gemini-pro-ai.p.rapidapi.com/"

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
        candidate = data["candidates"][0]
        reply_text = candidate["content"]["parts"][0]["text"]
        return reply_text.strip()
    except (KeyError, IndexError, TypeError) as e:
        print(data)
        raise e