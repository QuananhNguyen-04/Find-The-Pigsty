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
    l1 = pygame.draw.line(screen, (255, 10, 10), (begin, randY - 50), (begin, randY), 2)
    l2 = pygame.draw.line(screen, (255, 10, 10), (end, randY - 50), (end, randY), 2)
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
    randY = random.randint(HEIGHT - 200, HEIGHT)
    
    l1, l2, l3, obj = update_draw(screen, x_pos, y_pos, begin, end, randY)
    
    running = True
    win = False
    
    turns = 0
    counting = np.zeros(shape=4)
    UCB_c= 1

    while running:
        # print("turns", turns)
        special = 'nothing'
        pygame.time.Clock().tick(20)
        Q = np.zeros(shape=4)
        prob = random.randint(0,4)
        # action = random.randint(-12,7)
        # if action > 1:
        #     action = 2 + action % 2
        # elif action < 1:
        #     action = 0
        # else:
        #     action = 1
        if win == False:

            x_cur = x_pos + s_top / 2
            y_cur = y_pos + s_height / 2
            
            x_dis = x_cur - randn
            y_dis = randY - 20 - y_cur
            state_x = x_dis
            state_y = y_dis
            arr = np.array([[x_dis, y_dis]])

            # turns, counting, action, UCB_c, Q = reinforce.predict(x_dis, y_dis, turns, counting, UCB_c)
            y_pos += 5
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if key[pygame.K_ESCAPE]:
                    pygame.quit()
                elif key[pygame.K_UP] and y_pos >= 30:
                    action = 1
                    y_pos -= 30
                elif key[pygame.K_DOWN]:
                    # action = 1
                    y_pos += 10
                elif key[pygame.K_RIGHT] and x_pos + 30 <= WIDTH :
                    x_pos += 15
                    action = 3
                elif key[pygame.K_LEFT] and x_pos > 10:
                    x_pos -= 15
                    action = 2
            # turns += 1 
            # print(str(action))
            # if action == 2:
            #     x_pos -= 15
                # print(f"{x_dis},{y_dis},Left")
            # elif action == 3:
            #     x_pos += 15
            #   #  print(f"{x_dis},{y_dis},Right")
            # elif action == 1:
            #     y_pos -= 40
            #   #  print(f"{x_dis},{y_dis},Up")

            l1, l2, l3, obj = update_draw(screen, x_pos, y_pos, begin, end, randY)


        if y_pos >= randY - s_height - 7 and y_pos <= randY - s_height:
            if x_pos + 5 >= begin and x_pos + s_top - 5 <= end:
                screen.blit(win_text, win_rect)
                special = "landed"
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
                # print(f"{x_dis},{y_dis},{action}")
                # turns, counting, action, UCB_c, Q = reinforce.predict(x_dis, y_dis, turns, counting, UCB_c)
                # print(Q[action]) 
                # print(reinforce.compute_reward(state_x, state_y, action, special))

                pygame.time.delay(1000)
                win = False
                restart(screen)

        if collision.collide(l1, l2, l3, obj):
            screen.blit(lose_text, lose_rect)
            special = "crashed"
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
            # print(f"{x_dis},{y_dis},{action}") 
            # turns, counting, action, UCB_c, Q = reinforce.predict(x_dis, y_dis, turns, counting, UCB_c, special='crashed')
            # print(Q[action])
            # print(reinforce.compute_reward(state_x, state_y, action, special))
            pygame.time.delay(1000)
            win = False
            restart(screen)
        # if action != 0 or (action == 0 and prob > 2):
            # print(f"{x_dis},{y_dis},{action}") 
            # print(reinforce.compute_reward(state_x, state_y, action, special))
            # turns, counting, action, UCB_c, Q = reinforce.predict(x_dis, y_dis, turns, counting, UCB_c)
            # print(Q[action])

restart(screen)