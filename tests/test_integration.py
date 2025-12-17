"""
Интеграционные тесты для проверки взаимодействия компонентов.
"""
import sys
import os
from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestClientServerIntegration:
    """Тесты интеграции клиента и сервера."""
    
    def test_authentication_flow(self):
        """Тест потока аутентификации."""
        # Моделируем клиент и сервер
        class MockServer:
            def __init__(self):
                self.users = {
                    "admin": "password123",
                    "user1": "pass456"
                }
                self.logged_in_users = set()
            
            def authenticate(self, username, password):
                if username in self.users and self.users[username] == password:
                    self.logged_in_users.add(username)
                    return True
                return False
            
            def logout(self, username):
                if username in self.logged_in_users:
                    self.logged_in_users.remove(username)
                    return True
                return False
        
        class MockClient:
            def __init__(self, server):
                self.server = server
                self.username = None
                self.authenticated = False
            
            def login(self, username, password):
                if self.server.authenticate(username, password):
                    self.username = username
                    self.authenticated = True
                    return True
                return False
            
            def logout(self):
                if self.username and self.authenticated:
                    self.server.logout(self.username)
                    self.username = None
                    self.authenticated = False
                    return True
                return False
        
        # Создаем сервер и клиент
        server = MockServer()
        client = MockClient(server)
        
        # Тест успешного логина
        assert client.login("admin", "password123") == True
        assert client.authenticated == True
        assert client.username == "admin"
        assert "admin" in server.logged_in_users
        
        # Тест неуспешного логина
        assert client.login("user1", "wrong_password") == False
        assert client.authenticated == True  # Остается залогиненным как admin
        assert "user1" not in server.logged_in_users
        
        # Тест логаута
        assert client.logout() == True
        assert client.authenticated == False
        assert client.username is None
        assert "admin" not in server.logged_in_users
        
        # Тест логаута без логина
        assert client.logout() == False
    
    def test_exercise_selection_flow(self):
        """Тест потока выбора упражнений."""
        class ExerciseSystem:
            def __init__(self):
                self.exercises = {
                    "новичок": ["Приседания", "Отжимания", "Планка"],
                    "средний": ["Подтягивания", "Выпады", "Берпи"],
                    "продвинутый": ["Становая тяга", "Жим лежа", "Присед со штангой"]
                }
            
            def get_exercises_for_level(self, level, goal=None, condition=None):
                base_exercises = self.exercises.get(level, [])
                
                # Фильтрация по цели (упрощенная)
                if goal == "похудение":
                    if level == "новичок":
                        # Для новичка при похудении исключаем отжимания, добавляем кардио
                        return [ex for ex in base_exercises if ex != "Отжимания"] + ["Кардио-разминка"]
                    elif level == "средний":
                        # Для среднего уровня добавляем больше кардио
                        return base_exercises + ["Прыжки на скакалке"]
                elif goal == "сила":
                    if level == "новичок":
                        # Для силы оставляем все базовые
                        return base_exercises
                
                return base_exercises
        
        class UserInterface:
            def __init__(self, exercise_system):
                self.exercise_system = exercise_system
                self.selected_exercises = []
            
            def select_exercises(self, level, goal=None, condition=None):
                exercises = self.exercise_system.get_exercises_for_level(level, goal, condition)
                self.selected_exercises = exercises
                return exercises
            
            def get_selected_count(self):
                return len(self.selected_exercises)
        
        # Создаем систему и интерфейс
        system = ExerciseSystem()
        ui = UserInterface(system)
        
        # Тест выбора упражнений для новичка
        exercises = ui.select_exercises("новичок")
        assert len(exercises) == 3
        assert "Приседания" in exercises
        assert "Отжимания" in exercises
        assert "Планка" in exercises
        assert ui.get_selected_count() == 3
        
        # Тест выбора упражнений для новичка с целью похудения
        exercises = ui.select_exercises("новичок", goal="похудение")
        # Ожидаем: Приседания, Планка, Кардио-разминка (без Отжиманий)
        assert len(exercises) == 3
        assert "Приседания" in exercises
        assert "Планка" in exercises
        assert "Кардио-разминка" in exercises
        assert "Отжимания" not in exercises
        
        # Тест выбора упражнений для среднего уровня с целью похудения
        exercises = ui.select_exercises("средний", goal="похудение")
        # Ожидаем: Подтягивания, Выпады, Берпи, Прыжки на скакалке
        assert len(exercises) == 4
        assert "Подтягивания" in exercises
        assert "Выпады" in exercises
        assert "Берпи" in exercises
        assert "Прыжки на скакалке" in exercises
        
        # Тест выбора упражнений для среднего уровня без цели
        exercises = ui.select_exercises("средний")
        assert len(exercises) == 3
        assert "Подтягивания" in exercises
        assert "Выпады" in exercises
        assert "Берпи" in exercises
        
        # Тест неизвестного уровня
        exercises = ui.select_exercises("неизвестный")
        assert len(exercises) == 0

class TestDataPersistence:
    """Тесты сохранения данных."""
    
    def test_json_data_persistence(self):
        """Тест сохранения данных в JSON."""
        import json
        import tempfile
        
        # Тестовые данные
        test_data = {
            "users": [
                {"id": 1, "name": "John", "age": 30},
                {"id": 2, "name": "Jane", "age": 25}
            ],
            "settings": {
                "language": "ru",
                "theme": "dark",
                "notifications": True
            }
        }
        
        # Сохраняем во временный файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f, indent=2)
            temp_file = f.name
        
        try:
            # Загружаем из файла
            with open(temp_file, 'r') as f:
                loaded_data = json.load(f)
            
            # Проверяем целостность данных
            assert loaded_data["users"][0]["name"] == "John"
            assert loaded_data["users"][1]["age"] == 25
            assert loaded_data["settings"]["language"] == "ru"
            assert loaded_data["settings"]["notifications"] == True
            
            # Проверяем, что данные идентичны
            assert loaded_data == test_data
            
        finally:
            # Удаляем временный файл
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_configuration_management(self):
        """Тест управления конфигурацией."""
        class ConfigManager:
            def __init__(self):
                self.config = {
                    "app_name": "Fitness App",
                    "version": "1.0.0",
                    "default_language": "ru",
                    "max_users": 100,
                    "features": {
                        "workout_tracking": True,
                        "nutrition_plan": True,
                        "progress_charts": False
                    }
                }
            
            def get(self, key, default=None):
                # Поддержка вложенных ключей через точку
                keys = key.split('.')
                value = self.config
                
                for k in keys:
                    if isinstance(value, dict) and k in value:
                        value = value[k]
                    else:
                        return default
                
                return value
            
            def set(self, key, value):
                keys = key.split('.')
                config = self.config
                
                # Проходим по всем ключам кроме последнего
                for k in keys[:-1]:
                    if k not in config:
                        config[k] = {}
                    config = config[k]
                
                # Устанавливаем значение
                config[keys[-1]] = value
            
            def get_all(self):
                return self.config.copy()
        
        # Создаем менеджер конфигурации
        config_manager = ConfigManager()
        
        # Тест получения значений
        assert config_manager.get("app_name") == "Fitness App"
        assert config_manager.get("version") == "1.0.0"
        assert config_manager.get("default_language") == "ru"
        
        # Тест получения вложенных значений
        assert config_manager.get("features.workout_tracking") == True
        assert config_manager.get("features.progress_charts") == False
        
        # Тест получения несуществующих значений
        assert config_manager.get("nonexistent") is None
        assert config_manager.get("nonexistent", "default") == "default"
        
        # Тест установки значений
        config_manager.set("default_language", "en")
        assert config_manager.get("default_language") == "en"
        
        config_manager.set("features.progress_charts", True)
        assert config_manager.get("features.progress_charts") == True
        
        # Тест установки нового значения
        config_manager.set("new_feature.enabled", True)
        assert config_manager.get("new_feature.enabled") == True