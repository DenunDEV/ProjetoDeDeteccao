import pyperclip
import time

class ClipboardSensor:
    def __init__(self, logger):
        self.logger = logger
        self.last_content = ""
        
    def start_monitoring(self, monitor):
        """Monitora clipboard enquanto monitor.is_monitoring = True"""
        try:
            self.last_content = pyperclip.paste()
        except:
            self.last_content = ""
        
        while monitor.is_monitoring:
            try:
                current_content = pyperclip.paste()
                
                if current_content != self.last_content and current_content != "":
                    action = "CÓPIA" if len(current_content) > len(self.last_content) else "COLAGEM"
                    preview = current_content[:100] + "..." if len(current_content) > 100 else current_content
                    
                    self.logger.log_event("CLIPBOARD", action, f"Conteúdo: {preview}", "ALERTA")
                    self.last_content = current_content
                    
            except:
                pass
            
            time.sleep(0.5)