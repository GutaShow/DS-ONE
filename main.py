import pygame
pygame.init()

# Icone Do jogo
logo=pygame.image.load('img/DS-One_Logo.png')
pygame.display.set_icon(logo)

# Definicao da janela
janela=pygame.display.set_mode([1200, 611])
pygame.display.set_caption('DS-ONE: Multiverso do Caos Acadêmico') # Titulo da janela
fundo=pygame.image.load('img/fundo.jpg')
player=pygame.image.load('img/nave.png')

# Posicao do jogador
pos_yplayer=300 # Cima/Baixo
pos_xplayer=400 # Esquerda/Direita
vel_player=0.5 # Velocidade da nave

# VARIAVEIS
loop=True





# Loop do Jogo
while loop:
    # Botao de fechar a janela
    for events in pygame.event.get():
        if events.type==pygame.QUIT:
            loop=False
    
    # indentifica quais teclas estao sendo pressionadas 
    teclas=pygame.key.get_pressed()    
    
    # Movimentacao da nave       
    if teclas[pygame.K_UP]: # Cima
        pos_yplayer-=vel_player
    if teclas[pygame.K_DOWN]: # Baixo
        pos_yplayer+=vel_player
    if teclas[pygame.K_LEFT]: # Esquerda
        pos_xplayer-=vel_player
    if teclas[pygame.K_RIGHT]: # Direita
        pos_xplayer+=vel_player 
    
    # Bordas do Jogo
    if pos_yplayer <= -7:
        pos_yplayer=-7
    if pos_yplayer >= 548:
        pos_yplayer=548
    if pos_xplayer <= -20:
        pos_xplayer=-20
    if pos_xplayer >= 1082:
        pos_xplayer=1082
            
    # inserindo imagem na janela      
    janela.blit(fundo, (0, 0))
    janela.blit(player, (pos_xplayer, pos_yplayer))
    
    
    # Atualizacao da tela
    pygame.display.update()
    