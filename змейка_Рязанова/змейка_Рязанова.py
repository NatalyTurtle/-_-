import pygame
import math
import random
import time
import sys


#константы
WIDTH = 640
HEIGHT = 640
CELL = 32
SQUARE = int(WIDTH/CELL)
TIME = 100

#цвета
C1 = (138, 138, 138)
C2 = (132, 132, 132)
RED = (140, 29, 4)
BLUE = (0,0,80)
BLACK = (0, 0, 0)

class Background:
    
    def paint(self, surface):
        surface.fill( C1 )
        counter = 0
        for row in range(SQUARE):
            for col in range(SQUARE):
                if counter % 2 == 0:
                    pygame.draw.rect(surface, C2, (col * CELL, row * CELL, CELL, CELL))
                if col == SQUARE - 1:
                    continue
                counter += 1
                
class Apple:
    
    def __init__(self):
        self.spawn()
        
    def spawn(self):
        self.posX = random.randrange( 0, WIDTH , CELL )
        self.posY = random.randrange( 0, HEIGHT , CELL ) 
        
    def paint( self , surface ):
        pygame.draw.rect(surface , RED , (self.posX,self.posY, CELL, CELL) )
            
class Snake:
    
    def __init__(self):
        self.headX = random.randrange( 0, WIDTH , CELL )
        self.headY = random.randrange( 0, HEIGHT , CELL )
        self.colour = BLUE
        self.state = "STOP"
        self.bodies = []
        self.colour_of_body = 50
    
    def move_head (self):
        if self.state == "UP":
            self.headY -= CELL
        elif self.state == "DOWN":
            self.headY += CELL
        elif self.state == "RIGHT":
            self.headX += CELL
        elif self.state == "LEFT":
            self.headX -=  CELL

    def move_body (self):
        
        if len(self.bodies) > 0:
            for i in range (len(self.bodies) -1, -1, -1):
                if i == 0:
                    self.bodies[0].posX = self.headX
                    self.bodies[0].posY = self.headY
                else:
                    self.bodies[i].posX = self.bodies[i-1].posX
                    self.bodies[i].posY = self.bodies[i-1].posY

    def die(self):
        
        self.headX = random.randrange( 0, WIDTH , CELL )
        self.headY = random.randrange( 0, HEIGHT , CELL )
        self.state = "STOP"
        self.bodies = []
        self.colour_of_body = 50
        
   
    def plus_body (self):
        self.colour_of_body += 2
        body = Body( (0, 0, self.colour_of_body) , self.headX , self.headY)
        self.bodies.append(body)
        
        
    def paint (self, surface):
        pygame.draw.rect(surface, self.colour , (self.headX, self.headY , CELL , CELL ) )
        if len(self.bodies) > 0:
            for body in self.bodies:
                body.draw(surface)
                
class Colission:
    
    def between_oblects(self, snake, apple):
        distance = math.sqrt( math.pow( ( snake.headX - apple.posX ),2 ) + math.pow( (snake.headY - apple.posY), 2 ) )
        return distance < CELL
    
    def between_snake_and_walls( self, snake):
        if snake.headX < 0 or snake.headX > WIDTH - CELL or snake.headY < 0 or snake.headY > HEIGHT - CELL:
            return True
        return False
    
    def between_head_and_body(self,snake):
        for body in snake.bodies:
            distance = math.sqrt( math.pow( ( snake.headX - body.posX ),2 ) + math.pow( (snake.headY - body.posY), 2 ) )            
            if distance < CELL:
                return True
        return False 
    
class Body:
    
    def __init__(self, colour, posX, posY ):
        self.colour = colour 
        self.posX = posX
        self.posY = posY
    
    def draw(self,surface):
        pygame.draw.rect(surface, self.colour, ( self.posX , self.posY , CELL , CELL ) )
        
class Score:
    
    def __init__(self):
        self.points = 0
        self.font = pygame.font.SysFont('monospace', 30, bold = False)
        self.font2 = pygame.font.SysFont('monospace', 20, bold = False)
        self.font3 = pygame.font.SysFont('monospace', 30, bold = True)
        
    def increase(self):
        self.points += 1
     
    def reset(self):
        self.points = 0 
        
    def show(self, surface):
        label = self.font.render('Score: ' + str(self.points), 1, BLACK )
        label_2 = self.font2.render('made by', 1, BLACK)
        label_3 = self.font3.render('Ryazanova', 1, BLACK)
        surface.blit(label,(2,2))
        surface.blit(label_2,(380,610))
        surface.blit(label_3,(470,605))
   
        
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")

    #объекты игры
    background = Background()
    apple = Apple()
    snake = Snake()
    collision = Colission()
    score = Score()
    
    #основной алгоритм
    while True:
        background.paint( screen )   
        snake.paint( screen )
        apple.paint( screen )
        score.show( screen )
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake.state != "DOWN":
                        snake.state = "UP"
                if event.key == pygame.K_DOWN:
                    if snake.state != "UP":
                        snake.state = "DOWN"
                if event.key == pygame.K_RIGHT:
                    if snake.state != "LEFT":
                        snake.state = "RIGHT" 
                if event.key == pygame.K_LEFT:
                    if snake.state != "RIGHT":
                        snake.state = "LEFT" 
                if event.key == pygame.K_TAB:                   
                    snake.state = "STOP"
       
        if collision.between_oblects(snake, apple):
            apple.spawn()
            snake.plus_body()
            score.increase()
        
        #движение
        if snake.state != "STOP":
            snake.move_body()
            snake.move_head()
            
        if collision.between_snake_and_walls(snake):
            # проигрыш
            snake.die()
            apple.spawn()
            score.reset()
        
        if collision.between_head_and_body(snake):
            # проигрыш
            snake.die()
            apple.spawn()           
            score.reset()
            
        pygame.time.delay(100)

        pygame.display.update()
   
main()
