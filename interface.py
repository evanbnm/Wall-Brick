"""
interface.py
Classe principale pour gérer l'interface du jeu casse-brique.
"""

import tkinter as tk
from logic import GameLogic

class Interface:
    def __init__(self):
        """Initialise l'interface graphique et lie la logique."""
        self.root = tk.Tk()
        self.root.title("Casse-brique")
        self.root.attributes('-fullscreen', True)
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight() - 50

        # Canvas
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # Logique du jeu
        self.logic = GameLogic(self.width, self.height)

        # Affichage initial
        self.start_text = self.canvas.create_text(
            self.width / 2, self.height / 2,
            text="Appuyez sur une touche pour démarrer",
            fill="white", font=("Arial", 16)
        )
        self.game_over_text = None  # Texte "Game Over" (initialement caché)

        # Set des touches pressées pour les mouvements
        self.pressed_keys = set()

        # Bindings
        self.root.bind("<Left>", self.key_pressed)
        self.root.bind("<Right>", self.key_pressed)
        self.root.bind("<KeyRelease>", self.key_released)
        self.root.bind("<Key>", self.start_or_restart_game)

        # Lancement de l'affichage initial
        self.draw_game()

    def key_pressed(self, event):
        """Ajoute la touche pressée dans le set."""
        self.pressed_keys.add(event.keysym)

    def key_released(self, event):
        """Supprime la touche relâchée du set."""
        if event.keysym in self.pressed_keys:
            self.pressed_keys.remove(event.keysym)

    def move_paddle(self):
        """Déplace la raquette en fonction des touches pressées."""
        if "Left" in self.pressed_keys:
            self.logic.move_paddle("left")
        if "Right" in self.pressed_keys:
            self.logic.move_paddle("right")
        self.draw_game()

    def start_or_restart_game(self, event):
        """Démarre ou redémarre le jeu en fonction de l'état."""
        if self.game_over_text:  # Si "Game Over", on réinitialise et démarre
            self.reset_game()
            self.logic.running = True  # Démarre immédiatement après la réinitialisation
            self.update()
        elif not self.logic.running:  # Sinon, on démarre normalement
            self.logic.running = True
            self.canvas.delete(self.start_text)  # Supprime le texte d'attente
            self.update()

    def reset_game(self):
        """Réinitialise l'état du jeu."""
        self.logic = GameLogic(self.width, self.height)  # Réinitialise la logique
        self.game_over_text = None  # Supprime le texte "Game Over"
        self.draw_game()

    def update(self):
        """Met à jour la logique et l'affichage du jeu."""
        if self.logic.running:
            self.logic.update_ball_position()
            self.move_paddle()  # Déplace la raquette en fonction des touches pressées
            self.draw_game()

            # Vérifie si le joueur a perdu
            if not self.logic.running:  # Le jeu s'arrête si la balle tombe
                self.game_over_text = "Game Over\nAppuyez sur une touche pour recommencer"

            # Continue d'animer le jeu
            else:
                self.root.after(20, self.update)

    def draw_game(self):
        """Dessine tous les éléments du jeu sur le canvas."""
        self.canvas.delete("all")

        # Briques
        for brick in self.logic.bricks:
            self.canvas.create_rectangle(
                brick["x1"], brick["y1"], brick["x2"], brick["y2"],
                fill=brick["color"], outline="black"
            )

        # Raquette
        paddle = self.logic.paddle
        self.canvas.create_rectangle(
            paddle["x"], paddle["y"],
            paddle["x"] + paddle["width"], paddle["y"] + paddle["height"],
            fill="white"
        )

        # Balle
        ball = self.logic.ball
        self.canvas.create_oval(
            ball["x"], ball["y"],
            ball["x"] + ball["size"], ball["y"] + ball["size"],
            fill="white"
        )

        # Score
        self.canvas.create_text(
            50, 10, text=f"Score: {self.logic.score}",
            fill="white", font=("Arial", 14)
        )

        # Afficher le texte d'attente si le jeu n'a pas commencé
        if not self.logic.running and not self.game_over_text:
            self.start_text = self.canvas.create_text(
                self.width / 2, self.height / 2,
                text="Appuyez sur une touche pour démarrer",
                fill="white", font=("Arial", 16)
            )

        # Afficher "Game Over" si le joueur a perdu
        if self.game_over_text:
            self.canvas.create_text(
                self.width / 2, self.height / 2,
                text=self.game_over_text,
                fill="red", font=("Arial", 24)
            )

    def run(self):
        """Lance la boucle principale de Tkinter."""
        self.root.mainloop()