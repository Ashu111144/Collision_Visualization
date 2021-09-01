import random
import pygame

GREEN1 = (0, 255, 0)  # Healthy cells
RED = (255, 0, 0)  # Infected cells
GREEN2 = (0, 100, 0)  # Healthy cells not susecptible
BLACK = (0, 0, 0)  # Dead cells
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (225, 198, 153)
SCREEN_SIZE = (800, 800)

speed = [0.5, -0.5]


class Cell(pygame.sprite.Sprite):
    def __init__(self, color, speed, width, height):
        super().__init__()
        self.color = color
        self.speed = speed
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.radius = width // 2  # 5
        center = [width // 2, height // 2]
        pygame.draw.circle(self.image, self.color,
                           center, self.radius, width=0)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 400)
        self.rect.y = random.randint(50, 700)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.dir = pygame.math.Vector2(1, 0).rotate(random.randrange(360))

    def update(self):
        self.pos += self.dir * self.speed

        border_rect = pygame.Rect(0, 50, 400, 700)
        if self.pos.x - self.radius < border_rect.left:
            self.pos.x = border_rect.left + self.radius
            self.dir.x = abs(self.dir.x)
        elif self.pos.x + self.radius > border_rect.right:
            self.pos.x = border_rect.right - self.radius
            self.dir.x = -abs(self.dir.x)
        if self.pos.y - self.radius < border_rect.top:
            self.pos.y = border_rect.top + self.radius
            self.dir.y = abs(self.dir.y)
        elif self.pos.y + self.radius > border_rect.bottom:
            self.pos.y = border_rect.bottom - self.radius
            self.dir.y = -abs(self.dir.y)

        for other_cell in all_cells:
            if all_cells != self:
                distance_vec = self.pos - other_cell.pos
                if 0 < distance_vec.length_squared() < (self.radius*2) ** 2:
                    self.dir.reflect_ip(distance_vec)
                    other_cell.dir.reflect_ip(distance_vec)

        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)


pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Covid-19 Simualtion")
all_cells = pygame.sprite.Group()  # PEP8: lower_case_name

for i in range(100):
    cell = Cell(GREEN1, 5, 10, 10)  # PEP8: lower_case_name
    all_cells.add(cell)

clock = pygame.time.Clock()

end = False
while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
    all_cells.update()
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, BLACK, (0, 50, 400, 700), 3)
    all_cells.draw(screen)
    pygame.display.flip()
    clock.tick(30)  # to use less CPU
