"""
===============================================================================
MÓDULO: Sensor de Input
===============================================================================
"""

from pynput import keyboard, mouse
from datetime import datetime
import mss
import mss.tools
import os

class InputSensor:
    def __init__(self, logger, callback=None, monitor=None):
        self.logger = logger
        self.callback = callback
        self.monitor = monitor  # Referência ao monitor para chamar stop()
        self.keyboard_listener = None
        self.mouse_listener = None
        self.is_listening = False
        self.current_keys = set()
        
        self.suspicious_combinations = {
            frozenset({'ctrl', 'c'}): "COPIA (Ctrl+C)",
            frozenset({'ctrl', 'v'}): "COLA (Ctrl+V)",
            frozenset({'ctrl', 'x'}): "RECORTE (Ctrl+X)",
            frozenset({'ctrl', 'a'}): "SELECIONA_TUDO (Ctrl+A)",
            frozenset({'alt', 'tab'}): "TROCA_JANELA (Alt+Tab)",
            frozenset({'print_screen'}): "PRINT_SCREEN",
        }
        
        # Combinação de saída
        self.exit_combination = frozenset({'ctrl', 'alt', 'q'})
        
    def on_press(self, key):
        try:
            if hasattr(key, 'char'):
                key_name = key.char.lower()
            else:
                key_name = str(key).replace('Key.', '').lower()
            
            self.current_keys.add(key_name)
            
            # VERIFICAR COMBINAÇÃO DE SAÍDA (CTRL+ALT+Q)
            if self.exit_combination.issubset(self.current_keys):
                print("\n\n⏹️  CTRL+ALT+Q DETECTADO!")
                self.logger.log_event("SESSÃO", "FIM", "Usuário pressionou CTRL+ALT+Q", "INFO")
                if self.monitor:
                    self.monitor.stop_monitoring_from_sensor()
                return False  # Para o listener
            
            # Verificar combinações suspeitas
            self.check_suspicious_combination(key_name)
            
            # Detectar Print Screen
            if key_name == 'print_screen':
                self.handle_print_screen()
                
        except Exception as e:
            self.logger.log_event("ERRO", "INPUT_SENSOR", str(e), "ERROR")
    
    def on_release(self, key):
        try:
            if hasattr(key, 'char'):
                key_name = key.char.lower()
            else:
                key_name = str(key).replace('Key.', '').lower()
            self.current_keys.discard(key_name)
        except:
            pass
    
    def check_suspicious_combination(self, current_key):
        for combination, description in self.suspicious_combinations.items():
            if combination.issubset(self.current_keys):
                self.logger.log_event("TECLADO", description, f"Combinação: {', '.join(combination)}", "ALERTA")
                if self.callback:
                    self.callback("COMBINAÇÃO_TECLAS", description)
                break
    
    def handle_print_screen(self):
        """Captura screenshot usando MSS"""
        try:
            os.makedirs("screenshots", exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"print_{timestamp}.png"
            screenshot_path = os.path.join("screenshots", filename)
            
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_path)
            
            if os.path.exists(screenshot_path):
                file_size = os.path.getsize(screenshot_path)
                self.logger.log_event(
                    "SCREENSHOT",
                    "PRINT_SCREEN_DETECTADO",
                    f"Arquivo: {filename} ({file_size} bytes)",
                    "ALERTA"
                )
                print(f"📸 Screenshot: {filename}")
            else:
                raise Exception("Arquivo não criado")
            
        except Exception as e:
            self.logger.log_event("ERRO", "SCREENSHOT_FAIL", str(e), "ERROR")
            print(f"❌ Erro screenshot: {e}")
    
    def on_mouse_click(self, x, y, button, pressed):
        if pressed:
            self.logger.log_event("MOUSE", f"CLIQUE_{button.name.upper()}", f"Posição: ({x}, {y})", "INFO")
    
    def start_listening(self):
        self.is_listening = True
        
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.keyboard_listener.start()
        
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.mouse_listener.start()
        
        self.keyboard_listener.join()
        self.mouse_listener.join()
    
    def stop_listening(self):
        self.is_listening = False
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()