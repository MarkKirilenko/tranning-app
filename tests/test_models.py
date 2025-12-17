"""
Упрощенные тесты для моделей без зависимостей от SQLAlchemy.
"""
import pytest
import sys
import os
import tempfile
import sqlite3
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class SimpleDatabase:
    """
    Упрощенная реализация базы данных для тестирования.
    Использует SQLite напрямую, без SQLAlchemy.
    """
    
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        """Создание таблиц базы данных."""
        cursor = self.conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                phone TEXT,
                dob TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица упражнений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                muscle_group TEXT,
                level TEXT,
                equipment TEXT,
                duration_minutes INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица планов тренировок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workout_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                plan_name TEXT NOT NULL,
                level TEXT,
                goal TEXT,
                condition TEXT,
                exercises TEXT,  -- JSON список упражнений
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица истории тренировок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workout_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                workout_name TEXT NOT NULL,
                exercises TEXT,  -- JSON список упражнений
                duration_minutes INTEGER,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def add_user(self, username, password_hash, phone=None, dob=None):
        """Добавление пользователя."""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password_hash, phone, dob)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, phone, dob))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_user(self, username):
        """Получение пользователя по имени."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        
        if row:
            return {
                'id': row[0],
                'username': row[1],
                'password_hash': row[2],
                'phone': row[3],
                'dob': row[4],
                'created_at': row[5]
            }
        return None
    
    def check_password(self, username, password_hash):
        """Проверка пароля пользователя."""
        user = self.get_user(username)
        if user:
            return user['password_hash'] == password_hash
        return False
    
    def add_exercise(self, name, description, muscle_group, level, equipment="", duration=0):
        """Добавление упражнения."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO exercises (name, description, muscle_group, level, equipment, duration_minutes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, description, muscle_group, level, equipment, duration))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_exercises_by_level(self, level):
        """Получение упражнений по уровню сложности."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM exercises WHERE level = ?', (level,))
        rows = cursor.fetchall()
        
        exercises = []
        for row in rows:
            exercises.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'muscle_group': row[3],
                'level': row[4],
                'equipment': row[5],
                'duration_minutes': row[6],
                'created_at': row[7]
            })
        
        return exercises
    
    def save_workout_plan(self, username, plan_name, level, goal, condition, exercises):
        """Сохранение плана тренировки."""
        cursor = self.conn.cursor()
        exercises_json = json.dumps(exercises)
        
        cursor.execute('''
            INSERT INTO workout_plans (username, plan_name, level, goal, condition, exercises)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, plan_name, level, goal, condition, exercises_json))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_user_plans(self, username):
        """Получение планов тренировок пользователя."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM workout_plans WHERE username = ?', (username,))
        rows = cursor.fetchall()
        
        plans = []
        for row in rows:
            try:
                exercises = json.loads(row[6]) if row[6] else []
            except json.JSONDecodeError:
                exercises = []
            
            plans.append({
                'id': row[0],
                'username': row[1],
                'plan_name': row[2],
                'level': row[3],
                'goal': row[4],
                'condition': row[5],
                'exercises': exercises,
                'created_at': row[7]
            })
        
        return plans
    
    def save_workout_history(self, username, workout_name, exercises, duration_minutes):
        """Сохранение истории тренировки."""
        cursor = self.conn.cursor()
        exercises_json = json.dumps(exercises)
        
        cursor.execute('''
            INSERT INTO workout_history (username, workout_name, exercises, duration_minutes)
            VALUES (?, ?, ?, ?)
        ''', (username, workout_name, exercises_json, duration_minutes))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_workout_history(self, username, limit=10):
        """Получение истории тренировок пользователя."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM workout_history 
            WHERE username = ? 
            ORDER BY completed_at DESC 
            LIMIT ?
        ''', (username, limit))
        
        rows = cursor.fetchall()
        history = []
        
        for row in rows:
            try:
                exercises = json.loads(row[3]) if row[3] else []
            except json.JSONDecodeError:
                exercises = []
            
            history.append({
                'id': row[0],
                'username': row[1],
                'workout_name': row[2],
                'exercises': exercises,
                'duration_minutes': row[4],
                'completed_at': row[5]
            })
        
        return history
    
    def close(self):
        """Закрытие соединения с базой данных."""
        if self.conn:
            self.conn.close()

class TestSimpleDatabase:
    """Тесты для упрощенной базы данных."""
    
    @pytest.fixture
    def db(self):
        """Фикстура для создания временной базы данных в памяти."""
        database = SimpleDatabase(":memory:")
        yield database
        database.close()
    
    def test_create_tables(self, db):
        """Тест создания таблиц."""
        cursor = db.conn.cursor()
        
        # Проверяем существование таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert 'users' in tables
        assert 'exercises' in tables
        assert 'workout_plans' in tables
        assert 'workout_history' in tables
    
    def test_user_operations(self, db):
        """Тест операций с пользователями."""
        # Добавляем пользователя
        user_id = db.add_user(
            username="testuser",
            password_hash="hashed_password_123",
            phone="+79123456789",
            dob="1990-01-01"
        )
        
        assert user_id == 1
        
        # Получаем пользователя
        user = db.get_user("testuser")
        
        assert user is not None
        assert user['username'] == "testuser"
        assert user['phone'] == "+79123456789"
        assert user['dob'] == "1990-01-01"
        
        # Проверяем пароль
        assert db.check_password("testuser", "hashed_password_123") == True
        assert db.check_password("testuser", "wrong_password") == False
        assert db.check_password("nonexistent", "any_password") == False
    
    def test_exercise_operations(self, db):
        """Тест операций с упражнениями."""
        # Добавляем упражнения
        exercise1_id = db.add_exercise(
            name="Приседания",
            description="Базовое упражнение для ног",
            muscle_group="ноги",
            level="новичок",
            equipment="гантели",
            duration=10
        )
        
        exercise2_id = db.add_exercise(
            name="Отжимания",
            description="Упражнение для груди и рук",
            muscle_group="грудь, руки",
            level="новичок"
        )
        
        exercise3_id = db.add_exercise(
            name="Становая тяга",
            description="Сложное упражнение для спины",
            muscle_group="спина",
            level="продвинутый"
        )
        
        assert exercise1_id == 1
        assert exercise2_id == 2
        assert exercise3_id == 3
        
        # Получаем упражнения для новичков
        beginner_exercises = db.get_exercises_by_level("новичок")
        
        assert len(beginner_exercises) == 2
        assert beginner_exercises[0]['name'] == "Приседания"
        assert beginner_exercises[1]['name'] == "Отжимания"
        
        # Проверяем поля упражнений
        for exercise in beginner_exercises:
            assert exercise['level'] == "новичок"
    
    def test_workout_plan_operations(self, db):
        """Тест операций с планами тренировок."""
        # Добавляем пользователя
        db.add_user("testuser", "password_hash")
        
        # Создаем упражнения для плана
        exercises = [
            {"name": "Приседания", "sets": 3, "reps": 10},
            {"name": "Отжимания", "sets": 4, "reps": 12},
            {"name": "Планка", "duration": 60}
        ]
        
        # Сохраняем план тренировки
        plan_id = db.save_workout_plan(
            username="testuser",
            plan_name="Базовая тренировка",
            level="новичок",
            goal="похудение",
            condition="дом",
            exercises=exercises
        )
        
        assert plan_id == 1
        
        # Получаем планы пользователя
        plans = db.get_user_plans("testuser")
        
        assert len(plans) == 1
        assert plans[0]['plan_name'] == "Базовая тренировка"
        assert plans[0]['level'] == "новичок"
        assert plans[0]['goal'] == "похудение"
        assert len(plans[0]['exercises']) == 3
    
    def test_workout_history_operations(self, db):
        """Тест операций с историей тренировок."""
        # Добавляем пользователя
        db.add_user("testuser", "password_hash")
        
        # Создаем данные тренировки
        workout_exercises = [
            {"name": "Приседания", "completed": True},
            {"name": "Отжимания", "completed": True},
            {"name": "Планка", "completed": False}
        ]
        
        # Сохраняем историю тренировки
        history_id = db.save_workout_history(
            username="testuser",
            workout_name="Утренняя тренировка",
            exercises=workout_exercises,
            duration_minutes=45
        )
        
        assert history_id == 1
        
        # Получаем историю тренировок
        history = db.get_workout_history("testuser")
        
        assert len(history) == 1
        assert history[0]['workout_name'] == "Утренняя тренировка"
        assert history[0]['duration_minutes'] == 45
        assert len(history[0]['exercises']) == 3
    
    def test_duplicate_username(self, db):
        """Тест добавления пользователя с дублирующимся именем."""
        # Первый пользователь добавляется успешно
        user_id1 = db.add_user("user1", "hash1")
        assert user_id1 == 1
        
        # Второй пользователь с тем же именем должен вернуть None
        user_id2 = db.add_user("user1", "hash2")
        assert user_id2 is None
        
        # Третий пользователь с другим именем добавляется успешно
        user_id3 = db.add_user("user2", "hash3")
        assert user_id3 == 2