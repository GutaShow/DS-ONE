import pygame, time
pygame.init()

# Icone Do jogo
logo=pygame.image.load('img/DS-One_Logomini.png')
pygame.display.set_icon(logo)

# Imagens do Jogo
fundo=pygame.image.load('img/fundo.jpg') # Fundo da Fase 1
player=pygame.image.load('img/nave.png') # Jogador
fundoini=pygame.image.load('img/fundoini.gif') # Fundo da tela inicial
logocomp=pygame.image.load('img/DS-One_Logo.png') # Logo da tela inicial
atenun_boss=pygame.image.load('img/boss_atenun.png')

# Definicao da janela
janela=pygame.display.set_mode([1280, 720]) # Resolucao da Janela
pygame.display.set_caption('DS-ONE: Multiverso do Caos Acadêmico') # Titulo da janela

# Posicao do jogador
pos_yplayer=300 # Cima/Baixo
pos_xplayer=400 # Esquerda/Direita
vel_player=0.7 # Velocidade da nave

# VARIAVEIS
game=True
loop=True
inicio= True


while game:
    # Botao de fechar a janela
    for events in pygame.event.get():
            if events.type==pygame.QUIT:
                game=False
                inicio=False
                loop=False
    
    """# Loop da tela inicial
    while inicio:
        # Botao de fechar a janela
        for events in pygame.event.get():
            if events.type==pygame.QUIT:
                inicio=False
                
        
        # Chamar a imagem de Fundo
        janela.blit(fundoini, (0, 0))
        janela.blit(logocomp, (200, 200))
        
        # Atualizacao da tela
        pygame.display.update()"""


    # Loop do Jogo
    while loop:
        # Botao de fechar a janela
        for events in pygame.event.get():
            if events.type==pygame.QUIT:
                loop=False
                game=False
                inicio=False
        
        # indentifica quais teclas estao sendo pressionadas 
        teclas=pygame.key.get_pressed()    
        
        # Movimentacao da nave       
        if teclas[pygame.K_UP] or teclas[pygame.K_w]: # Cima
            pos_yplayer-=vel_player
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]: # Baixo
            pos_yplayer+=vel_player
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: # Esquerda
            pos_xplayer-=vel_player
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: # Direita
            pos_xplayer+=vel_player 
        
            
        
        # Bordas do Jogo
        if pos_yplayer <= -7:
            pos_yplayer=-7
        if pos_yplayer >= 660:
            pos_yplayer=660
        if pos_xplayer <= -20:
            pos_xplayer=-20
        if pos_xplayer >= 1160:
            pos_xplayer=1160
                
        # inserindo imagem na janela      
        janela.blit(fundo, (0, 0))
        janela.blit(player, (pos_xplayer, pos_yplayer))
        janela.blit(atenun_boss, (800, 100))
        
        
        # Atualizacao da tela
        pygame.display.update()
        