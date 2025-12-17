# nutrition.py
import json
import os

class NutritionPlan:
    """Класс для работы с планами питания."""
    
    def __init__(self):
        self.plans_file = "nutrition_plans.json"
        self.nutrition_plans = self._load_plans()
        
    def _load_plans(self):
        """Загружает планы питания из файла."""
        if os.path.exists(self.plans_file):
            with open(self.plans_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._create_default_plans()
    
    def _create_default_plans(self):
        """Создает базовые планы питания."""
        default_plans = {
            "Похудение": {
                "description": "Дефицит калорий для плавного снижения веса",
                "calories": 1800,
                "protein": 120,
                "carbs": 180,
                "fat": 50,
                "meals": [
                    {"time": "08:00", "name": "Завтрак", "description": "Овсянка с ягодами + яйцо"},
                    {"time": "11:00", "name": "Перекус", "description": "Яблоко + горсть орехов"},
                    {"time": "14:00", "name": "Обед", "description": "Куриная грудка с гречкой и овощами"},
                    {"time": "17:00", "name": "Перекус", "description": "Творог с йогуртом"},
                    {"time": "20:00", "name": "Ужин", "description": "Рыба на пару с салатом"}
                ],
                "tips": [
                    "Пейте 2-3 литра воды в день",
                    "Исключите сладкие напитки",
                    "Ешьте медленно, тщательно пережевывая пищу"
                ]
            },
            "Набор мышц": {
                "description": "Профицит калорий для роста мышечной массы",
                "calories": 2800,
                "protein": 180,
                "carbs": 320,
                "fat": 70,
                "meals": [
                    {"time": "07:00", "name": "Завтрак", "description": "Омлет из 3 яиц + тосты с авокадо"},
                    {"time": "10:00", "name": "Перекус", "description": "Протеиновый коктейль + банан"},
                    {"time": "13:00", "name": "Обед", "description": "Говядина с рисом и овощами"},
                    {"time": "16:00", "name": "Перекус", "description": "Творог + мед + орехи"},
                    {"time": "19:00", "name": "Ужин", "description": "Лосось с картофелем и брокколи"},
                    {"time": "21:30", "name": "Перед сном", "description": "Казеиновый протеин"}
                ],
                "tips": [
                    "Принимайте пищу каждые 2.5-3 часа",
                    "Увеличьте потребление белка",
                    "Не пропускайте приемы пищи"
                ]
            },
            "Поддержание": {
                "description": "Баланс калорий для поддержания текущего веса",
                "calories": 2300,
                "protein": 140,
                "carbs": 250,
                "fat": 60,
                "meals": [
                    {"time": "08:00", "name": "Завтрак", "description": "Гречневая каша с молоком"},
                    {"time": "11:00", "name": "Перекус", "description": "Йогурт с фруктами"},
                    {"time": "14:00", "name": "Обед", "description": "Индейка с киноа и салатом"},
                    {"time": "17:00", "name": "Перекус", "description": "Протеиновый батончик"},
                    {"time": "20:00", "name": "Ужин", "description": "Тунец с овощным рагу"}
                ],
                "tips": [
                    "Соблюдайте баланс БЖУ",
                    "Включайте разнообразные продукты",
                    "Слушайте сигналы голода и насыщения"
                ]
            }
        }
        
        # Сохраняем в файл
        with open(self.plans_file, 'w', encoding='utf-8') as f:
            json.dump(default_plans, f, ensure_ascii=False, indent=2)
        
        return default_plans
    
    def get_plan(self, goal):
        """Получает план питания по цели."""
        return self.nutrition_plans.get(goal)
    
    def save_user_plan(self, username, goal, customizations):
        """Сохраняет персонализированный план пользователя."""
        user_plans_file = f"user_nutrition_{username}.json"
        user_data = {
            "goal": goal,
            "base_plan": self.get_plan(goal),
            "customizations": customizations,
            "created_at": "2024-01-01"  # Здесь будет текущая дата
        }
        
        with open(user_plans_file, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
        
        return user_data