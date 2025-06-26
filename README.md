# Viple LaunchPad - Widget de Bureau Windows

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-Viple_SAS-green.svg)](https://viplegroup.com)
[![Version](https://img.shields.io/badge/Version-4.0-brightgreen.svg)](#)

> Widget de bureau élégant et transparent pour accéder rapidement aux outils Viple

![Viple LaunchPad Screenshot](https://via.placeholder.com/400x250?text=Viple+LaunchPad+V4)

## 📋 Table des matières

- [Aperçu](#-aperçu)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Configuration](#-configuration)
- [Versions](#-versions)
- [Dépannage](#-dépannage)
- [Contribuer](#-contribuer)
- [Support](#-support)
- [Licence](#-licence)

## 🎯 Aperçu

Viple LaunchPad est un widget de bureau Windows moderne et transparent qui fournit un accès rapide aux outils et services Viple. Conçu pour s'intégrer parfaitement dans votre environnement de travail, il combine élégance visuelle et fonctionnalité pratique.

### Caractéristiques principales

- 🎨 **Interface transparente** avec fond d'image de paysage
- 🚫 **Design épuré** sans barre de titre Windows
- 🖱️ **Déplacement intuitif** par glisser-déposer
- 🔧 **Icône système** avec menu contextuel complet
- ⚡ **Démarrage automatique** avec Windows
- 🎭 **Transparence réglable** (60% à 100%)

## ✨ Fonctionnalités

### Interface utilisateur
- Widget sans bordures avec transparence à 85%
- Fond d'image de paysage généré automatiquement (montagnes, ciel, nuages)
- Boutons colorés par fonction (bleu, vert, violet)
- Auto-masquage après 3 secondes d'inactivité
- Repositionnement automatique en haut à droite

### Fonctionnalités système
- **🆘 Obtenir de l'aide** : Accès direct au support Viple
- **🖥️ Lancer le Kiosk** : Exécution de l'application Kiosk
- **⚙️ Lancer le Manager** : Lancement du gestionnaire Viple
- **🎨 Gestion de transparence** : 5 niveaux de transparence
- **📍 Repositionnement** : Retour à la position par défaut

### Icône système
- Icône personnalisée Viple dans la barre système Windows
- Menu contextuel avec toutes les fonctions
- Clic simple pour afficher/masquer le widget
- Contrôle complet sans boutons sur le widget

## 🚀 Installation

### Prérequis
- Windows 10/11
- Python 3.7 ou supérieur
- Permissions administrateur (pour l'installation)

### Installation automatique

1. **Téléchargez les fichiers** du projet
2. **Ouvrez une invite de commande** en tant qu'administrateur
3. **Naviguez** vers le dossier du projet
4. **Exécutez** l'installation :

```bash
python setup_viple_v4_fixed.py
```

### Installation manuelle

```bash
# 1. Installer les dépendances
pip install Pillow>=8.0.0 pystray>=0.19.0

# 2. Créer le répertoire système
mkdir C:\viplestart

# 3. Copier vos exécutables dans C:\viplestart\
# - lkiosk.exe
# - lmanager.exe

# 4. Générer les ressources visuelles
python create_viple_icon.py
python create_background_image.py

# 5. Lancer le widget
python viple_launchpad_v4_fixed.py
```

### Démarrage automatique

L'installation configure automatiquement le widget pour se lancer au démarrage de Windows. Pour gérer cette fonctionnalité :

```bash
# Activer le démarrage automatique
python setup_viple_v4_fixed.py

# Désactiver le démarrage automatique
python setup_viple_v4_fixed.py --uninstall
```

## 🎮 Utilisation

### Contrôles de base

| Action | Méthode |
|--------|---------|
| **Déplacer le widget** | Cliquer et glisser n'importe où sur le widget |
| **Afficher/Masquer** | Clic simple sur l'icône système |
| **Menu complet** | Clic droit sur l'icône système |
| **Fermer** | Menu système → "Quitter complètement" |

### Menu système

L'icône dans la barre système (en bas à droite) donne accès à :

- 🔧 **Afficher/Masquer LaunchPad** (action par défaut)
- 🆘 **Obtenir de l'aide** → https://aidenum.viplegroup.com
- 🖥️ **Lancer le Kiosk** → C:\viplestart\lkiosk.exe
- ⚙️ **Lancer le Manager** → C:\viplestart\lmanager.exe
- 🎨 **Changer transparence** (cycle 60%-75%-85%-95%-100%)
- 📍 **Repositionner** (retour en haut à droite)
- ❌ **Quitter complètement**

### Niveaux de transparence

| Niveau | Opacité | Usage recommandé |
|--------|---------|------------------|
| 60% | Très transparent | Discrétion maximale |
| 75% | Transparent | Usage général |
| **85%** | **Défaut** | **Équilibre optimal** |
| 95% | Presque opaque | Meilleure lisibilité |
| 100% | Opaque | Pas de transparence |

## ⚙️ Configuration

### Structure des fichiers

```
Viple-LaunchPad/
├── viple_launchpad_v4_fixed.py     # Widget principal
├── create_viple_icon.py            # Générateur d'icône
├── create_background_image.py      # Générateur de fond
├── setup_viple_v4_fixed.py         # Script d'installation
├── startup_welcome.py              # Application de bienvenue
├── requirements.txt                # Dépendances Python
├── viple_icon.png                  # Icône générée
├── viple_background.png            # Fond d'image généré
└── README.md                       # Ce fichier
```

### Personnalisation

#### Changer l'image de fond
```python
# Modifier create_background_image.py puis exécuter :
python create_background_image.py
```

#### Modifier l'icône
```python
# Éditer create_viple_icon.py pour changer :
# - Couleurs (bg_color, text_color)
# - Texte ("V" par défaut)
# - Taille et style
python create_viple_icon.py
```

#### Ajuster la transparence par défaut
```python
# Dans viple_launchpad_v4_fixed.py, ligne ~87 :
self.root.attributes('-alpha', 0.85)  # Changer 0.85 (85%)
```

### Configuration système

| Élément | Emplacement |
|---------|------------|
| **Exécutables** | `C:\viplestart\lkiosk.exe`, `C:\viplestart\lmanager.exe` |
| **Registre Windows** | `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run` |
| **Démarrage** | Clé "VipleWelcomeV4Fixed" |

## 📚 Versions

### V4.0 (Actuelle) - 2025-06-26
- ✅ Suppression du bouton de fermeture
- ✅ Fond d'image de paysage automatique
- ✅ Transparence réglable (85% par défaut)
- ✅ Correction erreur "unknown color name"
- ✅ Boutons colorés par fonction

### V3.0
- Interface sans barre de titre
- Déplacement par glisser-déposer
- Bouton fermer personnalisé

### V2.0
- Icône personnalisée Viple
- Interface améliorée avec emojis
- Menu système enrichi

### V1.0
- Widget de base avec fonctionnalités essentielles
- Application de bienvenue au démarrage

## 🔧 Dépannage

### Problèmes courants

#### Le widget ne s'affiche pas
```bash
# 1. Vérifier que les dépendances sont installées
pip list | grep -E "(Pillow|pystray)"

# 2. Lancer manuellement pour voir les erreurs
python viple_launchpad_v4_fixed.py

# 3. Vérifier l'icône système dans la barre des tâches
```

#### Erreur "unknown color name"
```bash
# Utiliser la version corrigée
python viple_launchpad_v4_fixed.py
```

#### Les exécutables ne se lancent pas
```bash
# Vérifier que les fichiers existent
dir C:\viplestart\

# Remplacer les fichiers exemples par les vrais exécutables
```

#### Problème de transparence
```bash
# Réinitialiser la transparence via le menu système
# Clic droit sur icône → "Changer transparence"
```

### Logs et débogage

```python
# Pour activer plus de logs, modifier le widget :
print("Debug: Widget créé")  # Ajouter des prints pour debugging
```

### Désinstallation complète

```bash
# 1. Désinstaller du démarrage automatique
python setup_viple_v4_fixed.py --uninstall

# 2. Supprimer les fichiers
del viple_icon.png viple_background.png

# 3. Optionnel : supprimer le répertoire système
rmdir /s C:\viplestart
```

## 🤝 Contribuer

Nous accueillons les contributions ! Voici comment participer :

### Signaler un bug
1. Vérifiez que le bug n'a pas déjà été signalé
2. Créez une [nouvelle issue](../../issues/new)
3. Incluez :
   - Version de Windows
   - Version de Python
   - Étapes pour reproduire
   - Messages d'erreur complets

### Proposer une amélioration
1. Créez une [issue](../../issues/new) avec le tag `enhancement`
2. Décrivez clairement la fonctionnalité souhaitée
3. Expliquez pourquoi elle serait utile

### Développement
```bash
# 1. Forkez le repository
# 2. Créez une branche pour votre fonctionnalité
git checkout -b feature/ma-nouvelle-fonctionnalite

# 3. Committez vos changements
git commit -m "Ajout de ma nouvelle fonctionnalité"

# 4. Poussez vers votre fork
git push origin feature/ma-nouvelle-fonctionnalite

# 5. Créez une Pull Request
```

### Standards de code
- Code en français (commentaires et variables)
- Suivre la convention PEP 8 pour Python
- Inclure des commentaires explicatifs
- Tester sur Windows 10 et 11

## 📞 Support

### Aide officielle
- **Site web** : [https://aidenum.viplegroup.com](https://aidenum.viplegroup.com)
- **Documentation** : Voir le fichier `Guide_Utilisation_Viple_V4.txt`

### Communauté
- **Issues GitHub** : [Issues](../../issues)
- **Discussions** : [Discussions](../../discussions)

### Contact direct
- **Email** : support@viplegroup.com
- **Entreprise** : Viple SAS

## 📄 Licence

```
Copyright (c) 2025 Viple SAS
Tous droits réservés.

Ce logiciel est la propriété de Viple SAS et est protégé par les lois 
sur le droit d'auteur et autres lois sur la propriété intellectuelle.

L'utilisation de ce logiciel est soumise aux termes et conditions 
définies dans l'accord de licence Viple SAS.

Pour plus d'informations sur les licences, contactez :
https://viplegroup.com
```

---

## 🏷️ Tags

`windows` `desktop-widget` `python` `tkinter` `transparent` `viple` `launchpad` `system-tray` `auto-startup`

---

**Créé par Viple SAS** - Version 4.0 - 2025-06-26

*Pour la dernière version et les mises à jour, visitez : [viplegroup.com](https://viplegroup.com)*
