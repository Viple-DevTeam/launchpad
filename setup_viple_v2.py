# Créé par Viple SAS
import os
import sys
import subprocess
import winreg
import shutil

def check_python():
    """Vérifie que Python est correctement installé avec tkinter"""
    try:
        import tkinter
        print("✓ Python et tkinter sont disponibles")
        return True
    except ImportError:
        print("✗ Erreur: tkinter n'est pas disponible")
        print("Veuillez réinstaller Python en vous assurant que tkinter est inclus")
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

def create_viple_icons():
    """Crée les icônes Viple personnalisées"""
    try:
        print("Création des icônes Viple...")
        exec(open('create_viple_icon.py').read())
        print("✓ Icônes Viple créées")
        return True
    except Exception as e:
        print(f"✗ Erreur lors de la création des icônes: {e}")
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
        # Utiliser la version V2 du LaunchPad
        script_path = os.path.abspath("startup_welcome.py")
        python_path = sys.executable
        
        if not os.path.exists(script_path):
            print("✗ Erreur: startup_welcome.py non trouvé")
            return False
        
        # Modifier startup_welcome.py pour lancer la V2
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer l'ancien nom par le nouveau
        content = content.replace('viple_launchpad.py', 'viple_launchpad_v2.py')
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ Script de démarrage mis à jour pour la V2")
        
        # Commande à exécuter
        command = f'"{python_path}" "{script_path}"'
        
        # Ajouter au registre pour le démarrage automatique
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "VipleWelcomeV2", 0, winreg.REG_SZ, command)
        
        print("✓ Application V2 installée pour le démarrage automatique")
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de l'installation du démarrage automatique: {e}")
        return False

def main():
    print("=== INSTALLATION VIPLE LAUNCHPAD V2 ===")
    print("Créé par Viple SAS")
    print("Avec icône personnalisée Viple\n")
    
    # Vérifier Python et tkinter
    if not check_python():
        return
    
    # Installer les dépendances
    if not install_dependencies():
        print("Erreur lors de l'installation des dépendances")
        return
    
    # Créer les icônes Viple
    if not create_viple_icons():
        print("Attention: Les icônes n'ont pas pu être créées, mode de base utilisé")
    
    # Créer le répertoire viplestart
    if not create_viplestart_directory():
        print("Erreur lors de la création du répertoire viplestart")
        return
    
    # Installer le démarrage automatique
    if install_startup():
        print("\n✅ Installation V2 terminée avec succès !")
        print("\n🎯 Nouvelles fonctionnalités V2 :")
        print("   • Icône personnalisée Viple dans la barre système")
        print("   • Interface améliorée avec emojis")
        print("   • Menu enrichi dans la barre système")
        print("   • Clic simple pour afficher/masquer")
        print("\nLes applications Viple V2 sont maintenant installées.")
        print("Au prochain redémarrage, l'application se lancera automatiquement.")
        print("\nPour tester maintenant, exécutez : python viple_launchpad_v2.py")
    else:
        print("\n✗ Installation incomplète - vérifiez les erreurs ci-dessus")

def uninstall():
    """Désinstalle l'application de démarrage"""
    try:
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        # Supprimer les anciennes entrées
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            try:
                winreg.DeleteValue(reg_key, "VipleWelcome")
                print("✓ Ancienne version désinstallée")
            except FileNotFoundError:
                pass
            
            try:
                winreg.DeleteValue(reg_key, "VipleWelcomeV2")
                print("✓ Version V2 désinstallée du démarrage automatique")
            except FileNotFoundError:
                print("La version V2 n'était pas installée au démarrage")
        
    except Exception as e:
        print(f"✗ Erreur lors de la désinstallation: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Installation Viple LaunchPad V2")
    parser.add_argument("--uninstall", action="store_true", help="Désinstaller du démarrage")
    
    args = parser.parse_args()
    
    if args.uninstall:
        uninstall()
    else:
        main()