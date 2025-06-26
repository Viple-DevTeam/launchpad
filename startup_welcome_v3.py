# Créé par Viple SAS
import tkinter as tk
from tkinter import messagebox
import time
import threading

class VipleBienvenueAppV3:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.show_welcome()
    
    def setup_window(self):
        # Configuration de la fenêtre
        self.root.title("Viple - Bienvenue")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        
        # Centrer la fenêtre
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (200 // 2)
        self.root.geometry(f"400x200+{x}+{y}")
        
        # Configuration de la fenêtre (toujours au premier plan)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#2E86C1')
    
    def show_welcome(self):
        # Message de bienvenue
        welcome_label = tk.Label(
            self.root,
            text="Bienvenue chez Viple",
            font=("Arial", 18, "bold"),
            bg='#2E86C1',
            fg='white'
        )
        welcome_label.pack(expand=True)
        
        # Programmer l'affichage du message d'aide après 3 secondes
        self.root.after(3000, self.show_help_message)
    
    def show_help_message(self):
        self.root.destroy()
        
        # Nouvelle fenêtre pour le message d'aide
        help_window = tk.Tk()
        help_window.title("Viple - Aide")
        help_window.geometry("500x150")
        help_window.resizable(False, False)
        
        # Centrer la fenêtre
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (help_window.winfo_screenheight() // 2) - (150 // 2)
        help_window.geometry(f"500x150+{x}+{y}")
        
        help_window.attributes('-topmost', True)
        help_window.configure(bg='#2E86C1')
        
        # Message d'aide
        help_label = tk.Label(
            help_window,
            text="Besoin d'aide ? Rendez-vous sur le guide d'utilisation\nen cliquant sur guide en haut à droite",
            font=("Arial", 12),
            bg='#2E86C1',
            fg='white',
            justify='center'
        )
        help_label.pack(expand=True)
        
        # Fermer automatiquement après 5 secondes et lancer le widget V3
        help_window.after(5000, lambda: self.close_and_launch_widget(help_window))
    
    def close_and_launch_widget(self, window):
        window.destroy()
        # Lancer le widget LaunchPad V3
        import subprocess
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.Popen([
            'python', 
            os.path.join(script_dir, 'viple_launchpad_v4.py')
        ])
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VipleBienvenueAppV3()
    app.run()