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

class VipleLaunchPadV2:
    def __init__(self):
        self.widget_visible = True
        self.tray_icon = None
        self.icon_path = None
        self.create_icon()
        self.create_widget()
        if PIL_AVAILABLE:
            self.create_system_tray()
        else:
            print("Mode simplifié: pas d'icône système")
    
    def create_icon(self):
        """Crée l'icône Viple si elle n'existe pas"""
        png_path = "viple_icon.png"
        ico_path = "viple_icon.ico"
        
        if not os.path.exists(png_path) or not os.path.exists(ico_path):
            print("Création de l'icône Viple...")
            try:
                from create_viple_icon import create_viple_icon
                png_path, ico_path = create_viple_icon()
                self.icon_path = png_path
            except ImportError:
                # Créer une icône simple si le module n'est pas disponible
                self.create_simple_icon()
        else:
            self.icon_path = png_path
            print("✓ Icône Viple trouvée")
    
    def create_simple_icon(self):
        """Crée une icône simple si PIL n'est pas disponible"""
        if PIL_AVAILABLE:
            size = 64
            image = Image.new('RGBA', (size, size), (46, 134, 193, 255))  # Bleu Viple
            
            # Cercle simple
            from PIL import ImageDraw
            draw = ImageDraw.Draw(image)
            draw.ellipse([4, 4, size-4, size-4], fill=(46, 134, 193, 255), outline=(255, 255, 255, 255), width=2)
            
            # Texte "V"
            try:
                from PIL import ImageFont
                font = ImageFont.truetype("arial.ttf", 32)
            except:
                font = ImageFont.load_default()
            
            draw.text((18, 16), "V", fill=(255, 255, 255, 255), font=font)
            
            self.icon_path = "viple_icon_simple.png"
            image.save(self.icon_path, "PNG")
            print(f"✓ Icône simple créée : {self.icon_path}")
    
    def create_widget(self):
        self.root = tk.Tk()
        self.root.title("Viple LaunchPad V2")
        self.root.geometry("280x160")
        self.root.resizable(False, False)
        
        # Positionner en haut à droite
        self.root.update_idletasks()
        x = self.root.winfo_screenwidth() - 300
        y = 20
        self.root.geometry(f"280x160+{x}+{y}")
        
        # Configuration de la fenêtre
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#1B4F72')
        
        # Définir l'icône de la fenêtre
        if self.icon_path and os.path.exists(self.icon_path):
            try:
                icon_img = tk.PhotoImage(file=self.icon_path)
                self.root.iconphoto(False, icon_img)
            except:
                pass
        
        # Gérer la fermeture de la fenêtre
        if PIL_AVAILABLE:
            self.root.protocol("WM_DELETE_WINDOW", self.hide_widget)
        else:
            self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        
        # Bind pour détecter les clics ailleurs
        self.root.bind("<FocusOut>", self.on_focus_out)
        
        self.create_widget_content()
    
    def create_widget_content(self):
        # Frame pour le titre avec icône
        title_frame = tk.Frame(self.root, bg='#1B4F72')
        title_frame.pack(pady=(10, 15))
        
        # Charger et afficher l'icône à côté du titre
        if self.icon_path and os.path.exists(self.icon_path) and PIL_AVAILABLE:
            try:
                icon_img = Image.open(self.icon_path)
                icon_img = icon_img.resize((24, 24), Image.Resampling.LANCZOS)
                self.icon_tk = ImageTk.PhotoImage(icon_img)
                
                icon_label = tk.Label(
                    title_frame,
                    image=self.icon_tk,
                    bg='#1B4F72'
                )
                icon_label.pack(side='left', padx=(0, 8))
            except Exception as e:
                print(f"Erreur lors du chargement de l'icône : {e}")
        
        # Titre
        title_label = tk.Label(
            title_frame,
            text="Viple LaunchPad",
            font=("Arial", 14, "bold"),
            bg='#1B4F72',
            fg='white'
        )
        title_label.pack(side='left')
        
        # Frame pour les boutons
        button_frame = tk.Frame(self.root, bg='#1B4F72')
        button_frame.pack(expand=True, fill='both', padx=15)
        
        # Bouton Obtenir de l'aide
        help_btn = tk.Button(
            button_frame,
            text="🆘 Obtenir de l'aide",
            font=("Arial", 9),
            bg='#2E86C1',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.open_help,
            pady=5
        )
        help_btn.pack(fill='x', pady=3)
        
        # Bouton Lancer le Kiosk
        kiosk_btn = tk.Button(
            button_frame,
            text="🖥️ Lancer le Kiosk",
            font=("Arial", 9),
            bg='#2E86C1',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.launch_kiosk,
            pady=5
        )
        kiosk_btn.pack(fill='x', pady=3)
        
        # Bouton Lancer le Manager
        manager_btn = tk.Button(
            button_frame,
            text="⚙️ Lancer le Manager",
            font=("Arial", 9),
            bg='#2E86C1',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.launch_manager,
            pady=5
        )
        manager_btn.pack(fill='x', pady=3)
    
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
    
    def toggle_widget(self):
        """Basculer entre afficher et cacher le widget"""
        if self.widget_visible:
            self.hide_widget()
        else:
            self.show_widget()
    
    def on_focus_out(self, event):
        # Se cacher après un petit délai si on perd le focus
        self.root.after(1500, self.check_and_hide)
    
    def check_and_hide(self):
        # Cacher le widget si le focus est perdu
        if not self.root.focus_get() and self.widget_visible:
            self.hide_widget()
    
    def create_system_tray(self):
        if not PIL_AVAILABLE:
            return
            
        try:
            # Charger l'icône personnalisée
            if self.icon_path and os.path.exists(self.icon_path):
                image = Image.open(self.icon_path)
            else:
                # Icône par défaut si pas trouvée
                image = Image.new('RGB', (64, 64), color='#2E86C1')
            
            # Redimensionner pour la barre système
            image = image.resize((32, 32), Image.Resampling.LANCZOS)
            
            # Menu enrichi de l'icône système
            menu = pystray.Menu(
                item('Afficher/Masquer LaunchPad', self.toggle_widget, default=True),
                item('---', None),  # Séparateur
                item('🆘 Obtenir de l\'aide', self.open_help),
                item('🖥️ Lancer le Kiosk', self.launch_kiosk),
                item('⚙️ Lancer le Manager', self.launch_manager),
                item('---', None),  # Séparateur
                item('❌ Quitter', self.quit_app)
            )
            
            # Créer l'icône système
            self.tray_icon = pystray.Icon(
                "Viple LaunchPad",
                image,
                "Viple LaunchPad - Clic pour afficher/masquer",
                menu
            )
            
            # Définir l'action par défaut (clic simple)
            self.tray_icon.default_action = self.toggle_widget
            
            # Lancer l'icône système dans un thread séparé
            tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            tray_thread.start()
            
            print("✓ Icône Viple ajoutée à la barre système")
            
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
    app = VipleLaunchPadV2()
    app.run()