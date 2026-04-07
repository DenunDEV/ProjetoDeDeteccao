import os
import sys
import threading
import time
import json
from datetime import datetime

# ============================================================================
# IMPORTAÇÕES from
# ============================================================================

try:
    from sensors.input_sensor import InputSensor
    from sensors.window_sensor import WindowSensor
    from sensors.clipboard_sensor import ClipboardSensor
    from core.secure_logger import SecureLogger
except ImportError as e:
    print(f"\n❌ ERRO DE IMPORTAÇÃO: {e}")
    print("\nExecute: pip install mss pyzipper pycryptodomex pynput pyperclip psutil pygetwindow")
    input("\nPressione Enter para sair...")
    sys.exit(1)

# ============================================================================
# CLASSE PRINCIPAL
# ============================================================================

class ProctoringMonitor:
    """
    Gerencia o monitoramento com controle via botão da interface.
    """
    
    def __init__(self, admin_password=None):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.is_monitoring = False
        self.monitoring_started = False
        
        # Carregar senha
        if admin_password:
            self.password = admin_password
        else:
            config_path = os.path.join("config", "security_config.json")
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.password = config.get("admin_password", "SenhaPadrao123!")
            except:
                self.password = "SenhaPadrao123!"
        
        # Inicializar logger
        self.logger = SecureLogger(self.session_id, self.password)
        
        # Inicializar sensores (mas não iniciar ainda)
        self.input_sensor = InputSensor(self.logger, self.on_suspicious_action, self)
        self.window_sensor = WindowSensor(self.logger)
        self.clipboard_sensor = ClipboardSensor(self.logger)
        
        self.threads = []
        self.screenshots_list = []
        
        print(f"✅ Monitor inicializado (Session: {self.session_id})")
    
    def on_suspicious_action(self, action_type, details):
        print(f"⚠️ AÇÃO SUSPEITA: {action_type}")
    
    def start_monitoring(self):
        """
        Inicia o monitoramento (chamado pelo botão da interface).
        """
        if self.monitoring_started:
            print("⚠️  Monitoramento já está ativo!")
            return
        
        print("\n" + "=" * 60)
        print("🚀 INICIANDO MONITORAMENTO...")
        print("=" * 60)
        
        self.is_monitoring = True
        self.monitoring_started = True
        self._cleanup_old_screenshots()
        
        # Registrar início
        self.logger.log_event("SESSÃO", "INÍCIO", f"Session ID: {self.session_id}", "INFO")
        
        # Thread 1: Input
        t_input = threading.Thread(target=self.input_sensor.start_listening, daemon=True)
        t_input.start()
        self.threads.append(t_input)
        
        # Thread 2: Janela
        t_window = threading.Thread(
            target=self.window_sensor.start_monitoring,
            args=(self,),
            daemon=True
        )
        t_window.start()
        self.threads.append(t_window)
        
        # Thread 3: Clipboard
        t_clipboard = threading.Thread(
            target=self.clipboard_sensor.start_monitoring,
            args=(self,),
            daemon=True
        )
        t_clipboard.start()
        self.threads.append(t_clipboard)
        
        print("✅ Sensores ATIVOS")
        print("💡 Clique em 'PARAR MONITORAMENTO' para salvar os logs")
        print("=" * 60)
    
    def stop_monitoring(self):
        """
        Para o monitoramento e SALVA OS LOGS NO ZIP.
        Chamado pelo botão ou ao fechar a janela.
        """
        print("\n" + "=" * 70)
        print("⏹️ PARANDO MONITORAMENTO E SALVANDO LOGS...")
        print("=" * 70)
        
        self.is_monitoring = False
        
        # 1. Parar sensores
        print("\n[1/6] Parando sensores...")
        try:
            self.input_sensor.stop_listening()
            print("   ✅ Sensores parados")
        except Exception as e:
            print(f"   ⚠️ Erro: {e}")
        
        # 2. Aguardar threads
        print("\n[2/6] Aguardando threads...")
        for thread in self.threads:
            thread.join(timeout=2)
        print("   ✅ Threads finalizadas")
        
        # 3. Coletar screenshots
        print("\n[3/6] Coletando screenshots...")
        self.screenshots_list = []
        screenshots_dir = "screenshots"
        
        if os.path.exists(screenshots_dir):
            arquivos = os.listdir(screenshots_dir)
            arquivos.sort()
            for f in arquivos:
                if f.lower().endswith('.png'):
                    self.screenshots_list.append(os.path.join(screenshots_dir, f))
            print(f"   📸 {len(self.screenshots_list)} screenshot(s) encontrado(s)")
        else:
            print("   ⚠️ Pasta screenshots não existe")
        
        # 4. Verificar logger
        print("\n[4/6] Verificando logger...")
        print(f"   📊 Eventos registrados: {len(self.logger.buffer)}")
        print(f"   📊 Contagem: {dict(self.logger.event_counts)}")
        
        # 5. SALVAR ZIP ← PASSO CRÍTICO!
        print("\n[5/6] Criando ZIP criptografado com senha...")
        print("   🔄 Chamando save_and_encrypt()...")
        
        try:
            resultado = self.logger.save_and_encrypt(
                summary_data=dict(self.logger.event_counts),
                screenshots_list=self.screenshots_list
            )
            print(f"   ✅ ZIP CRIADO: {os.path.abspath(resultado)}")
        except Exception as e:
            print(f"   ❌ ERRO AO SALVAR: {e}")
            import traceback
            traceback.print_exc()
        
        # 6. Verificar arquivo
        print("\n[6/6] Verificando arquivo final...")
        if os.path.exists(self.logger.zip_filename):
            tamanho = os.path.getsize(self.logger.zip_filename)
            print(f"   ✅ SUCESSO! Arquivo: {tamanho / 1024:.2f} KB")
            print(f"   📁 Local: {os.path.abspath(self.logger.zip_filename)}")
            print(f"   🔑 Senha necessária para abrir")
        else:
            print(f"   ❌ ARQUIVO NÃO FOI CRIADO!")
        
        print("\n" + "=" * 70)
        print("✅ LOGS SALVOS COM SUCESSO!")
        print("=" * 70)
        print(f"\n📁 Verifique a pasta: secure_logs/")
        print("🔑 Use a senha do administrador para abrir o ZIP")
        print("=" * 70)
    
    def set_target_window(self, window_name):
        self.target_window = window_name
        self.window_sensor.set_target_window(window_name)
    
    def _cleanup_old_screenshots(self):
        screenshots_dir = "screenshots"
        if os.path.exists(screenshots_dir):
            count = 0
            for f in os.listdir(screenshots_dir):
                if f.endswith('.png'):
                    try:
                        os.remove(os.path.join(screenshots_dir, f))
                        count += 1
                    except:
                        pass
            if count > 0:
                print(f"🧹 {count} screenshot(s) antigo(s) removido(s).")