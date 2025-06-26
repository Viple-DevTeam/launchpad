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
            if os.path.exists('create_viple_icon.py'):
                exec(open('create_viple_icon.py').read())
            else:
                print("Avertissement: create_viple_icon.py non trouvé")
        
        # Créer les images de fond
        if not os.path.exists('viple_background.png'):
            if os.path.exists('create_background_image.py'):
                exec(open('create_background_image.py').read())
            else:
                print("Avertissement: create_background_image.py non trouvé")
        
        print("✓ Ressources visuelles traitées")
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

def update_startup_script():
    """Met à jour le script de démarrage pour utiliser la V4"""
    startup_files = ["startup_welcome_v3.py", "startup_welcome.py"]
    
    for file in startup_files:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remplacer les anciennes versions par la V4 corrigée
                content = content.replace('viple_launchpad_v3.py', 'viple_launchpad_v4_fixed.py')
                content = content.replace('viple_launchpad_v2.py', 'viple_launchpad_v4_fixed.py')
                content = content.replace('viple_launchpad_v4.py', 'viple_launchpad_v4_fixed.py')
                content = content.replace('viple_launchpad.py', 'viple_launchpad_v4_fixed.py')
                
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✓ Script de démarrage {file} mis à jour pour V4 corrigée")
                return file
            except Exception as e:
                print(f"Erreur lors de la mise à jour de {file}: {e}")
                continue
    
    return None

def install_startup():
    """Installe l'application de démarrage dans le registre Windows"""
    try:
        script_path = update_startup_script()
        
        if not script_path:
            print("✗ Erreur: Aucun fichier startup_welcome trouvé")
            return False
        
        script_path = os.path.abspath(script_path)
        python_path = sys.executable
        command = f'"{python_path}" "{script_path}"'
        
        # Ajouter au registre
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "VipleWelcomeV4Fixed", 0, winreg.REG_SZ, command)
        
        print("✓ Application V4 corrigée installée pour le démarrage automatique")
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de l'installation du démarrage automatique: {e}")
        return False

def main():
    print("=== INSTALLATION VIPLE LAUNCHPAD V4 CORRIGÉ ===")
    print("Créé par Viple SAS")
    print("Version transparente avec fond d'image - Correction des erreurs de couleur\n")
    
    if not check_python():
        return
    
    if not install_dependencies():
        print("Erreur lors de l'installation des dépendances")
        return
    
    if not create_assets():
        print("Attention: Certaines ressources visuelles n'ont pas pu être créées")
    
    if not create_viplestart_directory():
        print("Erreur lors de la création du répertoire viplestart")
        return
    
    if install_startup():
        print("\n🎉 Installation V4 CORRIGÉE terminée avec succès !")
        print("\n🔧 Corrections apportées :")
        print("   • Erreur 'unknown color name' corrigée")
        print("   • Couleurs de fond définies correctement")
        print("   • Gestion d'erreur améliorée pour les images")
        print("   • Fallback sur couleurs par défaut si images manquantes")
        print("\n🎨 Fonctionnalités V4 :")
        print("   • Widget transparent (85%)")
        print("   • Fond d'image de paysage")
        print("   • Boutons colorés (bleu, vert, violet)")
        print("   • Menu système complet")
        print("   • Pas de bouton de fermeture")
        print("\nPour tester maintenant : python viple_launchpad_v4_fixed.py")
    else:
        print("\n✗ Installation incomplète")

def uninstall():
    """Désinstalle toutes les versions"""
    try:
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            versions = [
                "VipleWelcome", "VipleWelcomeV2", "VipleWelcomeV3", 
                "VipleWelcomeV4", "VipleWelcomeV4Fixed"
            ]
            
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
    parser = argparse.ArgumentParser(description="Installation Viple LaunchPad V4 Corrigé")
    parser.add_argument("--uninstall", action="store_true", help="Désinstaller du démarrage")
    
    args = parser.parse_args()
    
    if args.uninstall:
        uninstall()
    else:
        main()