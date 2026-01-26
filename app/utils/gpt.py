from main import HF_API_KEY, HF_API_URL
import requests



def response_ai(text: str) -> str:
    prompt = f"""
    Ты — опытный преподаватель английского языка.

    Проанализируй текст студента и определи его уровень по шкале CEFR (A1–C2).

    ВАЖНО:
    — Отвечай СТРОГО в формате ниже
    — Используй русский язык
    — Не добавляй ничего от себя вне структуры
    — Форматируй ответ с эмодзи и маркерами

    ФОРМАТ ОТВЕТА:

    📊 Результат оценки:

    Ваш примерный уровень: **<УРОВЕНЬ> (<НАЗВАНИЕ>)**

    Что хорошо:
    ✔️ <пункт 1>
    ✔️ <пункт 2>

    Что стоит улучшить:
    • <пункт 1>
    • <пункт 2>

    💡 С таким уровнем вы уже можете:
    — <пункт 1>
    — <пункт 2>

    Текст студента:
    {text}
    """

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(HF_API_URL, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


