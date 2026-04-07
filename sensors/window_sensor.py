"""
===============================================================================
MÓDULO: Sensor de Janela
===============================================================================
"""

import pygetwindow as gw
import time

class WindowSensor:
    def __init__(self, logger):
        self.logger = logger
        self.last_window = None
        self.target_window = None
        
    def set_target_window(self, window_name):
        self.target_window = window_name
        
    def start_monitoring(self, monitor):
        """Monitora janelas enquanto monitor.is_monitoring = True"""
        while monitor.is_monitoring:
            try:
                active_window = gw.getActiveWindow()
                
                if active_window:
                    current_window = active_window.title
                    
                    if current_window != self.last_window:
                        self.logger.log_event(
                            "JANELA",
                            "MUDANÇA_FOCO",
                            f"Para: '{current_window}'",
                            "ALERTA"
                        )
                        
                        if self.target_window and self.target_window.lower() not in current_window.lower():
                            self.logger.log_event(
                                "JANELA",
                                "SAIU_JANELA_ALVO",
                                f"Janela: {current_window}",
                                "ALERTA"
                            )
                        
                        self.last_window = current_window
                        
            except:
                pass
            
            time.sleep(1)