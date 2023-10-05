import pygame
from __init import *

pygame.init()

def collide(l3, obj):
    DeathZone = pygame.Rect(0, 399, 700 ,2)
    lines = [l3, DeathZone]
    return True if any(obj.colliderect(*line) for line in lines) else False 
    

def victory(obj):
    vic = pygame.Rect(WIDTH / 2 - 15, HEIGHT - 180, 30, 10)

    if obj.colliderect(vic):
        return True