# client_styles.py
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox
from client_validation import Validator

# --- ЦВЕТОВАЯ ПАЛИТРА "WORKOUT COOL" ---
ACCENT_COLOR = "#007AFF"
HIGHLIGHT_COLOR = "#FF9500"
CARD_BG_COLOR = "#1C1C1E"
TEXT_HEADER_COLOR = "#FFFFFF"
TEXT_BODY_COLOR = "#E5E5E7"

# Шрифты
HEADER_FONT = ("Helvetica Neue", 28, "bold")
SUBHEADER_FONT = ("Helvetica Neue", 18)
BODY_FONT = ("Helvetica Neue", 14)
BUTTON_FONT = ("Helvetica Neue", 16, "bold")

class BaseFrame(ctk.CTkFrame):
    """Базовый класс фрейма с общим верхним меню (NavBar)."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller
        self._setup_nav_bar()

    def _setup_nav_bar(self):
        # Верхняя навигационная панель
        nav_bar = ctk.CTkFrame(self, fg_color=CARD_BG_COLOR, height=50, corner_radius=0)
        nav_bar.pack(fill="x", side="top")

        # Логотип / Название слева
        app_label = ctk.CTkLabel(nav_bar, text="🏋️ Fitness App", font=("Helvetica Neue", 16, "bold"), text_color=ACCENT_COLOR)
        app_label.pack(side="left", padx=20, pady=10)
        
        # Кнопки справа
        right_frame = ctk.CTkFrame(nav_bar, fg_color="transparent")
        right_frame.pack(side="right", padx=10)

        # Кнопка переключения языка
        self.lang_btn = ctk.CTkButton(right_frame, 
                                     width=50,
                                     font=BODY_FONT,
                                     fg_color="transparent", 
                                     text_color=TEXT_BODY_COLOR, 
                                     hover_color=CARD_BG_COLOR,
                                     command=self.controller.toggle_language)
        self.lang_btn.pack(side="left", padx=5)

        # Кнопка История тренировок
        if isinstance(self, (ExerciseFrame, ProgressFrame, NutritionPlanFrame, WorkoutHistoryFrame)):
            self.history_btn = ctk.CTkButton(right_frame, 
                                            font=BODY_FONT,
                                            fg_color="transparent", 
                                            text_color=TEXT_BODY_COLOR, 
                                            hover_color=CARD_BG_COLOR,
                                            command=self.controller.open_workout_history)
            self.history_btn.pack(side="left", padx=5)

        # Настройки
        settings_btn = ctk.CTkButton(right_frame, text="⚙️", width=40, font=BODY_FONT,
                                    fg_color="transparent", 
                                    text_color=TEXT_BODY_COLOR, 
                                    hover_color=CARD_BG_COLOR,
                                    command=self.controller.open_server_menu)
        settings_btn.pack(side="left", padx=5)
        
        # Выход
        self.logout_btn = ctk.CTkButton(right_frame, 
                                       width=60, 
                                       font=BODY_FONT,
                                       fg_color=HIGHLIGHT_COLOR, 
                                       hover_color="#E08500", 
                                       text_color=TEXT_HEADER_COLOR,
                                       command=self.controller.on_logout)
        self.logout_btn.pack(side="left", padx=5)
        
        # Обновляем тексты кнопок
        self.update_texts()

    def update_texts(self):
        """Обновляет тексты в навигационной панели."""
        self.lang_btn.configure(text=self.controller.loc.get("lang_btn"))
        if hasattr(self, 'history_btn'):
            self.history_btn.configure(text=self.controller.loc.get("workout_history"))
        self.logout_btn.configure(text=self.controller.loc.get("logout"))

# ==========================================
# НОВЫЕ ФРЕЙМЫ ДЛЯ ПОШАГОВОГО МАСТЕРА (WIZARD)
# ==========================================

class LandingFrame(BaseFrame):
    """Главный экран-лендинг после входа."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, **kwargs)
        self.welcome_label = None
        self.create_workout_label = None
        self.personalized_plan_label = None
        self.start_btn = None
        self.nutrition_btn = None
        self.existing_btn = None
        self.history_btn = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        # Центральный контент
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=40, pady=40)

        welcome_text = self.controller.loc.get("welcome_user", username=self.controller.username)
        self.welcome_label = ctk.CTkLabel(content_frame, text=welcome_text, font=SUBHEADER_FONT, text_color=ACCENT_COLOR)
        self.welcome_label.pack(pady=(0, 10), anchor="w")

        self.create_workout_label = ctk.CTkLabel(content_frame, text=self.controller.loc.get("create_workout"), 
                                                font=HEADER_FONT, text_color=TEXT_HEADER_COLOR, justify="left")
        self.create_workout_label.pack(pady=(0, 20), anchor="w")
        
        self.personalized_plan_label = ctk.CTkLabel(content_frame, text=self.controller.loc.get("personalized_plan"), 
                                                   font=SUBHEADER_FONT, text_color=TEXT_BODY_COLOR, justify="left")
        self.personalized_plan_label.pack(pady=(0, 40), anchor="w")

        # Фрейм для кнопок
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=10)

        # Первая строка кнопок
        top_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        top_buttons_frame.pack(fill="x", pady=(0, 10))

        # Кнопка "Начать создание плана" (занимает всю ширину)
        self.start_btn = ctk.CTkButton(top_buttons_frame, 
                                      font=BUTTON_FONT, height=50, corner_radius=25,
                                      fg_color=ACCENT_COLOR, hover_color="#0069D9",
                                      command=self.controller.start_wizard)
        self.start_btn.pack(fill="x", ipadx=20)

        # Вторая строка кнопок
        bottom_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        bottom_buttons_frame.pack(fill="x")

        # Кнопка "Создать план питания" (слева)
        self.nutrition_btn = ctk.CTkButton(bottom_buttons_frame, 
                                          font=("Helvetica Neue", 14, "bold"), height=45, corner_radius=20,
                                          fg_color=HIGHLIGHT_COLOR, hover_color="#E08500",
                                          command=self.controller.on_create_nutrition_plan)
        self.nutrition_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # Кнопка "Существующие планы" (справа)
        self.existing_btn = ctk.CTkButton(bottom_buttons_frame, 
                                         font=("Helvetica Neue", 14, "bold"), height=45, corner_radius=20,
                                         fg_color="#30D158", hover_color="#20B148",
                                         command=self.controller.on_use_existing_workout_plan)
        self.existing_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        # Кнопка "История тренировок" (третья строка)
        self.history_btn = ctk.CTkButton(buttons_frame,
                                        font=("Helvetica Neue", 14, "bold"), height=45, corner_radius=20,
                                        fg_color="#AF52DE", hover_color="#8E44D9",
                                        command=self.controller.open_workout_history)
        self.history_btn.pack(fill="x", pady=(10, 0))
        
        self.update_texts()
    
    def update_texts(self):
        """Обновляет тексты на фрейме."""
        super().update_texts()
        welcome_text = self.controller.loc.get("welcome_user", username=self.controller.username)
        self.welcome_label.configure(text=welcome_text)
        self.create_workout_label.configure(text=self.controller.loc.get("create_workout"))
        self.personalized_plan_label.configure(text=self.controller.loc.get("personalized_plan"))
        self.start_btn.configure(text=self.controller.loc.get("start"))
        self.nutrition_btn.configure(text="🍎 " + self.controller.loc.get("create_nutrition_plan"))
        self.existing_btn.configure(text="📁 " + self.controller.loc.get("existing_plans"))
        self.history_btn.configure(text="📊 " + self.controller.loc.get("workout_history"))

class StepFrameBase(BaseFrame):
    """Базовый класс для шагов мастера, добавляет заголовок и кнопку 'Назад'."""
    def __init__(self, master, controller, title_key, step_id, **kwargs):
        super().__init__(master, controller, **kwargs)
        self.step_id = step_id
        self.title_key = title_key
        self.back_btn = None
        self.title_label = None
        
        self._create_header()
        self._create_content()

    def _create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(30, 20))
        
        # Кнопка Назад
        self.back_btn = ctk.CTkButton(header_frame, font=BODY_FONT, width=80,
                                     fg_color="transparent", text_color=TEXT_BODY_COLOR, hover_color=CARD_BG_COLOR,
                                     command=self.on_back)
        self.back_btn.pack(side="left", anchor="w")

        # Заголовок шага
        self.title_label = ctk.CTkLabel(self, font=HEADER_FONT, text_color=TEXT_HEADER_COLOR)
        self.title_label.pack(pady=(0, 30))
        
        self.update_texts()

    def _create_content(self):
        pass  # Должен быть переопределен в дочерних классах

    def on_back(self):
        """Обработчик кнопки назад."""
        if self.step_id == "step2":
            self.controller.show_frame(StepPlaceFrame, "step1")
        elif self.step_id == "step3":
            self.controller.show_frame(StepGoalFrame, "step2")
        elif self.step_id == "nutrition":
            self.controller.on_back_to_main()
        else:
            self.controller.on_back_to_main()

    def create_option_button(self, parent, text_key, icon, command):
        """Вспомогательный метод для создания красивых кнопок выбора."""
        btn_text = f"{icon}\n\n{self.controller.loc.get(text_key)}"
        btn = ctk.CTkButton(parent, text=btn_text, font=("Helvetica Neue", 20, "bold"),
                            fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR,
                            border_width=2, border_color=CARD_BG_COLOR,
                            corner_radius=15, height=150, width=150,
                            command=command)
        return btn
    
    def update_texts(self):
        """Обновляет тексты на фрейме."""
        super().update_texts()
        self.back_btn.configure(text=self.controller.loc.get("back"))
        self.title_label.configure(text=self.controller.loc.get(self.title_key))

class StepPlaceFrame(StepFrameBase):
    """Шаг 1: Где тренируемся?"""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, "workout_location", "step1", **kwargs)
        
    def _create_content(self):
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.pack(expand=True)

        self.create_option_button(options_frame, "home", "🏠", 
                                 lambda: self.controller.set_wizard_condition("Дом")).pack(side="left", padx=20)
        
        self.create_option_button(options_frame, "gym", "🏋️‍♀️", 
                                 lambda: self.controller.set_wizard_condition("Зал")).pack(side="left", padx=20)

class StepGoalFrame(StepFrameBase):
    """Шаг 2: Какая цель?"""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, "workout_goal", "step2", **kwargs)
        
    def _create_content(self):
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.pack(expand=True, fill="x", padx=40)
        options_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.create_option_button(options_frame, "weight_loss", "🔥", 
                                 lambda: self.controller.set_wizard_goal("Похудение")).grid(row=0, column=0, padx=10, sticky="ew")
        
        self.create_option_button(options_frame, "muscle_gain", "💪", 
                                 lambda: self.controller.set_wizard_goal("Набор мышц")).grid(row=0, column=1, padx=10, sticky="ew")

        self.create_option_button(options_frame, "endurance", "🏃‍♂️", 
                                 lambda: self.controller.set_wizard_goal("Выносливость")).grid(row=0, column=2, padx=10, sticky="ew")

class StepLevelFrame(StepFrameBase):
    """Шаг 3: Какой уровень?"""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, "workout_level", "step3", **kwargs)
        
    def _create_content(self):
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.pack(expand=True, fill="x", padx=40)

        self.btn_novice = ctk.CTkButton(options_frame, font=BUTTON_FONT, height=60,
                                       fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
                                       command=lambda: self.controller.set_wizard_level("Новичок"))
        self.btn_novice.pack(fill="x", pady=10)

        self.btn_inter = ctk.CTkButton(options_frame, font=BUTTON_FONT, height=60,
                                       fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
                                       command=lambda: self.controller.set_wizard_level("Средний"))
        self.btn_inter.pack(fill="x", pady=10)

        self.btn_adv = ctk.CTkButton(options_frame, font=BUTTON_FONT, height=60,
                                     fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
                                     command=lambda: self.controller.set_wizard_level("Продвинутый"))
        self.btn_adv.pack(fill="x", pady=10)
        
        self.update_texts()
    
    def update_texts(self):
        """Обновляет тексты на фрейме."""
        super().update_texts()
        self.btn_novice.configure(text=f"🟢 {self.controller.loc.get('beginner')}")
        self.btn_inter.configure(text=f"🟡 {self.controller.loc.get('intermediate')}")
        self.btn_adv.configure(text=f"🔴 {self.controller.loc.get('advanced')}")

# ==========================================
# ФРЕЙМЫ ДЛЯ ПЛАНА ПИТАНИЯ
# ==========================================

class NutritionGoalFrame(StepFrameBase):
    """Фрейм выбора цели для плана питания."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, "nutrition_goal_title", "nutrition", **kwargs)
        self.desc_label = None
        self.btn_weight_loss = None
        self.btn_muscle_gain = None
        self.btn_maintenance = None
        
    def _create_content(self):
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.pack(expand=True, fill="x", padx=40)
        
        # Описание
        self.desc_label = ctk.CTkLabel(self, font=SUBHEADER_FONT, text_color=TEXT_BODY_COLOR, justify="center")
        self.desc_label.pack(pady=(0, 30))
        
        # Варианты целей питания
        self.btn_weight_loss = ctk.CTkButton(options_frame, 
                                            font=BODY_FONT, height=80,
                                            fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
                                            command=lambda: self.controller.set_nutrition_goal("Похудение"))
        self.btn_weight_loss.pack(fill="x", pady=10)
        
        self.btn_muscle_gain = ctk.CTkButton(options_frame,
                                            font=BODY_FONT, height=80,
                                            fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
                                            command=lambda: self.controller.set_nutrition_goal("Набор мышц"))
        self.btn_muscle_gain.pack(fill="x", pady=10)
        
        self.btn_maintenance = ctk.CTkButton(options_frame,
                                            font=BODY_FONT, height=80,
                                            fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
                                            command=lambda: self.controller.set_nutrition_goal("Поддержание"))
        self.btn_maintenance.pack(fill="x", pady=10)
        
        self.update_texts()
    
    def update_texts(self):
        """Обновляет тексты на фрейме."""
        super().update_texts()
        self.desc_label.configure(text=self.controller.loc.get("nutrition_goal_desc"))
        self.btn_weight_loss.configure(text=f"🍎 {self.controller.loc.get('weight_loss')}\n\n{self.controller.loc.get('weight_loss_desc')}")
        self.btn_muscle_gain.configure(text=f"💪 {self.controller.loc.get('muscle_gain')}\n\n{self.controller.loc.get('muscle_gain_desc')}")
        self.btn_maintenance.configure(text=f"⚖️ {self.controller.loc.get('maintenance')}\n\n{self.controller.loc.get('maintenance_desc')}")

class NutritionPlanFrame(BaseFrame):
    """Фрейм отображения плана питания."""
    def __init__(self, master, controller, plan_data, **kwargs):
        super().__init__(master, controller, **kwargs)
        self.plan_data = plan_data
        self.back_btn = None
        self.title_label = None
        self.content_frame = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        # Заголовок с кнопкой назад
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(30, 20))
        
        self.back_btn = ctk.CTkButton(header_frame, font=BODY_FONT, width=80,
                                     fg_color="transparent", text_color=TEXT_BODY_COLOR, hover_color=CARD_BG_COLOR,
                                     command=self.controller.on_back_to_main)
        self.back_btn.pack(side="left", anchor="w")
        
        self.title_label = ctk.CTkLabel(self, font=HEADER_FONT, text_color=ACCENT_COLOR)
        self.title_label.pack(pady=(0, 10))
        
        # Основной контент
        self.content_frame = ctk.CTkScrollableFrame(self, fg_color=CARD_BG_COLOR, corner_radius=15)
        self.content_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        self.display_plan(self.content_frame)
        self.update_texts()
    
    def display_plan(self, parent):
        """Отображает данные плана питания."""
        # Описание
        self.desc_label = ctk.CTkLabel(parent, text=self.plan_data["description"], 
                                      font=SUBHEADER_FONT, text_color=TEXT_BODY_COLOR, wraplength=600)
        self.desc_label.pack(pady=(20, 10), padx=20)
        
        # Макронутриенты
        macros_frame = ctk.CTkFrame(parent, fg_color="#2C2C2E", corner_radius=10)
        macros_frame.pack(fill="x", pady=10, padx=20)
        
        self.macros_title = ctk.CTkLabel(macros_frame, font=("Helvetica Neue", 16, "bold"), text_color=TEXT_HEADER_COLOR)
        self.macros_title.pack(pady=(15, 10))
        
        macros_grid = ctk.CTkFrame(macros_frame, fg_color="transparent")
        macros_grid.pack(pady=(0, 15), padx=20)
        
        self.calories_label = ctk.CTkLabel(macros_grid, font=BODY_FONT, text_color=HIGHLIGHT_COLOR)
        self.calories_label.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        
        self.protein_label = ctk.CTkLabel(macros_grid, font=BODY_FONT, text_color=TEXT_BODY_COLOR)
        self.protein_label.grid(row=0, column=1, padx=20, pady=5, sticky="w")
        
        self.carbs_label = ctk.CTkLabel(macros_grid, font=BODY_FONT, text_color=TEXT_BODY_COLOR)
        self.carbs_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        self.fat_label = ctk.CTkLabel(macros_grid, font=BODY_FONT, text_color=TEXT_BODY_COLOR)
        self.fat_label.grid(row=1, column=1, padx=20, pady=5, sticky="w")
        
        # Приемы пищи
        meals_frame = ctk.CTkFrame(parent, fg_color="#2C2C2E", corner_radius=10)
        meals_frame.pack(fill="x", pady=10, padx=20)
        
        self.meals_title = ctk.CTkLabel(meals_frame, font=("Helvetica Neue", 16, "bold"), text_color=TEXT_HEADER_COLOR)
        self.meals_title.pack(pady=(15, 10))
        
        self.meal_cards = []
        for i, meal in enumerate(self.plan_data["meals"]):
            meal_card = ctk.CTkFrame(meals_frame, fg_color="#3C3C3E", corner_radius=8)
            meal_card.pack(fill="x", pady=5, padx=15)
            
            time_label = ctk.CTkLabel(meal_card, text=f"⏰ {meal['time']}", 
                                      font=("Helvetica Neue", 12), text_color=HIGHLIGHT_COLOR)
            time_label.pack(side="left", padx=15, pady=10)
            
            meal_info = ctk.CTkFrame(meal_card, fg_color="transparent")
            meal_info.pack(side="left", fill="x", expand=True, padx=10, pady=10)
            
            name_label = ctk.CTkLabel(meal_info, text=meal["name"], 
                                     font=("Helvetica Neue", 14, "bold"), text_color=TEXT_HEADER_COLOR)
            name_label.pack(anchor="w")
            
            desc_label = ctk.CTkLabel(meal_info, text=meal["description"], 
                                     font=BODY_FONT, text_color=TEXT_BODY_COLOR, wraplength=400)
            desc_label.pack(anchor="w")
            
            self.meal_cards.append((time_label, name_label, desc_label))
        
        # Советы
        tips_frame = ctk.CTkFrame(parent, fg_color="#2C2C2E", corner_radius=10)
        tips_frame.pack(fill="x", pady=10, padx=20)
        
        self.tips_title = ctk.CTkLabel(tips_frame, font=("Helvetica Neue", 16, "bold"), text_color=TEXT_HEADER_COLOR)
        self.tips_title.pack(pady=(15, 10))
        
        self.tip_labels = []
        for i, tip in enumerate(self.plan_data["tips"]):
            tip_label = ctk.CTkLabel(tips_frame, text=f"• {tip}", 
                                    font=BODY_FONT, text_color=TEXT_BODY_COLOR, justify="left")
            tip_label.pack(anchor="w", padx=20, pady=5)
            self.tip_labels.append(tip_label)
    
    def update_texts(self):
        """Обновляет тексты на фрейме."""
        super().update_texts()
        self.back_btn.configure(text=self.controller.loc.get("back_to_main"))
        self.title_label.configure(text="🍎 " + self.controller.loc.get("nutrition_plan_title"))
        self.macros_title.configure(text="📊 " + self.controller.loc.get("macronutrients"))
        self.calories_label.configure(text=f"🔥 {self.controller.loc.get('calories')}: {self.plan_data['calories']} {self.controller.loc.get('kcal')}")
        self.protein_label.configure(text=f"🥩 {self.controller.loc.get('protein')}: {self.plan_data['protein']} {self.controller.loc.get('grams')}")
        self.carbs_label.configure(text=f"🍞 {self.controller.loc.get('carbs')}: {self.plan_data['carbs']} {self.controller.loc.get('grams')}")
        self.fat_label.configure(text=f"🥑 {self.controller.loc.get('fat')}: {self.plan_data['fat']} {self.controller.loc.get('grams')}")
        self.meals_title.configure(text="🍽️ " + self.controller.loc.get("meals"))
        self.tips_title.configure(text="💡 " + self.controller.loc.get("tips"))

# ==========================================
# ФРЕЙМЫ ДЛЯ СУЩЕСТВУЮЩИХ ПЛАНОВ И ИСТОРИИ
# ==========================================

class ExistingPlansFrame(BaseFrame):
    """Фрейм выбора существующего плана тренировок."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, **kwargs)
        self.back_btn = None
        self.title_label = None
        self.subtitle_label = None
        self.plans_frame = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(30, 10))
        
        self.back_btn = ctk.CTkButton(header_frame, font=BODY_FONT,
                                     fg_color="transparent", text_color=TEXT_BODY_COLOR, hover_color=CARD_BG_COLOR,
                                     command=self.controller.on_back_to_main)
        self.back_btn.pack(side="left")
        
        self.title_label = ctk.CTkLabel(self, font=HEADER_FONT, text_color=ACCENT_COLOR)
        self.title_label.pack(pady=(20, 10))
        
        self.subtitle_label = ctk.CTkLabel(self, font=SUBHEADER_FONT, text_color=TEXT_BODY_COLOR)
        self.subtitle_label.pack(pady=(0, 20))
        
        # Список планов
        self.plans_frame = ctk.CTkScrollableFrame(self, fg_color=CARD_BG_COLOR, corner_radius=15)
        self.plans_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        self.update_texts()
        # Загрузка планов
        self.load_plans()
    
    def load_plans(self):
        """Загружает список сохраненных планов."""
        if self.controller.username:
            self.controller.client.send({
                "action": "get_user_plans",
                "username": self.controller.username
            })
    
    def update_plans(self, plans):
        """Обновляет список планов."""
        for widget in self.plans_frame.winfo_children():
            widget.destroy()
        
        if not plans:
            ctk.CTkLabel(self.plans_frame, text=self.controller.loc.get("no_saved_plans"), 
                        font=BODY_FONT, text_color=TEXT_BODY_COLOR).pack(pady=20)
            return
        
        for plan in plans:
            self.add_plan_card(plan)
    
    def add_plan_card(self, plan):
        """Добавляет карточку плана."""
        card = ctk.CTkFrame(self.plans_frame, fg_color="#2C2C2E", corner_radius=10)
        card.pack(fill="x", pady=5, padx=5)
        
        # Верхняя часть карточки
        top_frame = ctk.CTkFrame(card, fg_color="transparent")
        top_frame.pack(fill="x", padx=15, pady=10)
        
        name_label = ctk.CTkLabel(top_frame, text=plan["name"], font=("Helvetica Neue", 16, "bold"), 
                                 text_color=TEXT_HEADER_COLOR)
        name_label.pack(side="left", anchor="w")
        
        date_label = ctk.CTkLabel(top_frame, text=f"📅 {plan['date']}", font=("Helvetica Neue", 12),
                                 text_color=HIGHLIGHT_COLOR)
        date_label.pack(side="right", anchor="e")
        
        # Детали плана
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        level_label = ctk.CTkLabel(details_frame, text=f"{self.controller.loc.get('level')}: {plan['level']}", 
                                  font=("Helvetica Neue", 13), text_color=TEXT_BODY_COLOR)
        level_label.pack(side="left", padx=(0, 20))
        
        goal_label = ctk.CTkLabel(details_frame, text=f"{self.controller.loc.get('goal')}: {plan['goal']}", 
                                 font=("Helvetica Neue", 13), text_color=TEXT_BODY_COLOR)
        goal_label.pack(side="left", padx=(0, 20))
        
        condition_label = ctk.CTkLabel(details_frame, text=f"{self.controller.loc.get('place')}: {plan['condition']}", 
                                      font=("Helvetica Neue", 13), text_color=TEXT_BODY_COLOR)
        condition_label.pack(side="left")
        
        # Кнопка загрузить
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        load_btn = ctk.CTkButton(btn_frame, text=self.controller.loc.get("load_plan"), font=BODY_FONT, height=35,
                                fg_color=ACCENT_COLOR, hover_color="#0069D9",
                                command=lambda p=plan: self.controller.load_existing_plan(p["id"]))
        load_btn.pack(side="right")
    
    def update_texts(self):
        """Обновляет тексты на фрейме."""
        super().update_texts()
        self.back_btn.configure(text=self.controller.loc.get("back_to_main"))
        self.title_label.configure(text="📁 " + self.controller.loc.get("your_workout_plans"))
        self.subtitle_label.configure(text=self.controller.loc.get("select_saved_plan"))

class WorkoutHistoryFrame(BaseFrame):
    """Фрейм истории тренировок."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, **kwargs)
        self.back_btn = None
        self.title_label = None
        self.history_frame = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(30, 10))
        
        self.back_btn = ctk.CTkButton(header_frame, font=BODY_FONT,
                                     fg_color="transparent", text_color=TEXT_BODY_COLOR, hover_color=CARD_BG_COLOR,
                                     command=self.controller.on_back_to_main)
        self.back_btn.pack(side="left")
        
        self.title_label = ctk.CTkLabel(self, font=HEADER_FONT, text_color=ACCENT_COLOR)
        self.title_label.pack(pady=(20, 10))
        
        # Список истории
        self.history_frame = ctk.CTkScrollableFrame(self, fg_color=CARD_BG_COLOR, corner_radius=15)
        self.history_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        self.update_texts()
        # Загрузка истории
        self.load_history()
    
    def load_history(self):
        """Загружает историю тренировок."""
        if self.controller.username:
            self.controller.client.send({
                "action": "get_workout_history",
                "username": self.controller.username
            })
    
    def update_history(self, history):
        """Обновляет список истории."""
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        if not history:
            ctk.CTkLabel(self.history_frame, text=self.controller.loc.get("no_workout_history"), 
                        font=BODY_FONT, text_color=TEXT_BODY_COLOR).pack(pady=20)
            return
        
        for record in history:
            self.add_history_card(record)
    
    def add_history_card(self, record):
        """Добавляет карточку истории тренировки."""
        card = ctk.CTkFrame(self.history_frame, fg_color="#2C2C2E", corner_radius=10)
        card.pack(fill="x", pady=5, padx=5)
        
        # Верхняя часть карточки
        top_frame = ctk.CTkFrame(card, fg_color="transparent")
        top_frame.pack(fill="x", padx=15, pady=10)
        
        name_label = ctk.CTkLabel(top_frame, text=record["workout_name"], font=("Helvetica Neue", 16, "bold"), 
                                 text_color=TEXT_HEADER_COLOR)
        name_label.pack(side="left", anchor="w")
        
        date_label = ctk.CTkLabel(top_frame, text=f"📅 {record['completed_at']}", font=("Helvetica Neue", 12),
                                 text_color=HIGHLIGHT_COLOR)
        date_label.pack(side="right", anchor="e")
        
        # Детали тренировки
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        duration_label = ctk.CTkLabel(details_frame, text=f"⏱️ {self.controller.loc.get('duration')}: {record['duration']} {self.controller.loc.get('minutes')}", 
                                     font=("Helvetica Neue", 13), text_color=TEXT_BODY_COLOR)
        duration_label.pack(side="left", padx=(0, 20))
        
        exercises_label = ctk.CTkLabel(details_frame, text=f"✅ {self.controller.loc.get('exercises')}: {len(record['exercises'])}", 
                                      font=("Helvetica Neue", 13), text_color=TEXT_BODY_COLOR)
        exercises_label.pack(side="left")
        
        # Список упражнений (свернутый)
        exercises_frame = ctk.CTkFrame(card, fg_color="#3C3C3E", corner_radius=8)
        exercises_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        exercises_title = ctk.CTkLabel(exercises_frame, text=self.controller.loc.get("completed_exercises"), 
                                      font=("Helvetica Neue", 12, "bold"), text_color=TEXT_BODY_COLOR)
        exercises_title.pack(anchor="w", padx=10, pady=5)
        
        for i, exercise in enumerate(record['exercises'][:3]):  # Показываем только первые 3
            ctk.CTkLabel(exercises_frame, text=f"• {exercise}", 
                        font=("Helvetica Neue", 11), text_color=TEXT_BODY_COLOR).pack(anchor="w", padx=20, pady=2)
        
        if len(record['exercises']) > 3:
            remaining = len(record['exercises']) - 3
            remaining_label = ctk.CTkLabel(exercises_frame, text=f"... {self.controller.loc.get('and_more')} {remaining} {self.controller.loc.get('exercises_remaining')}", 
                                          font=("Helvetica Neue", 11), text_color=HIGHLIGHT_COLOR)
            remaining_label.pack(anchor="w", padx=20, pady=2)
    
    def update_texts(self):
        """Обновляет тексты на фрейме."""
        super().update_texts()
        self.back_btn.configure(text=self.controller.loc.get("back_to_main"))
        self.title_label.configure(text="📊 " + self.controller.loc.get("workout_history"))

# ==========================================
# ЭКРАНЫ РЕЗУЛЬТАТОВ И ПРОГРЕССА
# ==========================================

class ExerciseFrame(BaseFrame):
    """Экран тренировки с поэтапным прохождением."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, **kwargs)
        
        self.all_exercises = []
        self.current_stage_idx = 0
        self.stages = []
        self.start_time = None
        self.completed_exercises = []
        self.workout_name = None
        
        self.stage_label = None
        self.sub_label = None
        self.exercise_list = None
        self.name_frame = None
        self.name_entry = None
        self.footer = None
        self.btn_next = None
        self.save_buttons_frame = None
        self.btn_save_plan = None
        self.btn_save_history = None
        
        self._create_widgets()
        self.update_texts()

    def _create_widgets(self):
        # Заголовок этапа
        self.stage_label = ctk.CTkLabel(self, text="", font=HEADER_FONT, text_color=ACCENT_COLOR)
        self.stage_label.pack(pady=(20, 5))
        
        self.sub_label = ctk.CTkLabel(self, text="", font=BODY_FONT, text_color=TEXT_BODY_COLOR)
        self.sub_label.pack(pady=(0, 15))

        # Список упражнений
        self.exercise_list = ctk.CTkScrollableFrame(self, fg_color=CARD_BG_COLOR, corner_radius=15)
        self.exercise_list.pack(pady=10, padx=40, fill="both", expand=True)

        # Панель ввода названия тренировки
        self.name_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.name_frame.pack(fill="x", padx=40, pady=(10, 0))
        
        name_prompt = ctk.CTkLabel(self.name_frame, text="", 
                                  font=BODY_FONT, text_color=TEXT_BODY_COLOR)
        name_prompt.pack(side="left", padx=(0, 10))
        
        self.name_entry = ctk.CTkEntry(self.name_frame, placeholder_text="",
                                      font=BODY_FONT, width=300)
        self.name_entry.pack(side="left", fill="x", expand=True)

        # Нижняя панель с кнопками
        self.footer = ctk.CTkFrame(self, fg_color="transparent")
        self.footer.pack(fill="x", padx=40, pady=20)
        
        self.btn_next = ctk.CTkButton(self.footer, text="", font=BUTTON_FONT, 
                                      height=50, fg_color=ACCENT_COLOR, state="disabled",
                                      command=self.next_stage)
        self.btn_next.pack(fill="x")
        
        # Кнопки сохранения
        self.save_buttons_frame = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.save_buttons_frame.pack(fill="x", pady=(10, 0))
        
        # Кнопка сохранения как плана
        self.btn_save_plan = ctk.CTkButton(self.save_buttons_frame, 
                                          font=BODY_FONT, height=40, 
                                          fg_color=HIGHLIGHT_COLOR, hover_color="#E08500",
                                          command=self.save_as_training_plan)
        self.btn_save_plan.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Кнопка сохранения в историю
        self.btn_save_history = ctk.CTkButton(self.save_buttons_frame, 
                                             font=BODY_FONT, height=40,
                                             fg_color="#30D158", hover_color="#20B148",
                                             command=self.save_to_history)
        self.btn_save_history.pack(side="right", fill="x", expand=True, padx=(5, 0))

    def load_exercises(self, exercises):
        """Загружает упражнения."""
        self.all_exercises = exercises
        self.current_stage_idx = 0
        self.start_time = datetime.now()
        self.completed_exercises = []
        self.workout_name = f"{self.controller.loc.get('workout')} {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        self.name_entry.delete(0, 'end')
        self.name_entry.insert(0, self.workout_name)
        
        # Обновляем названия этапов
        self.stages = [
            f"🔥 {self.controller.loc.get('warmup')}",
            f"⚡ {self.controller.loc.get('main_workout')}",
            f"🧘 {self.controller.loc.get('cooldown')}"
        ]
        
        self.show_stage()

    def get_current_stage_data(self):
        """Фильтрует упражнения для текущего этапа."""
        stage_name = self.stages[self.current_stage_idx]
        
        if self.controller.loc.get('warmup') in stage_name:
            return [ex for ex in self.all_exercises if self.controller.loc.get('warmup') in ex]
        elif self.controller.loc.get('main_workout') in stage_name:
            # Основная тренировка - все упражнения, кроме разминки и заминки
            return [ex for ex in self.all_exercises if 
                   self.controller.loc.get('warmup') not in ex and 
                   self.controller.loc.get('cooldown') not in ex]
        else:  # Заминка
            return [ex for ex in self.all_exercises if self.controller.loc.get('cooldown') in ex]

    def show_stage(self):
        """Отрисовывает упражнения текущего этапа."""
        for widget in self.exercise_list.winfo_children():
            widget.destroy()
            
        current_stage_name = self.stages[self.current_stage_idx]
        self.stage_label.configure(text=current_stage_name)
        
        stage_data = self.get_current_stage_data()
        self.checkbox_vars = []

        if not stage_data:
            self.next_stage()
            return

        for ex in stage_data:
            var = ctk.StringVar(value="off")
            self.checkbox_vars.append(var)
            
            card = ctk.CTkFrame(self.exercise_list, fg_color="#2C2C2E", corner_radius=10)
            card.pack(fill="x", pady=5, padx=5)
            
            cb = ctk.CTkCheckBox(card, text=ex, variable=var, onvalue="on", offvalue="off",
                                 font=("Helvetica Neue", 15), text_color=TEXT_HEADER_COLOR,
                                 checkmark_color=ACCENT_COLOR,
                                 command=self.check_completion)
            cb.pack(pady=15, padx=15, anchor="w")
        
        next_text = self.controller.loc.get("next_stage") if self.current_stage_idx < 2 else self.controller.loc.get("finish_workout")
        self.btn_next.configure(state="disabled", text=next_text)
        self.check_completion()

    def check_completion(self):
        """Проверяет, все ли галочки стоят."""
        all_done = all(v.get() == "on" for v in self.checkbox_vars)
        if all_done:
            self.btn_next.configure(state="normal", fg_color=ACCENT_COLOR)
        else:
            self.btn_next.configure(state="disabled")

    def next_stage(self):
        """Переход к следующему этапу или завершение."""
        # Сохраняем выполненные упражнения
        stage_data = self.get_current_stage_data()
        for i, var in enumerate(self.checkbox_vars):
            if var.get() == "on":
                ex_name = stage_data[i]
                self.completed_exercises.append(ex_name)
                self.controller.on_check_exercise(ex_name, True)

        if self.current_stage_idx < len(self.stages) - 1:
            self.current_stage_idx += 1
            self.show_stage()
        else:
            # Завершение тренировки
            self.finish_workout()

    def finish_workout(self):
        """Завершает тренировку и сохраняет историю."""
        duration = int((datetime.now() - self.start_time).total_seconds() / 60)
        workout_name = self.name_entry.get().strip() or self.workout_name
        
        # Сохраняем историю тренировки
        self.controller.save_workout_history(workout_name, self.completed_exercises, duration)
        
        messagebox.showinfo(self.controller.loc.get("congratulations"), 
                           f"{self.controller.loc.get('workout_complete')} '{workout_name}'!")
        self.controller.on_back_to_main()

    def save_as_training_plan(self):
        """Сохраняет текущую тренировку как план."""
        plan_name = self.name_entry.get().strip() or f"{self.controller.loc.get('training_plan')} {datetime.now().strftime('%d.%m.%Y')}"
        
        if hasattr(self.controller, 'wizard_selections'):
            level = self.controller.wizard_selections.get("level", self.controller.loc.get("beginner"))
            goal = self.controller.wizard_selections.get("goal", self.controller.loc.get("weight_loss"))
            condition = self.controller.wizard_selections.get("condition", self.controller.loc.get("home"))
            
            # Сохраняем план тренировки
            self.controller.save_training_plan_with_history(plan_name, level, goal, condition, self.all_exercises)
            messagebox.showinfo(self.controller.loc.get("saved"), 
                              f"{self.controller.loc.get('plan_saved_message')} '{plan_name}'!")

    def save_to_history(self):
        """Сохраняет текущую тренировку в историю."""
        workout_name = self.name_entry.get().strip() or f"{self.controller.loc.get('workout')} {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        duration = int((datetime.now() - self.start_time).total_seconds() / 60) if self.start_time else 0
        
        # Сохраняем историю тренировки
        self.controller.save_workout_history(workout_name, self.completed_exercises, duration)
        messagebox.showinfo(self.controller.loc.get("saved"), 
                          f"{self.controller.loc.get('workout_saved_message')} '{workout_name}'!")

    def update_texts(self):
        """Обновляет тексты на фрейме."""
        super().update_texts()
        self.sub_label.configure(text=self.controller.loc.get("complete_all_exercises"))
        
        # Обновляем плейсхолдер для названия тренировки
        self.name_entry.configure(placeholder_text=self.controller.loc.get("enter_workout_name"))
        
        # Обновляем названия этапов
        if self.all_exercises:
            self.stages = [
                f"🔥 {self.controller.loc.get('warmup')}",
                f"⚡ {self.controller.loc.get('main_workout')}",
                f"🧘 {self.controller.loc.get('cooldown')}"
            ]
            if self.current_stage_idx < len(self.stages):
                self.stage_label.configure(text=self.stages[self.current_stage_idx])
        
        # Обновляем кнопки
        if self.current_stage_idx < 2:
            self.btn_next.configure(text=self.controller.loc.get("next_stage"))
        else:
            self.btn_next.configure(text=self.controller.loc.get("finish_workout"))
        
        self.btn_save_plan.configure(text="💾 " + self.controller.loc.get("save_plan"))
        self.btn_save_history.configure(text="📊 " + self.controller.loc.get("save_workout"))

class ProgressFrame(BaseFrame):
    """Экран истории прогресса."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, **kwargs)
        self.back_btn = None
        self.title_label = None
        self.progress_display = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(30, 10))
        
        self.back_btn = ctk.CTkButton(header_frame, font=BODY_FONT,
                                     fg_color="transparent", text_color=TEXT_BODY_COLOR, hover_color=CARD_BG_COLOR,
                                     command=self.controller.on_back_to_main)
        self.back_btn.pack(side="left")
        
        self.title_label = ctk.CTkLabel(self, font=HEADER_FONT, text_color=TEXT_HEADER_COLOR)
        self.title_label.pack(pady=(20, 20))
        
        self.progress_display = ctk.CTkScrollableFrame(self, fg_color=CARD_BG_COLOR, corner_radius=15)
        self.progress_display.pack(pady=10, padx=40, fill="both", expand=True)
        
        self.update_texts()

    def load_progress(self, progress_data):
        for widget in self.progress_display.winfo_children():
            widget.destroy()
        
        if not progress_data:
            ctk.CTkLabel(self.progress_display, text=self.controller.loc.get("no_history"), 
                        font=BODY_FONT, text_color=TEXT_BODY_COLOR).pack(pady=20)
            return

        for entry in progress_data:
            row = ctk.CTkFrame(self.progress_display, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            date_str = entry.get('timestamp', '???')[:16].replace('T', ' ')
            ex_name = entry.get('exercise_name', self.controller.loc.get("unknown"))
            
            ctk.CTkLabel(row, text=f"📅 {date_str}", font=("Helvetica Neue", 12), 
                        text_color=HIGHLIGHT_COLOR).pack(anchor="w")
            ctk.CTkLabel(row, text=f"✅ {self.controller.loc.get('completed')}: {ex_name}", 
                        font=("Helvetica Neue", 14, "bold"), text_color=TEXT_HEADER_COLOR).pack(anchor="w", pady=(2, 10))
            ctk.CTkFrame(row, height=1, fg_color=CARD_BG_COLOR).pack(fill="x")
    
    def update_texts(self):
        """Обновляет тексты на фрейме."""
        super().update_texts()
        self.back_btn.configure(text=self.controller.loc.get("back_to_main"))
        self.title_label.configure(text=self.controller.loc.get("progress"))

# ==========================================
# МОДАЛЬНЫЕ ОКНА
# ==========================================

class AuthWindow(ctk.CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title(self.controller.loc.get("login_title"))
        self.geometry("400x450")
        self.protocol("WM_DELETE_WINDOW", self.controller.on_close) 
        self.configure(fg_color=ctk.ThemeManager.theme["CTk"]["fg_color"][1])
        
        self.entry_user = None
        self.entry_pass = None
        
        self._create_widgets()
        
    def _create_widgets(self):
        ctk.CTkLabel(self, text="🏋️", font=("Helvetica Neue", 60)).pack(pady=(40, 10))
        
        title_label = ctk.CTkLabel(self, text="", font=HEADER_FONT, text_color=TEXT_HEADER_COLOR)
        title_label.pack(pady=(0, 30))
        
        self.entry_user = ctk.CTkEntry(self, placeholder_text="", height=40, font=BODY_FONT)
        self.entry_user.pack(pady=10, padx=40, fill="x")

        self.entry_pass = ctk.CTkEntry(self, placeholder_text="", show="*", height=40, font=BODY_FONT)
        self.entry_pass.pack(pady=10, padx=40, fill="x")
        
        login_btn = ctk.CTkButton(self, text="", font=BUTTON_FONT, height=45, fg_color=ACCENT_COLOR, hover_color="#0069D9",
                                 command=self.on_login)
        login_btn.pack(pady=(20, 10), padx=40, fill="x")

        register_btn = ctk.CTkButton(self, text="", font=BODY_FONT, fg_color="transparent", hover_color=CARD_BG_COLOR,
                                    command=self.controller.open_register_window)
        register_btn.pack(pady=5)

        server_btn = ctk.CTkButton(self, text="", font=("Helvetica Neue", 10), fg_color="transparent", text_color=TEXT_BODY_COLOR,
                                  command=self.controller.open_server_menu)
        server_btn.pack(side="bottom", pady=10)
        
        self.update_texts()

    def on_login(self):
        self.controller.on_login(self.entry_user.get().strip(), self.entry_pass.get().strip())
        
    def update_texts(self):
        self.title(self.controller.loc.get("login_title"))
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.cget("font") == HEADER_FONT:
                widget.configure(text=self.controller.loc.get("login_title"))
            elif isinstance(widget, ctk.CTkButton):
                if widget.cget("text") == self.controller.loc.get("login"):
                    widget.configure(text=self.controller.loc.get("login"))
                elif widget.cget("text") == self.controller.loc.get("no_account"):
                    widget.configure(text=self.controller.loc.get("no_account"))
                elif "server_settings" in widget.cget("text"):
                    widget.configure(text=self.controller.loc.get("server_settings"))
        
        self.entry_user.configure(placeholder_text=self.controller.loc.get("username"))
        self.entry_pass.configure(placeholder_text=self.controller.loc.get("password"))

class RegisterWindow(ctk.CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title(self.controller.loc.get("register_title"))
        self.geometry("400x550")
        self.transient(master)
        self.grab_set()
        self.configure(fg_color=ctk.ThemeManager.theme["CTk"]["fg_color"][1])
        
        self.e_user = None
        self.e_pass = None
        self.e_phone = None
        self.e_dob = None
        
        self._create_widgets()
        
    def _create_widgets(self):
        title_label = ctk.CTkLabel(self, text="", font=HEADER_FONT, text_color=TEXT_HEADER_COLOR)
        title_label.pack(pady=(40, 30))
        
        self.e_user = ctk.CTkEntry(self, placeholder_text="", height=40, font=BODY_FONT)
        self.e_user.pack(pady=5, padx=40, fill="x")
        
        self.e_pass = ctk.CTkEntry(self, placeholder_text="", show="*", height=40, font=BODY_FONT)
        self.e_pass.pack(pady=5, padx=40, fill="x")
        
        self.e_phone = ctk.CTkEntry(self, placeholder_text="", height=40, font=BODY_FONT)
        self.e_phone.pack(pady=5, padx=40, fill="x")
        
        self.e_dob = ctk.CTkEntry(self, placeholder_text="", height=40, font=BODY_FONT)
        self.e_dob.pack(pady=5, padx=40, fill="x")

        register_btn = ctk.CTkButton(self, text="", font=BUTTON_FONT, height=45, fg_color=HIGHLIGHT_COLOR, hover_color="#E08500",
                                    command=self.on_register)
        register_btn.pack(pady=(30, 20), padx=40, fill="x")

        self.update_texts()

    def on_register(self):
        u, p = self.e_user.get().strip(), self.e_pass.get().strip()
        ph, dob = self.e_phone.get().strip(), self.e_dob.get().strip()
        
        if not u or not p or not ph or not dob:
             messagebox.showwarning(self.controller.loc.get("error"), self.controller.loc.get("fill_all_fields"))
             return

        if not Validator.is_valid_phone_by(ph):
            messagebox.showerror(self.controller.loc.get("error"), self.controller.loc.get("invalid_phone"))
            return
        valid_date, msg = Validator.is_valid_date(dob)
        if not valid_date:
            messagebox.showerror(self.controller.loc.get("error"), msg)
            return

        if self.controller.on_register(u, p, ph, dob):
            self.destroy()
            
    def update_texts(self):
        self.title(self.controller.loc.get("register_title"))
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.cget("font") == HEADER_FONT:
                widget.configure(text=self.controller.loc.get("register_title"))
            elif isinstance(widget, ctk.CTkButton):
                if widget.cget("text") == self.controller.loc.get("register_button"):
                    widget.configure(text=self.controller.loc.get("register_button"))
        
        self.e_user.configure(placeholder_text=self.controller.loc.get("username"))
        self.e_pass.configure(placeholder_text=self.controller.loc.get("password"))
        self.e_phone.configure(placeholder_text=self.controller.loc.get("phone_placeholder"))
        self.e_dob.configure(placeholder_text=self.controller.loc.get("dob_placeholder"))

class ServerMenuWindow(ctk.CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title(self.controller.loc.get("server_settings"))
        self.geometry("300x200")
        self.transient(master)
        self.configure(fg_color=CARD_BG_COLOR)
        
        self.btn_stop_server = None
        self._create_widgets()
        
    def _create_widgets(self):
        title_label = ctk.CTkLabel(self, text="", font=SUBHEADER_FONT)
        title_label.pack(pady=20)

        start_btn = ctk.CTkButton(self, text="", font=BUTTON_FONT, fg_color=ACCENT_COLOR,
                                 command=self.controller.on_start_server)
        start_btn.pack(pady=10, padx=20, fill="x")
        
        self.btn_stop_server = ctk.CTkButton(self, text="", font=BUTTON_FONT, fg_color=HIGHLIGHT_COLOR, hover_color="#E08500",
                                            command=self.controller.on_stop, 
                                            state="disabled" if not self.controller.server_running else "normal")
        self.btn_stop_server.pack(pady=5, padx=20, fill="x")
        
        self.update_texts()
        
    def update_texts(self):
        self.title(self.controller.loc.get("server_settings"))
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text=self.controller.loc.get("manage_server"))
            elif isinstance(widget, ctk.CTkButton):
                if "start_server" in widget.cget("text") or widget.cget("text") == "":
                    widget.configure(text=self.controller.loc.get("start_server"))
                elif "stop_server" in widget.cget("text") or widget == self.btn_stop_server:
                    widget.configure(text=self.controller.loc.get("stop_server"))