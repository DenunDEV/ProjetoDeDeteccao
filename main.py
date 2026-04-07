"""
===============================================================================
PROJETO: Sistema de Proctoring v0.3
DEVELOPER: Denun
CONTROLE: Botão Iniciar/Parar + Salvamento Automático
===============================================================================
"""

import sys
import os
from datetime import datetime

# ============================================================================
# VERIFICAÇÃO DE DEPENDÊNCIAS
# ============================================================================

def verificar_dependencias():
    dependencias = ['mss', 'pyzipper', 'pynput', 'pyperclip', 'psutil', 'pygetwindow']
    faltando = []
    
    for modulo in dependencias:
        try:
            __import__(modulo)
        except ImportError:
            faltando.append(modulo)
    
    if faltando:
        print("=" * 70)
        print("❌ DEPENDÊNCIAS FALTANDO")
        print("=" * 70)
        print(f"\nExecute: pip install {' '.join(faltando)}")
        print("Ou: instalar.bat")
        print("=" * 70)
        input("Pressione Enter para sair...")
        sys.exit(1)

verificar_dependencias()

# ============================================================================
# IMPORTAÇÕES
# ============================================================================

from core.monitor import ProctoringMonitor
from indicators.visual_indicator import VisualIndicator

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    print("=" * 70)
    print("🔒 SISTEMA DE PROCTORING v0.3")
    print("=" * 70)
    print(f"⏰ Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 70)
    
    # Criar diretórios
    os.makedirs("logs", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("secure_logs", exist_ok=True)
    
    # Inicializar monitor
    print("\n📦 Inicializando sistema...")
    monitor = ProctoringMonitor()
    
    # Inicializar interface (COM REFERÊNCIA AO MONITOR)
    print("🎨 Iniciando interface visual...")
    indicador = VisualIndicator(monitor=monitor)
    
    # Iniciar interface (bloqueante - controla todo o ciclo de vida)
    indicador.start()
    
    # Quando a interface fecha, chega aqui
    print("\n" + "=" * 70)
    print("✅ SISTEMA FINALIZADO")
    print("=" * 70)
    print(f"📁 Logs em: {os.path.abspath('secure_logs')}")
    print("🔑 Use a senha do ADM para abrir o ZIP")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrompido pelo usuário")
    except Exception as e:
        print(f"\n\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nPressione Enter para sair...")