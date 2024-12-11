class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

    def move(self, speed):
        self.y += speed