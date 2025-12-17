# timer_utils.py
import threading
import time

class WorkoutTimer:
    def __init__(self, callback):
        self.callback = callback
        self.seconds = 0
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def _run(self):
        while self.running:
            mins, secs = divmod(self.seconds, 60)
            time_str = f"{mins:02d}:{secs:02d}"
            self.callback(time_str)
            time.sleep(1)
            self.seconds += 1

    def stop(self):
        self.running = False
        self.seconds = 0

    def pause(self):
        self.running = False