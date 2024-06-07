import pygame
import random

pygame.init()

class Game:
    def __init__(self):
        self.wnx = 1000
        self.score = 0
        self.wny = 600
        self.lost = False
        self.player_speed = 1
        self.screen = pygame.display.set_mode((self.wnx, self.wny))
        self.playing = True
        self.fps = 100
        self.jx = random.randint(0, 10)
        self.jy = random.randint(0, 10)
        self.clock = pygame.time.Clock()
        self.player_rect = pygame.Rect(self.wnx / 2, self.wny / 2, 40, 40)
        self.random_rect = pygame.Rect(random.randint(0, self.wnx - 104), random.randint(0, self.wny - 104), 57, 55)
        self.moving = ""

        # Load and scale images
        self.bg = pygame.image.load("bg.png")
        self.bg = pygame.transform.scale(self.bg, (self.wnx*4+105, self.wny*4+80))
        self.player_image = pygame.image.load("player.png")
        self.player_image = pygame.transform.scale(self.player_image, (40, 40))
        self.food_image = pygame.image.load("food.png")
        self.food_image = pygame.transform.scale(self.food_image, (104, 104))
        self.jumpscare_image = pygame.image.load("jumpscare.png")
        self.jumpscare_sound = pygame.mixer.Sound("jumpscare.mp3")
        self.coin = pygame.mixer.Sound("coin_2.mp3")
        self.jumpscare_sound.set_volume(1.0)
        self.music = pygame.mixer.Sound("music.mp3")
        self.music.play(loops=-1)
        self.music.set_volume(1.0)

    def run(self):
        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    break

            self.window()
            self.player_handle()
            self.food_handle()
            pygame.display.flip()
            self.clock.tick(self.fps)
        

        if self.lost:
            self.music.stop()
            for i in range(998):
                self.jumpscare()    

        # Show jumpscare at the end of the game


    def player_handle(self):
        self.pressed = pygame.key.get_pressed()
        if self.pressed[pygame.K_UP] and not self.moving == "DOWN":
            self.moving = "UP"
        if self.pressed[pygame.K_DOWN] and not self.moving == "UP":
            self.moving = "DOWN"
        if self.pressed[pygame.K_LEFT] and not self.moving == "RIGHT":
            self.moving = "LEFT"
        if self.pressed[pygame.K_RIGHT] and not self.moving == "LEFT":
            self.moving = "RIGHT"

        if self.moving == "LEFT":
            self.player_rect.x -= self.player_speed
        if self.moving == "RIGHT":
            self.player_rect.x += self.player_speed
        if self.moving == "UP":
            self.player_rect.y -= self.player_speed
        if self.moving == "DOWN":
            self.player_rect.y += self.player_speed

        if self.player_rect.colliderect(self.random_rect):
            self.collision()
            self.score += 1
            if self.fps <= 600:
                self.fps += 20
            else:
                self.player_speed += 1 

        if self.player_rect.x < 0 or self.player_rect.x > 960 or self.player_rect.y < 0 or self.player_rect.y > 560:
            self.loose()

        self.screen.blit(self.player_image, (self.player_rect.x, self.player_rect.y))

    def loose(self):
        self.playing = False
        self.lost = True

    def food_handle(self):
        self.screen.blit(self.food_image, (self.random_rect.centerx - self.random_rect.w + 3, self.random_rect.centery - self.random_rect.h + 3))
        

    def collision(self):
        self.coin.play()
        self.random_rect = pygame.Rect(random.randint(0, self.wnx - 104), random.randint(0, self.wny - 104),  57, 55)
        

    def window(self):
        self.screen.fill((120, 10, 10))
        self.screen.blit(self.bg, (-1553, -940))
        pygame.display.set_caption(f'MINOR GAME | {self.score}')

    def jumpscare(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        if self.jx >= 3:
            self.screen.blit(pygame.transform.scale(self.jumpscare_image, (1000, 600)), (self.jx, self.jy))
        else:
            self.screen.fill((0, 0, 0))
        self.jx = random.randint(0, 10)
        self.jy = random.randint(0, 10)
        pygame.mixer.Sound.play(self.jumpscare_sound)
        pygame.display.flip()

game = Game()
game.run()
pygame.quit()
