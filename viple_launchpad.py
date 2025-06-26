# Créé par Viple SAS
import tkinter as tk
from tkinter import messagebox
import webbrowser
import subprocess
import os
import sys
import threading

try:
    from PIL import Image, ImageTk
    import pystray
    from pystray import MenuItem as item
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Attention: PIL ou pystray non disponibles. L'icône système sera simplifiée.")

class VipleLaunchPad:
    def __init__(self):
        self.widget_visible = True
        self.tray_icon = None
        self.create_widget()
        if PIL_AVAILABLE:
            self.create_system_tray()
        else:
            print("Mode simplifié: pas d'icône système")
    
    def create_widget(self):
        self.root = tk.Tk()
        self.root.title("Viple LaunchPad")
        self.root.geometry("250x140")
        self.root.resizable(False, False)
        
        # Positionner en haut à droite
        self.root.update_idletasks()
        x = self.root.winfo_screenwidth() - 270
        y = 20
        self.root.geometry(f"250x140+{x}+{y}")
        
        # Configuration de la fenêtre
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#1B4F72')
        
        # Gérer la fermeture de la fenêtre
        if PIL_AVAILABLE:
            self.root.protocol("WM_DELETE_WINDOW", self.hide_widget)
        else:
            self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        
        # Bind pour détecter les clics ailleurs
        self.root.bind("<FocusOut>", self.on_focus_out)
        
        self.create_widget_content()
    
    def create_widget_content(self):
        # Titre
        title_label = tk.Label(
            self.root,
            text="Viple LaunchPad",
            font=("Arial", 14, "bold"),
            bg='#1B4F72',
            fg='white'
        )
        title_label.pack(pady=(10, 15))
        
        # Frame pour les boutons
        button_frame = tk.Frame(self.root, bg='#1B4F72')
        button_frame.pack(expand=True, fill='both', padx=10)
        
        # Bouton Obtenir de l'aide
        help_btn = tk.Button(
            button_frame,
            text="Obtenir de l'aide",
            font=("Arial", 9),
            bg='#2E86C1',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.open_help
        )
        help_btn.pack(fill='x', pady=2)
        
        # Bouton Lancer le Kiosk
        kiosk_btn = tk.Button(
            button_frame,
            text="Lancer le Kiosk",
            font=("Arial", 9),
            bg='#2E86C1',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.launch_kiosk
        )
        kiosk_btn.pack(fill='x', pady=2)
        
        # Bouton Lancer le Manager
        manager_btn = tk.Button(
            button_frame,
            text="Lancer le Manager",
            font=("Arial", 9),
            bg='#2E86C1',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.launch_manager
        )
        manager_btn.pack(fill='x', pady=2)
    
    def open_help(self):
        try:
            webbrowser.open("https://aidenum.viplegroup.com")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le navigateur: {str(e)}")
    
    def launch_kiosk(self):
        try:
            if os.path.exists(r"C:\viplestart\lkiosk.exe"):
                subprocess.Popen([r"C:\viplestart\lkiosk.exe"])
            else:
                messagebox.showwarning("Fichier manquant", "lkiosk.exe non trouvé dans C:\\viplestart\\")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer le Kiosk: {str(e)}")
    
    def launch_manager(self):
        try:
            if os.path.exists(r"C:\viplestart\lmanager.exe"):
                subprocess.Popen([r"C:\viplestart\lmanager.exe"])
            else:
                messagebox.showwarning("Fichier manquant", "lmanager.exe non trouvé dans C:\\viplestart\\")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer le Manager: {str(e)}")
    
    def hide_widget(self):
        if PIL_AVAILABLE:
            self.root.withdraw()
            self.widget_visible = False
        else:
            self.quit_app()
    
    def show_widget(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.widget_visible = True
    
    def on_focus_out(self, event):
        # Se cacher après un petit délai si on perd le focus
        self.root.after(1000, self.check_and_hide)
    
    def check_and_hide(self):
        # Cacher le widget si le focus est perdu
        if not self.root.focus_get() and self.widget_visible:
            self.hide_widget()
    
    def create_system_tray(self):
        if not PIL_AVAILABLE:
            return
            
        try:
            # Créer une image simple pour l'icône
            image = Image.new('RGB', (64, 64), color='#2E86C1')
            
            # Menu de l'icône système
            menu = pystray.Menu(
                item('Afficher LaunchPad', self.show_widget),
                item('Quitter', self.quit_app)
            )
            
            # Créer l'icône système
            self.tray_icon = pystray.Icon(
                "Viple LaunchPad",
                image,
                "Viple LaunchPad",
                menu
            )
            
            # Lancer l'icône système dans un thread séparé
            tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            tray_thread.start()
            
        except Exception as e:
            print(f"Erreur lors de la création de l'icône système: {e}")
    
    def quit_app(self, icon=None, item=None):
        if hasattr(self, 'tray_icon') and self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()
        if hasattr(self.root, 'destroy'):
            self.root.destroy()
        sys.exit()
    
    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.quit_app()

if __name__ == "__main__":
    app = VipleLaunchPad()
    app.run()