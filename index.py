import pygame
from pygame.locals import *
import time
import random

size = 40
bg_color = (133, 9, 0)
class Apple:
    def __init__(self, surface):
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = surface
        self.x = size *3
        self.y = size*3
        
    def draw(self):
        self.parent_screen.blit(self.apple,(self.x,self.y))
        
        pygame.display.flip()
    
    def move(self):
        self.x = random.randint(0,24)*size
        self.y = random.randint(0,19)*size



class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [size]*length
        self.y = [size]*length
        self.direction = ''
    
    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'
    
    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'
    
    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]


        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size
        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size

        self.draw()

    
class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000,800))
        pygame.mixer.init()
        self.play_bgm()
        self.surface.fill((133, 9, 0))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
    
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False
    def play_bgm(self):
        pygame.mixer.music.load("resources/jwbg.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.3)

    

    def render_bg(self):
        bg = pygame.image.load("resources/bgimg.jpg")
        self.surface.blit(bg, (0,0))
        
    

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_bg()
        self.snake.walk()
        self.apple.draw()
        self.score()
        pygame.display.flip()

        # snake eat  apple

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('crumch')
            self.snake.increase_length()
            self.apple.move()

        # snake collision with itself
        
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('windows_error')
                raise "Collision Occurred"
        
        # collision w boundaries
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('windows_error')
            raise "Collision Occurred"
            
    
    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)


    
    def score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(score, (800,10))
    

    def show_game_over(self):
        self.render_bg()
        self.surface.fill(bg_color)
        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"Game over! Your Score was {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (200,300))
        line2 = font.render("To play again press Enter. To exit press Escape", True, (255,255,255))
        self.surface.blit(line2, (200,350))
        pygame.display.flip()
        pygame.mixer.music.pause()

        

        
    
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                        pygame.mixer.music.rewind()

                        

                    if not pause:
                        if event.key == K_UP or event.key == K_w:
                            self.snake.move_up()                    
                        if event.key == K_DOWN or event.key == K_s:
                            self.snake.move_down()
                            
                        if event.key == K_LEFT or event.key == K_a:
                            self.snake.move_left()

                        if event.key == K_RIGHT or event.key == K_d:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False            
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            
            pygame.time.delay(100)


if __name__ == "__main__":
    game = Game()
    game.run()
    
    
    

    

    pygame.display.flip()

    
