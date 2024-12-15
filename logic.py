"""
logic.py
Classe principale pour gérer la logique du jeu casse-brique.
"""

import random

class GameLogic:
    def __init__(self, width, height):
        """Initialise la logique du jeu."""
        self.width = width
        self.height = height

        # Balle
        self.ball = {
            "x": width // 2,
            "y": height // 2,
            "size": 10,
            "dx": random.choice([-3, 3]),
            "dy": -3,
        }

        # Raquette
        self.paddle = {
            "x": width // 2 - 50,
            "y": height - 30,
            "width": 100,
            "height": 10,
            "speed": 20,
        }

        # Briques
        self.bricks = []
        self.create_bricks()

        # Score
        self.score = 0

        # État du jeu
        self.running = False

    def create_bricks(self):
        """Crée les briques initiales."""
        rows = 5
        cols = 10
        brick_width = self.width // cols
        brick_height = 20

        colors = ["red", "orange", "yellow", "green", "blue"]

        for row in range(rows):
            for col in range(cols):
                self.bricks.append({
                    "x1": col * brick_width,
                    "y1": row * brick_height,
                    "x2": (col + 1) * brick_width,
                    "y2": (row + 1) * brick_height,
                    "color": colors[row % len(colors)],
                })

    def update_ball_position(self):
        """Met à jour la position de la balle et gère les collisions."""
        ball = self.ball
        ball["x"] += ball["dx"]
        ball["y"] += ball["dy"]

        # Collision avec les murs
        if ball["x"] <= 0 or ball["x"] + ball["size"] >= self.width:
            ball["dx"] *= -1
        if ball["y"] <= 0:
            ball["dy"] *= -1

        # Collision avec le bas de l'écran (perte)
        if ball["y"] + ball["size"] >= self.height:
            self.running = False  # Arrête le jeu

        # Collision avec la raquette
        paddle = self.paddle
        if (paddle["x"] < ball["x"] < paddle["x"] + paddle["width"] and
                paddle["y"] < ball["y"] + ball["size"] < paddle["y"] + paddle["height"]):
            ball["dy"] *= -1

        # Collision avec les briques
        self.check_brick_collisions()

    def check_brick_collisions(self):
        """Vérifie et gère les collisions entre la balle et les briques."""
        ball = self.ball
        ball_next_x = ball["x"] + ball["dx"]
        ball_next_y = ball["y"] + ball["dy"]
        ball_size = ball["size"]

        for brick in self.bricks[:]:
            # Coordonnées de la brique
            x1, y1, x2, y2 = brick["x1"], brick["y1"], brick["x2"], brick["y2"]

            # Collision détectée ?
            if (x1 <= ball_next_x + ball_size and ball_next_x <= x2 and
                    y1 <= ball_next_y + ball_size and ball_next_y <= y2):
                # Détermine le côté touché
                if ball_next_y + ball_size - y1 < abs(ball["dy"]):  # Haut
                    ball["dy"] *= -1
                elif y2 - ball_next_y < abs(ball["dy"]):  # Bas
                    ball["dy"] *= -1
                elif ball_next_x + ball_size - x1 < abs(ball["dx"]):  # Gauche
                    ball["dx"] *= -1
                elif x2 - ball_next_x < abs(ball["dx"]):  # Droite
                    ball["dx"] *= -1

                # Supprimer la brique et augmenter le score
                self.bricks.remove(brick)
                self.score += 10
                break  # Une collision par frame

    def move_paddle(self, direction):
        """Déplace la raquette vers la gauche ou la droite."""
        if direction == "left" and self.paddle["x"] > 0:
            self.paddle["x"] -= self.paddle["speed"]
        elif direction == "right" and self.paddle["x"] + self.paddle["width"] < self.width:
            self.paddle["x"] += self.paddle["speed"]