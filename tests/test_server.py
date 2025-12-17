"""
Тесты для серверной части.
"""
import sys
import os
import json
from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestServerLogic:
    """Тесты логики сервера."""
    
    def test_request_processing(self):
        """Тест обработки запросов."""
        # Функция обработки запросов (упрощенная версия)
        def process_request(request):
            action = request.get("action")
            
            if action == "ping":
                return {"status": "pong"}
            elif action == "echo":
                return {"message": request.get("message", "")}
            elif action == "login":
                username = request.get("username")
                password = request.get("password")
                if username == "admin" and password == "1234":
                    return {"success": True, "username": username}
                else:
                    return {"success": False, "error": "Invalid credentials"}
            else:
                return {"error": "Unknown action"}
        
        # Тестируем различные запросы
        # Пинг
        ping_request = {"action": "ping"}
        ping_response = process_request(ping_request)
        assert ping_response["status"] == "pong"
        
        # Эхо
        echo_request = {"action": "echo", "message": "Hello"}
        echo_response = process_request(echo_request)
        assert echo_response["message"] == "Hello"
        
        # Успешный логин
        login_success = {"action": "login", "username": "admin", "password": "1234"}
        login_response = process_request(login_success)
        assert login_response["success"] == True
        assert login_response["username"] == "admin"
        
        # Неуспешный логин
        login_fail = {"action": "login", "username": "user", "password": "wrong"}
        fail_response = process_request(login_fail)
        assert fail_response["success"] == False
        
        # Неизвестное действие
        unknown_request = {"action": "unknown"}
        unknown_response = process_request(unknown_request)
        assert "error" in unknown_response
    
    def test_json_parsing(self):
        """Тест парсинга JSON."""
        # Тестовые данные
        test_data = {
            "action": "test",
            "value": 123,
            "nested": {
                "key": "value"
            },
            "list": [1, 2, 3]
        }
        
        # Преобразуем в JSON и обратно
        json_str = json.dumps(test_data)
        parsed_data = json.loads(json_str)
        
        # Проверяем целостность данных
        assert parsed_data["action"] == "test"
        assert parsed_data["value"] == 123
        assert parsed_data["nested"]["key"] == "value"
        assert parsed_data["list"] == [1, 2, 3]
    
    def test_error_handling(self):
        """Тест обработки ошибок."""
        # Функция с обработкой ошибок
        def safe_process(data):
            try:
                if not isinstance(data, dict):
                    raise ValueError("Data must be a dictionary")
                
                if "divide" in data:
                    numerator = data.get("numerator", 0)
                    denominator = data.get("denominator", 1)
                    if denominator == 0:
                        raise ZeroDivisionError("Division by zero")
                    return numerator / denominator
                
                return {"processed": True}
                
            except (ValueError, ZeroDivisionError) as e:
                return {"error": str(e)}
            except Exception:
                return {"error": "Unknown error"}
        
        # Тест корректных данных
        assert safe_process({"test": 1}) == {"processed": True}
        
        # Тест деления
        assert safe_process({"divide": True, "numerator": 10, "denominator": 2}) == 5
        
        # Тест ошибок
        assert "error" in safe_process("not a dict")
        assert "error" in safe_process({"divide": True, "numerator": 10, "denominator": 0})

class TestLogger:
    """Тесты для системы логирования."""
    
    def test_logger_basic(self):
        """Базовый тест логгера."""
        class Logger:
            def __init__(self):
                self.logs = []
            
            def log(self, message, level="INFO"):
                self.logs.append({
                    "message": message,
                    "level": level,
                    "timestamp": "2024-01-01T00:00:00"
                })
            
            def get_logs(self):
                return self.logs
            
            def clear_logs(self):
                self.logs = []
        
        logger = Logger()
        
        # Проверяем начальное состояние
        assert len(logger.get_logs()) == 0
        
        # Добавляем логи
        logger.log("Тестовое сообщение 1")
        logger.log("Ошибка", "ERROR")
        logger.log("Предупреждение", "WARNING")
        
        # Проверяем логи
        logs = logger.get_logs()
        assert len(logs) == 3
        assert logs[0]["message"] == "Тестовое сообщение 1"
        assert logs[1]["level"] == "ERROR"
        assert logs[2]["level"] == "WARNING"
        
        # Очищаем логи
        logger.clear_logs()
        assert len(logger.get_logs()) == 0
    
    def test_logger_with_observer(self):
        """Тест логгера с паттерном наблюдатель."""
        class Observer:
            def __init__(self, name):
                self.name = name
                self.messages = []
            
            def update(self, message):
                self.messages.append(message)
        
        class LoggerWithObservers:
            def __init__(self):
                self.observers = []
            
            def add_observer(self, observer):
                self.observers.append(observer)
            
            def remove_observer(self, observer):
                self.observers.remove(observer)
            
            def notify_observers(self, message):
                for observer in self.observers:
                    observer.update(message)
            
            def log(self, message):
                self.notify_observers(message)
        
        # Создаем логгер и наблюдателей
        logger = LoggerWithObservers()
        observer1 = Observer("Observer1")
        observer2 = Observer("Observer2")
        
        # Добавляем наблюдателей
        logger.add_observer(observer1)
        logger.add_observer(observer2)
        
        # Логируем сообщение
        test_message = "Test log message"
        logger.log(test_message)
        
        # Проверяем, что наблюдатели получили сообщение
        assert len(observer1.messages) == 1
        assert observer1.messages[0] == test_message
        assert len(observer2.messages) == 1
        assert observer2.messages[0] == test_message
        
        # Удаляем одного наблюдателя
        logger.remove_observer(observer1)
        logger.log("Another message")
        
        # Проверяем, что только оставшийся наблюдатель получил сообщение
        assert len(observer1.messages) == 1  # Не изменилось
        assert len(observer2.messages) == 2  # Добавилось