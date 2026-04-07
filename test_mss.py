"""Teste de screenshot com MSS (sem Pillow)"""
import mss
import mss.tools
import os
from datetime import datetime

print("=" * 60)
print("TESTE MSS - CAPTURA DE TELA")
print("=" * 60)

try:
    # Criar pasta
    os.makedirs("test_mss", exist_ok=True)
    
    # Capturar
    print("\n📸 Capturando tela com MSS...")
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Monitor principal
        screenshot = sct.grab(monitor)
        
        # Salvar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_mss_{timestamp}.png"
        path = os.path.join("test_mss", filename)
        
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=path)
    
    # Verificar
    if os.path.exists(path):
        tamanho = os.path.getsize(path)
        print(f"\n✅ SUCESSO!")
        print(f"📁 Arquivo: {path}")
        print(f"📦 Tamanho: {tamanho} bytes")
        print(f"\nAbra a pasta 'test_mss' e verifique a imagem!")
    else:
        print("\n❌ FALHA: Arquivo não foi criado!")
        
except Exception as e:
    print(f"\n❌ ERRO: {e}")

print("=" * 60)
input("\nPressione Enter para sair...")