import asyncio
import aiohttp
import logging

async def fetch_temperature(session, url):
    try:
        async with session.get(url) as response:
            data = await response.json()
            return data['temperatureC']
    except Exception as e:
        logging.error(f"Ошибка при получении температуры из {url}: {e}")

async def get_temperatures(sensor_urls, timeout):
    temperatures = {}
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in sensor_urls:
            task = asyncio.create_task(fetch_temperature(session, url))
            tasks.append(task)
        try:
            done, pending = await asyncio.wait(tasks, timeout=timeout)
            for task in done:
                result = task.result()
                if result is not None:
                    temperatures[task.get_name()] = result
        except asyncio.TimeoutError:
            logging.warning("Время получения данных о температуре истекло")
            for task in tasks:
                if not task.done():
                    task.cancel()
    return temperatures

# Пример использования
sensor_urls = [
    "http://example.com/sensor1",
    "http://example.com/sensor2",
    "http://example.com/sensor3"
]

logging.basicConfig(level=logging.INFO)
temperatures = asyncio.run(get_temperatures(sensor_urls, timeout=5))
logging.info(f"Температурa: {temperatures}")
