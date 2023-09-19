import pygame
import random
import Messages
import __init
import numpy as np
import reinforce
import collision

pygame.init()

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
        ]
    )
    l1 = pygame.draw.line(screen, (255, 10, 10), (begin, randY + 50), (begin, randY), 2)
    l2 = pygame.draw.line(screen, (255, 10, 10), (end, randY + 50), (end, randY), 2)
    l3 = pygame.draw.line(screen, (0, 255, 150), (begin,randY), (end,randY), 5)
    pygame.display.flip()
    return l1, l2, l3, obj

def restart(screen):
    X = random.randint(40, WIDTH - 40)
    Y = 0
    x_pos = X
    y_pos = Y

    randn = random.randint(60, WIDTH - 60)
    begin = randn - 50
    end = randn + 50
    randY = random.randint(HEIGHT - 300, HEIGHT - 150)
    
    l1, l2, l3, obj = update_draw(screen, x_pos, y_pos, begin, end, randY)
    
    running = True
    win = False

    special = "nothing" # init for reinforce special reward
    turns = 0 # for various situation

    while running:
        action = random.randint(-7, 7)
        action = 0 if action < -1 else 1 if action < 2 else (action % 2 + 2) 
        pygame.time.Clock().tick(10)
        if win == False:

            y_pos += 7
            
            #output pre status
            x_dis = obj.centerx - randn
            y_dis = randY - obj.centery + 10
            
            #player action
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if key[pygame.K_ESCAPE]:
                    pygame.quit()
                elif key[pygame.K_UP] and y_pos >= 30:
                    action = 1
                    y_pos -= 25
                elif key[pygame.K_DOWN]:
                    # action = 1
                    y_pos += 10
                elif key[pygame.K_RIGHT] and x_pos + 30 <= WIDTH :
                    x_pos += 15
                    action = 3
                elif key[pygame.K_LEFT] and x_pos > 10:
                    x_pos -= 15
                    action = 2

            # random/AI choosing action 
            if action == 2:
                x_pos -= 15
            elif action == 3:
                x_pos += 15
            elif action == 1:
                y_pos -= 30
            turns += 1
            reinforce.compute_reward(obj.centerx, obj.centery, x_dis, y_dis, action, obj.centerx - randn, randY - obj.centery, special)

            l1, l2, l3, obj = update_draw(screen, x_pos, y_pos, begin, end, randY)

        if obj.top > randY  and obj.top <= randY + 21:
            if obj.bottomleft[0] >= begin and obj.bottomright[0] <= end:
                screen.blit(win_text, win_rect)
                special = "landed"
                reinforce.compute_reward(obj.centerx, obj.centery,x_dis, y_dis, action, obj.centerx - randn, randY - obj.centery, special)
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
                pygame.time.delay(1000)
                win = False
                restart(screen)

        elif collision.collide(l1, l2, l3, obj):
            screen.blit(lose_text, lose_rect)
            special = "crashed"
            reinforce.compute_reward(obj.centerx, obj.centery,x_dis, y_dis, action, obj.centerx - randn, randY - obj.centery, special)
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
            pygame.time.delay(1000)
            win = False
            restart(screen)
        if turns == 200:
            restart(screen)
restart(screen)