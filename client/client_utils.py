# client_utils.py
import socket
import json
import customtkinter as ctk
from tkinter import messagebox

# --- Паттерн Factory (Для UI) ---

class FrameFactory:
    """Паттерн Factory для создания фреймов, принимает классы фреймов."""
    
    def __init__(self, main_frame_class, exercise_frame_class, progress_frame_class):
        self.main_frame_class = main_frame_class
        self.exercise_frame_class = exercise_frame_class
        self.progress_frame_class = progress_frame_class

    def create_frame(self, frame_type, master, controller):
        if frame_type == "main":
            frame = self.main_frame_class(master, controller, corner_radius=10)
        elif frame_type == "exercise":
            frame = self.exercise_frame_class(master, controller, corner_radius=10)
        elif frame_type == "progress":
            frame = self.progress_frame_class(master, controller, corner_radius=10)
        else:
            raise ValueError(f"Unknown frame type: {frame_type}")
        
        # setup_ui вызывается после создания фрейма
        frame.setup_ui()
        return frame

# --- Вспомогательные классы для сети и логирования ---

class Client:
    """Класс клиента для взаимодействия с сервером."""
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        if self.sock:
            return True 
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            return True
        except Exception:
            self.sock = None
            messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к серверу {self.host}:{self.port}.")
            return False

    def send(self, data):
        if self.sock:
            try:
                self.sock.sendall(json.dumps(data).encode("utf-8") + b"\n")
            except Exception:
                self.close()

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None

class UILogger:
    """Observer для UI-лога."""
    def __init__(self, log_text):
        self.log_text = log_text

    def update(self, message):
        self.log_text.after(0, self._append_log, message)
        
    def _append_log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.yview_moveto(1)