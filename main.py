import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from constants import GENRES, LANGS
import gpt
import llama

load_dotenv()

user_data = {}

async def start(update: Update, context):
    ''' обработка команды start '''
    user_data[update.effective_user.id] = {"step": 0}
    await update.message.reply_text(
        "Выберите модель:",
        reply_markup=ReplyKeyboardMarkup([["GPT", "Llama"]], one_time_keyboard=True)
    )

async def handle_text(update: Update, context):
    ''' обработка текстового ввода '''
    user_id = update.effective_user.id
    text = update.message.text
    step = user_data[user_id].get("step", 0)

    # сохраняем выбор модели, спрашиваем возраст
    if step == 0:
        if text in ["GPT", "Llama"]:
            user_data[user_id]["model"] = text.lower()
            user_data[user_id]["step"] = 1
            await update.message.reply_text("Возраст младшего зрителя? (например: 10 или 18+)")
        else:
            await update.message.reply_text("Выберите модель: GPT или Llama.")
        return

    # сохраняем возраст, спрашиваем жанр
    if step == 1:
        user_data[user_id]["age"] = text
        user_data[user_id]["step"] = 2
        kb = [GENRES[i:i+2] for i in range(0, len(GENRES), 2)]
        await update.message.reply_text("Жанр:", reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True))
        return

    # сохраняем жанр, спрашиваем страну производства
    if step == 2:
        if text in GENRES:
            user_data[user_id]["genre"] = text
            user_data[user_id]["step"] = 3
            kb = [LANGS[i:i+2] for i in range(0, len(LANGS), 2)]
            await update.message.reply_text("Страна:", reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True))
        else:
            await update.message.reply_text("Выберите жанр из списка.")
        return

    # сохраняем страну, спрашиваем особые пожелания
    if step == 3:
        if text in LANGS:
            user_data[user_id]["country"] = text
            user_data[user_id]["step"] = 4
            await update.message.reply_text("Особые пожелания? Напишите или 'нет'.")
        else:
            await update.message.reply_text("Выберите страну производства.")
        return

    # сохраняем особые пожелания, отдаем 3 фильма
    if step == 4:
        prefs = "Нет" if text.lower() in ("нет", " ", "-", ".") else text
        user_data[user_id]["prefs"] = prefs

        d = user_data[user_id]
        prompt = (
            f"Предложи 3 фильма. Возраст младшего зрителя: {d['age']}. Жанр: {d['genre']}. "
            f"Страна производства: {d['country']}. Пожелания: {d['prefs']}. "
            f"Для каждого — название, год, краткое описание без спойлеров. Список. "
            f"Не добавляй особенного форматирования - только то, что будет удобно читать в виде сырого текста"
        )

        await update.message.chat.send_action("typing")

        # получаем ответ модели
        if d["model"] == "gpt":
            resp = await gpt.ask(prompt)
        else:
            resp = await llama.ask(prompt)

        await update.message.reply_text(resp)
        await update.message.reply_text("Готово! /start — начать заново.")

# запуск бота
app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
# команда старт
app.add_handler(CommandHandler("start", start))
# обработка текста
app.add_handler(MessageHandler(filters.TEXT, handle_text))
# получение сообщений
app.run_polling()
