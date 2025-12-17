# main.py
import threading
import sys
import os

# Импортируем Server, константы и функции для запуска из server.py
from server import run_server, HOST, PORT, LoggerObserver 
# Импортируем DatabaseManager, чтобы гарантировать создание таблиц перед запуском сервера
from models import DatabaseManager

def mock_log(message):
    """Простая функция логирования для консоли."""
    print(f"[LOG] {message}")

def start_server():
    """Инициализирует и запускает сервер в главном потоке."""
    print(f"--- Запуск Fitness App Server на {HOST}:{PORT} ---")
    
    # Инициализация DatabaseManager, которая создает файл БД ('fitness_app.db') и таблицы.
    try:
        DatabaseManager() 
        print(f"[INFO] База данных инициализирована. Файл: fitness_app.db")
    except Exception as e:
        print(f"[FATAL] Ошибка инициализации базы данных: {e}")
        return

    stop_event = threading.Event()
    run_server(stop_event, mock_log)

if __name__ == "__main__":
    start_server()