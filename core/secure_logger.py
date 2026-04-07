"""
===============================================================================
DESCRIÇÃO: Salva logs e screenshots em ZIP criptografado com AES-256.
           WinRAR/7-Zip solicitarão senha para abrir.
===============================================================================
"""

import os
import pyzipper
from datetime import datetime
from collections import defaultdict

class SecureLogger:
    """
    Gerencia o registro de eventos e salva tudo em um arquivo ZIP 
    protegido por senha com criptografia AES-256.
    """
    
    def __init__(self, session_id, password, log_dir="secure_logs"):
        self.session_id = session_id
        self.password = password.encode('utf-8')
        self.log_dir = log_dir
        self.buffer = []
        self.event_counts = defaultdict(int)
        
        # Criar diretório
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Nome do arquivo ZIP
        timestamp_safe = session_id.replace(":", "-")
        self.zip_filename = os.path.join(
            self.log_dir,
            f"proctor_logs_{timestamp_safe}.zip"
        )
        
        # Nome do arquivo de log interno
        self.internal_log_file = f"proctor_log_{timestamp_safe}.txt"
        
        # Escrever cabeçalho
        self._write_header()
    
    def _write_header(self):
        """Escreve o cabeçalho informativo no início do log"""
        header = f"""================================================================================
LOG DE MONITORAMENTO - SISTEMA DE PROCTORING
================================================================================
Session ID: {self.session_id}
Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Sistema: Monitoramento de Integridade Acadêmica
PROTEGIDO COM CRIPTOGRAFIA AES-256
================================================================================

LEGENDA DE SEVERIDADE:
  [INFO]   - Informação normal de operação
  [ALERTA] - Ação suspeita detectada
  [ERROR]  - Erro no sistema

================================================================================

"""
        self.buffer.append(header)
    
    def log_event(self, category, event_type, details, severity="INFO"):
        """
        Registra um evento no buffer de memória.
        
        Args:
            category: Categoria (TECLADO, MOUSE, CLIPBOARD, SCREENSHOT, etc)
            event_type: Tipo do evento
            details: Detalhes descritivos
            severity: Nível de severidade (INFO, ALERTA, ERROR)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] [{severity:6}] [{category:12}] {event_type}: {details}\n"
        self.buffer.append(log_entry)
        self.event_counts[f"{category}_{severity}"] += 1
    
    def save_and_encrypt(self, summary_data=None, screenshots_list=None):
        """
        Finaliza o log, adiciona resumo e screenshots, e salva em ZIP criptografado.
        """
        # =========================================================================
        # 1. ADICIONAR RESUMO FINAL AO LOG
        # =========================================================================
        # ⚠️ ATENÇÃO: Esta linha deve ser "if summary_data:" NÃO "if summary_"
        if summary_data:
            summary = f"""
================================================================================
RESUMO DA SESSÃO
================================================================================
Término: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

CONTAGEM DE EVENTOS:
"""
            for event_type, count in summary_data.items():
                summary += f"  - {event_type}: {count}\n"
            
            total_events = sum(summary_data.values())
            summary += f"\nTOTAL DE EVENTOS: {total_events}\n"
            
            if screenshots_list and len(screenshots_list) > 0:
                summary += f"SCREENSHOTS ANEXADOS: {len(screenshots_list)}\n"
            
            summary += "=" * 80 + "\n"
            self.buffer.append(summary)
        
        # =========================================================================
        # 2. CONVERTER LOG PARA BYTES
        # =========================================================================
        log_content = "".join(self.buffer).encode('utf-8')
        
        # =========================================================================
        # 3. CRIAR ZIP COM CRIPTOGRAFIA AES-256
        # =========================================================================
        try:
            with pyzipper.AESZipFile(
                self.zip_filename,
                'w',
                compression=pyzipper.ZIP_LZMA,
                encryption=pyzipper.WZ_AES
            ) as zf:
                zf.setpassword(self.password)
                zf.writestr(self.internal_log_file, log_content)
                
                if screenshots_list and len(screenshots_list) > 0:
                    for img_path in screenshots_list:
                        if os.path.exists(img_path):
                            arcname = os.path.join("screenshots", os.path.basename(img_path))
                            zf.write(img_path, arcname, compress_type=pyzipper.ZIP_DEFLATED)
            
            print(f"\n🔒 ZIP criado: {os.path.abspath(self.zip_filename)}")
            
        except Exception as e:
            print(f"\n❌ ERRO: {e}")
            import traceback
            traceback.print_exc()
        
        return self.zip_filename
    
    def get_log_content(self):
        """Retorna o conteúdo atual do log em string"""
        return "".join(self.buffer)