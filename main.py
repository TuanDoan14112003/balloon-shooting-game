import pygame
import random


class Tank(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/image/tank.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vel = 4

    def update(self, screen_width, screen_height):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left - self.vel > 0:
            self.rect.x -= self.vel
        if key[pygame.K_RIGHT] and self.rect.right + self.vel < screen_width:
            self.rect.x += self.vel
        if key[pygame.K_DOWN] and self.rect.bottom + self.vel < screen_height:
            self.rect.y += self.vel
        if key[pygame.K_UP] and self.rect.top - self.vel > 0:
            self.rect.y -= self.vel


class Balloon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/image/balloon.png"), (64, 64))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vel_x = 2
        self.vel_y = 2

    def update(self, screen_width, screen_height):
        if random.randint(1, 50) == 1:
            self.vel_x = -self.vel_x
        if random.randint(1, 1000) == 1:
            self.vel_y = -self.vel_y

        if self.rect.right + self.vel_x > screen_width / 3 or self.rect.left + self.vel_x < 0:
            self.vel_x = - self.vel_x
        if self.rect.bottom + self.vel_y > screen_height or self.rect.top + self.vel_y < 0:
            self.vel_y = - self.vel_y
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y


class Bullet(pygame.sprite.Sprite):
    missed_shots = 0

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface([15, 15])

        pygame.draw.rect(self.image,
                         (255, 0, 0),
                         pygame.Rect(0, 0, 15, 15))

        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vel = 20

    def update(self):
        self.rect.x -= self.vel
        if self.rect.right < 0:
            Bullet.missed_shots += 1
            self.kill()

    @classmethod
    def reset_missed_shots(cls):
        cls.missed_shots = 0


class Game:
    def __init__(self, screen_width, screen_height):
        pygame.init()
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.tank_and_balloon = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.tank = Tank((self.width * 3 / 4, self.height // 2))
        self.balloon = Balloon((self.width // 4, self.height // 2))
        self.tank_and_balloon.add(self.tank)
        self.tank_and_balloon.add(self.balloon)
        self.pop_sound = pygame.mixer.Sound("assets/sound/pop.wav")
        self.laser_sound = pygame.mixer.Sound("assets/sound/laser.wav")
        self.game_over = False
        self.quit_game = False
        Bullet.reset_missed_shots()

    def display_missed_shots(self):
        missed_shots_count_font = pygame.font.Font("assets/font/game_over.ttf", 64)
        missed_shots_count_text = missed_shots_count_font.render(f"Missed shots: {Bullet.missed_shots}", True,
                                                                 (255, 255, 255))
        self.screen.blit(missed_shots_count_text, (0, 0))

    def end_game(self):
        self.game_over = True
        self.pop_sound.play()
        self.balloon.vel_x = 0
        self.balloon.vel_y = 0
        self.tank.vel = 0
        self.balloon.kill()
        for bullet in self.bullets:
            bullet.vel = 0

    def display_game_over(self):
        game_over_font = pygame.font.Font('assets/font/game_over.ttf', 128)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (self.width // 2, self.height // 2)

        play_again_font = pygame.font.Font('assets/font/game_over.ttf', 64)
        play_again_text = play_again_font.render("Press ENTER to play again", True, (255, 255, 255))
        play_again_text_rect = play_again_text.get_rect()
        play_again_text_rect.center = (self.width // 2, self.height // 2 + 50)

        self.screen.blit(game_over_text, game_over_text_rect)
        self.screen.blit(play_again_text, play_again_text_rect)

    def start_game(self):
        clock = pygame.time.Clock()
        while not self.quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over:
                        self.laser_sound.play()
                        new_bullet = Bullet((self.tank.rect.centerx, self.tank.rect.centery))
                        self.bullets.add(new_bullet)
                    if event.key == pygame.K_RETURN and self.game_over:
                        self.__init__(self.width, self.height)

            self.tank_and_balloon.update(self.width, self.height)
            self.bullets.update()
            self.screen.fill((0, 0, 0))
            self.display_missed_shots()
            self.tank_and_balloon.draw(self.screen)
            self.bullets.draw(self.screen)

            if pygame.sprite.spritecollideany(self.balloon, self.bullets) and not self.game_over:
                self.end_game()

            if self.game_over:
                self.display_game_over()

            pygame.display.update()
            clock.tick(60)


new_game = Game(900, 900)
new_game.start_game()

# def display_missed_shots():
#     missed_shots_count_font = pygame.font.Font("assets/font/game_over.ttf", 64)
#     missed_shots_count_text = missed_shots_count_font.render(f"Missed shots: {Bullet.missed_shots}", True,
#                                                              (255, 255, 255))
#     screen.blit(missed_shots_count_text, (0, 0))
#
#
# def end_game():
#     global balloon, tank, bullets, game_over
#     game_over = True
#     pop_sound.play()
#     balloon.vel_x = 0
#     balloon.vel_y = 0
#     tank.vel = 0
#     balloon.kill()
#     for bullet in bullets:
#         bullet.vel = 0
#
#
# def initialize():
#     global balloon, tank, bullets, game_over, missed_shots
#     print('rest')
#     game_over = False
#     pop_sound.play()
#     balloon.vel_x = 2
#     balloon.vel_y = 2
#     tank.vel = 4
#     balloon.kill()
#     for bullet in bullets:
#         bullet.vel = 20
#
#
# def display_game_over():
#     game_over_font = pygame.font.Font('assets/font/game_over.ttf', 128)
#     over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
#     over_text_rect = over_text.get_rect()
#     over_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
#     screen.blit(over_text, over_text_rect)
#
# game_over = False
# quit_game = False
#
# tank_and_balloon = pygame.sprite.Group()
# bullets = pygame.sprite.Group()
# tank = Tank((SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT // 2))
# balloon = Balloon((SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
# tank_and_balloon.add(tank)
# tank_and_balloon.add(balloon)
# pop_sound = pygame.mixer.Sound("assets/sound/pop.wav")
# laser_sound = pygame.mixer.Sound("assets/sound/laser.wav")
# clock = pygame.time.Clock()
# missed_shots = 0
#
# while not quit_game:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             quit_game = True
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE and not game_over:
#                 laser_sound.play()
#                 new_bullet = Bullet((tank.rect.centerx, tank.rect.centery))
#                 bullets.add(new_bullet)
#             if event.key == pygame.K_RETURN:
#                 restart_game()
#
#     tank_and_balloon.update()
#     bullets.update()
#     screen.fill((0, 0, 0))
#     display_missed_shots()
#     tank_and_balloon.draw(screen)
#     bullets.draw(screen)
#
#     if pygame.sprite.spritecollideany(balloon, bullets) and not game_over:
#         end_game()
#
#     if game_over:
#         display_game_over()
#
#     pygame.display.update()
#     clock.tick(60)
