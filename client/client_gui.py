# client_gui.py
import socket
import threading
import customtkinter as ctk
import json
from tkinter import messagebox
import sys
from datetime import datetime

# Импортируем новые красивые UI классы из styles
from client_styles import (
    LandingFrame, StepPlaceFrame, StepGoalFrame, StepLevelFrame,
    ExerciseFrame, ProgressFrame, NutritionGoalFrame, NutritionPlanFrame,
    ExistingPlansFrame, WorkoutHistoryFrame, AuthWindow, RegisterWindow, ServerMenuWindow
)
from localization import LocalizationManager

# --- ЗАГЛУШКИ ДЛЯ СЕРВЕРА ---
try:
    from server.server import run_server, HOST, PORT, LoggerObserver
except ImportError:
    HOST, PORT = "127.0.0.1", 65432
    def run_server(stop_event, logger_func): pass
    class LoggerObserver:
        def add_observer(self, obs): pass
        def notify(self, msg): pass

class Client:
    """Класс клиента для сетевого взаимодействия."""
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        if self.sock: return True
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.sock.settimeout(5)
            return True
        except Exception as e:
            print(f"CLIENT: Connection error: {e}")
            return False

    def send(self, data):
        if not self.connect(): return
        try:
            json_data = json.dumps(data).encode("utf-8") + b"\n"
            self.sock.sendall(json_data)
        except Exception as e:
            print(f"CLIENT: Send error: {e}")
            self.close()

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None

class AppController(ctk.CTk):
    """Главный контроллер приложения."""
    def __init__(self):
        super().__init__()
        self.loc = LocalizationManager()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.title(f"Fitness App - Create Your Perfect Workout [{self.loc.current_lang.upper()}]")
        self.geometry("800x700")
        self.minsize(700, 600)
        
        # Состояние
        self.stop_event = threading.Event()
        self.server_thread = None
        self.server_running = False
        self.client = Client()
        self.authenticated = False
        self.username = None
        
        # Состояние Мастера
        self.wizard_selections = {
            "condition": None,
            "goal": None,
            "level": None
        }
        
        self.current_exercises = []
        self.current_workout_name = None
        self.logger = LoggerObserver()
        self.frames = {}
        self.current_frame = None

        self.withdraw()
        self.auth_window = AuthWindow(self, self)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # ... (остальные методы остаются такими же)

    def set_nutrition_goal(self, goal):
        """Устанавливает цель питания и загружает план."""
        self.client.send({
            "action": "get_nutrition_plan",
            "goal": goal,
            "username": self.username
        })
        
    def save_training_plan_with_history(self, plan_name, level, goal, condition, exercises):
        """Сохраняет план тренировки и добавляет в историю."""
        if self.username:
            # Сохраняем план тренировки
            self.client.send({
                "action": "save_plan",
                "username": self.username,
                "plan_name": plan_name,
                "level": level,
                "goal": goal,
                "condition": condition,
                "exercises": exercises
            })
            
            # Также сохраняем как выполненную тренировку в историю
            workout_name = f"Сохраненный план: {plan_name}"
            self.save_workout_history(workout_name, exercises, 0)  # Длительность 0 для сохраненных планов
    
    def finish_workout_and_save(self, workout_name, exercises, duration, save_as_plan=False):
        """Завершает тренировку и сохраняет при необходимости."""
        # Сохраняем в историю тренировок
        self.save_workout_history(workout_name, exercises, duration)
        
        # Если нужно сохранить как план
        if save_as_plan and hasattr(self, 'wizard_selections'):
            level = self.wizard_selections.get("level", "Новичок")
            goal = self.wizard_selections.get("goal", "Похудение")
            condition = self.wizard_selections.get("condition", "Дом")
            plan_name = f"План: {workout_name}"
            
            self.save_training_plan_with_history(plan_name, level, goal, condition, exercises)
    """Главный контроллер приложения."""
    def __init__(self):
        super().__init__()
        self.loc = LocalizationManager()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.title(f"Fitness App - Create Your Perfect Workout [{self.loc.current_lang.upper()}]")
        self.geometry("800x700")
        self.minsize(700, 600)
        
        # Состояние
        self.stop_event = threading.Event()
        self.server_thread = None
        self.server_running = False
        self.client = Client()
        self.authenticated = False
        self.username = None
        
        # Состояние Мастера
        self.wizard_selections = {
            "condition": None,
            "goal": None,
            "level": None
        }
        
        self.current_exercises = []
        self.logger = LoggerObserver()
        self.frames = {}
        self.current_frame = None

        self.withdraw()
        self.auth_window = AuthWindow(self, self)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def log(self, message):
        print(f"[SYSTEM] {message}")
        self.logger.notify(message)

    def toggle_language(self):
        """Переключает язык приложения."""
        new_lang = 'en' if self.loc.current_lang == 'ru' else 'ru'
        self.loc.set_language(new_lang)
        
        self.title(f"Fitness App - Create Your Perfect Workout [{new_lang.upper()}]")
        
        if self.current_frame:
            frame_class = type(self.current_frame)
            frame_key = None
            
            for key, frame in self.frames.items():
                if frame == self.current_frame:
                    frame_key = key
                    break
            
            if frame_key:
                self.frames.pop(frame_key)
                self.frames[frame_key] = frame_class(self, self)
                self.show_frame(frame_class, frame_key)
        
        if hasattr(self, 'auth_window') and self.auth_window.winfo_exists():
            self.auth_window.update_texts()
        
        if hasattr(self, 'register_window') and self.register_window.winfo_exists():
            self.register_window.update_texts()

    # --- Новые методы ---
    
    def on_create_nutrition_plan(self):
        """Открывает окно создания плана питания."""
        self.show_frame(NutritionGoalFrame, "nutrition_goal")

    def on_use_existing_workout_plan(self):
        """Открывает окно выбора существующего плана тренировок."""
        self.show_frame(ExistingPlansFrame, "existing_plans")
        
    def set_nutrition_goal(self, goal):
        """Устанавливает цель питания и загружает план."""
        self.client.send({
            "action": "get_nutrition_plan",
            "goal": goal
        })
        
    def load_existing_plan(self, plan_id):
        """Загружает существующий план тренировок."""
        if self.username:
            self.client.send({
                "action": "load_existing_plan",
                "username": self.username,
                "plan_id": plan_id
            })

    def open_workout_history(self):
        """Открывает историю тренировок."""
        self.show_frame(WorkoutHistoryFrame, "workout_history")
        if self.username:
            self.client.send({
                "action": "get_workout_history",
                "username": self.username
            })

    def save_workout_history(self, workout_name, exercises, duration):
        """Сохраняет историю тренировки."""
        if self.username:
            self.client.send({
                "action": "save_workout_history",
                "username": self.username,
                "workout_name": workout_name,
                "exercises": exercises,
                "duration": duration
            })

    def save_training_plan(self, plan_name, level, goal, condition, exercises):
        """Сохраняет план тренировки."""
        if self.username:
            self.client.send({
                "action": "save_plan",
                "username": self.username,
                "plan_name": plan_name,
                "level": level,
                "goal": goal,
                "condition": condition,
                "exercises": exercises
            })

    # --- Управление окнами и навигация ---
    
    def show_frame(self, frame_class, frame_key=None, **kwargs):
        """Универсальный метод переключения фреймов."""
        if self.current_frame:
            self.current_frame.pack_forget()
        
        key = frame_key if frame_key else frame_class.__name__
        
        if key not in self.frames or key in ["existing_plans", "workout_history", "nutrition_plan"]:
            if frame_class == NutritionPlanFrame:
                self.frames[key] = frame_class(self, self, **kwargs)
            else:
                self.frames[key] = frame_class(self, self)

        self.current_frame = self.frames[key]
        self.current_frame.pack(fill="both", expand=True)
        
        if isinstance(self.current_frame, ExerciseFrame) and self.current_exercises:
            self.current_frame.load_exercises(self.current_exercises)

    def open_server_menu(self):
        if not hasattr(self, 'server_menu') or not self.server_menu.winfo_exists():
            self.server_menu = ServerMenuWindow(self, self)
        else:
            self.server_menu.focus()

    def open_register_window(self):
        if not hasattr(self, 'register_window') or not self.register_window.winfo_exists():
            self.register_window = RegisterWindow(self, self)
        else:
             self.register_window.focus()

    # --- Логика Пошагового Мастера ---

    def start_wizard(self):
        self.wizard_selections = {"condition": None, "goal": None, "level": None}
        self.show_frame(StepPlaceFrame, "step1")

    def set_wizard_condition(self, condition):
        self.wizard_selections["condition"] = condition
        self.show_frame(StepGoalFrame, "step2")

    def set_wizard_goal(self, goal):
        self.wizard_selections["goal"] = goal
        self.show_frame(StepLevelFrame, "step3")

    def set_wizard_level(self, level):
        self.wizard_selections["level"] = level
        self.finish_wizard()

    def finish_wizard(self):
        self.client.send({
            "action": "get_exercises", 
            "level": self.wizard_selections["level"], 
            "goal": self.wizard_selections["goal"],
            "condition": self.wizard_selections["condition"],
            "username": self.username
        })

    def wizard_back(self, current_step):
        if current_step == "step2":
            self.show_frame(StepPlaceFrame, "step1")
        elif current_step == "step3":
             self.show_frame(StepGoalFrame, "step2")

    # --- Сетевая логика ---

    def on_start_server(self):
        if self.server_thread is None or not self.server_thread.is_alive():
            self.stop_event.clear()
            self.server_thread = threading.Thread(target=run_server, args=(self.stop_event, self.log), daemon=True)
            self.server_thread.start()
            self.server_running = True
            if hasattr(self, 'server_menu') and self.server_menu.winfo_exists():
                self.server_menu.btn_stop_server.configure(state="normal")
            self.log("Сервер запущен локально.")
    
    def on_stop(self):
        self.stop_event.set()
        self.server_running = False
        if hasattr(self, 'server_menu') and self.server_menu.winfo_exists():
            self.server_menu.btn_stop_server.configure(state="disabled")
        self.log("Остановка сервера запрошена.")

    def on_login(self, username, password):
        if not self.client.connect():
            messagebox.showerror("Ошибка", "Не удалось подключиться к серверу.")
            return
        self.client.send({"action": "login", "username": username, "password": password})
        threading.Thread(target=self.reader_loop, daemon=True).start()

    def on_register(self, username, password, phone, dob):
        if not self.client.connect():
            messagebox.showerror("Ошибка", "Не удалось подключиться к серверу.")
            return False
        self.client.send({
            "action": "register", "username": username, "password": password,
            "phone": phone, "dob": dob
        })
        return True

    def reader_loop(self):
        try:
            buffer = ""
            while True:
                if not self.client.sock: break
                try:
                    data = self.client.sock.recv(1024).decode("utf-8")
                    if not data: break
                    buffer += data
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        if line:
                            response = json.loads(line)
                            self.after(0, lambda r=response: self.handle_server_response(r))
                except socket.timeout:
                    continue
                except Exception as e:
                     print(f"Socket error in loop: {e}")
                     break
        except Exception as e:
            print(f"Reader loop critical error: {e}")
        finally:
            self.client.close()

    def handle_server_response(self, response):
        action = response.get("action")
        print(f"Server response: {response}")
        
        if action == "auth":
            if response["success"]:
                self.authenticated = True
                self.username = response["username"]
                if hasattr(self, 'auth_window') and self.auth_window.winfo_exists():
                    self.auth_window.destroy()
                self.deiconify()
                self.show_frame(LandingFrame, "landing")
            else:
                messagebox.showerror("Ошибка входа", response.get("message", "Неверные данные"))
                
        elif action == "register":
            if response["success"]:
                messagebox.showinfo("Успех", "Регистрация успешна! Теперь выполните вход.")
                if hasattr(self, 'register_window') and self.register_window.winfo_exists():
                    self.register_window.destroy()
            else:
                messagebox.showerror("Ошибка регистрации", response.get("message", "Error"))
                
        elif action == "exercises":
            self.current_exercises = response.get("exercises", [])
            self.show_frame(ExerciseFrame, "exercise")
            
        elif action == "workout_history":
            history = response.get("history", [])
            if "workout_history" in self.frames:
                self.frames["workout_history"].update_history(history)
                
        elif action == "user_plans":
            plans = response.get("plans", [])
            if "existing_plans" in self.frames:
                self.frames["existing_plans"].update_plans(plans)
                
        elif action == "nutrition_plan":
            if response["success"]:
                plan_data = response.get("plan")
                self.show_frame(NutritionPlanFrame, "nutrition_plan", plan_data=plan_data)
            else:
                messagebox.showerror("Ошибка", response.get("message", "Не удалось загрузить план питания"))
                
        elif action == "existing_plan_loaded":
            if response["success"]:
                plan = response.get("plan")
                self.current_exercises = plan.get("exercises", [])
                self.show_frame(ExerciseFrame, "exercise")
            else:
                messagebox.showerror("Ошибка", response.get("message", "Не удалось загрузить план"))
                
        elif action == "workout_history_saved":
            if response["success"]:
                print("История тренировки сохранена")
            else:
                messagebox.showerror("Ошибка", "Не удалось сохранить историю тренировки")
                
        elif action == "plan_saved":
            if response["success"]:
                print("План тренировки сохранен")
            else:
                messagebox.showerror("Ошибка", "Не удалось сохранить план тренировки")

    # --- Обработчики событий UI ---

    def on_check_exercise(self, exercise_name, is_checked):
        if is_checked and self.username:
            self.client.send({
                "action": "track_progress",
                "username": self.username,
                "exercise": exercise_name
            })

    def on_open_progress(self):
        self.show_frame(ProgressFrame, "progress")

    def on_back_to_main(self):
        self.show_frame(LandingFrame, "landing")

    def on_logout(self):
        self.authenticated = False
        self.username = None
        self.client.close()
        self.withdraw()
        for frame in self.frames.values():
            frame.destroy()
        self.frames = {}
        self.auth_window = AuthWindow(self, self)
    

    def on_close(self):
        self.client.close()
        self.stop_event.set()
        self.destroy()
        sys.exit(0)
    
    def save_training_plan_with_history(self, plan_name, level, goal, condition, exercises):
    
        if self.username:
            self.client.send({
                "action": "save_plan_with_history",
                "username": self.username,
                "plan_name": plan_name,
                "level": level,
                "goal": goal,
                "condition": condition,
                "exercises": exercises
            })

if __name__ == "__main__":
    app = AppController()
    app.mainloop()