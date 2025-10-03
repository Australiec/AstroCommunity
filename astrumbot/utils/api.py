import aiohttp
import asyncio

# Отправляет API запрос на URL и повторяет попытку в случае ошибки
async def api_request(url: str, retries=3):
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if await response.text() == "Server Error":
                        if attempt < retries - 1:
                            await asyncio.sleep(30)
                        else:
                            return None
                    else:
                        return await response.text()
        # Повторяем попытку если сервер недоступен
        except Exception:
            if attempt < retries - 1:
                await asyncio.sleep(30)
            else:
                return None