"""
Teste DIRETO de criação de ZIP em secure_logs/
"""

import os
import pyzipper
from datetime import datetime

print("=" * 70)
print("🔐 TESTE DIRETO - CRIAÇÃO DE ZIP EM secure_logs/")
print("=" * 70)

# 1. Criar pasta secure_logs
print("\n[1/4] Criando pasta secure_logs/...")
os.makedirs("secure_logs", exist_ok=True)
print(f"✅ Pasta criada: {os.path.abspath('secure_logs')}")

# 2. Definir senha e caminho
print("\n[2/4] Configurando senha e caminho...")
senha = b"SenhaTeste123!"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
zip_path = os.path.join("secure_logs", f"teste_{timestamp}.zip")
print(f"📁 Caminho do ZIP: {zip_path}")

# 3. Criar conteúdo de teste
print("\n[3/4] Criando conteúdo de teste...")
conteudo_log = f"""================================================================================
LOG DE TESTE
================================================================================
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Status: Teste de criação de ZIP
================================================================================

[2026-04-01 14:00:00.000] [INFO   ] [SESSÃO       ] INÍCIO DO TESTE
[2026-04-01 14:00:01.000] [ALERTA ] [TECLADO     ] COPIA (Ctrl+C)
[2026-04-01 14:00:02.000] [ALERTA ] [SCREENSHOT  ] PRINT_SCREEN_DETECTADO
[2026-04-01 14:00:03.000] [INFO   ] [SESSÃO       ] FIM DO TESTE

================================================================================
"""
conteudo_bytes = conteudo_log.encode('utf-8')

# 4. Criar ZIP criptografado
print("\n[4/4] Criando ZIP criptografado...")

try:
    with pyzipper.AESZipFile(
        zip_path,
        'w',
        compression=pyzipper.ZIP_LZMA,
        encryption=pyzipper.WZ_AES
    ) as zf:
        zf.setpassword(senha)
        zf.writestr("teste_log.txt", conteudo_bytes)
    
    print(f"\n✅ SUCESSO! ZIP criado em: {os.path.abspath(zip_path)}")
    print(f"📦 Tamanho: {os.path.getsize(zip_path) / 1024:.2f} KB")
    print(f"🔑 Senha: {'*' * len(senha)}")
    
    print("\n" + "=" * 70)
    print("📁 AGORA VERIFIQUE MANUALMENTE:")
    print("=" * 70)
    print(f"1. Abra o Explorer em: {os.path.abspath('secure_logs')}")
    print(f"2. Você deve ver o arquivo: teste_{timestamp}.zip")
    print(f"3. Tente abrir com WinRAR/7-Zip - DEVE pedir senha!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ ERRO CRÍTICO: {e}")
    print("\nPossíveis causas:")
    print("  1. pyzipper não instalado: pip install pyzipper pycryptodomex")
    print("  2. Sem permissão de escrita na pasta")
    print("  3. Antivírus bloqueando")

input("\nPressione Enter para sair...")