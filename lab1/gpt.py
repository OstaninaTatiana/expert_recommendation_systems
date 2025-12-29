import os
import aiohttp


async def ask(prompt):
    ''' отправка запроса к модели gpt '''
    url = "https://openrouter.ai/api/v1/chat/completions"
    key = os.getenv("OPENROUTER_API_KEY")

    # открытие сессии
    async with aiohttp.ClientSession() as session:
        # отправка запроса
        async with session.post(
                url,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-oss-20b:free",
                    "messages": [{"role": "user", "content": prompt}]
                }
        ) as response:
            data = await response.json()
            if "choices" not in data:
                return 'Ошибка. Попробуйте ещё раз'
            return data["choices"][0]["message"]["content"]