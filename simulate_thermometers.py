# thermometer_app/simulate_thermometers.py
import asyncio
import random
import aiohttp

BASE_URL = "http://127.0.0.1:8000/api/"
TOKEN = "02668a2389c6bac86ba5e99c5d09204799e70dd5" 

async def simulate_thermometer(thermometer_id):
    async with aiohttp.ClientSession() as session:
        while True:
            temperature = random.uniform(-20, 40)
            data = {
                "thermometer": thermometer_id,
                "temperature": temperature,
            }
            headers = {"Authorization": f"Token {TOKEN}"}  # Добавляем заголовок с токеном
            async with session.post(f"{BASE_URL}measurements/", json=data, headers=headers) as response:
                print(f"Термометр {thermometer_id}: Отправлено: {data}, Ответ: {response.status}")
            await asyncio.sleep(1)

async def main():
    # Запускаем симуляцию для двух термометров
    await asyncio.gather(
        simulate_thermometer(1),
        simulate_thermometer(2),
    )

if __name__ == "__main__":
    asyncio.run(main())