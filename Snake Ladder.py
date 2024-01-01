import pygame
from sys import exit
from random import randint

# Player object 
class Player:
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name


def board_rectangles():
    array = []
    for row in range(10):
        row_rectangles = []
        for col in range(10):
            rect = pygame.Rect(col * (500 // 10), row * (500 // 10), (500 // 10), (500 // 10))
            row_rectangles.append(rect)
        array.append(row_rectangles)
    return array

def player_position(dice,player_x,player_y):
    global rectangles_array

    current_x = player_x // 50
    arr_x = [9,8,7,6,5,4,3,2,1,0]

    new_x = current_x + dice
    new_y = player_y // 50

    # Reverse movement
    if new_y % 2 == 0 and new_y != 0:
        new_x = (player_x// 50) - dice

    if new_y <= 0 and current_x <= 9:
        new_x = current_x - dice
        
        if (dice - current_x) <= 0 and current_x < 7:
            new_x = current_x - dice
            
        elif (dice - current_x) >= 0: 
            new_x = current_x
            
    # Boundary
    if new_x > 9 and new_y != 0:
        new_y -= 1
        x_index = abs(10 - current_x - dice)
        new_x = arr_x[x_index]
    elif new_x < 0:
        new_y -= 1
        x_index = abs(dice - current_x - 10)
        new_x = arr_x[x_index]
                
    rect = rectangles_array[new_y][new_x]
    player_x,player_y = rect.x ,rect.y 
    return player_x, player_y

def move_player(player,dice):
    snake_dict = {
        (100,300):(0,400),
        (450,200):(450,450),
        (200,100):(300,200),
        (450,0):(350,100),
        (150,0):(0,150),
    }
    ladder_dict = {
        (200,450):(100,200),
        (300,400):(400,250),
        (350,200):(400,100),
        (150,150):(100,50),
    }
    player.x,player.y = player_position(dice,player.x,player.y)
    if (player.x,player.y) in snake_dict:
        player.x,player.y = snake_dict[(player.x,player.y)]
        return "Snake"
    if (player.x,player.y) in ladder_dict:
        player.x,player.y = ladder_dict[(player.x,player.y)]
        return "Ladder"
        

pygame.init()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption('Snake And Ladder')
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf',50)
dice_number = 1
player1 = Player(0,450,"Player 1")             # Instance
player2 = Player(0,450,"Player 2")
game_state = True
player = True
rectangles_array = board_rectangles()
text = font.render("", False, 'black')
text_2 = font.render("", False, 'black')
sound = pygame.mixer.Sound('audio/jump.mp3')
sound.set_volume(0.2)

bg = pygame.image.load('graphics/Untitled design.png').convert()
bg_rect = bg.get_rect(topleft = (0,0))

player1_image = pygame.image.load('graphics/player/player1.png').convert_alpha()
player2_image = pygame.image.load('graphics/player/player2.png').convert_alpha()

dice_dict = { 
    1:pygame.image.load('graphics/dice/dice_1.png').convert_alpha(),
    2:pygame.image.load('graphics/dice/dice_2.png').convert_alpha(),
    3:pygame.image.load('graphics/dice/dice_3.png').convert_alpha(),
    4:pygame.image.load('graphics/dice/dice_4.png').convert_alpha(),
    5:pygame.image.load('graphics/dice/dice_5.png').convert_alpha(),
    6:pygame.image.load('graphics/dice/dice_6.png').convert_alpha(),
    }

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_state:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                dice_number = randint(1,6)
                sound.play()
                if player:
                    jump = move_player(player1,dice_number)
                    text = font.render(f"{player1.name}",False,('black'))
                    if jump != None:
                        text_2 = font.render(f"{jump}",False,('black'))
                    else:
                        text_2 = font.render(f"Turn",False,'black')
                    player = False
                else:
                    jump = move_player(player2,dice_number)
                    text = font.render(f"{player2.name}",False,('black'))
                    if jump != None:
                        text_2 = font.render(f"{jump}",False,('black'))
                    else:
                        text_2 = font.render(f"Turn",False,'black')
                    player = True
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = True
                player1.x,player1.y = 0,450
                player2.x,player2.y = 0,450
                text = font.render("", False, 'black')
                text_2 = font.render("",False,('black'))

    if game_state:
        screen.fill('white')
        screen.blit(bg,bg_rect)
        screen.blit(text,(540,300))
        screen.blit(text_2,(550,340))
        screen.blit(dice_dict[dice_number],(550,100))
        screen.blit(player1_image,(player1.x,player1.y))
        screen.blit(player2_image,(player2.x+20,player2.y+10))

        if (player1.x <= 0 and player1.y <= 0):
            game_state = False
            flag = 1
        elif (player2.x <= 0 and player2.y <= 0):
            game_state = False
            flag = 0
    elif flag == 1 and game_state == False:
        screen.fill((250, 255, 104, 1))
        text = font.render("Player 1 Wins!",False,'black')
        screen.blit(text,(250,220))
    elif flag == 0 and game_state == False:
        screen.fill((245, 67, 67, 0.8))
        text = font.render("Player 2 Wins!",False,'black')
        screen.blit(text,(250,220))

    pygame.display.update()
    clock.tick(60)