import os
import pyzipper
import getpass

def extract_logs(zip_path, password, output_dir="logs_extraidos"):
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        with pyzipper.AESZipFile(zip_path, 'r', encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(password.encode('utf-8'))
            zf.extractall(output_dir)
            
        print(f"✅ Logs extraídos em: {os.path.abspath(output_dir)}")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("=" * 70)
    print("🔓 EXTRATOR DE LOGS - PROCTORING SYSTEM")
    print("=" * 70)
    
    zip_path = input("\n📁 Caminho do ZIP: ").strip().strip('"')
    
    if not os.path.exists(zip_path):
        print("❌ Arquivo não encontrado!")
        return
    
    password = getpass.getpass("🔑 Senha do ADM: ")
    
    print("\n🔄 Extraindo...")
    extract_logs(zip_path, password)
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()