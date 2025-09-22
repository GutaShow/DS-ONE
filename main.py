import pygame

# Definicao da janela
janela=pygame.display.set_mode([800, 600])
pygame.display.set_caption('DS-ONE: Multiverso do Caos Acadêmico') # Titulo da janela

# VARIAVEIS
loop=True

while loop:
    for events in pygame.event.get():
        if events.type==pygame.QUIT:
            loop=False
    pygame.display.update()