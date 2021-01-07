import pygame
from pygame.constants import WINDOWHITTEST
import random
import os

pygame.mixer.init()

pygame.init()

#colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)

#Creating window
screen_width=900
screen_height=600
gameWindow = pygame.display.set_mode((screen_width,screen_height))

#background images
bgimg = pygame.image.load("nobita.jpg")
bgimg = pygame.transform.scale(bgimg,(screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snakes with akshit")
pygame.display.update()
font = pygame.font.SysFont(None, 55)
clock = pygame.time.Clock()


def text_Screen(text,color, x,y):
    screen_text= font.render(text,True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow,color,snk_list,snake_size):
    #print(snk_list)
    for x,y in snk_list:
        pygame.draw.rect(gameWindow,color,[x,y,snake_size,snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,200,190))
        text_Screen("Welcome to Snakes", black ,270 , 250)
        text_Screen("Press space bar to play", black ,240 , 290)
        for event in pygame.event.get():
            # print(event)
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("man.mp3")
                    pygame.mixer.music.play()
                    gameLoop()

        pygame.display.update()
        #clock = pygame.time.Clock()
        clock.tick(60)

# game loop
def gameLoop():
    #Game Specific variables
    exit_game = False
    game_over = False
    snake_x=45
    snake_y=55
    velocity_x=4
    velocity_y=4
    snk_list=[]
    snk_length = 1

    clock = pygame.time.Clock()

    # check if hiscore file exists
    if (not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")
    
    with open("hiscore.txt","r") as f:
        hiscore = f.read()

    food_x = random.randint(20,screen_width/2)
    food_y = random.randint(20,screen_height/2)
    score = 0
    init_velocity=5
    snake_size=10
    fps = 60
    while not exit_game:
        if game_over:
            with open("hiscore.txt","w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            text_Screen("GAME OVER! Press Enter To Continue", red, 120,250)
            for event in pygame.event.get():
                # print(event)
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                # print(event)
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x=init_velocity
                        velocity_y=0
                    if event.key == pygame.K_LEFT:
                        velocity_x=-init_velocity
                        velocity_y=0
                    if event.key == pygame.K_UP:
                        velocity_y=-init_velocity
                        velocity_x=0
                    if event.key == pygame.K_DOWN:
                        velocity_y=init_velocity
                        velocity_x=0

                    if event.key ==pygame.K_q:
                        score +=10
                        init_velocity=3


            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
            if abs(snake_x - food_x)<7 and abs(snake_y - food_y)<7:
                score+=10
                # print(hiscore)
                #print("Score :", score*10)
                snk_length+=5
                food_x = random.randint(20,screen_width/2)
                food_y = random.randint(20,screen_height/2)
                if score > int(hiscore):
                    hiscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0,0))
            text_Screen("Score : "+str(score) +  "      Hiscore: "+str(hiscore),red, 5 ,5)
            pygame.draw.rect(gameWindow,red, [food_x,food_y,snake_size,snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
            if len(snk_list)>snk_length:
                del snk_list[0]
            
            if head in snk_list[:-1]:
                pygame.mixer.music.load("apna.mp3")
                pygame.mixer.music.play()
                game_over=True

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y > screen_height:
                game_over= True
                pygame.mixer.music.load("apna.mp3")
                pygame.mixer.music.play()
            # pygame.draw.rect(gameWindow,black,[snake_x,snake_y,snake_size,snake_size])
            plot_snake(gameWindow, black,snk_list,snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()