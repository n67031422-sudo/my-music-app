import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher
import yt_dlp

# Инициализация приложения
app = FastAPI()

# Разрешаем нашему сайту на GitHub Pages делать запросы к серверу
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = "9105900940:AAF4PBCWXqSIREwzXyEc50l1DzbGjyea4DY"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@app.get("/")
def read_root():
    return {"status": "Music Server is Running"}

# Маршрут для поиска музыки
@app.get("/search")
def search_music(query: str):
    if not query:
        return {"error": "Пустой запрос"}
    
    # Настройки для поиска через yt-dlp (ищет аудио в YouTube Music/YouTube)
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'default_search': 'ytsearch5', # Возвращает топ-5 результатов
        'quiet': True
    }
    
    results = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Ищем трек по названию или автору
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    results.append({
                        "title": entry.get("title", "Неизвестный трек"),
                        "author": entry.get("uploader", "Неизвестный автор"),
                        "url": entry.get("url"), # Прямая ссылка на аудиопоток для плеера
                        "duration": entry.get("duration")
                    })
        except Exception as e:
            return {"error": str(e)}
            
    return {"tracks": results}
