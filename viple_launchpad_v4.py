# Créé par Viple SAS
import tkinter as tk
from tkinter import messagebox
import webbrowser
import subprocess
import os
import sys
import threading

try:
    from PIL import Image, ImageTk, ImageEnhance
    import pystray
    from pystray import MenuItem as item
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Attention: PIL ou pystray non disponibles. L'icône système sera simplifiée.")

class VipleLaunchPadV4:
    def __init__(self):
        self.widget_visible = True
        self.tray_icon = None
        self.icon_path = None
        self.background_path = None
        self.drag_data = {"x": 0, "y": 0}
        self.create_icon()
        self.create_background()
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
                self.create_simple_icon()
        else:
            self.icon_path = png_path
            print("✓ Icône Viple trouvée")
    
    def create_background(self):
        """Crée l'image de fond si elle n'existe pas"""
        bg_files = ["viple_background.png", "viple_background_abstract.png"]
        
        # Chercher une image de fond existante
        for bg_file in bg_files:
            if os.path.exists(bg_file):
                self.background_path = bg_file
                print(f"✓ Image de fond trouvée : {bg_file}")
                return
        
        # Créer l'image de fond si elle n'existe pas
        try:
            from create_background_image import create_landscape_background
            self.background_path = create_landscape_background()
        except ImportError:
            print("Module de création de fond non trouvé, utilisation du fond par défaut")
            self.background_path = None
    
    def create_simple_icon(self):
        """Crée une icône simple si PIL n'est pas disponible"""
        if PIL_AVAILABLE:
            size = 64
            image = Image.new('RGBA', (size, size), (46, 134, 193, 255))
            
            from PIL import ImageDraw
            draw = ImageDraw.Draw(image)
            draw.ellipse([4, 4, size-4, size-4], fill=(46, 134, 193, 255), outline=(255, 255, 255, 255), width=2)
            
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
        
        # Supprimer la barre de titre
        self.root.overrideredirect(True)
        
        self.root.geometry("280x160")
        self.root.resizable(False, False)
        
        # Appliquer la transparence (0.0 = invisible, 1.0 = opaque)
        self.root.attributes('-alpha', 0.85)  # 85% d'opacité = 15% de transparence
        
        # Positionner en haut à droite
        self.root.update_idletasks()
        x = self.root.winfo_screenwidth() - 300
        y = 20
        self.root.geometry(f"280x160+{x}+{y}")
        
        # Configuration de la fenêtre
        self.root.attributes('-topmost', True)
        
        # Charger l'image de fond
        if self.background_path and os.path.exists(self.background_path) and PIL_AVAILABLE:
            try:
                # Charger et redimensionner l'image de fond
                bg_image = Image.open(self.background_path)
                bg_image = bg_image.resize((280, 160), Image.Resampling.LANCZOS)
                
                # Appliquer un léger assombrissement pour améliorer la lisibilité du texte
                enhancer = ImageEnhance.Brightness(bg_image)
                bg_image = enhancer.enhance(0.7)  # Assombrir à 70%
                
                self.bg_photo = ImageTk.PhotoImage(bg_image)
                self.root.configure(bg='white')  # Couleur de secours
            except Exception as e:
                print(f"Erreur lors du chargement de l'image de fond: {e}")
                self.bg_photo = None
                self.root.configure(bg='#1B4F72')  # Bleu par défaut
        else:
            self.bg_photo = None
            self.root.configure(bg='#1B4F72')  # Bleu par défaut
        
        # Permettre de déplacer la fenêtre en cliquant et glissant
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)
        
        # Bind pour détecter les clics ailleurs
        self.root.bind("<FocusOut>", self.on_focus_out)
        
        self.create_widget_content()
    
    def start_drag(self, event):
        """Commence le déplacement de la fenêtre"""
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
    
    def do_drag(self, event):
        """Effectue le déplacement de la fenêtre"""
        x = self.root.winfo_x() + (event.x - self.drag_data["x"])
        y = self.root.winfo_y() + (event.y - self.drag_data["y"])
        self.root.geometry(f"+{x}+{y}")
    
    def create_widget_content(self):
        # Frame principale avec image de fond
        if self.bg_photo:
            # Créer un label avec l'image de fond qui couvre tout
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Permettre de déplacer en cliquant sur le fond
            bg_label.bind("<Button-1>", self.start_drag)
            bg_label.bind("<B1-Motion>", self.do_drag)
            
            # Frame principale transparente par-dessus
            main_frame = tk.Frame(self.root, bg='', bd=0)
        else:
            main_frame = tk.Frame(self.root, bg='#1B4F72', bd=0)
        
        main_frame.place(x=0, y=0, width=280, height=160)
        
        # Permettre de déplacer la fenêtre en cliquant sur la frame principale
        main_frame.bind("<Button-1>", self.start_drag)
        main_frame.bind("<B1-Motion>", self.do_drag)
        
        # Frame pour le header avec logo et titre
        header_frame = tk.Frame(main_frame, bg='', bd=0)
        header_frame.pack(pady=(15, 10))
        
        # Permettre de déplacer la fenêtre en cliquant sur le header
        header_frame.bind("<Button-1>", self.start_drag)
        header_frame.bind("<B1-Motion>", self.do_drag)
        
        # Charger et afficher l'icône à côté du titre
        if self.icon_path and os.path.exists(self.icon_path) and PIL_AVAILABLE:
            try:
                icon_img = Image.open(self.icon_path)
                icon_img = icon_img.resize((28, 28), Image.Resampling.LANCZOS)
                self.icon_tk = ImageTk.PhotoImage(icon_img)
                
                icon_label = tk.Label(
                    header_frame,
                    image=self.icon_tk,
                    bg='',
                    bd=0
                )
                icon_label.pack(side='left', padx=(0, 10))
                
                # Permettre de déplacer la fenêtre en cliquant sur l'icône
                icon_label.bind("<Button-1>", self.start_drag)
                icon_label.bind("<B1-Motion>", self.do_drag)
            except Exception as e:
                print(f"Erreur lors du chargement de l'icône : {e}")
        
        # Titre avec ombre pour meilleure lisibilité
        title_label = tk.Label(
            header_frame,
            text="Viple LaunchPad",
            font=("Arial", 14, "bold"),
            bg='',
            fg='white',
            bd=0
        )
        title_label.pack(side='left')
        
        # Permettre de déplacer la fenêtre en cliquant sur le titre
        title_label.bind("<Button-1>", self.start_drag)
        title_label.bind("<B1-Motion>", self.do_drag)
        
        # Frame pour les boutons
        button_frame = tk.Frame(main_frame, bg='', bd=0)
        button_frame.pack(expand=True, fill='both', padx=20)
        
        # Style des boutons avec transparence
        button_style = {
            'font': ("Arial", 9, "bold"),
            'fg': 'white',
            'relief': 'flat',
            'cursor': 'hand2',
            'pady': 6,
            'bd': 1,
            'highlightthickness': 0
        }
        
        # Bouton Obtenir de l'aide
        help_btn = tk.Button(
            button_frame,
            text="🆘 Obtenir de l'aide",
            bg='#2E86C1',
            activebackground='#3498DB',
            command=self.open_help,
            **button_style
        )
        help_btn.pack(fill='x', pady=2)
        
        # Bouton Lancer le Kiosk
        kiosk_btn = tk.Button(
            button_frame,
            text="🖥️ Lancer le Kiosk",
            bg='#27AE60',
            activebackground='#2ECC71',
            command=self.launch_kiosk,
            **button_style
        )
        kiosk_btn.pack(fill='x', pady=2)
        
        # Bouton Lancer le Manager
        manager_btn = tk.Button(
            button_frame,
            text="⚙️ Lancer le Manager",
            bg='#8E44AD',
            activebackground='#9B59B6',
            command=self.launch_manager,
            **button_style
        )
        manager_btn.pack(fill='x', pady=2)
        
        # Petit texte d'info en bas avec meilleure lisibilité
        info_label = tk.Label(
            main_frame,
            text="Glisser pour déplacer • Icône système pour fermer",
            font=("Arial", 7),
            bg='',
            fg='white',
            bd=0
        )
        info_label.pack(side='bottom', pady=(5, 10))
        
        # Permettre de déplacer la fenêtre en cliquant sur l'info
        info_label.bind("<Button-1>", self.start_drag)
        info_label.bind("<B1-Motion>", self.do_drag)
    
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
        # Se cacher après un délai plus long pour éviter de fermer accidentellement
        self.root.after(3000, self.check_and_hide)  # 3 secondes
    
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
                # Icône par défaut
                image = Image.new('RGB', (64, 64), color='#2E86C1')
            
            # Redimensionner pour la barre système
            image = image.resize((32, 32), Image.Resampling.LANCZOS)
            
            # Menu enrichi de l'icône système (plus d'options car pas de bouton fermer)
            menu = pystray.Menu(
                item('🔧 Afficher/Masquer LaunchPad', self.toggle_widget, default=True),
                item('---', None),
                item('🆘 Obtenir de l\'aide', self.open_help),
                item('🖥️ Lancer le Kiosk', self.launch_kiosk),
                item('⚙️ Lancer le Manager', self.launch_manager),
                item('---', None),
                item('🎨 Changer transparence', self.change_transparency),
                item('📍 Repositionner', self.reset_position),
                item('---', None),
                item('❌ Quitter complètement', self.quit_app)
            )
            
            # Créer l'icône système
            self.tray_icon = pystray.Icon(
                "Viple LaunchPad V4",
                image,
                "Viple LaunchPad V4 - Transparent avec fond d'image",
                menu
            )
            
            # Définir l'action par défaut (clic simple)
            self.tray_icon.default_action = self.toggle_widget
            
            # Lancer l'icône système dans un thread séparé
            tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            tray_thread.start()
            
            print("✓ Icône Viple V4 ajoutée à la barre système (version transparente)")
            
        except Exception as e:
            print(f"Erreur lors de la création de l'icône système: {e}")
    
    def change_transparency(self, icon=None, item=None):
        """Change le niveau de transparence"""
        current_alpha = self.root.attributes('-alpha')
        
        # Cycle entre différents niveaux de transparence
        transparency_levels = [0.6, 0.75, 0.85, 0.95, 1.0]
        
        try:
            current_index = transparency_levels.index(current_alpha)
            next_index = (current_index + 1) % len(transparency_levels)
        except ValueError:
            next_index = 0
        
        new_alpha = transparency_levels[next_index]
        self.root.attributes('-alpha', new_alpha)
        
        print(f"Transparence changée à {int(new_alpha * 100)}%")
    
    def reset_position(self, icon=None, item=None):
        """Remet le widget en haut à droite"""
        x = self.root.winfo_screenwidth() - 300
        y = 20
        self.root.geometry(f"280x160+{x}+{y}")
        if not self.widget_visible:
            self.show_widget()
    
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
    app = VipleLaunchPadV4()
    app.run()