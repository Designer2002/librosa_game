import pygame
import random
import librosa.feature
import os
import sys
import tracemalloc
import  scipy.special._cdflib

if getattr(sys, 'frozen', False) and hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)

y, sr = librosa.load('resources/amogus.mp3')
tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
beat_frames = librosa.frames_to_time(librosa.util.fix_frames(librosa.beat.beat_track(y=y, sr=sr)[1]), sr=sr)
onset_env = librosa.onset.onset_strength(y=y, sr=sr)


# Инициализация Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer_music.load("resources/amogus.mp3")
pygame.mixer_music.play()

# Установка размеров экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Спавн кругов и движение вниз")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BRIGHT = (255, 125, 255)
IDK = (115, 160, 84)

# Настройки кругов
circle_speed = 3
third_distance = HEIGHT / 3 / circle_speed / 10 # Расстояние от начала экрана до его трети
time_to_reach_third = third_distance / circle_speed  # Время, за которое круг достигнет трети экрана




def move(circle, circles):
    circle.y += circle_speed
    if circle.y > HEIGHT + circle.radius * 2 + circle.radius and circle in circles:
        circles.remove(circle)  # Удаляем круг из списка

def spawn4():
    some_circles = []
    radius = 10


    for x in range(radius * -8, radius * 8, radius * 4):
        some_circles.append(Circle(WIDTH // 2 + x, 0, radius))

    return some_circles

def spawn(d):

    radius = 10
    multiplier = [x for x in range(radius * -8, radius * 8, radius * 4)]
    if d == 1:
        return Circle(WIDTH // 2 + multiplier[0], 0, radius)
    elif d == 2:
        return Circle(WIDTH // 2 + multiplier[1], 0, radius)
    elif d == 3:
        return Circle(WIDTH // 2 + multiplier[2], 0, radius)
    elif d == 4:
        return Circle(WIDTH // 2 + multiplier[3], 0, radius)

def spawn_hp(r):

    radius = 12
    if r == 1:
        return Circle(WIDTH // 2 + radius * -15, 0, radius)
    else:
        return Circle(WIDTH // 2 + radius * 15, 0, radius)


# Создание класса круга
class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, color):
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

tracemalloc.start()
all_circles = []
all_circles_FREQ = []
hp_circles = []
current_beat = 0
last_beat_time = pygame.time.get_ticks()

onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)
adjusted_beat_frames = [beat_frame - time_to_reach_third for beat_frame in beat_frames]
adjusted_onset_times = [a - time_to_reach_third for a in onset_times]

clock = pygame.time.Clock()

# print("beat frames:", beat_frames)
# print("new beat frames", adjusted_beat_frames)
# print("freq_frames", onset_times)
# print("new freq_frames", adjusted_onset_times)

# Основной игровой цикл
running = True
index=0
diag = 1
dir = 1 #1 - asc 0 - desc
end = False
while running:

    r=random.randint(1, 400)
    if r < 3 and not end:
        hp_circles.append(spawn_hp(r))
    current_time = pygame.time.get_ticks()

    if index < len(adjusted_onset_times) and pygame.time.get_ticks() >= adjusted_onset_times[index] * 1000:
        all_circles_FREQ.append(spawn(diag))
        if dir == 1:
            diag += 1
        if dir == 0:
            diag -= 1
        if diag == 4:
            dir = 0
        if diag == 1:
            dir = 1
        index += 1
    elif index == len(adjusted_onset_times):
        end = True


    # Проверка игры бита
    if current_beat < len(adjusted_beat_frames) and current_time >= adjusted_beat_frames[current_beat] * 1000:
        circles = spawn4()
        all_circles.append(circles)
        current_beat += 1


    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Движение кругов вниз
    for circles in all_circles:
        for circle in circles:
            move( circle, all_circles)
    for circle in all_circles_FREQ:
        move(circle, all_circles_FREQ)
    for circle in hp_circles:
        move(circle, hp_circles)

    # Отрисовка экрана

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(0, HEIGHT // 3, WIDTH, HEIGHT // 3))

    for circles in all_circles:
        for circle in circles:
            circle.draw(RED)
    for circle in all_circles_FREQ:
        circle.draw(BRIGHT)
    for circle in hp_circles:
        circle.draw(IDK)

    pygame.draw.rect(surface, (0, 0, 0, 225), pygame.Rect(0, HEIGHT, WIDTH, HEIGHT // 3))
    screen.blit(surface, (0, HEIGHT - HEIGHT//3))
    pygame.draw.rect(surface, (0, 0, 0, 225), pygame.Rect(0, 0, WIDTH, HEIGHT // 3))
    screen.blit(surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print(tracemalloc.get_traced_memory())
tracemalloc.stop()
print(len(all_circles))