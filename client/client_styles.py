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
        lang_btn = ctk.CTkButton(right_frame, 
                                text=self.controller.loc.get("lang_btn"), 
                                width=50,
                                font=BODY_FONT,
                                fg_color="transparent", 
                                text_color=TEXT_BODY_COLOR, 
                                hover_color=CARD_BG_COLOR,
                                command=self.controller.toggle_language)
        lang_btn.pack(side="left", padx=5)

        # Кнопка История тренировок
        if isinstance(self, (ExerciseFrame, ProgressFrame, NutritionPlanFrame, WorkoutHistoryFrame)):
            history_btn = ctk.CTkButton(right_frame, 
                                       text=self.controller.loc.get("workout_history"), 
                                       font=BODY_FONT,
                                       fg_color="transparent", 
                                       text_color=TEXT_BODY_COLOR, 
                                       hover_color=CARD_BG_COLOR,
                                       command=self.controller.open_workout_history)
            history_btn.pack(side="left", padx=5)

        # Настройки
        settings_btn = ctk.CTkButton(right_frame, text="⚙️", width=40, font=BODY_FONT,
                                    fg_color="transparent", 
                                    text_color=TEXT_BODY_COLOR, 
                                    hover_color=CARD_BG_COLOR,
                                    command=self.controller.open_server_menu)
        settings_btn.pack(side="left", padx=5)
        
        # Выход
        logout_btn = ctk.CTkButton(right_frame, 
                                  text=self.controller.loc.get("logout"), 
                                  width=60, 
                                  font=BODY_FONT,
                                  fg_color=HIGHLIGHT_COLOR, 
                                  hover_color="#E08500", 
                                  text_color=TEXT_HEADER_COLOR,
                                  command=self.controller.on_logout)
        logout_btn.pack(side="left", padx=5)

# ==========================================
# НОВЫЕ ФРЕЙМЫ ДЛЯ ПОШАГОВОГО МАСТЕРА (WIZARD)
# ==========================================

class LandingFrame(BaseFrame):
    """Главный экран-лендинг после входа."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, **kwargs)
        
        # Центральный контент
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=40, pady=40)

        welcome_text = self.controller.loc.get("welcome_user", username=self.controller.username)
        ctk.CTkLabel(content_frame, text=welcome_text, font=SUBHEADER_FONT, text_color=ACCENT_COLOR).pack(pady=(0, 10), anchor="w")

        ctk.CTkLabel(content_frame, text=self.controller.loc.get("create_workout"), 
                     font=HEADER_FONT, text_color=TEXT_HEADER_COLOR, justify="left").pack(pady=(0, 20), anchor="w")
        
        ctk.CTkLabel(content_frame, text=self.controller.loc.get("personalized_plan"), 
                     font=SUBHEADER_FONT, text_color=TEXT_BODY_COLOR, justify="left").pack(pady=(0, 40), anchor="w")

        # Фрейм для кнопок
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=10)

        # Первая строка кнопок
        top_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        top_buttons_frame.pack(fill="x", pady=(0, 10))

        # Кнопка "Начать создание плана" (занимает всю ширину)
        start_btn = ctk.CTkButton(top_buttons_frame, text=self.controller.loc.get("start"), 
                                  font=BUTTON_FONT, height=50, corner_radius=25,
                                  fg_color=ACCENT_COLOR, hover_color="#0069D9",
                                  command=self.controller.start_wizard)
        start_btn.pack(fill="x", ipadx=20)

        # Вторая строка кнопок
        bottom_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        bottom_buttons_frame.pack(fill="x")

        # Кнопка "Создать план питания" (слева)
        nutrition_btn = ctk.CTkButton(bottom_buttons_frame, 
                                     text="🍎 СОЗДАТЬ ПЛАН ПИТАНИЯ",
                                     font=("Helvetica Neue", 14, "bold"), height=45, corner_radius=20,
                                     fg_color=HIGHLIGHT_COLOR, hover_color="#E08500",
                                     command=self.controller.on_create_nutrition_plan)
        nutrition_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # Кнопка "Существующие планы" (справа)
        existing_btn = ctk.CTkButton(bottom_buttons_frame, 
                                    text="📁 СУЩЕСТВУЮЩИЕ ПЛАНЫ",
                                    font=("Helvetica Neue", 14, "bold"), height=45, corner_radius=20,
                                    fg_color="#30D158", hover_color="#20B148",
                                    command=self.controller.on_use_existing_workout_plan)
        existing_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        # Кнопка "История тренировок" (третья строка)
        history_btn = ctk.CTkButton(buttons_frame,
                                   text="📊 ИСТОРИЯ ТРЕНИРОВОК",
                                   font=("Helvetica Neue", 14, "bold"), height=45, corner_radius=20,
                                   fg_color="#AF52DE", hover_color="#8E44D9",
                                   command=self.controller.open_workout_history)
        history_btn.pack(fill="x", pady=(10, 0))

class StepFrameBase(BaseFrame):
    """Базовый класс для шагов мастера, добавляет заголовок и кнопку 'Назад'."""
    def __init__(self, master, controller, title_key, step_id, **kwargs):
        super().__init__(master, controller, **kwargs)
        self.step_id = step_id
        self.title_key = title_key
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(30, 20))
        
        # Кнопка Назад
        back_btn = ctk.CTkButton(header_frame, text=self.controller.loc.get("back"), font=BODY_FONT, width=80,
                                 fg_color="transparent", text_color=TEXT_BODY_COLOR, hover_color=CARD_BG_COLOR,
                                 command=self.on_back)
        back_btn.pack(side="left", anchor="w")

        # Заголовок шага
        ctk.CTkLabel(self, text=self.controller.loc.get(title_key), font=HEADER_FONT, text_color=TEXT_HEADER_COLOR).pack(pady=(0, 30))

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

class StepPlaceFrame(StepFrameBase):
    """Шаг 1: Где тренируемся?"""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, "workout_location", "step1", **kwargs)
        
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
        
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.pack(expand=True, fill="x", padx=40)

        btn_novice = ctk.CTkButton(options_frame, text=f"🟢 {self.controller.loc.get('beginner')}", font=BUTTON_FONT, height=60,
                                   fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
                                   command=lambda: self.controller.set_wizard_level("Новичок"))
        btn_novice.pack(fill="x", pady=10)

        btn_inter = ctk.CTkButton(options_frame, text=f"🟡 {self.controller.loc.get('intermediate')}", font=BUTTON_FONT, height=60,
                                   fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
                                   command=lambda: self.controller.set_wizard_level("Средний"))
        btn_inter.pack(fill="x", pady=10)

        btn_adv = ctk.CTkButton(options_frame, text=f"🔴 {self.controller.loc.get('advanced')}", font=BUTTON_FONT, height=60,
                                   fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
                                   command=lambda: self.controller.set_wizard_level("Продвинутый"))
        btn_adv.pack(fill="x", pady=10)

# ==========================================
# ФРЕЙМЫ ДЛЯ ПЛАНА ПИТАНИЯ
# ==========================================

class NutritionGoalFrame(StepFrameBase):
    """Фрейм выбора цели для плана питания."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, "nutrition_goal_title", "nutrition", **kwargs)
        
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.pack(expand=True, fill="x", padx=40)
        
        # Описание
        desc_label = ctk.CTkLabel(self, 
            text="Выберите вашу основную цель для составления\nперсонализированного плана питания:",
            font=SUBHEADER_FONT, text_color=TEXT_BODY_COLOR, justify="center")
        desc_label.pack(pady=(0, 30))
        
        # Варианты целей питания
        btn_weight_loss = ctk.CTkButton(options_frame, 
            text=f"🍎 {self.controller.loc.get('weight_loss')}\n\nСоздать дефицит калорий для снижения веса",
            font=BODY_FONT, height=80,
            fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
            command=self.on_select_weight_loss)
        btn_weight_loss.pack(fill="x", pady=10)
        
        btn_muscle_gain = ctk.CTkButton(options_frame,
            text=f"💪 {self.controller.loc.get('muscle_gain')}\n\nСоздать профицит калорий для роста мышц",
            font=BODY_FONT, height=80,
            fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
            command=self.on_select_muscle_gain)
        btn_muscle_gain.pack(fill="x", pady=10)
        
        btn_maintenance = ctk.CTkButton(options_frame,
            text=f"⚖️ {self.controller.loc.get('maintenance')}\n\nСохранить текущий вес и тонус мышц",
            font=BODY_FONT, height=80,
            fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
            command=self.on_select_maintenance)
        btn_maintenance.pack(fill="x", pady=10)

    def on_select_weight_loss(self):
        """Обработчик выбора похудения."""
        self.controller.set_nutrition_goal("Похудение")

    def on_select_muscle_gain(self):
        """Обработчик выбора набора мышц."""
        self.controller.set_nutrition_goal("Набор мышц")

    def on_select_maintenance(self):
        """Обработчик выбора поддержания."""
        self.controller.set_nutrition_goal("Поддержание")

    """Фрейм выбора цели для плана питания."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, "nutrition_goal_title", "nutrition", **kwargs)
        
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.pack(expand=True, fill="x", padx=40)
        
        # Описание
        desc_label = ctk.CTkLabel(self, 
            text="Выберите вашу основную цель для составления\nперсонализированного плана питания:",
            font=SUBHEADER_FONT, text_color=TEXT_BODY_COLOR, justify="center")
        desc_label.pack(pady=(0, 30))
        
        # Варианты целей питания
        btn_weight_loss = ctk.CTkButton(options_frame, 
            text=f"🍎 {self.controller.loc.get('weight_loss')}\n\nСоздать дефицит калорий для снижения веса",
            font=BODY_FONT, height=80,
            fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
            command=lambda: self.controller.set_nutrition_goal("Похудение"))
        btn_weight_loss.pack(fill="x", pady=10)
        
        btn_muscle_gain = ctk.CTkButton(options_frame,
            text=f"💪 {self.controller.loc.get('muscle_gain')}\n\nСоздать профицит калорий для роста мышц",
            font=BODY_FONT, height=80,
            fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
            command=lambda: self.controller.set_nutrition_goal("Набор мышц"))
        btn_muscle_gain.pack(fill="x", pady=10)
        
        btn_maintenance = ctk.CTkButton(options_frame,
            text=f"⚖️ {self.controller.loc.get('maintenance')}\n\nСохранить текущий вес и тонус мышц",
            font=BODY_FONT, height=80,
            fg_color=CARD_BG_COLOR, hover_color=ACCENT_COLOR, corner_radius=10,
            command=lambda: self.controller.set_nutrition_goal("Поддержание"))
        btn_maintenance.pack(fill="x", pady=10)

class NutritionPlanFrame(BaseFrame):
    """Фрейм отображения плана питания."""
    def __init__(self, master, controller, plan_data, **kwargs):
        super().__init__(master, controller, **kwargs)
        self.plan_data = plan_data
        
        # Заголовок с кнопкой назад
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(30, 20))
        
        back_btn = ctk.CTkButton(header_frame, text=self.controller.loc.get("back"), font=BODY_FONT, width=80,
                                 fg_color="transparent", text_color=TEXT_BODY_COLOR, hover_color=CARD_BG_COLOR,
                                 command=self.controller.on_back_to_main)
        back_btn.pack(side="left", anchor="w")
        
        ctk.CTkLabel(self, text="🍎 ПЛАН ПИТАНИЯ", font=HEADER_FONT, text_color=ACCENT_COLOR).pack(pady=(0, 10))
        
        # Основной контент
        content_frame = ctk.CTkScrollableFrame(self, fg_color=CARD_BG_COLOR, corner_radius=15)
        content_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        self.display_plan(content_frame)
    
    def display_plan(self, parent):
        """Отображает данные плана питания."""
        # Описание
        ctk.CTkLabel(parent, text=self.plan_data["description"], 
                     font=SUBHEADER_FONT, text_color=TEXT_BODY_COLOR, wraplength=600).pack(pady=(20, 10), padx=20)
        
        # Макронутриенты
        macros_frame = ctk.CTkFrame(parent, fg_color="#2C2C2E", corner_radius=10)
        macros_frame.pack(fill="x", pady=10, padx=20)
        
        ctk.CTkLabel(macros_frame, text="📊 МАКРОНУТРИЕНТЫ В ДЕНЬ", 
                     font=("Helvetica Neue", 16, "bold"), text_color=TEXT_HEADER_COLOR).pack(pady=(15, 10))
        
        macros_grid = ctk.CTkFrame(macros_frame, fg_color="transparent")
        macros_grid.pack(pady=(0, 15), padx=20)
        
        ctk.CTkLabel(macros_grid, text=f"🔥 Калории: {self.plan_data['calories']} ккал",
                     font=BODY_FONT, text_color=HIGHLIGHT_COLOR).grid(row=0, column=0, padx=20, pady=5, sticky="w")
        ctk.CTkLabel(macros_grid, text=f"🥩 Белки: {self.plan_data['protein']} г",
                     font=BODY_FONT, text_color=TEXT_BODY_COLOR).grid(row=0, column=1, padx=20, pady=5, sticky="w")
        ctk.CTkLabel(macros_grid, text=f"🍞 Углеводы: {self.plan_data['carbs']} г",
                     font=BODY_FONT, text_color=TEXT_BODY_COLOR).grid(row=1, column=0, padx=20, pady=5, sticky="w")
        ctk.CTkLabel(macros_grid, text=f"🥑 Жиры: {self.plan_data['fat']} г",
                     font=BODY_FONT, text_color=TEXT_BODY_COLOR).grid(row=1, column=1, padx=20, pady=5, sticky="w")
        
        # Приемы пищи
        meals_frame = ctk.CTkFrame(parent, fg_color="#2C2C2E", corner_radius=10)
        meals_frame.pack(fill="x", pady=10, padx=20)
        
        ctk.CTkLabel(meals_frame, text="🍽️ ПРИЕМЫ ПИЩИ", 
                     font=("Helvetica Neue", 16, "bold"), text_color=TEXT_HEADER_COLOR).pack(pady=(15, 10))
        
        for i, meal in enumerate(self.plan_data["meals"]):
            meal_card = ctk.CTkFrame(meals_frame, fg_color="#3C3C3E", corner_radius=8)
            meal_card.pack(fill="x", pady=5, padx=15)
            
            time_label = ctk.CTkLabel(meal_card, text=f"⏰ {meal['time']}", 
                                      font=("Helvetica Neue", 12), text_color=HIGHLIGHT_COLOR)
            time_label.pack(side="left", padx=15, pady=10)
            
            meal_info = ctk.CTkFrame(meal_card, fg_color="transparent")
            meal_info.pack(side="left", fill="x", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(meal_info, text=meal["name"], 
                        font=("Helvetica Neue", 14, "bold"), text_color=TEXT_HEADER_COLOR).pack(anchor="w")
            ctk.CTkLabel(meal_info, text=meal["description"], 
                        font=BODY_FONT, text_color=TEXT_BODY_COLOR, wraplength=400).pack(anchor="w")
        
        # Советы
        tips_frame = ctk.CTkFrame(parent, fg_color="#2C2C2E", corner_radius=10)
        tips_frame.pack(fill="x", pady=10, padx=20)
        
        ctk.CTkLabel(tips_frame, text="💡 СОВЕТЫ", 
                     font=("Helvetica Neue", 16, "bold"), text_color=TEXT_HEADER_COLOR).pack(pady=(15, 10))
        
        for i, tip in enumerate(self.plan_data["tips"]):
            ctk.CTkLabel(tips_frame, text=f"• {tip}", 
                        font=BODY_FONT, text_color=TEXT_BODY_COLOR, justify="left").pack(anchor="w", padx=20, pady=5)

# ==========================================
# ФРЕЙМЫ ДЛЯ СУЩЕСТВУЮЩИХ ПЛАНОВ И ИСТОРИИ
# ==========================================

class ExistingPlansFrame(BaseFrame):
    """Фрейм выбора существующего плана тренировок."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, **kwargs)
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(30, 10))
        
        back_btn = ctk.CTkButton(header_frame, text=self.controller.loc.get("back_to_main"), font=BODY_FONT,
                                fg_color="transparent", text_color=TEXT_BODY_COLOR, hover_color=CARD_BG_COLOR,
                                command=self.controller.on_back_to_main)
        back_btn.pack(side="left")
        
        ctk.CTkLabel(self, text="📁 ВАШИ ПЛАНЫ ТРЕНИРОВОК", font=HEADER_FONT, text_color=ACCENT_COLOR).pack(pady=(20, 10))
        ctk.CTkLabel(self, text="Выберите сохраненный план для повторения:", font=SUBHEADER_FONT, text_color=TEXT_BODY_COLOR).pack(pady=(0, 20))
        
        # Список планов
        self.plans_frame = ctk.CTkScrollableFrame(self, fg_color=CARD_BG_COLOR, corner_radius=15)
        self.plans_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
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
            ctk.CTkLabel(self.plans_frame, text="У вас пока нет сохраненных планов", 
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
        
        ctk.CTkLabel(top_frame, text=plan["name"], font=("Helvetica Neue", 16, "bold"), 
                    text_color=TEXT_HEADER_COLOR).pack(side="left", anchor="w")
        
        ctk.CTkLabel(top_frame, text=f"📅 {plan['date']}", font=("Helvetica Neue", 12),
                    text_color=HIGHLIGHT_COLOR).pack(side="right", anchor="e")
        
        # Детали плана
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(details_frame, text=f"Уровень: {plan['level']}", 
                    font=("Helvetica Neue", 13), text_color=TEXT_BODY_COLOR).pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(details_frame, text=f"Цель: {plan['goal']}", 
                    font=("Helvetica Neue", 13), text_color=TEXT_BODY_COLOR).pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(details_frame, text=f"Место: {plan['condition']}", 
                    font=("Helvetica Neue", 13), text_color=TEXT_BODY_COLOR).pack(side="left")
        
        # Кнопка загрузить
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkButton(btn_frame, text="ЗАГРУЗИТЬ ПЛАН", font=BODY_FONT, height=35,
                     fg_color=ACCENT_COLOR, hover_color="#0069D9",
                     command=lambda p=plan: self.controller.load_existing_plan(p["id"])).pack(side="right")

class WorkoutHistoryFrame(BaseFrame):
    """Фрейм истории тренировок."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, **kwargs)
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(30, 10))
        
        back_btn = ctk.CTkButton(header_frame, text=self.controller.loc.get("back_to_main"), font=BODY_FONT,
                                fg_color="transparent", text_color=TEXT_BODY_COLOR, hover_color=CARD_BG_COLOR,
                                command=self.controller.on_back_to_main)
        back_btn.pack(side="left")
        
        ctk.CTkLabel(self, text="📊 ИСТОРИЯ ТРЕНИРОВОК", font=HEADER_FONT, text_color=ACCENT_COLOR).pack(pady=(20, 10))
        
        # Список истории
        self.history_frame = ctk.CTkScrollableFrame(self, fg_color=CARD_BG_COLOR, corner_radius=15)
        self.history_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
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
            ctk.CTkLabel(self.history_frame, text="У вас пока нет завершенных тренировок", 
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
        
        ctk.CTkLabel(top_frame, text=record["workout_name"], font=("Helvetica Neue", 16, "bold"), 
                    text_color=TEXT_HEADER_COLOR).pack(side="left", anchor="w")
        
        ctk.CTkLabel(top_frame, text=f"📅 {record['completed_at']}", font=("Helvetica Neue", 12),
                    text_color=HIGHLIGHT_COLOR).pack(side="right", anchor="e")
        
        # Детали тренировки
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(details_frame, text=f"⏱️ Длительность: {record['duration']} мин", 
                    font=("Helvetica Neue", 13), text_color=TEXT_BODY_COLOR).pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(details_frame, text=f"✅ Упражнений: {len(record['exercises'])}", 
                    font=("Helvetica Neue", 13), text_color=TEXT_BODY_COLOR).pack(side="left")
        
        # Список упражнений (свернутый)
        exercises_frame = ctk.CTkFrame(card, fg_color="#3C3C3E", corner_radius=8)
        exercises_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(exercises_frame, text="Выполненные упражнения:", 
                    font=("Helvetica Neue", 12, "bold"), text_color=TEXT_BODY_COLOR).pack(anchor="w", padx=10, pady=5)
        
        for i, exercise in enumerate(record['exercises'][:3]):  # Показываем только первые 3
            ctk.CTkLabel(exercises_frame, text=f"• {exercise}", 
                        font=("Helvetica Neue", 11), text_color=TEXT_BODY_COLOR).pack(anchor="w", padx=20, pady=2)
        
        if len(record['exercises']) > 3:
            ctk.CTkLabel(exercises_frame, text=f"... и еще {len(record['exercises']) - 3} упражнений", 
                        font=("Helvetica Neue", 11), text_color=HIGHLIGHT_COLOR).pack(anchor="w", padx=20, pady=2)

# ==========================================
# ЭКРАНЫ РЕЗУЛЬТАТОВ И ПРОГРЕССА
# ==========================================

class ExerciseFrame(BaseFrame):
    """Экран тренировки с поэтапным прохождением."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, **kwargs)
        
        self.all_exercises = []
        self.current_stage_idx = 0
        self.stages = ["🔥 РАЗМИНКА", "⚡ ОСНОВНАЯ ТРЕНИРОВКА", "🧘 ЗАМИНКА"]
        self.start_time = None
        self.completed_exercises = []
        self.workout_name = None
        
        # Заголовок этапа
        self.stage_label = ctk.CTkLabel(self, text="", font=HEADER_FONT, text_color=ACCENT_COLOR)
        self.stage_label.pack(pady=(20, 5))
        
        self.sub_label = ctk.CTkLabel(self, text="Выполните все упражнения этапа", font=BODY_FONT, text_color=TEXT_BODY_COLOR)
        self.sub_label.pack(pady=(0, 15))

        # Список упражнений
        self.exercise_list = ctk.CTkScrollableFrame(self, fg_color=CARD_BG_COLOR, corner_radius=15)
        self.exercise_list.pack(pady=10, padx=40, fill="both", expand=True)

        # Панель ввода названия тренировки
        self.name_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.name_frame.pack(fill="x", padx=40, pady=(10, 0))
        
        ctk.CTkLabel(self.name_frame, text="Название тренировки:", 
                    font=BODY_FONT, text_color=TEXT_BODY_COLOR).pack(side="left", padx=(0, 10))
        
        self.name_entry = ctk.CTkEntry(self.name_frame, placeholder_text="Введите название тренировки",
                                      font=BODY_FONT, width=300)
        self.name_entry.pack(side="left", fill="x", expand=True)

        # Нижняя панель с кнопками
        self.footer = ctk.CTkFrame(self, fg_color="transparent")
        self.footer.pack(fill="x", padx=40, pady=20)
        
        self.btn_next = ctk.CTkButton(self.footer, text="Следующий этап", font=BUTTON_FONT, 
                                      height=50, fg_color=ACCENT_COLOR, state="disabled",
                                      command=self.next_stage)
        self.btn_next.pack(fill="x")
        
        # Кнопки сохранения
        self.save_buttons_frame = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.save_buttons_frame.pack(fill="x", pady=(10, 0))
        
        # Кнопка сохранения как плана
        self.btn_save_plan = ctk.CTkButton(self.save_buttons_frame, text="💾 СОХРАНИТЬ ПЛАН ТРЕНИРОВКИ", 
                                          font=BODY_FONT, height=40, 
                                          fg_color=HIGHLIGHT_COLOR, hover_color="#E08500",
                                          command=self.save_as_training_plan)
        self.btn_save_plan.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Кнопка сохранения в историю
        self.btn_save_history = ctk.CTkButton(self.save_buttons_frame, text="📊 СОХРАНИТЬ В ИСТОРИЮ", 
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
        self.workout_name = f"Тренировка от {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        self.name_entry.delete(0, 'end')
        self.name_entry.insert(0, self.workout_name)
        self.show_stage()

    def get_current_stage_data(self):
        """Фильтрует упражнения для текущего этапа."""
        stage_name = self.stages[self.current_stage_idx]
        
        if "РАЗМИНКА" in stage_name:
            return [ex for ex in self.all_exercises if "РАЗМИНКА" in ex]
        elif "ОСНОВНАЯ" in stage_name:
            # Основная тренировка - все упражнения, кроме разминки и заминки
            return [ex for ex in self.all_exercises if "РАЗМИНКА" not in ex and "ЗАМИНКА" not in ex]
        else:  # Заминка
            return [ex for ex in self.all_exercises if "ЗАМИНКА" in ex]

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
        
        next_text = "Следующий этап" if self.current_stage_idx < 2 else "Завершить тренировку"
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
        from tkinter import messagebox
        
        duration = int((datetime.now() - self.start_time).total_seconds() / 60)
        workout_name = self.name_entry.get().strip() or self.workout_name
        
        # Сохраняем историю тренировки
        self.controller.save_workout_history(workout_name, self.completed_exercises, duration)
        
        messagebox.showinfo("Поздравляем!", f"Тренировка '{workout_name}' успешно завершена и сохранена в истории!")
        self.controller.on_back_to_main()

    def save_as_training_plan(self):
        """Сохраняет текущую тренировку как план."""
        from tkinter import messagebox
        
        plan_name = self.name_entry.get().strip() or f"План тренировки от {datetime.now().strftime('%d.%m.%Y')}"
        
        if hasattr(self.controller, 'wizard_selections'):
            level = self.controller.wizard_selections.get("level", "Новичок")
            goal = self.controller.wizard_selections.get("goal", "Похудение")
            condition = self.controller.wizard_selections.get("condition", "Дом")
            
            # Сохраняем план тренировки
            self.controller.save_training_plan_with_history(plan_name, level, goal, condition, self.all_exercises)
            messagebox.showinfo("Сохранено", f"План тренировки '{plan_name}' успешно сохранен!")

    def save_to_history(self):
        """Сохраняет текущую тренировку в историю."""
        from tkinter import messagebox
        
        workout_name = self.name_entry.get().strip() or f"Тренировка от {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        duration = int((datetime.now() - self.start_time).total_seconds() / 60) if self.start_time else 0
        
        # Сохраняем историю тренировки
        self.controller.save_workout_history(workout_name, self.completed_exercises, duration)
        messagebox.showinfo("Сохранено", f"Тренировка '{workout_name}' сохранена в истории!")
    """Экран тренировки с поэтапным прохождением."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, **kwargs)
        
        self.all_exercises = []
        self.current_stage_idx = 0
        self.stages = ["🔥 РАЗМИНКА", "⚡ ОСНОВНАЯ ТРЕНИРОВКА", "🧘 ЗАМИНКА"]
        self.start_time = None
        self.completed_exercises = []
        
        # Заголовок этапа
        self.stage_label = ctk.CTkLabel(self, text="", font=HEADER_FONT, text_color=ACCENT_COLOR)
        self.stage_label.pack(pady=(20, 5))
        
        self.sub_label = ctk.CTkLabel(self, text="Выполните все упражнения этапа", font=BODY_FONT, text_color=TEXT_BODY_COLOR)
        self.sub_label.pack(pady=(0, 15))

        # Список упражнений
        self.exercise_list = ctk.CTkScrollableFrame(self, fg_color=CARD_BG_COLOR, corner_radius=15)
        self.exercise_list.pack(pady=10, padx=40, fill="both", expand=True)

        # Нижняя панель с кнопкой
        self.footer = ctk.CTkFrame(self, fg_color="transparent")
        self.footer.pack(fill="x", padx=40, pady=20)
        
        self.btn_next = ctk.CTkButton(self.footer, text="Следующий этап", font=BUTTON_FONT, 
                                      height=50, fg_color=ACCENT_COLOR, state="disabled",
                                      command=self.next_stage)
        self.btn_next.pack(fill="x")
        
        # Кнопка сохранения плана
        self.btn_save = ctk.CTkButton(self.footer, text="💾 СОХРАНИТЬ ПЛАН", font=BODY_FONT,
                                      height=40, fg_color=HIGHLIGHT_COLOR, hover_color="#E08500",
                                      command=self.save_current_plan)
        self.btn_save.pack(pady=(10, 0))

    def load_exercises(self, exercises):
        """Загружает упражнения."""
        self.all_exercises = exercises
        self.current_stage_idx = 0
        self.start_time = datetime.now()
        self.completed_exercises = []
        self.show_stage()

    def get_current_stage_data(self):
        """Фильтрует упражнения для текущего этапа."""
        stage_name = self.stages[self.current_stage_idx]
        
        if "РАЗМИНКА" in stage_name:
            return [ex for ex in self.all_exercises if "РАЗМИНКА" in ex]
        elif "ОСНОВНАЯ" in stage_name:
            # Основная тренировка - все упражнения, кроме разминки и заминки
            return [ex for ex in self.all_exercises if "РАЗМИНКА" not in ex and "ЗАМИНКА" not in ex]
        else:  # Заминка
            return [ex for ex in self.all_exercises if "ЗАМИНКА" in ex]

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
        
        next_text = "Следующий этап" if self.current_stage_idx < 2 else "Завершить тренировку"
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
        from datetime import datetime
        duration = int((datetime.now() - self.start_time).total_seconds() / 60)
        
        workout_name = f"Тренировка от {datetime.now().strftime('%d.%m.%Y')}"
        
        # Сохраняем историю тренировки
        self.controller.save_workout_history(workout_name, self.completed_exercises, duration)
        
        messagebox.showinfo("Поздравляем!", "Тренировка успешно завершена!")
        self.controller.on_back_to_main()

    def save_current_plan(self):
        """Сохраняет текущий план тренировок."""
        plan_name = f"План тренировки от {datetime.now().strftime('%d.%m.%Y')}"
        
        if hasattr(self.controller, 'wizard_selections'):
            level = self.controller.wizard_selections.get("level", "Новичок")
            goal = self.controller.wizard_selections.get("goal", "Похудение")
            condition = self.controller.wizard_selections.get("condition", "Дом")
            
            self.controller.save_training_plan(plan_name, level, goal, condition, self.all_exercises)
            messagebox.showinfo("Сохранено", "План тренировки успешно сохранен!")

class ProgressFrame(BaseFrame):
    """Экран истории прогресса."""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, **kwargs)
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(30, 10))
        ctk.CTkButton(header_frame, text=self.controller.loc.get("back_to_main"), font=BODY_FONT,
                        fg_color="transparent", text_color=TEXT_BODY_COLOR, hover_color=CARD_BG_COLOR,
                        command=self.controller.on_back_to_main).pack(side="left")
                        
        ctk.CTkLabel(self, text=self.controller.loc.get("workout_history"), font=HEADER_FONT, text_color=TEXT_HEADER_COLOR).pack(pady=(20, 20))
        
        self.progress_display = ctk.CTkScrollableFrame(self, fg_color=CARD_BG_COLOR, corner_radius=15)
        self.progress_display.pack(pady=10, padx=40, fill="both", expand=True)

    def load_progress(self, progress_data):
        for widget in self.progress_display.winfo_children():
            widget.destroy()
        
        if not progress_data:
            ctk.CTkLabel(self.progress_display, text=self.controller.loc.get("no_history"), font=BODY_FONT, text_color=TEXT_BODY_COLOR).pack(pady=20)
            return

        for entry in progress_data:
            row = ctk.CTkFrame(self.progress_display, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            date_str = entry.get('timestamp', '???')[:16].replace('T', ' ')
            ex_name = entry.get('exercise_name', 'Неизвестно')
            
            ctk.CTkLabel(row, text=f"📅 {date_str}", font=("Helvetica Neue", 12), text_color=HIGHLIGHT_COLOR).pack(anchor="w")
            ctk.CTkLabel(row, text=f"✅ Выполнено: {ex_name}", font=("Helvetica Neue", 14, "bold"), text_color=TEXT_HEADER_COLOR).pack(anchor="w", pady=(2, 10))
            ctk.CTkFrame(row, height=1, fg_color=CARD_BG_COLOR).pack(fill="x")

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
        
        self._create_widgets()
        
    def _create_widgets(self):
        ctk.CTkLabel(self, text="🏋️", font=("Helvetica Neue", 60)).pack(pady=(40, 10))
        ctk.CTkLabel(self, text=self.controller.loc.get("login_title"), font=HEADER_FONT, text_color=TEXT_HEADER_COLOR).pack(pady=(0, 30))
        
        self.entry_user = ctk.CTkEntry(self, placeholder_text=self.controller.loc.get("username"), height=40, font=BODY_FONT)
        self.entry_user.pack(pady=10, padx=40, fill="x")

        self.entry_pass = ctk.CTkEntry(self, placeholder_text=self.controller.loc.get("password"), show="*", height=40, font=BODY_FONT)
        self.entry_pass.pack(pady=10, padx=40, fill="x")
        
        ctk.CTkButton(self, text=self.controller.loc.get("login"), font=BUTTON_FONT, height=45, fg_color=ACCENT_COLOR, hover_color="#0069D9",
                      command=self.on_login).pack(pady=(20, 10), padx=40, fill="x")

        ctk.CTkButton(self, text=self.controller.loc.get("no_account"), font=BODY_FONT, fg_color="transparent", hover_color=CARD_BG_COLOR,
                      command=self.controller.open_register_window).pack(pady=5)

        ctk.CTkButton(self, text=self.controller.loc.get("server_settings"), font=("Helvetica Neue", 10), fg_color="transparent", text_color=TEXT_BODY_COLOR,
                      command=self.controller.open_server_menu).pack(side="bottom", pady=10)

    def on_login(self):
        self.controller.on_login(self.entry_user.get().strip(), self.entry_pass.get().strip())
        
    def update_texts(self):
        self.title(self.controller.loc.get("login_title"))
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
        
        self._create_widgets()
        
    def _create_widgets(self):
        ctk.CTkLabel(self, text=self.controller.loc.get("register_title"), font=HEADER_FONT, text_color=TEXT_HEADER_COLOR).pack(pady=(40, 30))
        
        self.e_user = ctk.CTkEntry(self, placeholder_text=self.controller.loc.get("username"), height=40, font=BODY_FONT)
        self.e_user.pack(pady=5, padx=40, fill="x")
        
        self.e_pass = ctk.CTkEntry(self, placeholder_text=self.controller.loc.get("password"), show="*", height=40, font=BODY_FONT)
        self.e_pass.pack(pady=5, padx=40, fill="x")
        
        self.e_phone = ctk.CTkEntry(self, placeholder_text=self.controller.loc.get("phone_placeholder"), height=40, font=BODY_FONT)
        self.e_phone.pack(pady=5, padx=40, fill="x")
        
        self.e_dob = ctk.CTkEntry(self, placeholder_text=self.controller.loc.get("dob_placeholder"), height=40, font=BODY_FONT)
        self.e_dob.pack(pady=5, padx=40, fill="x")

        ctk.CTkButton(self, text=self.controller.loc.get("register_button"), font=BUTTON_FONT, height=45, fg_color=HIGHLIGHT_COLOR, hover_color="#E08500",
                      command=self.on_register).pack(pady=(30, 20), padx=40, fill="x")

    def on_register(self):
        u, p = self.e_user.get().strip(), self.e_pass.get().strip()
        ph, dob = self.e_phone.get().strip(), self.e_dob.get().strip()
        
        if not u or not p or not ph or not dob:
             messagebox.showwarning("Ошибка", self.controller.loc.get("fill_all_fields"))
             return

        if not Validator.is_valid_phone_by(ph):
            messagebox.showerror("Ошибка", self.controller.loc.get("invalid_phone"))
            return
        valid_date, msg = Validator.is_valid_date(dob)
        if not valid_date:
            messagebox.showerror("Ошибка", msg)
            return

        if self.controller.on_register(u, p, ph, dob):
            self.destroy()
            
    def update_texts(self):
        self.title(self.controller.loc.get("register_title"))
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
        
        self._create_widgets()
        
    def _create_widgets(self):
        ctk.CTkLabel(self, text=self.controller.loc.get("manage_server"), font=SUBHEADER_FONT).pack(pady=20)

        ctk.CTkButton(self, text=self.controller.loc.get("start_server"), font=BUTTON_FONT, fg_color=ACCENT_COLOR,
                      command=self.controller.on_start_server).pack(pady=10, padx=20, fill="x")
        
        self.btn_stop_server = ctk.CTkButton(self, text=self.controller.loc.get("stop_server"), font=BUTTON_FONT, fg_color=HIGHLIGHT_COLOR, hover_color="#E08500",
                                             command=self.controller.on_stop, state="disabled" if not self.controller.server_running else "normal")
        self.btn_stop_server.pack(pady=5, padx=20, fill="x")
        
    def update_texts(self):
        self.title(self.controller.loc.get("server_settings"))