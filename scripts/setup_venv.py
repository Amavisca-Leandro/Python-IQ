"""
Script para configurar o ambiente virtual Python.
Automatiza a criação do venv e instalação de dependências.
"""
import os
import sys
import subprocess
import platform
from pathlib import Path


def get_python_command():
    """Retorna o comando Python apropriado para o sistema operacional."""
    if platform.system() == "Windows":
        return "python"
    return "python3"


def get_venv_activate_command():
    """Retorna o comando para ativar o venv baseado no SO."""
    if platform.system() == "Windows":
        return r"venv\Scripts\activate"
    return "source venv/bin/activate"


def check_python_version():
    """Verifica se a versão do Python é 3.11 ou superior."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"❌ Python 3.11+ é necessário. Versão atual: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True


def create_virtual_environment():
    """Cria o ambiente virtual."""
    print("\n📦 Criando ambiente virtual...")
    python_cmd = get_python_command()
    
    try:
        subprocess.run([python_cmd, "-m", "venv", "venv"], check=True)
        print("✅ Ambiente virtual criado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar ambiente virtual: {e}")
        return False


def get_pip_command():
    """Retorna o caminho do pip no venv."""
    if platform.system() == "Windows":
        return r"venv\Scripts\pip.exe"
    return "venv/bin/pip"


def install_dependencies():
    """Instala as dependências do requirements.txt."""
    print("\n📥 Instalando dependências...")
    pip_cmd = get_pip_command()
    
    if not Path("requirements.txt").exists():
        print("⚠️  requirements.txt não encontrado. Pulando instalação de dependências.")
        return True
    
    try:
        # Upgrade pip primeiro
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        
        # Instalar dependências
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False


def install_playwright_browsers():
    """Instala os browsers do Playwright."""
    print("\n🌐 Instalando browsers do Playwright...")
    
    playwright_cmd = get_pip_command().replace("pip", "playwright")
    
    try:
        subprocess.run([playwright_cmd, "install"], check=True)
        print("✅ Browsers do Playwright instalados com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print("⚠️  Erro ao instalar browsers do Playwright (pode ser instalado depois)")
        print(f"   Execute manualmente: playwright install")
        return True  # Não falha o setup por causa disso


def create_env_file():
    """Cria o arquivo .env se não existir."""
    if Path(".env").exists():
        print("\n✅ Arquivo .env já existe")
        return
    
    if not Path(".env.example").exists():
        print("\n⚠️  .env.example não encontrado. Pulando criação do .env")
        return
    
    print("\n📝 Criando arquivo .env...")
    try:
        with open(".env.example", "r") as source:
            content = source.read()
        
        with open(".env", "w") as target:
            target.write(content)
        
        print("✅ Arquivo .env criado. Configure suas variáveis de ambiente!")
    except Exception as e:
        print(f"⚠️  Erro ao criar .env: {e}")


def print_next_steps():
    """Imprime os próximos passos para o usuário."""
    activate_cmd = get_venv_activate_command()
    
    print("\n" + "="*60)
    print("🎉 Setup concluído com sucesso!")
    print("="*60)
    print("\n📋 Próximos passos:")
    print(f"\n1. Ative o ambiente virtual:")
    print(f"   {activate_cmd}")
    print("\n2. Configure o arquivo .env com suas credenciais")
    print("\n3. Execute os testes:")
    print("   pytest")
    print("\n4. Gere relatórios Allure:")
    print("   pytest --alluredir=allure-results")
    print("   allure serve allure-results")
    print("\n" + "="*60)


def main():
    """Função principal."""
    print("="*60)
    print("🚀 Setup do Framework de Automação de Testes Python")
    print("="*60)
    
    # Verificar versão do Python
    if not check_python_version():
        sys.exit(1)
    
    # Criar ambiente virtual
    if not create_virtual_environment():
        sys.exit(1)
    
    # Instalar dependências
    if not install_dependencies():
        sys.exit(1)
    
    # Instalar browsers do Playwright
    install_playwright_browsers()
    
    # Criar arquivo .env
    create_env_file()
    
    # Imprimir próximos passos
    print_next_steps()


if __name__ == "__main__":
    main()
