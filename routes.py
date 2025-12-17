# routes.py
import json
from sqlalchemy.exc import IntegrityError
from models import User, Progress, DatabaseManager, SavedPlan, WorkoutHistory
from datetime import datetime

def handle_login(db_manager: DatabaseManager, username, password):
    session = db_manager.Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    
    if user and user.password == password:
        return {"action": "auth", "success": True, "username": username}
    return {"action": "auth", "success": False, "message": "Неверный логин или пароль"}

def handle_register(db_manager: DatabaseManager, username, password, phone, dob):
    session = db_manager.Session()
    new_user = User(username=username, password=password, phone=phone, dob=dob)
    
    try:
        session.add(new_user)
        session.commit()
        return {"action": "register", "success": True}
    except IntegrityError:
        session.rollback()
        return {"action": "register", "success": False, "message": "Пользователь уже существует"}
    finally:
        session.close()

def handle_get_exercises(db_manager: DatabaseManager, condition, level, goal):
    exercises = db_manager.get_exercises(condition, level, goal)
    
    if exercises:
        return {"action": "exercises", "success": True, "exercises": exercises}
    return {"action": "exercises", "success": False, "message": "Неверный уровень, цель или условия"}

def handle_track_progress(db_manager: DatabaseManager, username, exercise_name):
    session = db_manager.Session()
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        new_progress = Progress(user_id=user.id, exercise_name=exercise_name)
        session.add(new_progress)
        session.commit()
        session.close()
        return {"action": "progress", "success": True}
    
    session.close()
    return {"action": "progress", "success": False, "message": "Пользователь не найден"}

def handle_save_workout_history(db_manager: DatabaseManager, username, workout_name, exercises, duration):
    session = db_manager.Session()
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        try:
            history_id = db_manager.save_workout_history(user.id, workout_name, exercises, duration)
            session.close()
            return {"action": "workout_history_saved", "success": True, "history_id": history_id}
        except Exception as e:
            session.close()
            return {"action": "workout_history_saved", "success": False, "message": f"Ошибка сохранения: {str(e)}"}
    
    session.close()
    return {"action": "workout_history_saved", "success": False, "message": "Пользователь не найден"}

def handle_get_workout_history(db_manager: DatabaseManager, username):
    session = db_manager.Session()
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        history = db_manager.get_workout_history(user.id)
        session.close()
        return {"action": "workout_history", "success": True, "history": history}
    
    session.close()
    return {"action": "workout_history", "success": False, "message": "Пользователь не найден"}

def handle_get_user_plans(db_manager: DatabaseManager, username):
    session = db_manager.Session()
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        plans = db_manager.get_user_plans(user.id)
        session.close()
        return {"action": "user_plans", "success": True, "plans": plans}
    
    session.close()
    return {"action": "user_plans", "success": False, "message": "Пользователь не найден"}

def handle_get_nutrition_plan(db_manager: DatabaseManager, goal):
    try:
        with open('nutrition_plans.json', 'r', encoding='utf-8') as f:
            plans = json.load(f)
        
        plan = plans.get(goal)
        if plan:
            return {"action": "nutrition_plan", "success": True, "plan": plan}
        return {"action": "nutrition_plan", "success": False, "message": "План питания не найден"}
    except FileNotFoundError:
        return {"action": "nutrition_plan", "success": False, "message": "Файл с планами питания не найден"}
    except json.JSONDecodeError:
        return {"action": "nutrition_plan", "success": False, "message": "Ошибка чтения файла с планами питания"}
    except Exception as e:
        return {"action": "nutrition_plan", "success": False, "message": f"Ошибка загрузки плана: {str(e)}"}

def handle_load_existing_plan(db_manager: DatabaseManager, username, plan_id):
    session = db_manager.Session()
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        plan = db_manager.get_saved_plan_by_id(plan_id, user.id)
        session.close()
        if plan:
            return {"action": "existing_plan_loaded", "success": True, "plan": plan}
        return {"action": "existing_plan_loaded", "success": False, "message": "План не найден"}
    
    session.close()
    return {"action": "existing_plan_loaded", "success": False, "message": "Пользователь не найден"}

def handle_save_plan(db_manager: DatabaseManager, username, plan_name, level, goal, condition, exercises):
    session = db_manager.Session()
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        try:
            plan_id = db_manager.save_user_plan(user.id, plan_name, level, goal, condition, exercises)
            session.close()
            return {"action": "plan_saved", "success": True, "plan_id": plan_id}
        except Exception as e:
            session.close()
            return {"action": "plan_saved", "success": False, "message": f"Ошибка сохранения: {str(e)}"}
    
    session.close()
    return {"action": "plan_saved", "success": False, "message": "Пользователь не найден"}

def handle_save_plan_with_history(db_manager: DatabaseManager, username, plan_name, level, goal, condition, exercises):
    """Сохраняет план тренировки и добавляет в историю."""
    session = db_manager.Session()
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        try:
            # Сохраняем план тренировки
            plan_id = db_manager.save_user_plan(user.id, plan_name, level, goal, condition, exercises)
            
            # Сохраняем в историю тренировок
            history_id = db_manager.save_workout_history(
                user.id, 
                f"Сохраненный план: {plan_name}", 
                exercises, 
                0  # Длительность 0 для сохраненных планов
            )
            
            session.close()
            return {
                "action": "plan_with_history_saved", 
                "success": True, 
                "plan_id": plan_id, 
                "history_id": history_id
            }
        except Exception as e:
            session.close()
            return {"action": "plan_with_history_saved", "success": False, "message": f"Ошибка сохранения: {str(e)}"}
    
    session.close()
    return {"action": "plan_with_history_saved", "success": False, "message": "Пользователь не найден"}

def handle_get_progress_history(db_manager: DatabaseManager, username):
    """Получает историю прогресса пользователя (выполненные упражнения)."""
    session = db_manager.Session()
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        progress_history = []
        # Получаем прогресс пользователя
        progress_records = session.query(Progress).filter_by(user_id=user.id).order_by(Progress.timestamp.desc()).all()
        
        for record in progress_records:
            progress_history.append({
                "exercise_name": record.exercise_name,
                "timestamp": record.timestamp.strftime("%Y-%m-%d %H:%M")
            })
        
        session.close()
        return {"action": "progress_history", "success": True, "progress": progress_history}
    
    session.close()
    return {"action": "progress_history", "success": False, "message": "Пользователь не найден"}

def process_request(request, db_manager):
    """Основная функция обработки запросов."""
    action = request.get("action")
    
    if action == "login":
        return handle_login(
            db_manager,
            request.get("username"),
            request.get("password")
        )
    
    elif action == "register":
        return handle_register(
            db_manager,
            request.get("username"),
            request.get("password"),
            request.get("phone"),
            request.get("dob")
        )
    
    elif action == "get_exercises":
        return handle_get_exercises(
            db_manager,
            request.get("condition"),
            request.get("level"),
            request.get("goal")
        )
    
    elif action == "track_progress":
        return handle_track_progress(
            db_manager,
            request.get("username"),
            request.get("exercise")
        )
    
    elif action == "save_workout_history":
        return handle_save_workout_history(
            db_manager,
            request.get("username"),
            request.get("workout_name"),
            request.get("exercises"),
            request.get("duration")
        )
    
    elif action == "get_workout_history":
        return handle_get_workout_history(
            db_manager,
            request.get("username")
        )
    
    elif action == "get_user_plans":
        return handle_get_user_plans(
            db_manager,
            request.get("username")
        )
    
    elif action == "get_nutrition_plan":
        return handle_get_nutrition_plan(
            db_manager,
            request.get("goal")
        )
    
    elif action == "load_existing_plan":
        return handle_load_existing_plan(
            db_manager,
            request.get("username"),
            request.get("plan_id")
        )
    
    elif action == "save_plan":
        return handle_save_plan(
            db_manager,
            request.get("username"),
            request.get("plan_name"),
            request.get("level"),
            request.get("goal"),
            request.get("condition"),
            request.get("exercises")
        )
    
    elif action == "save_plan_with_history":
        return handle_save_plan_with_history(
            db_manager,
            request.get("username"),
            request.get("plan_name"),
            request.get("level"),
            request.get("goal"),
            request.get("condition"),
            request.get("exercises")
        )
    
    elif action == "get_progress_history":
        return handle_get_progress_history(
            db_manager,
            request.get("username")
        )
    
    else:
        return {"error": "Unknown action", "action": action}