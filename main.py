import math
import random
import pygame


FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF

YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = random.choice(GAME_COLORS)
        self.live = 300

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if(self.live >= 0):
            self.vx -= self.vx * 0.005
            self.vy -= self.vy * 0.005
            self.vy -= 1
            self.x += self.vx
            self.y -= self.vy
            self.live -= 1
            if(self.r + self.x >= WIDTH or - self.r + self.x <= 0):
                if (self.r + self.x >= WIDTH):
                    self.x -= 2 * ((self.x + self.r) - WIDTH)
                if (-self.r + self.x <= 0):
                    self.x -= 2 * (self.x - self.r)
                self.vx = -self.vx * 0.98
            if(self.r + self.y >= HEIGHT or - self.r + self.y <= 0):
                if(self.r + self.y >= HEIGHT):
                    self.y -= 2 * ((self.y + self.r) - HEIGHT)
                self.vy = -self.vy*0.98
        else:
            balls.remove(self)



    def draw(self):
        if(self.live > 0):
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )

    def hittest(self, obj):
        if(self.live >=0):
            if((self.x - obj.x)*(self.x - obj.x) + (self.y - obj.y)*(self.y - obj.y) < (self.r + obj.r)*(self.r + obj.r)):
                return True
            else:
                return False



class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 1

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.polygon(
            self.screen,
            'black',
            [[40, 450],[10, 505],[0, 500], [25, 455]]
        )
        pygame.draw.polygon(
            self.screen,
            'black',
            [[40+10, 450+20], [10+20, 505+20], [20, 515], [25+20, 455]]
        )
        pygame.draw.circle(
            self.screen,
            (self.f2_power*2, 255 - self.f2_power*2.55, 200-self.f2_power),
            (0, 550),
            60
        )
        pass
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()
    def __init__(self):
        """ Инициализация новой цели. """
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(8, 70)
        self.color = RED
        self.live = 1
        self.points = 0
    def new_target(self):
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(2, 50)
        self.color = RED
        self.live = 1
    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        txt = "Your score is {score:n}"
        font = pygame.font.SysFont(None, 24)
        img = font.render(txt.format(score = self.points), True, BLUE)
        screen.blit(img, (20, 20))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()
