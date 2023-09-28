import pygame
import random
import Messages
import __init
import numpy as np
import reinforce
import collision
import time

pygame.init()
start_time = time.time() #stop the program after a while

WIDTH = __init.WIDTH
HEIGHT = __init.HEIGHT
s_top = __init.SHIP_top
s_bottom = __init.SHIP_bottom
s_height = __init.SHIP_height
screen = pygame.display.set_mode((WIDTH, HEIGHT))

win_rect, win_text = Messages.win_rect, Messages.win_text
lose_rect, lose_text = Messages.lose_rect, Messages.lose_text

def update_draw(screen, x_pos, y_pos, begin, end, randY):
    screen.fill((30, 60, 60))
    pygame.draw.circle(screen, (155, 155, 155), (WIDTH / 2, HEIGHT * 2), radius= WIDTH)
    obj = pygame.draw.polygon(screen, (255, 130, 240), 
        [
        (x_pos + s_bottom - (s_bottom - s_top) / 2, y_pos), 
        (x_pos + (s_bottom - s_top) / 2, y_pos), 
        (x_pos, y_pos + s_height),
        (x_pos + s_bottom, y_pos + s_height)
        ])
    l1 = pygame.draw.line(screen, (255, 10, 10), (begin, randY), (begin, randY + 30), 2)
    l2 = pygame.draw.line(screen, (255, 10, 10), (end, randY), (end, randY + 30), 2)
    l3 = pygame.draw.line(screen, (0, 255, 150), (begin,randY), (end,randY), 5)
    pygame.display.flip()
    return l3, obj

def restart(screen):
    now = time.time()
    if (now - start_time > 400):
        pygame.quit() 
    #limit player position
    X = random.randint(4, (WIDTH - 40)/10) * 10
    Y = random.randint(0, 3) * 50
    if (Y >= HEIGHT):
        Y -= 55
    x_pos = X
    y_pos = Y
    # anchor the target for easy version
    randn = WIDTH / 2
    begin = randn - 50
    end = randn + 50
    randY = HEIGHT - 200
    
    l3, obj = update_draw(screen, x_pos, y_pos, begin, end, randY)
    
    running = True
    win = False

    special = "nothing" # init for reinforce special reward
    counting = np.zeros(shape=4) # exploration rate 
    turns = 0 # for various situation

    while running:
        # action = random.randint(-7, 7)
        # action = 0 if action < 0 else (action % 2 + 2) if action > 1 else 1

        if win == False:
            # pygame.time.delay(20)
            y_pos += 7
            
            #output pre status
            x_dis = obj.centerx - randn
            y_dis = randY - obj.centery + 23
            counting, action = reinforce.predict(obj.centerx, obj.centery, x_dis, y_dis, turns, counting, special)
            
            #player action
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if key[pygame.K_ESCAPE]:
                    pygame.quit()
                if key[pygame.K_UP] and y_pos >= 30:
                    action = 1
                    y_pos -= 25
                if key[pygame.K_DOWN]:
                    # action = 1
                    y_pos += 10
                if key[pygame.K_RIGHT] and x_pos + 30 <= WIDTH :
                    x_pos += 15
                    action = 3
                if key[pygame.K_LEFT] and x_pos > 10:
                    x_pos -= 15
                    action = 2

            # random/AI choosing action 
            if action == 2:
                x_pos -= 15
            elif action == 3:
                x_pos += 15
            elif action == 1:
                y_pos -= 25
            turns += 1

            l3, obj = update_draw(screen, x_pos, y_pos, begin, end, randY)

        if collision.collide(l3, obj):
            screen.blit(lose_text, lose_rect)
            special = "crashed"
            
            reinforce.predict(obj.centerx, obj.centery,x_dis, y_dis, turns, counting, special)
            reinforce.predict(obj.centerx, obj.centery,x_dis, y_dis, turns, counting, special)
            reinforce.predict(obj.centerx, obj.centery,x_dis, y_dis, turns, counting, special)
            
            pygame.display.flip()
            win = True
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                # if key[pygame.K_r]:
                #     win = False
                #     restart(screen)
                if key[pygame.K_ESCAPE]:
                    pygame.quit()
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.time.delay(500)
            win = False
            restart(screen)

        if obj.top > randY  and obj.top <= randY + 25:
            if obj.bottomleft[0] >= begin and obj.bottomright[0] <= end:
                screen.blit(win_text, win_rect)
                special = "landed"
                reinforce.predict(obj.centerx, obj.centery,x_dis, y_dis, turns, counting, special)
                win = True
                pygame.display.flip()
                key = pygame.key.get_pressed()
                for event in pygame.event.get():
                    # if key[pygame.K_r]:
                    #     win = False
                    #     restart(screen)
                    if key[pygame.K_ESCAPE]:
                        pygame.quit()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                pygame.time.delay(200)
                win = False
                restart(screen)

        if turns == 100:
            restart(screen)
restart(screen)
