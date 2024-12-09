import pyttsx3
import threading
import time

class TTSSystem:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)    # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        self.last_warning = None
        self.is_speaking = False
        self.last_speak_time = 0
        self.speak_buffer = 5  # 5 second buffer between speeches
        
    def speak(self, text):
        current_time = time.time()
        
        # Don't repeat the same warning or speak if not enough time has passed
        if (text == self.last_warning or 
            current_time - self.last_speak_time < self.speak_buffer):
            return
            
        self.last_warning = text
        self.last_speak_time = current_time
        
        # Run speech in a separate thread to avoid blocking the game
        def speak_thread():
            self.is_speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
            self.is_speaking = False
            
        if not self.is_speaking:
            thread = threading.Thread(target=speak_thread)
            thread.start() 