#------------------------------------------------------------------
# DS-ONE: Multiverso do Ca-aos Acadêmico
# Um jogo de nave para desviar de tiros
#------------------------------------------------------------------

import pygame, sys, random

# === PREPARANDO O BÁSICO ===
# Inicia o Pygame. É como ligar o motor do carro antes de dirigir.
pygame.init()

# O tamanho da nossa tela, em pixels (largura, altura).
LARGURA, ALTURA = 1280, 720
# Cria a janela do jogo com o tamanho que definimos.
janela = pygame.display.set_mode((LARGURA, ALTURA))
# O título que aparece na barra da janela do jogo.
pygame.display.set_caption('DS-ONE: Multiverso do Caos Acadêmico')

# Um reloginho para controlar a velocidade do jogo e garantir que ele rode igual em todos os computadores.
clock = pygame.time.Clock()

# === NOSSA PALETA DE CORES (em formato RGB) ===
AMARELO = (255, 255, 0)
AZUL_CLARO = (0, 255, 255) # Usado para ver a hitbox
BRANCO = (255, 255, 255)
CINZA_ESCURO = (50, 50, 50)   # Cor principal dos botões
CINZA_CLARO = (80, 80, 80)    # Cor do botão quando o mouse está em cima
VERMELHO = (200, 0, 0)        # Cor do texto de "Game Over"

# === PREPARANDO AS FONTES PARA OS TEXTOS ===
# Usamos 'None' para pegar a fonte padrão do Pygame, que é simples e funciona bem.
fonte_botao = pygame.font.Font(None, 50)      # Fonte para os textos dos botões.
fonte_gameover = pygame.font.Font(None, 100)  # Uma fonte maior para o "GAME OVER".


# === O MOLDE PARA CRIAR BOTÕES (CLASSE BUTTON) ===
# Criar uma "classe" é como desenhar a planta de uma casa.
# Depois, podemos construir quantas casas (botões) quisermos usando essa planta.
class Button:
    # O "construtor": o que acontece quando um novo botão é criado.
    # Ele define a posição, tamanho, texto e cores do botão.
    def __init__(self, x, y, largura, altura, texto, cor_fundo, cor_hover):
        self.rect = pygame.Rect(x, y, largura, altura) # O retângulo que define a área do botão.
        self.texto = texto
        self.cor_fundo = cor_fundo
        self.cor_hover = cor_hover
        self.cor_atual = cor_fundo # A cor começa normal.
        
        # Prepara o texto do botão para ser desenhado.
        self.fonte = fonte_botao
        self.texto_surf = self.fonte.render(texto, True, BRANCO)
        self.texto_rect = self.texto_surf.get_rect(center=self.rect.center)

    # Verifica se o mouse está em cima do botão para mudar a cor.
    def checar_hover(self, pos_mouse):
        if self.rect.collidepoint(pos_mouse):
            self.cor_atual = self.cor_hover # Se o mouse está em cima, muda a cor.
        else:
            self.cor_atual = self.cor_fundo # Se não, volta à cor normal.

    # Desenha o botão na tela.
    def desenhar(self, tela):
        # Desenha o retângulo do botão. 'border_radius' deixa os cantos arredondados.
        pygame.draw.rect(tela, self.cor_atual, self.rect, border_radius=12)
        # Desenha o texto no centro do botão.
        tela.blit(self.texto_surf, self.texto_rect)

    # Responde "sim" ou "não" se o botão foi clicado.
    def foi_clicado(self, event):
        # Verifica se o evento foi um clique do mouse E se o clique foi dentro da área do botão.
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False

# === CARREGANDO NOSSAS IMAGENS E SONS ===
# '.convert_alpha()' mantém a transparência da imagem (ex: fundo de um PNG).
# '.convert()' otimiza a imagem para o Pygame rodar mais rápido.
logo = pygame.image.load('img/DS-One_Logomini.png').convert_alpha()
pygame.display.set_icon(logo)

fundoini = pygame.image.load('img/fundoini.gif').convert()
logocomp = pygame.image.load('img/DS-One_Logo.png').convert_alpha()
# Pega as dimensões do logo e cria um retângulo para posicioná-lo no centro da tela.
logo_rect = logocomp.get_rect(center=(LARGURA / 2, 230))

fundo = pygame.image.load('img/fundo.jpg').convert()
player_img = pygame.image.load('img/nave.png').convert_alpha()
boss_img_original = pygame.image.load('img/boss_atenun.png').convert_alpha()

# === CRIANDO OS BOTÕES QUE USAREMOS NO JOGO ===
# Definimos um tamanho padrão para os botões.
LARGURA_BOTAO, ALTURA_BOTAO = 320, 70
# Posição inicial (no eixo Y) para o primeiro botão.
pos_y_botoes = 450

# Botões do Menu Principal
botao_jogar = Button(LARGURA/2 - LARGURA_BOTAO/2, pos_y_botoes, LARGURA_BOTAO, ALTURA_BOTAO, 'Jogar', CINZA_ESCURO, CINZA_CLARO)
# Coloca o próximo botão 80 pixels abaixo do anterior.
botao_conquistas = Button(LARGURA/2 - LARGURA_BOTAO/2, pos_y_botoes + 80, LARGURA_BOTAO, ALTURA_BOTAO, 'Conquistas', CINZA_ESCURO, CINZA_CLARO)
botao_sair = Button(LARGURA/2 - LARGURA_BOTAO/2, pos_y_botoes + 160, LARGURA_BOTAO, ALTURA_BOTAO, 'Sair', CINZA_ESCURO, CINZA_CLARO)
botoes_menu = [botao_jogar, botao_conquistas, botao_sair]

# Botões da Tela de Game Over
botao_jogar_novamente = Button(LARGURA/2 - LARGURA_BOTAO/2, 450, LARGURA_BOTAO, ALTURA_BOTAO, 'Jogar Novamente', CINZA_ESCURO, CINZA_CLARO)
botao_voltar_menu = Button(LARGURA/2 - LARGURA_BOTAO/2, 450 + 80, LARGURA_BOTAO, ALTURA_BOTAO, 'Voltar ao Menu', CINZA_ESCURO, CINZA_CLARO)
botoes_gameover = [botao_jogar_novamente, botao_voltar_menu]

# === PREPARANDO O JOGADOR E O CHEFÃO ===
# Jogador
player_rect = player_img.get_rect(center=(150, ALTURA / 2)) # Retângulo para a imagem.
vel_player = 10
# A hitbox é a "área de dano" real, menor que a imagem, para o jogo ser mais justo.
HITBOX_LARGURA, HITBOX_ALTURA = 80, 40
player_hitbox = pygame.Rect(0, 0, HITBOX_LARGURA, HITBOX_ALTURA)
player_hitbox.center = player_rect.center # Centraliza a hitbox na nave.

# Boss
# Redimensiona a imagem do boss para ocupar toda a altura da tela, mantendo a proporção.
altura_original_boss = boss_img_original.get_height()
largura_original_boss = boss_img_original.get_width()
nova_largura_boss = int(largura_original_boss * (ALTURA / altura_original_boss))
boss_img = pygame.transform.scale(boss_img_original, (nova_largura_boss, ALTURA))
# Posiciona o boss gigante "colado" na borda direita.
boss_rect = boss_img.get_rect(topright=(LARGURA, 0))

# Tiros
tiros_boss = []
VELOCIDADE_TIRO = 12
# Cria um "alarme" (evento customizado) que vai disparar de tempos em tempos para o boss atirar.
EVENTO_TIRO_BOSS = pygame.USEREVENT + 1
pygame.time.set_timer(EVENTO_TIRO_BOSS, 250) # O alarme toca a cada 250 milissegundos.


# === FUNÇÃO PARA RECOMEÇAR O JOGO (MUITO IMPORTANTE!) ===
# Esta função arruma tudo para uma nova partida, colocando as coisas no lugar.
def reiniciar_jogo():
    # Reposiciona o jogador no local inicial.
    player_rect.center = (150, ALTURA / 2)
    player_hitbox.center = player_rect.center
    # Limpa todos os tiros que ainda estavam na tela.
    tiros_boss.clear()

# === VARIÁVEIS QUE CONTROLAM O JOGO ===
game = True # Enquanto esta variável for 'True', o jogo continua rodando no loop principal.
estado_jogo = "tela_inicial" # A "página" ou "cena" atual do jogo. Começamos na tela inicial.

# === O CORAÇÃO DO JOGO (O LOOP PRINCIPAL) ===
# Tudo que está dentro deste 'while' acontece 60 vezes por segundo, criando a ilusão de movimento.
while game:
    # Pega a posição do mouse a cada quadro. Útil para os botões.
    pos_mouse = pygame.mouse.get_pos()
    
    #---
    # Se estamos na TELA INICIAL...
    #---
    if estado_jogo == "tela_inicial":
        # Vemos se o jogador fez alguma coisa (fechou a janela, clicou num botão).
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game = False
            # Verifica se algum dos botões do menu foi clicado.
            if botao_jogar.foi_clicado(event): estado_jogo = "jogando"
            if botao_conquistas.foi_clicado(event): print("Tela de Conquistas - A ser implementada!")
            if botao_sair.foi_clicado(event): game = False
        
        # Desenha o fundo e o logo da tela inicial.
        janela.blit(fundoini, (0, 0))
        janela.blit(logocomp, logo_rect)

        # Atualiza e desenha cada botão do menu.
        for botao in botoes_menu:
            botao.checar_hover(pos_mouse)
            botao.desenhar(janela)

    #---
    # Se estamos JOGANDO...
    #---
    elif estado_jogo == "jogando":
        # Vemos se o jogador fez alguma coisa.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game = False
            # Se o "alarme" do tiro do boss tocou...
            if event.type == EVENTO_TIRO_BOSS:
                # ...cria um novo tiro e adiciona na lista de tiros.
                pos_y_tiro = random.randint(boss_rect.top, boss_rect.bottom)
                novo_tiro = pygame.Rect(boss_rect.left, pos_y_tiro, 20, 10)
                tiros_boss.append(novo_tiro)

        # Movimentação da nave
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] or teclas[pygame.K_w]: player_rect.y -= vel_player
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]: player_rect.y += vel_player
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: player_rect.x -= vel_player
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: player_rect.x += vel_player
        
        # Garante que a hitbox sempre siga a imagem da nave.
        player_hitbox.center = player_rect.center

        # Limites da tela para a nave não fugir.
        if player_rect.top <= 0: player_rect.top = 0
        if player_rect.bottom >= ALTURA: player_rect.bottom = ALTURA
        if player_rect.left <= 0: player_rect.left = 0
        if player_rect.right >= boss_rect.left: player_rect.right = boss_rect.left
        
        # Move cada tiro na lista e remove os que saíram da tela.
        for tiro in tiros_boss[:]: # Usamos [:] para criar uma cópia da lista, evitando bugs ao remover itens.
            tiro.x -= VELOCIDADE_TIRO
            if tiro.right < 0: tiros_boss.remove(tiro)

        # Verifica se algum tiro acertou a hitbox do jogador.
        for tiro in tiros_boss:
            if player_hitbox.colliderect(tiro):
                estado_jogo = "game_over" # Se acertou, muda para a tela de Game Over.
        
        # Desenha tudo da cena do jogo: fundo, jogador, boss e os tiros.
        janela.blit(fundo, (0, 0))
        janela.blit(player_img, player_rect)
        janela.blit(boss_img, boss_rect)
        for tiro in tiros_boss: pygame.draw.ellipse(janela, AMARELO, tiro)

    #---
    # Se deu GAME OVER...
    #---
    elif estado_jogo == "game_over":
        # Vemos se o jogador fez alguma coisa.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game = False
            # Verifica se os botões de "Game Over" foram clicados.
            if botao_jogar_novamente.foi_clicado(event):
                reiniciar_jogo()
                estado_jogo = "jogando"
            if botao_voltar_menu.foi_clicado(event):
                reiniciar_jogo()
                estado_jogo = "tela_inicial"
        
        # Cria uma camada escura semi-transparente para dar o clima de "fim de jogo".
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) # O último número (180) é a transparência.
        janela.blit(overlay, (0, 0))

        # Desenha o texto "GAME OVER" na tela.
        texto_surf = fonte_gameover.render("GAME OVER", True, VERMELHO)
        texto_rect = texto_surf.get_rect(center=(LARGURA / 2, ALTURA / 3))
        janela.blit(texto_surf, texto_rect)

        # Desenha os botões de "Game Over".
        for botao in botoes_gameover:
            botao.checar_hover(pos_mouse)
            botao.desenhar(janela)

    # === ATUALIZAÇÃO FINAL DA TELA ===
    # Pega tudo que desenhamos e mostra na tela de uma vez.
    pygame.display.update()
    # Garante que o jogo não passe de 60 quadros por segundo (FPS).
    clock.tick(60)

# === FIM DO JOGO ===
# Se o loop 'while game' terminar, o jogo fecha de forma organizada.
pygame.quit()
sys.exit()