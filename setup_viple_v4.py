# Créé par Viple SAS
import os
import sys
import subprocess
import winreg

def check_python():
    """Vérifie que Python est correctement installé avec tkinter"""
    try:
        import tkinter
        print("✓ Python et tkinter sont disponibles")
        return True
    except ImportError:
        print("✗ Erreur: tkinter n'est pas disponible")
        return False

def install_dependencies():
    """Installe les dépendances Python nécessaires"""
    print("Installation des dépendances...")
    
    dependencies = [
        "Pillow>=8.0.0",
        "pystray>=0.19.0"
    ]
    
    for dep in dependencies:
        try:
            print(f"Installation de {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ {dep} installé avec succès")
        except subprocess.CalledProcessError as e:
            print(f"✗ Erreur lors de l'installation de {dep}: {e}")
            return False
    
    return True

def create_assets():
    """Crée les icônes et images de fond"""
    try:
        print("Création des ressources visuelles...")
        
        # Créer l'icône
        if not os.path.exists('viple_icon.png'):
            exec(open('create_viple_icon.py').read())
        
        # Créer les images de fond
        if not os.path.exists('viple_background.png'):
            exec(open('create_background_image.py').read())
        
        print("✓ Ressources visuelles créées")
        return True
    except Exception as e:
        print(f"✗ Erreur lors de la création des ressources: {e}")
        return False

def create_viplestart_directory():
    """Crée le répertoire C:\viplestart s'il n'existe pas"""
    viplestart_path = r"C:\viplestart"
    
    if not os.path.exists(viplestart_path):
        try:
            os.makedirs(viplestart_path)
            print(f"✓ Répertoire {viplestart_path} créé")
            
            # Créer des fichiers exemples
            example_files = ["lkiosk.exe", "lmanager.exe"]
            for file in example_files:
                example_path = os.path.join(viplestart_path, file)
                with open(example_path, 'w') as f:
                    f.write("# Fichier exemple - remplacez par le vrai exécutable")
                print(f"✓ Fichier exemple {file} créé")
                
        except PermissionError:
            print(f"✗ Erreur: Permissions insuffisantes pour créer {viplestart_path}")
            print("Veuillez exécuter ce script en tant qu'administrateur")
            return False
        except Exception as e:
            print(f"✗ Erreur lors de la création de {viplestart_path}: {e}")
            return False
    else:
        print(f"✓ Répertoire {viplestart_path} existe déjà")
    
    return True

def install_startup():
    """Installe l'application de démarrage dans le registre Windows"""
    try:
        # Chercher le fichier de démarrage
        startup_files = ["startup_welcome_v3.py", "startup_welcome.py"]
        script_path = None
        
        for file in startup_files:
            if os.path.exists(file):
                script_path = os.path.abspath(file)
                
                # Modifier le fichier pour lancer la V4
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remplacer l'ancien nom par la V4
                content = content.replace('viple_launchpad_v3.py', 'viple_launchpad_v4.py')
                content = content.replace('viple_launchpad_v2.py', 'viple_launchpad_v4.py')
                content = content.replace('viple_launchpad.py', 'viple_launchpad_v4.py')
                
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                break
        
        if not script_path:
            print("✗ Erreur: Aucun fichier startup_welcome trouvé")
            return False
        
        python_path = sys.executable
        command = f'"{python_path}" "{script_path}"'
        
        # Ajouter au registre
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "VipleWelcomeV4", 0, winreg.REG_SZ, command)
        
        print("✓ Application V4 installée pour le démarrage automatique")
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de l'installation du démarrage automatique: {e}")
        return False

def main():
    print("=== INSTALLATION VIPLE LAUNCHPAD V4 ===")
    print("Créé par Viple SAS")
    print("Version transparente avec fond d'image de paysage\n")
    
    if not check_python():
        return
    
    if not install_dependencies():
        print("Erreur lors de l'installation des dépendances")
        return
    
    if not create_assets():
        print("Attention: Les ressources visuelles n'ont pas pu être créées")
    
    if not create_viplestart_directory():
        print("Erreur lors de la création du répertoire viplestart")
        return
    
    if install_startup():
        print("\n🌟 Installation V4 terminée avec succès !")
        print("\n🎨 Nouvelles fonctionnalités V4 :")
        print("   • Widget SANS bouton de fermeture (plus épuré)")
        print("   • Fond d'image de paysage automatique")
        print("   • Transparence à 85% (modifiable)")
        print("   • Couleurs des boutons différenciées")
        print("   • Menu système enrichi avec options de transparence")
        print("   • Repositionnement automatique")
        print("\n🎯 Utilisation :")
        print("   • Glisser-déposer pour déplacer")
        print("   • Icône système pour toutes les actions")
        print("   • Auto-masquage après 3 secondes")
        print("\nPour tester maintenant : python viple_launchpad_v4.py")
    else:
        print("\n✗ Installation incomplète")

def uninstall():
    """Désinstalle toutes les versions"""
    try:
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            versions = ["VipleWelcome", "VipleWelcomeV2", "VipleWelcomeV3", "VipleWelcomeV4"]
            
            for version in versions:
                try:
                    winreg.DeleteValue(reg_key, version)
                    print(f"✓ {version} désinstallée")
                except FileNotFoundError:
                    pass
        
    except Exception as e:
        print(f"✗ Erreur lors de la désinstallation: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Installation Viple LaunchPad V4")
    parser.add_argument("--uninstall", action="store_true", help="Désinstaller du démarrage")
    
    args = parser.parse_args()
    
    if args.uninstall:
        uninstall()
    else:
        main()