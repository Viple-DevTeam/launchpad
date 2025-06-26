# Créé par Viple SAS
import os
import shutil
import winreg
import sys

def install_startup():
    """Installe l'application de démarrage dans le registre Windows"""
    try:
        # Chemin du script de démarrage
        script_path = os.path.abspath("startup_welcome.py")
        python_path = sys.executable
        
        # Commande à exécuter
        command = f'"{python_path}" "{script_path}"'
        
        # Ajouter au registre pour le démarrage automatique
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "VipleWelcome", 0, winreg.REG_SZ, command)
        
        print("Installation réussie ! L'application se lancera au démarrage de Windows.")
        
    except Exception as e:
        print(f"Erreur lors de l'installation : {str(e)}")

def uninstall_startup():
    """Désinstalle l'application de démarrage du registre Windows"""
    try:
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.DeleteValue(reg_key, "VipleWelcome")
        
        print("Désinstallation réussie !")
        
    except FileNotFoundError:
        print("L'application n'était pas installée au démarrage.")
    except Exception as e:
        print(f"Erreur lors de la désinstallation : {str(e)}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Installer/Désinstaller Viple Welcome au démarrage")
    parser.add_argument("--uninstall", action="store_true", help="Désinstaller du démarrage")
    
    args = parser.parse_args()
    
    if args.uninstall:
        uninstall_startup()
    else:
        install_startup()