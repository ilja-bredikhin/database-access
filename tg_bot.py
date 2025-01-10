from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import aiohttp
import asyncio
import logging

# Токен
TELEGRAM_BOT_TOKEN = "your_token"

# URL Django API
DJANGO_API_URL = "http://127.0.0.1:8000/api/measurements/"

# Логирование
logging.basicConfig(level=logging.INFO)

# Список пользователей, которые нажали /start
subscribed_users = set()

async def fetch_data(session, url, timeout=10):
    try:
        async with session.get(url, timeout=timeout) as response:
            response.raise_for_status()
            return await response.json()
    except asyncio.TimeoutError:
        return f"Таймаут при запросе {url}"
    except aiohttp.ClientError as e:
        return f"Ошибка при запросе {url}: {str(e)}"

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    subscribed_users.add(user_id)
    logging.info(f"Пользователь {user_id} подписался на уведомления")
    await update.message.reply_text("Привет! Я бот для получения текущей температуры. Используй команду /temperature, чтобы узнать температуру.")

# Обработчик команды /temperature
async def temperature(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = await get_current_temperatures()
    await update.message.reply_text(message)

async def get_current_temperatures():
    async with aiohttp.ClientSession() as session:
        # Получаем список термометров
        thermometers_url = "http://127.0.0.1:8000/api/thermometers/"
        thermometers_response = await fetch_data(session, thermometers_url)
        if isinstance(thermometers_response, str):
            return thermometers_response  # Возвращаем ошибку

        thermometers = thermometers_response

        # Формируем сообщение
        message = "Текущая температура со всех термометров:\n"
        for index, thermometer in enumerate(thermometers, start=1):
            # Получаем последнюю температуру для текущего термометра
            thermometer_id = thermometer['id']
            measurements_url = f"{DJANGO_API_URL}?thermometer={thermometer_id}"
            measurements_response = await fetch_data(session, measurements_url)
            if isinstance(measurements_response, str):
                message += f"{index}. {thermometer['name']} ({thermometer['location']}) - Ошибка при получении данных\n"
                continue

            if measurements_response:
                # Сортируем измерения по времени (timestamp) в порядке убывания
                measurements_response.sort(key=lambda x: x['timestamp'], reverse=True)
                last_measurement = measurements_response[0]  # Берём последнюю запись
                temperature = last_measurement['temperature']
                message += f"{index}. {thermometer['name']} ({thermometer['location']}): {temperature:.2f}°C\n"
            else:
                message += f"{index}. {thermometer['name']} ({thermometer['location']}) - Данные отсутствуют\n"

        return message

async def check_high_temperatures(application):
    logging.info("Проверка температуры запущена")
    async with aiohttp.ClientSession() as session:
        # Получаем список термометров
        thermometers_url = "http://127.0.0.1:8000/api/thermometers/"
        thermometers_response = await fetch_data(session, thermometers_url)
        if isinstance(thermometers_response, str):
            logging.error(f"Ошибка при получении термометров: {thermometers_response}")
            return

        thermometers = thermometers_response

        for thermometer in thermometers:
            thermometer_id = thermometer['id']
            measurements_url = f"{DJANGO_API_URL}?thermometer={thermometer_id}"
            measurements_response = await fetch_data(session, measurements_url)
            if isinstance(measurements_response, str):
                logging.error(f"Ошибка при получении измерений для термометра {thermometer_id}: {measurements_response}")
                continue

            if measurements_response:
                # Сортируем измерения по времени (timestamp) в порядке убывания
                measurements_response.sort(key=lambda x: x['timestamp'], reverse=True)
                last_measurement = measurements_response[0]  # Берём последнюю запись
                temperature = last_measurement['temperature']
                logging.info(f"Термометр {thermometer['name']}: {temperature}°C")  # Логируем температуру
                if temperature > 35:
                    message = f"Внимание! {temperature:.2f} градусов на термометре {thermometer['name']} ({thermometer['location']})"
                    logging.info(f"Отправка уведомления: {message}")
                    await send_notifications(application, message)  # Отправляем уведомления всем пользователям

async def send_notifications(application, message):
    tasks = []
    for user_id in subscribed_users:
        tasks.append(application.bot.send_message(chat_id=user_id, text=message))
    await asyncio.gather(*tasks)  # Отправляем все уведомления асинхронно

async def check_high_temperatures_loop(application):
    while True:
        await check_high_temperatures(application)
        await asyncio.sleep(1)  # Проверка каждую секунду

# Основная функция
def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("temperature", temperature))

    # Запускаем фоновую задачу
    application.job_queue.run_repeating(lambda context: asyncio.create_task(check_high_temperatures_loop(application)), interval=10, first=0)

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
