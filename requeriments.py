import subprocess
import sys

def install_package(package):
    """Instalar paquete usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado correctamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando {package}: {e}")

# Lista de paquetes necesarios
packages = [
    # PyTorch (ajusta según tu configuración CUDA)
    "torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118",  # Para CUDA 11.8
    # Para CPU solamente, usa: "torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"
    
    # MONAI y dependencias relacionadas
    "monai[all]==1.4",
    "nibabel",
    
    
    # Augmentaciones y procesamiento de imágenes
    "opencv-python",
    "Pillow",
    
    # Visualización y plotting
    "matplotlib",
    "seaborn",
    "pyvista",
    
    # Utilidades y métricas
    "tqdm",
    "scikit-learn",
    "numpy",
    "pandas",
    
    
    # Jupyter y notebook utilities
    "ipywidgets",
    "jupyterlab",
]

print("🚀 Iniciando instalación de dependencias...")
print("=" * 50)

for package in packages:
    if package.startswith("torch"):
        # Instalación especial para PyTorch
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + package.split())
            print(f"✅ PyTorch instalado correctamente")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando PyTorch: {e}")
    else:
        install_package(package)