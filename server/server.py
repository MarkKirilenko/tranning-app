# server.py
import socket
import threading
import json
from models import DatabaseManager
import routes as routes

HOST = '0.0.0.0'
PORT = 65432

class LoggerObserver:
    def __init__(self):
        self.observers = []
    
    def add_observer(self, obs):
        self.observers.append(obs)
    
    def notify(self, msg):
        for obs in self.observers:
            obs.update(msg)

def handle_client(conn, addr, db_manager, logger):
    print(f"[SERVER] Подключен {addr}")
    
    try:
        buffer = ""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            buffer += data.decode("utf-8")
            
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if line:
                    try:
                        request = json.loads(line)
                        print(f"[SERVER] Получен запрос: {request}")
                        response = process_request(request, db_manager)
                        conn.sendall(json.dumps(response).encode("utf-8") + b"\n")
                    except json.JSONDecodeError:
                        conn.sendall(json.dumps({"error": "Invalid JSON"}).encode("utf-8") + b"\n")
    except Exception as e:
        print(f"[SERVER] Ошибка с клиентом {addr}: {e}")
    finally:
        conn.close()
        print(f"[SERVER] Отключен {addr}")

def process_request(request, db_manager):
    action = request.get("action")
    
    if action == "login":
        return routes.handle_login(
            db_manager,
            request.get("username"),
            request.get("password")
        )
    
    elif action == "register":
        return routes.handle_register(
            db_manager,
            request.get("username"),
            request.get("password"),
            request.get("phone"),
            request.get("dob")
        )
    
    elif action == "get_exercises":
        return routes.handle_get_exercises(
            db_manager,
            request.get("condition"),
            request.get("level"),
            request.get("goal")
        )
    
    elif action == "track_progress":
        return routes.handle_track_progress(
            db_manager,
            request.get("username"),
            request.get("exercise")
        )
    
    elif action == "save_workout_history":
        return routes.handle_save_workout_history(
            db_manager,
            request.get("username"),
            request.get("workout_name"),
            request.get("exercises"),
            request.get("duration")
        )
    
    elif action == "get_workout_history":
        return routes.handle_get_workout_history(
            db_manager,
            request.get("username")
        )
    
    elif action == "get_user_plans":
        return routes.handle_get_user_plans(
            db_manager,
            request.get("username")
        )
    
    elif action == "get_nutrition_plan":
        return routes.handle_get_nutrition_plan(
            db_manager,
            request.get("goal")
        )
    
    elif action == "load_existing_plan":
        return routes.handle_load_existing_plan(
            db_manager,
            request.get("username"),
            request.get("plan_id")
        )
    
    elif action == "save_plan":
        return routes.handle_save_plan(
            db_manager,
            request.get("username"),
            request.get("plan_name"),
            request.get("level"),
            request.get("goal"),
            request.get("condition"),
            request.get("exercises")
        )
    
    else:
        return {"error": "Unknown action", "action": action}

def run_server(stop_event, logger_func):
    db_manager = DatabaseManager()
    logger = LoggerObserver()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(1)
        
        print(f"[SERVER] Сервер запущен на {HOST}:{PORT}")
        
        while not stop_event.is_set():
            try:
                conn, addr = s.accept()
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(conn, addr, db_manager, logger),
                    daemon=True
                )
                client_thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                if not stop_event.is_set():
                    print(f"[SERVER] Ошибка: {e}")
                break
        
        print("[SERVER] Сервер остановлен")