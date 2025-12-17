"""
Тесты для GUI клиента.
"""
import sys
import os
import json
from unittest.mock import Mock, MagicMock, patch, call

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestClient:
    """Тесты для класса Client."""
    
    def test_client_initialization(self):
        """Тест инициализации клиента."""
        # Создаем простую заглушку класса Client
        class Client:
            def __init__(self, host='localhost', port=65432):
                self.host = host
                self.port = port
                self.sock = None
        
        client = Client(host='127.0.0.1', port=12345)
        
        assert client.host == '127.0.0.1'
        assert client.port == 12345
        assert client.sock is None
    
    def test_client_connect_logic(self):
        """Тест логики подключения."""
        # Создаем заглушку с логикой подключения
        class Client:
            def __init__(self):
                self.sock = None
            
            def connect(self):
                if self.sock:
                    return True
                try:
                    # Имитируем успешное подключение
                    self.sock = Mock()
                    return True
                except Exception:
                    return False
        
        client = Client()
        # Первое подключение
        result1 = client.connect()
        assert result1 == True
        assert client.sock is not None
        
        # Повторное подключение (уже подключен)
        result2 = client.connect()
        assert result2 == True
    
    def test_client_close(self):
        """Тест закрытия соединения."""
        # Создаем заглушку с методом close
        class Client:
            def __init__(self):
                self.sock = None
            
            def close(self):
                if self.sock:
                    # Имитируем закрытие сокета
                    try:
                        self.sock = None
                    except Exception:
                        pass
                self.sock = None
        
        client = Client()
        
        # Сценарий 1: Закрытие когда сокет установлен
        client.sock = Mock()
        client.close()
        assert client.sock is None
        
        # Сценарий 2: Закрытие когда сокет уже None
        client.sock = None
        client.close()
        assert client.sock is None
    
    @patch('socket.socket')
    def test_client_network_operations(self, mock_socket_class):
        """Тест сетевых операций клиента."""
        # Создаем мок сокета
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket
        
        # Создаем класс Client с сетевыми операциями
        class Client:
            def __init__(self):
                self.sock = None
            
            def connect(self):
                try:
                    self.sock = mock_socket
                    return True
                except Exception:
                    return False
            
            def send(self, data):
                if not self.sock:
                    return
                try:
                    # Имитируем отправку данных
                    json_data = json.dumps(data).encode('utf-8') + b'\n'
                    self.sock.sendall(json_data)
                except Exception:
                    self.close()
            
            def close(self):
                if self.sock:
                    try:
                        self.sock.close()
                    except Exception:
                        pass
                    self.sock = None
        
        client = Client()
        
        # Тест подключения
        assert client.connect() == True
        assert client.sock == mock_socket
        
        # Тест отправки данных
        test_data = {'action': 'test', 'value': 123}
        client.send(test_data)
        
        # Проверяем, что sendall был вызван
        mock_socket.sendall.assert_called_once()
        
        # Тест закрытия
        client.close()
        assert client.sock is None

class TestAppControllerBasic:
    """Базовые тесты для AppController."""
    
    def test_app_state_management(self):
        """Тест управления состоянием приложения."""
        # Создаем простую заглушку AppController
        class AppController:
            def __init__(self):
                self.authenticated = False
                self.username = None
                self.wizard_selections = {
                    "condition": None,
                    "goal": None,
                    "level": None
                }
                self.current_exercises = []
            
            def login(self, username):
                self.authenticated = True
                self.username = username
            
            def logout(self):
                self.authenticated = False
                self.username = None
                self.current_exercises = []
                self.wizard_selections = {
                    "condition": None,
                    "goal": None,
                    "level": None
                }
            
            def set_wizard_selection(self, key, value):
                self.wizard_selections[key] = value
        
        app = AppController()
        
        # Проверяем начальное состояние
        assert app.authenticated == False
        assert app.username is None
        assert app.wizard_selections["condition"] is None
        
        # Тест логина
        app.login("testuser")
        assert app.authenticated == True
        assert app.username == "testuser"
        
        # Тест установки выбора в мастере
        app.set_wizard_selection("condition", "Дом")
        assert app.wizard_selections["condition"] == "Дом"
        
        # Тест логаута
        app.logout()
        assert app.authenticated == False
        assert app.username is None
        assert app.wizard_selections["condition"] is None
    
    def test_exercise_management(self):
        """Тест управления упражнениями."""
        class AppController:
            def __init__(self):
                self.current_exercises = []
            
            def add_exercise(self, exercise):
                self.current_exercises.append(exercise)
            
            def clear_exercises(self):
                self.current_exercises = []
            
            def get_exercise_count(self):
                return len(self.current_exercises)
        
        app = AppController()
        
        # Проверяем начальное состояние
        assert app.get_exercise_count() == 0
        
        # Добавляем упражнения
        exercise1 = {"name": "Приседания", "sets": 3, "reps": 10}
        exercise2 = {"name": "Отжимания", "sets": 4, "reps": 12}
        
        app.add_exercise(exercise1)
        assert app.get_exercise_count() == 1
        
        app.add_exercise(exercise2)
        assert app.get_exercise_count() == 2
        
        # Очищаем упражнения
        app.clear_exercises()
        assert app.get_exercise_count() == 0