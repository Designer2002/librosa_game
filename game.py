import pygame
import pickle
import random
import os
from audio_worker import make_frequency

# Инициализация Pygame
pygame.init()

# Параметры игры
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Танцевальная игра по частоте")

# Цвета
RED = (255, 0, 0)
BRIGHT = (255, 125, 255)
IDK = (115, 160, 84)

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, color):
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

    def move(self, speed):
        self.y += speed

class FrequencyData:
    def __init__(self, filename):
        if not os.path.isfile(filename):
            make_frequency
        with open(filename, "rb") as file:
            self.data = pickle.loads(file.read())
        self.adjusted_beat_frames = self.data["beat"]
        self.adjusted_onset_times = self.data["onset"]

class Game:
    def __init__(self):
        self.all_circles = []
        self.hp_circles = []
        self.circle_speed = 3
        self.clock = pygame.time.Clock()
        self.running = True
        self.index_beat = 0
        self.index_onset = 0
        self.frequency_data = FrequencyData("resources/frequency")

    def spawn_circle(self, track):
        radius = 10
        x = WIDTH // 2 + (track - 2) * 100  # Расположение круга по оси X
        return Circle(x, 0, radius)

    def run(self):
        while self.running:
            current_time = pygame.time.get_ticks()

            # Генерация кругов по битам
            if self.index_beat < len(self.frequency_data.adjusted_beat_frames) and current_time >= self.frequency_data.adjusted_beat_frames[self.index_beat] * 1000:
                track = random.randint(0, 4)  # Случайная дорожка (0-4 для 5 дорожек)
                self.all_circles.append(self.spawn_circle(track))
                self.index_beat += 1

            # Генерация кругов по онсетам
            if self.index_onset < len(self.frequency_data.adjusted_onset_times) and current_time >= self.frequency_data.adjusted_onset_times[self.index_onset] * 1000:
                track = random.randint(0, 4)  # Случайная дорожка (0-4 для 5 дорожек)
                self.all_circles.append(self.spawn_circle(track))
                self.index_onset += 1

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Движение кругов вниз
            for circle in self.all_circles:
                circle.move(self.circle_speed)

            # Отрисовка экрана
            screen.fill((0, 0, 0))
            for circle in self.all_circles:
                circle.draw(RED)

            pygame.display.flip()
            self.clock.tick(60)
