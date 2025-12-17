# localization.py
import json

class LocalizationManager:
    def __init__(self):
        self.current_lang = 'ru'
        self.translations = self._load_translations()
    
    def _load_translations(self):
        try:
            with open('localization.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._get_default_translations()
    
    def _get_default_translations(self):
        return {
            'ru': {
                'login_title': 'Вход в систему',
                'username': 'Имя пользователя',
                'password': 'Пароль',
                'login': 'Войти',
                'no_account': 'Нет аккаунта? Зарегистрируйтесь',
                'register_title': 'Регистрация',
                'register_button': 'Зарегистрироваться',
                'phone_placeholder': 'Телефон (+375...)',
                'dob_placeholder': 'Дата рождения (ДД.ММ.ГГГГ)',
                'fill_all_fields': 'Заполните все поля',
                'invalid_phone': 'Неверный формат телефона',
                'server_settings': 'Настройки сервера',
                'manage_server': 'Управление сервером',
                'start_server': 'Запустить сервер',
                'stop_server': 'Остановить сервер',
                'welcome_user': 'Привет, {username}!',
                'create_workout': 'Создайте свою идеальную тренировку',
                'personalized_plan': 'Персонализированный план под ваш уровень и цели',
                'start': 'НАЧАТЬ СОЗДАНИЕ ПЛАНА',
                'workout_location': 'Где будем тренироваться?',
                'home': 'Дома',
                'gym': 'В зале',
                'workout_goal': 'Какую цель преследуем?',
                'weight_loss': 'Похудение',
                'muscle_gain': 'Набор мышц',
                'endurance': 'Выносливость',
                'workout_level': 'Ваш уровень подготовки?',
                'beginner': 'Новичок',
                'intermediate': 'Средний',
                'advanced': 'Продвинутый',
                'back': 'Назад',
                'back_to_main': 'На главную',
                'complete_all': 'Выполните все упражнения этапа',
                'next_stage': 'Следующий этап',
                'finish_workout': 'Завершить тренировку',
                'workout_complete': 'Тренировка успешно завершена!',
                'workout_history': 'История тренировок',
                'no_history': 'История тренировок пуста',
                'progress': 'Прогресс',
                'logout': 'Выйти',
                'lang_btn': 'EN',
                'nutrition_goal_title': 'Выберите цель питания',
                'maintenance': 'Поддержание формы',
                'workout_history': 'История тренировок'
            },
            'en': {
                'login_title': 'Login',
                'username': 'Username',
                'password': 'Password',
                'login': 'Login',
                'no_account': 'No account? Register',
                'register_title': 'Registration',
                'register_button': 'Register',
                'phone_placeholder': 'Phone (+375...)',
                'dob_placeholder': 'Date of birth (DD.MM.YYYY)',
                'fill_all_fields': 'Fill all fields',
                'invalid_phone': 'Invalid phone format',
                'server_settings': 'Server Settings',
                'manage_server': 'Server Management',
                'start_server': 'Start Server',
                'stop_server': 'Stop Server',
                'welcome_user': 'Welcome, {username}!',
                'create_workout': 'Create Your Perfect Workout',
                'personalized_plan': 'Personalized plan for your level and goals',
                'start': 'START CREATING PLAN',
                'workout_location': 'Where will we train?',
                'home': 'Home',
                'gym': 'Gym',
                'workout_goal': 'What is your goal?',
                'weight_loss': 'Weight Loss',
                'muscle_gain': 'Muscle Gain',
                'endurance': 'Endurance',
                'workout_level': 'Your fitness level?',
                'beginner': 'Beginner',
                'intermediate': 'Intermediate',
                'advanced': 'Advanced',
                'back': 'Back',
                'back_to_main': 'To Main',
                'complete_all': 'Complete all exercises of the stage',
                'next_stage': 'Next Stage',
                'finish_workout': 'Finish Workout',
                'workout_complete': 'Workout successfully completed!',
                'workout_history': 'Workout History',
                'no_history': 'Workout history is empty',
                'progress': 'Progress',
                'logout': 'Logout',
                'lang_btn': 'RU',
                'nutrition_goal_title': 'Select Nutrition Goal',
                'maintenance': 'Maintenance',
                'workout_history': 'Workout History'
            }
        }
    
    def set_language(self, lang):
        if lang in self.translations:
            self.current_lang = lang
    
    def get(self, key, **kwargs):
        text = self.translations.get(self.current_lang, {}).get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except:
                pass
        return text