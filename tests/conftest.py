import pytest
import sys
import os
import tempfile
import json
from unittest.mock import Mock, MagicMock, patch

# Добавляем корневую директорию в путь Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Создаем заглушки для отсутствующих модулей
if 'customtkinter' not in sys.modules:
    sys.modules['customtkinter'] = MagicMock()

# Мокаем Tkinter модули для GUI тестов
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()

# Глобальные заглушки для импортов
class MockCTk:
    def __init__(self):
        pass

class MockLocalizationManager:
    def __init__(self):
        self.current_lang = 'ru'
    
    def set_language(self, lang):
        self.current_lang = lang

# Регистрируем заглушки
sys.modules['localization'] = type(sys)('localization')
sys.modules['localization'].LocalizationManager = MockLocalizationManager

# Фикстуры для тестов
@pytest.fixture
def temp_db_path():
    """Фикстура для временного файла БД (путь, а не URL)."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    yield db_path
    # Удаление после теста
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def mock_socket():
    """Фикстура для мока сокета."""
    with patch('socket.socket') as mock_socket_class:
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket
        yield mock_socket

@pytest.fixture
def sample_user_data():
    """Пример данных пользователя."""
    return {
        'username': 'testuser',
        'password': 'Password123!',
        'phone': '+79123456789',
        'dob': '1990-01-01'
    }

@pytest.fixture
def sample_exercise():
    """Пример упражнения."""
    return {
        'name': 'Приседания',
        'description': 'Базовое упражнение для ног',
        'sets': 3,
        'reps': 10,
        'duration': 60
    }

@pytest.fixture
def mock_db_manager():
    """Мок менеджера БД."""
    mock = Mock()
    mock.check_password.return_value = True
    mock.get_user.return_value = {'username': 'testuser', 'id': 1}
    mock.add_user.return_value = 1
    mock.get_exercises_by_criteria.return_value = [
        {'name': 'Приседания', 'sets': 3, 'reps': 10}
    ]
    return mock

@pytest.fixture
def mock_client():
    """Мок клиента."""
    with patch('client_gui.Client') as mock:
        client_instance = MagicMock()
        client_instance.connect.return_value = True
        client_instance.sock = None
        mock.return_value = client_instance
        yield client_instance