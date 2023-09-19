import pygame
import time

start_time = time.time()

pygame.init()

screen = pygame.display.set_mode((700, 400))
pygame.display.flip()
def restart():
    now = time.time() 
    if (now - start_time > 5) :
        pygame.quit()
    r = pygame.Rect(0, 300, 700, 50)
    while True:
        keys = pygame.key.get_pressed()
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
        screen.fill("white")
        pygame.draw.rect(screen, (50,50,50), r)
        pygame.display.flip()



restart()