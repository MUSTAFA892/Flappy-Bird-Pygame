import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 512
ground_height = 100
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# define colours
white = (255, 255, 255)
black = (0, 0, 0)

# define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
high_score = 0  # For the scoreboard

# load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
play_button_img = pygame.image.load('img/play.png')  # New play button image
game_over_img = pygame.image.load('img/gameover.png')
message_img = pygame.image.load('img/message.png')  # Game over image
scoreboard_img = pygame.image.load('img/scoreboard.png')  # Scoreboard image

# Scale the images
scale_factor_message = 1.2  # Adjust as needed for message image
scale_factor_play_button = 0.5  # Adjust as needed for play button

message_img = pygame.transform.scale(message_img, (int(message_img.get_width() * scale_factor_message), int(message_img.get_height() * scale_factor_message)))
play_button_img = pygame.transform.scale(play_button_img, (int(play_button_img.get_width() * scale_factor_play_button), int(play_button_img.get_height() * scale_factor_play_button)))
game_over_img = pygame.transform.scale(game_over_img, (int(game_over_img.get_width() * scale_factor_message), int(game_over_img.get_height() * scale_factor_message)))
scoreboard_img = pygame.transform.scale(scoreboard_img, (int(scoreboard_img.get_width() * scale_factor_message), int(scoreboard_img.get_height() * scale_factor_message)))

# Load number images (0-9)
number_images = []
for num in range(10):
    img = pygame.image.load(f'img/{num}.png')  # Ensure images are named '0.png', '1.png', ..., '9.png'
    number_images.append(img)

def draw_score(score, x, y):
    score_str = str(score)
    current_x = x
    for digit in score_str:
        if digit != '0':  # Skip the digit '0'
            digit_img = number_images[int(digit)]
            screen.blit(digit_img, (current_x, y))
            current_x += digit_img.get_width()

def draw_scoreboard(current_score, high_score, x, y):
    # Draw the scoreboard background
    screen.blit(scoreboard_img, (x, y))
    
    # Draw the current score
    draw_score(current_score, x + 410, y + 80)  # Adjust position as needed
    
    # Draw the high score
    draw_score(high_score, x + 410, y + 170)  # Adjust position as needed

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < screen_height - ground_height:
                self.rect.y += int(self.vel)

        if not game_over:
            keys = pygame.key.get_pressed()
            if (pygame.mouse.get_pressed()[0] == 1 or keys[K_SPACE] or keys[K_UP]) and not self.clicked:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0 and not (keys[K_SPACE] or keys[K_UP]):
                self.clicked = False

            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

play_button = Button(screen_width // 2 - play_button_img.get_width() // 2, screen_height // 2 + 100, play_button_img)

run = True
while run:

    clock.tick(fps)

    screen.blit(bg, (0, 0))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    screen.blit(ground_img, (ground_scroll, screen_height - ground_height))
    screen.blit(ground_img, (ground_scroll + screen_width, screen_height - ground_height))

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and not pass_pipe:
            pass_pipe = True
        if pass_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_score(score, screen_width // 2 - 20, 20)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    if flappy.rect.bottom >= screen_height - ground_height:
        game_over = True
        flying = False

    if not game_over and flying:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if ground_scroll <= -screen_width:
            ground_scroll = 0

        pipe_group.update()

    if not flying and not game_over:
        screen.blit(message_img, (screen_width // 2 - message_img.get_width() // 2, screen_height // 2 - message_img.get_height() // 2))

    if game_over:
        if score > high_score:
            high_score = score
        screen.blit(game_over_img, (screen_width // 2 - game_over_img.get_width() // 2, screen_height // 2 - game_over_img.get_height() // 2 - 150))
        draw_scoreboard(score, high_score, screen_width // 2 - scoreboard_img.get_width() // 2, screen_height // 2 - scoreboard_img.get_height() // 2 + 50)
        if play_button.draw():
            score = reset_game()
            game_over = False
            flying = False

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and not flying and not game_over:
                flying = True
                game_over = False
                flappy.vel = -10

    pygame.display.update()
