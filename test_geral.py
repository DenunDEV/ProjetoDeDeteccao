"""Teste geral de todas as dependências"""
import sys

print("=" * 70)
print("TESTE GERAL DE DEPENDÊNCIAS - PROCTORING v0.3")
print("=" * 70)
print(f"Python: {sys.version}")
print(f"Caminho: {sys.executable}")
print()

dependencias = {
    'mss': 'Captura de tela',
    'pyzipper': 'ZIP criptografado',
    'pynput': 'Teclado e mouse',
    'pyperclip': 'Clipboard',
    'psutil': 'Sistema',
    'pygetwindow': 'Janelas'
}

print("Verificando módulos:\n")

todas_ok = True

for modulo, descricao in dependencias.items():
    try:
        __import__(modulo)
        print(f"✅ {modulo:<15} - {descricao}")
    except ImportError:
        print(f"❌ {modulo:<15} - {descricao}")
        todas_ok = False

print()
print("=" * 70)

if todas_ok:
    print("🎉 TODAS AS DEPENDÊNCIAS INSTALADAS!")
    print("=" * 70)
    print("\n✅ Você pode executar: python main.py")
else:
    print("⚠️  ALGUMAS DEPENDÊNCIAS FALTANDO!")
    print("=" * 70)
    print("\nExecute: python -m pip install mss pyzipper pynput pyperclip psutil pygetwindow")

print("=" * 70)
input("\nPressione Enter para sair...")