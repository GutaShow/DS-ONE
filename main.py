# (O início do código continua igual: import, pygame.init(), tela, clock, cores...)
import pygame, sys, random

pygame.init()
LARGURA, ALTURA = 1280, 720
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('DS-ONE: Multiverso do Caos Acadêmico')
clock = pygame.time.Clock()
# ... Cores ...
AMARELO = (255, 255, 0); AZUL_CLARO = (0, 255, 255); BRANCO = (255, 255, 255); CINZA_ESCURO = (50, 50, 50); CINZA_CLARO = (80, 80, 80); VERMELHO = (200, 0, 0); CINZA_CONQUISTA = (100, 100, 100); OURO = (255, 215, 0)

# === PREPARANDO AS FONTES PARA OS TEXTOS ===
fonte_botao = pygame.font.Font(None, 50)
fonte_gameover = pygame.font.Font(None, 100)
fonte_titulo = pygame.font.Font(None, 80)      # Fonte para títulos de telas
fonte_conquista = pygame.font.Font(None, 40)  # Fonte para o texto das conquistas
fonte_descricao = pygame.font.Font(None, 30) # Fonte para a descrição

# (A classe Button continua a mesma)
class Button:
    def __init__(self, x, y, largura, altura, texto, cor_fundo, cor_hover):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_fundo = cor_fundo
        self.cor_hover = cor_hover
        self.cor_atual = cor_fundo
        self.fonte = fonte_botao
        self.texto_surf = self.fonte.render(texto, True, BRANCO)
        self.texto_rect = self.texto_surf.get_rect(center=self.rect.center)
    def checar_hover(self, pos_mouse):
        if self.rect.collidepoint(pos_mouse): self.cor_atual = self.cor_hover
        else: self.cor_atual = self.cor_fundo
    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor_atual, self.rect, border_radius=12)
        tela.blit(self.texto_surf, self.texto_rect)
    def foi_clicado(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos): return True
        return False

# === SISTEMA DE CONQUISTAS === (NOVO)
# Usamos um dicionário para guardar todas as informações das conquistas.
conquistas = {
    "SOBREVIVENTE_30S": {
        "nome": "Sobrevivente",
        "descricao": "Sobreviva por 30 segundos em uma única partida.",
        "desbloqueada": False
    },
    "ESQUIVA_100": {
        "nome": "Esquiva Rápida",
        "descricao": "Desvie de um total de 100 tiros do chefe.",
        "desbloqueada": False
    },
    "MESTRE_DO_CAOS": {
        "nome": "Mestre do Caos",
        "descricao": "Desvie de 500 tiros no total.",
        "desbloqueada": False
    }
}

# Variáveis para rastrear o progresso das conquistas
tempo_inicio_partida = 0
tiros_desviados_total = 0

# === CARREGANDO IMAGENS E CRIANDO BOTÕES ===
# (Carregamento de imagens continua o mesmo...)
logo = pygame.image.load('img/DS-One_Logomini.png').convert_alpha(); pygame.display.set_icon(logo)
fundoini = pygame.image.load('img/fundoini.gif').convert(); logocomp = pygame.image.load('img/DS-One_Logo.png').convert_alpha()
logo_rect = logocomp.get_rect(center=(LARGURA / 2, 230))
fundo = pygame.image.load('img/fundo.jpg').convert(); player_img = pygame.image.load('img/nave.png').convert_alpha()
boss_img_original = pygame.image.load('img/boss_atenun.png').convert_alpha()

# Botões
LARGURA_BOTAO, ALTURA_BOTAO = 320, 70
botao_jogar = Button(LARGURA/2 - LARGURA_BOTAO/2, 450, LARGURA_BOTAO, ALTURA_BOTAO, 'Jogar', CINZA_ESCURO, CINZA_CLARO)
botao_conquistas = Button(LARGURA/2 - LARGURA_BOTAO/2, 450 + 80, LARGURA_BOTAO, ALTURA_BOTAO, 'Conquistas', CINZA_ESCURO, CINZA_CLARO)
botao_sair = Button(LARGURA/2 - LARGURA_BOTAO/2, 450 + 160, LARGURA_BOTAO, ALTURA_BOTAO, 'Sair', CINZA_ESCURO, CINZA_CLARO)
botoes_menu = [botao_jogar, botao_conquistas, botao_sair]
botao_jogar_novamente = Button(LARGURA/2 - LARGURA_BOTAO/2, 450, LARGURA_BOTAO, ALTURA_BOTAO, 'Jogar Novamente', CINZA_ESCURO, CINZA_CLARO)
botao_voltar_menu = Button(LARGURA/2 - LARGURA_BOTAO/2, 450 + 80, LARGURA_BOTAO, ALTURA_BOTAO, 'Voltar ao Menu', CINZA_ESCURO, CINZA_CLARO)
botoes_gameover = [botao_jogar_novamente, botao_voltar_menu]
# Novo botão para a tela de conquistas
botao_voltar = Button(LARGURA/2 - LARGURA_BOTAO/2, ALTURA - 90, LARGURA_BOTAO, ALTURA_BOTAO, 'Voltar', CINZA_ESCURO, CINZA_CLARO)

# === CONFIGURAÇÃO DOS OBJETOS DO JOGO ===
# (Toda a configuração de jogador, boss e tiros continua a mesma)
player_rect = player_img.get_rect(center=(150, ALTURA / 2)); vel_player = 10
HITBOX_LARGURA, HITBOX_ALTURA = 80, 40; player_hitbox = pygame.Rect(0, 0, HITBOX_LARGURA, HITBOX_ALTURA); player_hitbox.center = player_rect.center
altura_original_boss = boss_img_original.get_height(); largura_original_boss = boss_img_original.get_width()
nova_largura_boss = int(largura_original_boss * (ALTURA / altura_original_boss)); boss_img = pygame.transform.scale(boss_img_original, (nova_largura_boss, ALTURA))
boss_rect = boss_img.get_rect(topright=(LARGURA, 0)); tiros_boss = []; VELOCIDADE_TIRO = 12
EVENTO_TIRO_BOSS = pygame.USEREVENT + 1; pygame.time.set_timer(EVENTO_TIRO_BOSS, 250)

# === FUNÇÃO PARA RECOMEÇAR O JOGO ===
def reiniciar_jogo():
    global tempo_inicio_partida
    player_rect.center = (150, ALTURA / 2)
    player_hitbox.center = player_rect.center
    tiros_boss.clear()
    # Zera o cronômetro da partida atual
    tempo_inicio_partida = pygame.time.get_ticks()

# === VARIÁVEIS DE CONTROLE DO JOGO ===
game = True
estado_jogo = "tela_inicial"

# === O CORAÇÃO DO JOGO (O LOOP PRINCIPAL) ===
while game:
    pos_mouse = pygame.mouse.get_pos()
    
    #---
    # Se estamos na TELA INICIAL...
    #---
    if estado_jogo == "tela_inicial":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game = False
            if botao_jogar.foi_clicado(event): 
                reiniciar_jogo() # Reinicia o jogo antes de começar
                estado_jogo = "jogando"
            if botao_conquistas.foi_clicado(event): 
                estado_jogo = "tela_conquistas" # Muda para a nova tela
            if botao_sair.foi_clicado(event): game = False
        janela.blit(fundoini, (0, 0)); janela.blit(logocomp, logo_rect)
        for botao in botoes_menu:
            botao.checar_hover(pos_mouse); botao.desenhar(janela)

    #---
    # Se estamos na TELA DE CONQUISTAS... (NOVO)
    #---
    elif estado_jogo == "tela_conquistas":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game = False
            if botao_voltar.foi_clicado(event):
                estado_jogo = "tela_inicial"

        # Desenha o fundo e o título
        janela.blit(fundoini, (0, 0))
        titulo_surf = fonte_titulo.render("Conquistas", True, BRANCO)
        titulo_rect = titulo_surf.get_rect(center=(LARGURA/2, 80))
        janela.blit(titulo_surf, titulo_rect)
        
        # Desenha a lista de conquistas
        pos_y_conquista = 180
        for id, conquista in conquistas.items():
            # Define a cor baseada em se a conquista foi desbloqueada
            cor_nome = OURO if conquista["desbloqueada"] else BRANCO
            cor_desc = BRANCO if conquista["desbloqueada"] else CINZA_CONQUISTA
            
            # Desenha o nome da conquista
            nome_surf = fonte_conquista.render(conquista["nome"], True, cor_nome)
            nome_rect = nome_surf.get_rect(topleft=(100, pos_y_conquista))
            janela.blit(nome_surf, nome_rect)
            
            # Desenha a descrição
            desc_surf = fonte_descricao.render(conquista["descricao"], True, cor_desc)
            desc_rect = desc_surf.get_rect(topleft=(100, pos_y_conquista + 40))
            janela.blit(desc_surf, desc_rect)

            # Desenha uma linha separadora
            pygame.draw.line(janela, CINZA_CONQUISTA, (100, pos_y_conquista + 80), (LARGURA - 100, pos_y_conquista + 80), 1)
            
            pos_y_conquista += 100 # Espaçamento para a próxima conquista
            
        # Desenha o botão de voltar
        botao_voltar.checar_hover(pos_mouse)
        botao_voltar.desenhar(janela)

    #---
    # Se estamos JOGANDO...
    #---
    elif estado_jogo == "jogando":
        for event in pygame.event.get():
            # ... (eventos de QUIT e EVENTO_TIRO_BOSS continuam iguais)
            if event.type == pygame.QUIT: game = False
            if event.type == EVENTO_TIRO_BOSS:
                pos_y_tiro = random.randint(boss_rect.top, boss_rect.bottom); novo_tiro = pygame.Rect(boss_rect.left, pos_y_tiro, 20, 10); tiros_boss.append(novo_tiro)

        # (Movimentação e limites da tela continuam iguais)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] or teclas[pygame.K_w]: player_rect.y -= vel_player
        # ... (resto da movimentação) ...
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]: player_rect.y += vel_player
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: player_rect.x -= vel_player
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: player_rect.x += vel_player
        player_hitbox.center = player_rect.center
        if player_rect.top <= 0: player_rect.top = 0
        if player_rect.bottom >= ALTURA: player_rect.bottom = ALTURA
        if player_rect.left <= 0: player_rect.left = 0
        if player_rect.right >= boss_rect.left: player_rect.right = boss_rect.left

        # Movimento e remoção de tiros
        for tiro in tiros_boss[:]:
            tiro.x -= VELOCIDADE_TIRO
            if tiro.right < 0:
                tiros_boss.remove(tiro)
                tiros_desviados_total += 1 # RASTREAMENTO: Incrementa o contador de desvios

        # Colisão
        for tiro in tiros_boss:
            if player_hitbox.colliderect(tiro):
                estado_jogo = "game_over"
        
        # --- RASTREAMENTO E DESBLOQUEIO DE CONQUISTAS --- (NOVO)
        # 1. Conquista de tempo
        tempo_atual = pygame.time.get_ticks()
        tempo_sobrevivido = tempo_atual - tempo_inicio_partida
        if not conquistas["SOBREVIVENTE_30S"]["desbloqueada"] and tempo_sobrevivido >= 30000: # 30000 ms = 30s
            conquistas["SOBREVIVENTE_30S"]["desbloqueada"] = True
            print("CONQUISTA DESBLOQUEADA: Sobrevivente!")
        
        # 2. Conquista de desvios
        if not conquistas["ESQUIVA_100"]["desbloqueada"] and tiros_desviados_total >= 100:
            conquistas["ESQUIVA_100"]["desbloqueada"] = True
            print("CONQUISTA DESBLOQUEADA: Esquiva Rápida!")

        if not conquistas["MESTRE_DO_CAOS"]["desbloqueada"] and tiros_desviados_total >= 500:
            conquistas["MESTRE_DO_CAOS"]["desbloqueada"] = True
            print("CONQUISTA DESBLOQUEADA: Mestre do Caos!")
        
        # (Desenho da cena do jogo continua igual)
        janela.blit(fundo, (0, 0)); janela.blit(player_img, player_rect); janela.blit(boss_img, boss_rect)
        for tiro in tiros_boss: pygame.draw.ellipse(janela, AMARELO, tiro)

    #---
    # Se deu GAME OVER...
    #---
    elif estado_jogo == "game_over":
        # (A tela de Game Over continua a mesma)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game = False
            if botao_jogar_novamente.foi_clicado(event): reiniciar_jogo(); estado_jogo = "jogando"
            if botao_voltar_menu.foi_clicado(event): reiniciar_jogo(); estado_jogo = "tela_inicial"
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA); overlay.fill((0, 0, 0, 180)); janela.blit(overlay, (0, 0))
        texto_surf = fonte_gameover.render("GAME OVER", True, VERMELHO); texto_rect = texto_surf.get_rect(center=(LARGURA / 2, ALTURA / 3)); janela.blit(texto_surf, texto_rect)
        for botao in botoes_gameover:
            botao.checar_hover(pos_mouse); botao.desenhar(janela)

    # === ATUALIZAÇÃO FINAL DA TELA ===
    pygame.display.update()
    clock.tick(60)

# === FIM DO JOGO ===
pygame.quit()
sys.exit()