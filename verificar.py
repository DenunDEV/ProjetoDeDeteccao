"""
===============================================================================
VERIFICADOR DE DEPENDÊNCIAS E ESTRUTURA - PROCTORING SYSTEM v0.3
===============================================================================
DESCRIÇÃO: Verifica se todas as dependências estão instaladas e se a 
           estrutura do projeto está correta para execução.
VERSÃO: 0.3
===============================================================================
"""

import sys
import subprocess
import os
from datetime import datetime

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

CORES = {
    'verde': '\033[92m',
    'vermelho': '\033[91m',
    'amarelo': '\033[93m',
    'azul': '\033[94m',
    'reset': '\033[0m',
    'negrito': '\033[1m'
}

DEPENDENCIAS = {
    # Captura de Tela
    'mss': 'Captura de screenshots (substitui Pillow/pyautogui)',
    
    # Segurança
    'pyzipper': 'ZIP criptografado com senha',
    'pycryptodomex': 'Criptografia AES para pyzipper',
    
    # Monitoramento
    'pynput': 'Hook de teclado e mouse',
    'pyperclip': 'Acesso à área de transferência',
    'psutil': 'Monitoramento de processos e janelas',
    'pygetwindow': 'Detecção de janela ativa',
    
    # Rede e Utilitários
    'requests': 'Comunicação com API',
    'dateutil': 'Manipulação de datas (python-dateutil)'
}

PASTAS_NECESSARIAS = [
    'core',
    'sensors',
    'indicators',
    'config',
    'utils',
    'logs',
    'screenshots',
    'secure_logs',
    'keys'
]

ARQUIVOS_INIT = [
    'core/__init__.py',
    'sensors/__init__.py',
    'indicators/__init__.py',
    'config/__init__.py',
    'utils/__init__.py'
]

ARQUIVOS_CONFIG = [
    'config/security_config.json',
    'requirements.txt',
    'main.py',
    'instalar.bat'
]

# ============================================================================
# FUNÇÕES DE VERIFICAÇÃO
# ============================================================================

def imprimir_cabecalho():
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 80)
    print(f"{CORES['azul']}{CORES['negrito']}🔍 VERIFICADOR - PROCTORING SYSTEM v3.1{CORES['reset']}")
    print("=" * 80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 80 + "\n")

def verificar_python():
    """Verifica versão e caminho do Python"""
    print(f"{CORES['negrito']}📌 INFORMAÇÕES DO PYTHON{CORES['reset']}")
    print("-" * 80)
    
    print(f"Versão: {CORES['azul']}{sys.version}{CORES['reset']}")
    print(f"Caminho: {CORES['azul']}{sys.executable}{CORES['reset']}")
    print(f"Plataforma: {CORES['azul']}{sys.platform}{CORES['reset']}")
    print(f"Arquitetura: {CORES['azul']}{'64-bit' if sys.maxsize > 2**32 else '32-bit'}{CORES['reset']}")
    print()

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print(f"{CORES['negrito']}📦 VERIFICANDO DEPENDÊNCIAS{CORES['reset']}")
    print("-" * 80)
    print(f"{'Módulo':<20} {'Status':<15} {'Descrição'}")
    print("-" * 80)
    
    instalados = []
    faltando = []
    
    for modulo, descricao in DEPENDENCIAS.items():
        try:
            # Caso especial para dateutil (o import é differente do nome do pacote)
            if modulo == 'dateutil':
                __import__('dateutil')
            else:
                __import__(modulo)
            
            print(f"{CORES['verde']}✅{CORES['reset']} {modulo:<18} {CORES['verde']}{'INSTALADO':<15}{CORES['reset']} {descricao}")
            instalados.append(modulo)
        except ImportError:
            print(f"{CORES['vermelho']}❌{CORES['reset']} {modulo:<18} {CORES['vermelho']}{'FALTANDO':<15}{CORES['reset']} {descricao}")
            faltando.append(modulo)
    
    print("-" * 80)
    print(f"\nResumo: {CORES['azul']}{len(instalados)}/{len(DEPENDENCIAS)}{CORES['reset']} módulos instalados\n")
    
    return instalados, faltando

def verificar_pastas():
    """Verifica se todas as pastas necessárias existem"""
    print(f"{CORES['negrito']}📁 VERIFICANDO ESTRUTURA DE PASTAS{CORES['reset']}")
    print("-" * 80)
    
    pastas_ok = []
    pastas_faltando = []
    
    for pasta in PASTAS_NECESSARIAS:
        if os.path.exists(pasta):
            print(f"{CORES['verde']}✅{CORES['reset']} {pasta}/")
            pastas_ok.append(pasta)
        else:
            print(f"{CORES['vermelho']}❌{CORES['reset']} {pasta}/ {CORES['amarelo']}(criando...){CORES['reset']}")
            os.makedirs(pasta, exist_ok=True)
            pastas_faltando.append(pasta)
    
    print("-" * 80)
    
    if pastas_faltando:
        print(f"\n{CORES['amarelo']}⚠️  {len(pastas_faltando)} pasta(s) criada(s) automaticamente{CORES['reset']}\n")
    else:
        print(f"\n{CORES['verde']}✅ Todas as pastas existem{CORES['reset']}\n")
    
    return pastas_ok, pastas_faltando

def verificar_arquivos_init():
    """Verifica se todos os arquivos __init__.py existem"""
    print(f"{CORES['negrito']}📄 VERIFICANDO ARQUIVOS __init__.py{CORES['reset']}")
    print("-" * 80)
    
    arquivos_ok = []
    arquivos_faltando = []
    
    for arquivo in ARQUIVOS_INIT:
        if os.path.exists(arquivo):
            print(f"{CORES['verde']}✅{CORES['reset']} {arquivo}")
            arquivos_ok.append(arquivo)
        else:
            print(f"{CORES['vermelho']}❌{CORES['reset']} {arquivo} {CORES['amarelo']}(criando...){CORES['reset']}")
            # Criar diretório pai se não existir
            diretorio = os.path.dirname(arquivo)
            os.makedirs(diretorio, exist_ok=True)
            # Criar arquivo __init__.py
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(f"# Pacote: {diretorio}\n")
            arquivos_faltando.append(arquivo)
    
    print("-" * 80)
    
    if arquivos_faltando:
        print(f"\n{CORES['amarelo']}⚠️  {len(arquivos_faltando)} arquivo(s) criado(s) automaticamente{CORES['reset']}\n")
    else:
        print(f"\n{CORES['verde']}✅ Todos os arquivos __init__.py existem{CORES['reset']}\n")
    
    return arquivos_ok, arquivos_faltando

def verificar_arquivos_config():
    """Verifica se arquivos de configuração importantes existem"""
    print(f"{CORES['negrito']}⚙️  VERIFICANDO ARQUIVOS DE CONFIGURAÇÃO{CORES['reset']}")
    print("-" * 80)
    
    arquivos_ok = []
    arquivos_faltando = []
    
    for arquivo in ARQUIVOS_CONFIG:
        if os.path.exists(arquivo):
            print(f"{CORES['verde']}✅{CORES['reset']} {arquivo}")
            arquivos_ok.append(arquivo)
        else:
            print(f"{CORES['vermelho']}❌{CORES['reset']} {arquivo} {CORES['amarelo']}(FALTANDO){CORES['reset']}")
            arquivos_faltando.append(arquivo)
    
    print("-" * 80)
    
    # Verificar senha padrão no security_config.json
    if os.path.exists('config/security_config.json'):
        try:
            import json
            with open('config/security_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                senha = config.get('admin_password', '')
                if senha == 'MudeEstaSenha123!':
                    print(f"\n{CORES['amarelo']}⚠️  ATENÇÃO: Senha padrão ainda está em uso!{CORES['reset']}")
                    print(f"   Edite config/security_config.json e mude a senha antes de usar.")
        except:
            pass
    
    print()
    return arquivos_ok, arquivos_faltando

def verificar_testes():
    """Verifica se arquivos de teste existem"""
    print(f"{CORES['negrito']}🧪 VERIFICANDO ARQUIVOS DE TESTE{CORES['reset']}")
    print("-" * 80)
    
    testes = ['test_geral.py', 'test_mss.py']
    
    for teste in testes:
        if os.path.exists(teste):
            print(f"{CORES['verde']}✅{CORES['reset']} {teste}")
        else:
            print(f"{CORES['amarelo']}⚠️{CORES['reset']} {teste} {CORES['amarelo']}(opcional){CORES['reset']}")
    
    print("-" * 80)
    print()

def oferecer_instalacao(faltando):
    """Oferece instalar dependências faltando"""
    if not faltando:
        return
    
    print("=" * 80)
    print(f"{CORES['vermelho']}{CORES['negrito']}⚠️  DEPENDÊNCIAS FALTANDO: {len(faltando)}{CORES['reset']}")
    print("=" * 80)
    print(f"\nMódulos faltando: {CORES['vermelho']}{', '.join(faltando)}{CORES['reset']}\n")
    
    # Mapear nomes corretos para pip install
    mapeamento_pip = {
        'dateutil': 'python-dateutil'
    }
    
    pacotes_pip = [mapeamento_pip.get(pkg, pkg) for pkg in faltando]
    
    print("-" * 80)
    print("COMANDO PARA INSTALAR:")
    print("-" * 80)
    print(f"{CORES['azul']}pip install {' '.join(pacotes_pip)}{CORES['reset']}")
    print("-" * 80)
    print()
    
    resposta = input(f"{CORES['negrito']}Deseja instalar automaticamente agora? (s/n): {CORES['reset']}").strip().lower()
    
    if resposta == 's':
        print(f"\n{CORES['azul']}📦 Instalando dependências faltantes...{CORES['reset']}\n")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + pacotes_pip)
            print(f"\n{CORES['verde']}✅ Instalação concluída!{CORES['reset']}")
            print("\nExecute verificar.py novamente para confirmar.")
        except Exception as e:
            print(f"\n{CORES['vermelho']}❌ Erro na instalação: {e}{CORES['reset']}")
            print("\nTente executar como Administrador ou use:")
            print(f"  pip install --user {' '.join(pacotes_pip)}")
    else:
        print(f"\n{CORES['amarelo']}Instale manualmente com o comando acima.{CORES['reset']}")

def imprimir_resumo(instalados, faltando, pastas_faltando, arquivos_faltando):
    """Imprime resumo final da verificação"""
    print("\n" + "=" * 80)
    print(f"{CORES['negrito']}📊 RESUMO DA VERIFICAÇÃO{CORES['reset']}")
    print("=" * 80)
    
    # Dependências
    if not faltando:
        print(f"{CORES['verde']}✅ Todas as dependências instaladas ({len(instalados)}/{len(DEPENDENCIAS)}){CORES['reset']}")
    else:
        print(f"{CORES['vermelho']}❌ {len(faltando)} dependência(s) faltando ({len(instalados)}/{len(DEPENDENCIAS)}){CORES['reset']}")
    
    # Pastas
    if not pastas_faltando:
        print(f"{CORES['verde']}✅ Todas as pastas existem{CORES['reset']}")
    else:
        print(f"{CORES['amarelo']}⚠️  {len(pastas_faltando)} pasta(s) criada(s) automaticamente{CORES['reset']}")
    
    # Arquivos __init__.py
    if not arquivos_faltando:
        print(f"{CORES['verde']}✅ Todos os arquivos __init__.py existem{CORES['reset']}")
    else:
        print(f"{CORES['amarelo']}⚠️  {len(arquivos_faltando)} arquivo(s) __init__.py criado(s){CORES['reset']}")
    
    print("=" * 80)
    
    # Status final
    if not faltando:
        print(f"\n{CORES['verde']}{CORES['negrito']}🎉 SISTEMA PRONTO PARA USO!{CORES['reset']}")
        print(f"\n{CORES['azul']}Próximos passos:{CORES['reset']}")
        print(f"  1. Edite config/security_config.json e mude a senha")
        print(f"  2. Execute: python main.py")
    else:
        print(f"\n{CORES['amarelo']}⚠️  SISTEMA NÃO ESTÁ PRONTO - INSTALE AS DEPENDÊNCIAS{CORES['reset']}")
        print(f"\n{CORES['azul']}Próximos passos:{CORES['reset']}")
        print(f"  1. Execute: pip install {' '.join([p for p in faltando])}")
        print(f"  2. Execute verificar.py novamente")
    
    print("\n" + "=" * 80)

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal do verificador"""
    try:
        # Cabeçalho
        imprimir_cabecalho()
        
        # Verificações
        verificar_python()
        instalados, faltando = verificar_dependencias()
        pastas_ok, pastas_faltando = verificar_pastas()
        arquivos_init_ok, arquivos_init_faltando = verificar_arquivos_init()
        arquivos_config_ok, arquivos_config_faltando = verificar_arquivos_config()
        verificar_testes()
        
        # Oferecer instalação se faltar algo
        if faltando:
            oferecer_instalacao(faltando)
        
        # Resumo final
        imprimir_resumo(instalados, faltando, pastas_faltando, arquivos_init_faltando)
        
    except KeyboardInterrupt:
        print(f"\n\n{CORES['amarelo']}⏹️  Verificação interrompida pelo usuário{CORES['reset']}")
    except Exception as e:
        print(f"\n{CORES['vermelho']}❌ ERRO CRÍTICO: {e}{CORES['reset']}")
        print("\nTente executar como Administrador.")
    
    finally:
        input(f"\n{CORES['negrito']}Pressione Enter para sair...{CORES['reset']}")

if __name__ == "__main__":
    main()