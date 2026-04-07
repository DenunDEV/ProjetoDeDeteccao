"""
Teste para verificar se o ZIP está realmente protegido por senha
"""

import os
import pyzipper
from datetime import datetime

print("=" * 70)
print("🔐 TESTE DE PROTEÇÃO ZIP - PROCTORING SYSTEM")
print("=" * 70)

# Criar um ZIP de teste
senha_teste = b"piaoliang"
zip_teste = "test_protecao.zip"

print(f"\n📝 Criando ZIP de teste com senha...")

try:
    with pyzipper.AESZipFile(
        zip_teste,
        'w',
        compression=pyzipper.ZIP_LZMA,
        encryption=pyzipper.WZ_AES
    ) as zf:
        zf.setpassword(senha_teste)
        zf.writestr("teste.txt", "Conteúdo secreto do Proctoring System v0.3")
    
    print(f"✅ ZIP criado: {zip_teste}")
    print(f"🔑 Senha: {'*' * len(senha_teste)}")
    
    # Tentar abrir SEM senha (deve falhar)
    print(f"\n🔍 Testando abertura SEM senha...")
    try:
        with pyzipper.AESZipFile(zip_teste, 'r') as zf:
            zf.setpassword(b"SenhaErrada")
            zf.read("teste.txt")
        print("❌ FALHA: ZIP abriu sem senha correta!")
    except:
        print("✅ SUCESSO: ZIP bloqueado sem senha correta!")
    
    # Tentar abrir COM senha (deve funcionar)
    print(f"\n🔍 Testando abertura COM senha correta...")
    try:
        with pyzipper.AESZipFile(zip_teste, 'r') as zf:
            zf.setpassword(senha_teste)
            conteudo = zf.read("teste.txt")
        print(f"✅ SUCESSO: ZIP abriu com senha correta!")
        print(f"   Conteúdo: {conteudo.decode('utf-8')}")
    except Exception as e:
        print(f"❌ FALHA: {e}")
    
    print("\n" + "=" * 70)
    print("📁 Agora tente abrir este arquivo no WinRAR/7-Zip:")
    print(f"   {os.path.abspath(zip_teste)}")
    print("\n   Ele DEVE pedir senha!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    print("💡 Verifique: pip install pyzipper pycryptodomex")

input("\nPressione Enter para sair...")