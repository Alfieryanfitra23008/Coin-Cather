import pygame
import random
import sys

# Konstanta
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FPS = 60

# Inisialisasi pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Catcher")

# Load suara
coin_sound = pygame.mixer.Sound("PBO/UAS/Sound_Coin.mp3")
explosion_sound = pygame.mixer.Sound("PBO/Minggu 4/Sound_Bomb.mp3")

# Kelas Partikel
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 5)
        self.color = color
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.lifetime = random.randint(20, 40)
        self.alpha = 255

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        self.alpha -= 5

    def draw(self, screen):
        if self.alpha > 0:
            surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.color, self.alpha), (self.radius, self.radius), self.radius)
            screen.blit(surface, (self.x - self.radius, self.y - self.radius))

# Kelas Player
class Player:
    def __init__(self):
        self.width, self.height = 120, 60
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 10
        self.speed = 7
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Gambar keranjang dengan pegangan
        basket_color = (139, 69, 19)  # Warna cokelat untuk keranjang
        handle_color = (160, 82, 45)  # Warna cokelat untuk pegangan
        stripe_color = (205, 133, 63) # Warna untuk garis anyaman

        # Keranjang bagian bawah
        pygame.draw.rect(self.image, basket_color, (0, self.height // 2, self.width, self.height // 2))
        
        # Garis-garis anyaman horizontal
        for i in range(self.height // 2, self.height, 10):
            pygame.draw.line(self.image, stripe_color, (0, i), (self.width, i), 2)

        # Pegangan
        pygame.draw.arc(self.image, handle_color, (-20, -self.height, self.width + 40, self.height * 2), 
                        3.14, 0, 5)  # Pegangan melengkung di atas keranjang

        # Pinggiran atas keranjang
        pygame.draw.rect(self.image, handle_color, (0, self.height // 2 - 5, self.width, 10))

        self.destroyed = False
        self.fragments = []
        self.destruction_timer = 0

    def move(self, keys):
        if not self.destroyed:
            # Gerakan horizontal
            if keys[pygame.K_LEFT] and self.x > 0:
                self.x -= self.speed
            if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
                self.x += self.speed

    def destroy(self):
        self.destroyed = True
        self.destruction_timer = 60
        for _ in range(20):
            fragment = Particle(self.x + self.width // 2, self.y + self.height // 2, WHITE)
            fragment.speed_x *= 3
            fragment.speed_y *= 3
            self.fragments.append(fragment)

    def update(self):
        if self.destroyed:
            for fragment in self.fragments:
                fragment.update()
            self.destruction_timer -= 1

    def draw(self, screen):
        if not self.destroyed:
            screen.blit(self.image, (self.x, self.y))
        else:
            for fragment in self.fragments:
                fragment.draw(screen)

# Kelas Coin
class Coin:
    def __init__(self, speed):
        self.radius = 25
        self.x = random.randint(0, WIDTH - self.radius * 2)
        self.y = -self.radius * 2
        self.speed = speed
        self.angle = 0
        self.rotation_speed = random.uniform(2, 5)

        # Tentukan warna dan poin
        self.image = None
        coin_type = random.choices(
            ["yellow", "green", "blue"],
            weights=[0.6, 0.3, 0.1],
            k=1
        )[0]

        if coin_type == "yellow":
            self.image = pygame.image.load("PBO/Minggu 4/coin yellow.png")
            self.color = (255, 223, 0)  # Kuning
            self.points = 1
        elif coin_type == "green":
            self.image = pygame.image.load("PBO/Minggu 4/coin green.png")
            self.color = (0, 255, 0)  # Hijau
            self.points = 5
        elif coin_type == "blue": 
            self.image = pygame.image.load("PBO/UAS/coin blue.png")
            self.color = (0, 0, 255)  # Biru
            self.points = 10

        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))

    def update(self):
        self.y += self.speed
        self.angle += self.rotation_speed

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x + self.radius, self.y + self.radius))
        screen.blit(rotated_image, new_rect.topleft)
