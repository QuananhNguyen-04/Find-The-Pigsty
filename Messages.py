import pygame
import __init
pygame.init()

font = pygame.font.SysFont("timesnewroman", 50)
win_text = font.render("You Win", True, (50,100,200), (200,200,200))
lose_text = font.render("You Crashed", True, (50,100,200), (200,200,200))

win_rect = win_text.get_rect()
lose_rect = lose_text.get_rect()

win_rect.center = (__init.WIDTH / 2, __init.HEIGHT / 2 - 20)
lose_rect.center = (__init.WIDTH / 2, __init.HEIGHT / 2 - 20)