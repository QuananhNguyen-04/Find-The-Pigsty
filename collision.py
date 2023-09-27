import pygame
import __init

pygame.init()

def collide(l3, obj):
    DeathZone = pygame.Rect(0, 399, 700 ,2)
    lines = [l3, DeathZone]
    return True if any(obj.colliderect(*line) for line in lines) else False 
    