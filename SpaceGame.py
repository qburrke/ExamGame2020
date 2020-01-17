import pygame
import math
import random

# Init stuff
pygame.init()
size = (700, 500)
clock = pygame.time.Clock()
run = True
win = pygame.display.set_mode(size)
win_rect = win.get_rect()
pygame.display.set_caption("Caleb's Space Game")

# Colors ###
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Game info vars ###
game_width = 2000
game_height = 2000
number_of_stars = 2000
number_of_enemies = 10
enemy_health = 2
bullet_speed = 5


# Pictures ###
player_img = pygame.image.load("//2260M01/users/student/BurkCale489/ExamGame2020/Pictures/player_space_ship.png")
player_img = pygame.transform.scale(player_img, (50, 50))

enemy_img = pygame.image.load("//2260M01/users/student/BurkCale489/ExamGame2020/Pictures/enemy_space_ship.png")
enemy_img = pygame.transform.scale(enemy_img, (120, 60))

enemy_boss_img = pygame.image.load("//2260M01/users/student/BurkCale489/ExamGame2020/Pictures/enemy_boss_space_ship.png")
enemy_boss_img = pygame.transform.scale(enemy_boss_img, (100, 40))


# Math formulas
def ds(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def findrise(y1, y2):
    return y2 - y1


def findrun(x1, x2):
    return x2 - x1


def normalize(origin, mouse_pos):
    dis = ds(origin, mouse_pos)
    return findrise(origin[0], mouse_pos[0]) / dis, findrun(origin[1], mouse_pos[1]) / dis


class Player:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.original_image = image
        self.image = self.original_image.copy()
        self.image_rect = self.original_image.get_rect(center=win_rect.center)
        self.angle = 0

    def draw(self, window):
        window.blit(self.image, self.image_rect)
        pos = pygame.mouse.get_pos()
        self.angle = 360 - 90 - math.atan2(pos[1] - size[1]/2, pos[0] - size[0]/2)*180/math.pi
        self.rotate()

    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image_rect = self.image.get_rect(center=self.image_rect.center)
        self.angle += 1


class GameBoard:
    def __init__(self, r, s, speed, player_rect):  # r is rect, s is size
        # Velocities ###
        self.up_vel = speed
        self.down_vel = -speed
        self.right_vel = -speed
        self.left_vel = speed

        # Player rect
        self.player_rect = player_rect
        self.player_center = [int(player_rect[0] + player_rect[2]/2), int(player_rect[1] + player_rect[3]/2)]
        self.player_life = 10
        print(self.player_life)

        # Border rectangles ###
        self.top_rect = pygame.Rect(r[0] - r[2] / 2, r[1] - r[3] / 2 - s, r[2] + s, s)
        self.right_rect = pygame.Rect(r[0] + r[2] / 2, r[1] - r[3] / 2, s, r[3] + s)
        self.bottom_rect = pygame.Rect(r[0] - r[2] / 2 - s, r[1] + r[3] / 2, r[2] + s, s)
        self.left_rect = pygame.Rect(r[0] - r[2] / 2 - s, r[1] - r[3] / 2 - s, s, r[3] + s)
        self.border_size = s
        self.border = [
            self.top_rect,
            self.right_rect,
            self.bottom_rect,
            self.left_rect,
        ]

        # Stars
        self.star_list = []
        for i in range(number_of_stars):
            x = random.randrange(o[0] - game_width / 2, o[0] + game_width / 2)
            y = random.randrange(o[1] - game_height / 2, o[1] + game_height / 2)
            self.star_list.append([x, y, 2])

        # Enemies
        self.enemy_list = []
        self.enemy_health_list = []
        self.enemy_vel_x_list = []
        self.enemy_vel_y_list = []
        for i in range(number_of_enemies):
            x = random.randrange(o[0] - game_width / 2, o[0] + game_width / 2)
            y = random.randrange(o[1] - game_height / 2, o[1] + game_height / 2)
            self.enemy_list.append(pygame.Rect(x, y, enemy_img.get_rect()[2], enemy_img.get_rect()[3]))
            self.enemy_vel_x_list.append(random.randrange(-5, 5))
            self.enemy_vel_y_list.append(random.randrange(-5, 5))
            self.enemy_health_list.append(enemy_health)

        # Bullet
        self.bullets = []

        # All non-player objects to do base move
        self.move_objects = [
            self.border,
            self.star_list,
            self.enemy_list,
            self.bullets,
        ]

    def draw(self, window):
        for border in self.border:
            pygame.draw.rect(window, RED, border)
        for star in self.star_list:
            pygame.draw.circle(window, WHITE, (star[0], star[1]), star[2])
        for enemy in self.enemy_list:
            window.blit(enemy_img, (enemy[0], enemy[1]))
        for bullet in self.bullets:
            pygame.draw.circle(window, RED, (int(bullet[0]), int(bullet[1])), 5)

        if self.player_life <= 0:
            print("You lost")

        self.move()

    def move(self):
        # Enemy collision ###
        for i in range(len(self.enemy_list)):
            if self.enemy_list[i].move(self.enemy_vel_x_list[i], self.enemy_vel_y_list[i]).colliderect(self.player_rect):
                self.player_life -= 1
                self.enemy_list[i][0] = random.randrange(
                    self.top_rect[0] + 5, self.right_rect[0] - enemy_img.get_rect()[2] - 5
                )
                self.enemy_list[i][1] = random.randrange(
                    self.top_rect[1] + self.border_size + 5,
                    self.bottom_rect[1] - enemy_img.get_rect()[3] - 5,
                )
                print(
                    "New X: ", self.enemy_list[i][0],
                    "New Y: ", self.enemy_list[i][1],
                )
                print(self.player_life)
                break
            collide_index = self.enemy_list[i].move(
                self.enemy_vel_x_list[i],
                self.enemy_vel_y_list[i],
            ).collidelist(self.border)
            if collide_index == -1:
                self.enemy_list[i][0] += self.enemy_vel_x_list[i]
                self.enemy_list[i][1] += self.enemy_vel_y_list[i]

            else:
                if collide_index == 0:
                    self.enemy_vel_y_list[i] *= -1
                if collide_index == 1:
                    self.enemy_vel_x_list[i] *= -1
                if collide_index == 2:
                    self.enemy_vel_y_list[i] *= -1
                if collide_index == 3:
                    self.enemy_vel_x_list[i] *= -1

        # Bullets
        for bullet in self.bullets:
            bullet[0] += bullet[2]*50
            bullet[1] += bullet[3]*50

            for i in range(len(self.enemy_list)):
                for bullet in self.bullets:
                    if self.enemy_list[i].collidepoint((bullet[0], bullet[1])):
                        self.enemy_health_list[i] -= 1
                        self.bullets.remove(bullet)

                if self.enemy_health_list[i] <= 0:
                    print("Nice kill")
                    self.enemy_health_list[i] = enemy_health
                    self.enemy_list[i][0] = random.randrange(
                        self.top_rect[0] + 5, self.right_rect[0] - enemy_img.get_rect()[2] - 5
                    )
                    self.enemy_list[i][1] = random.randrange(
                        self.top_rect[1] + self.border_size + 5,
                        self.bottom_rect[1] - enemy_img.get_rect()[3] - 5,
                    )

            for i in range(len(self.border)):
                if self.border[i].collidepoint((bullet[0], bullet[1])):
                    self.bullets.remove(bullet)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if not self.top_rect.move(0, self.up_vel).colliderect(self.player_rect):
                for i in range(len(self.move_objects)):
                    for k in range(len(self.move_objects[i])):
                        self.move_objects[i][k][1] += self.up_vel
        if keys[pygame.K_a]:
            if not self.left_rect.move(self.left_vel, 0).colliderect(self.player_rect):
                for i in range(len(self.move_objects)):
                    for k in range(len(self.move_objects[i])):
                        self.move_objects[i][k][0] += self.left_vel
        if keys[pygame.K_s]:
            if not self.bottom_rect.move(0, self.down_vel).colliderect(self.player_rect):
                for i in range(len(self.move_objects)):
                    for k in range(len(self.move_objects[i])):
                        self.move_objects[i][k][1] += self.down_vel
        if keys[pygame.K_d]:
            if not self.right_rect.move(self.right_vel, 0).colliderect(self.player_rect):
                for i in range(len(self.move_objects)):
                    for k in range(len(self.move_objects[i])):
                        self.move_objects[i][k][0] += self.right_vel

    def shoot(self):
        rise, run = normalize(self.player_center, pygame.mouse.get_pos())
        self.bullets.append(
            [self.player_center[0], self.player_center[1], rise, run]
        )

# Defining vars ###
o = (size[0] / 2, size[1] / 2)  # Center of screen
player = Player(
    o[0] - 50 / 2,
    o[1] - 50 / 2,
    50,
    50,
    player_img,
)
game = GameBoard(
    (o[0], o[1], game_width, game_height),  # origin, width, height
    50,  # border rect size
    5,  # Speed of background
    player.rect,  # Player rectangle
)

# Main Game Loop ###
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                game.shoot()

    win.fill(BLACK)
    # Draw Stuff ###
    player.draw(win)
    game.draw(win)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
