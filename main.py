# (O início do código continua igual)
import pygame, sys, random
pygame.init()
LARGURA, ALTURA = 1280, 720
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('DS-ONE: Multiverso do Caos Acadêmico')
clock = pygame.time.Clock()
# ... Cores ...
AMARELO = (255, 255, 0); AZUL_CLARO = (0, 255, 255); BRANCO = (255, 255, 255); CINZA_ESCURO = (50, 50, 50); CINZA_CLARO = (80, 80, 80); VERMELHO = (200, 0, 0); CINZA_CONQUISTA = (100, 100, 100); OURO = (255, 215, 0)
# (Fontes, Classe Button, etc. continuam iguais...)
fonte_botao = pygame.font.Font(None, 50); fonte_gameover = pygame.font.Font(None, 100); fonte_titulo = pygame.font.Font(None, 80)
fonte_conquista = pygame.font.Font(None, 40); fonte_descricao = pygame.font.Font(None, 30); fonte_hud = pygame.font.Font(None, 40)
class Button:
    def __init__(self, x, y, largura, altura, texto, cor_fundo, cor_hover):
        self.rect = pygame.Rect(x, y, largura, altura); self.texto = texto; self.cor_fundo = cor_fundo; self.cor_hover = cor_hover; self.cor_atual = cor_fundo; self.fonte = fonte_botao; self.texto_surf = self.fonte.render(texto, True, BRANCO); self.texto_rect = self.texto_surf.get_rect(center=self.rect.center)
    def checar_hover(self, pos_mouse):
        if self.rect.collidepoint(pos_mouse): self.cor_atual = self.cor_hover
        else: self.cor_atual = self.cor_fundo
    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor_atual, self.rect, border_radius=12); tela.blit(self.texto_surf, self.texto_rect)
    def foi_clicado(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos): return True
        return False
conquistas = { "SOBREVIVENTE_30S": {"nome": "Sobrevivente", "descricao": "Sobreviva por 30 segundos...", "desbloqueada": False}, "ESQUIVA_100": {"nome": "Esquiva Rápida", "descricao": "Desvie de 100 tiros...", "desbloqueada": False}, "MESTRE_DO_CAOS": {"nome": "Mestre do Caos", "descricao": "Desvie de 500 tiros...", "desbloqueada": False} }
logo = pygame.image.load('img/DS-One_Logomini.png').convert_alpha(); pygame.display.set_icon(logo)
fundoini = pygame.image.load('img/fundoini.gif').convert(); logocomp = pygame.image.load('img/DS-One_Logo.png').convert_alpha()
logo_rect = logocomp.get_rect(center=(LARGURA / 2, 230)); fundo = pygame.image.load('img/fundo.jpg').convert()
player_img = pygame.image.load('img/nave.png').convert_alpha(); boss_img_original = pygame.image.load('img/boss_atenun.png').convert_alpha()
LARGURA_BOTAO, ALTURA_BOTAO = 320, 70
botao_jogar = Button(LARGURA/2 - LARGURA_BOTAO/2, 450, LARGURA_BOTAO, ALTURA_BOTAO, 'Jogar', CINZA_ESCURO, CINZA_CLARO)
botao_conquistas = Button(LARGURA/2 - LARGURA_BOTAO/2, 450 + 80, LARGURA_BOTAO, ALTURA_BOTAO, 'Conquistas', CINZA_ESCURO, CINZA_CLARO)
botao_sair = Button(LARGURA/2 - LARGURA_BOTAO/2, 450 + 160, LARGURA_BOTAO, ALTURA_BOTAO, 'Sair', CINZA_ESCURO, CINZA_CLARO)
botoes_menu = [botao_jogar, botao_conquistas, botao_sair]; botao_jogar_novamente = Button(LARGURA/2 - LARGURA_BOTAO/2, 450, LARGURA_BOTAO, ALTURA_BOTAO, 'Jogar Novamente', CINZA_ESCURO, CINZA_CLARO)
botao_voltar_menu = Button(LARGURA/2 - LARGURA_BOTAO/2, 450 + 80, LARGURA_BOTAO, ALTURA_BOTAO, 'Voltar ao Menu', CINZA_ESCURO, CINZA_CLARO)
botoes_gameover = [botao_jogar_novamente, botao_voltar_menu]; botao_voltar = Button(LARGURA/2 - LARGURA_BOTAO/2, ALTURA - 90, LARGURA_BOTAO, ALTURA_BOTAO, 'Voltar', CINZA_ESCURO, CINZA_CLARO)
player_rect = player_img.get_rect(center=(150, ALTURA / 2)); vel_player = 10; HITBOX_LARGURA, HITBOX_ALTURA = 80, 40; player_hitbox = pygame.Rect(0, 0, HITBOX_LARGURA, HITBOX_ALTURA); player_hitbox.center = player_rect.center
altura_original_boss = boss_img_original.get_height(); largura_original_boss = boss_img_original.get_width()
nova_largura_boss = int(largura_original_boss * (ALTURA / altura_original_boss)); boss_img = pygame.transform.scale(boss_img_original, (nova_largura_boss, ALTURA))
boss_rect = boss_img.get_rect(topright=(LARGURA, 0)); tiros_boss = []; EVENTO_TIRO_BOSS = pygame.USEREVENT + 1; pygame.time.set_timer(EVENTO_TIRO_BOSS, 250)

# --- VARIÁVEIS DE DIFICULDADE E PONTUAÇÃO --- 
# Valores iniciais
VELOCIDADE_TIRO_INICIAL = 9    # <-- AJUSTADO (era 7)
PONTOS_POR_SEGUNDO_INICIAL = 1 # <-- AJUSTADO (era 2)

# Variáveis que vão mudar durante o jogo
velocidade_tiro_atual = VELOCIDADE_TIRO_INICIAL
pontos_por_segundo_atual = PONTOS_POR_SEGUNDO_INICIAL
proximo_aumento_dificuldade = 0 

# Variáveis de rastreamento
tempo_inicio_partida = 0; tiros_desviados_total = 0; pontuacao_atual = 0; pontuacao_final = 0

# === FUNÇÃO PARA RECOMEÇAR O JOGO ===
def reiniciar_jogo():
    global tempo_inicio_partida, pontuacao_atual, velocidade_tiro_atual, pontos_por_segundo_atual, proximo_aumento_dificuldade
    player_rect.center = (150, ALTURA / 2); player_hitbox.center = player_rect.center
    tiros_boss.clear()
    
    tempo_inicio_partida = pygame.time.get_ticks()
    pontuacao_atual = 0
    velocidade_tiro_atual = VELOCIDADE_TIRO_INICIAL
    pontos_por_segundo_atual = PONTOS_POR_SEGUNDO_INICIAL
    proximo_aumento_dificuldade = 60000 # <-- AJUSTADO (era 15000) O primeiro aumento será em 20 segundos

# === VARIÁVEIS DE CONTROLE DO JOGO ===
game = True; estado_jogo = "tela_inicial"; tela_cheia = False

# === O CORAÇÃO DO JOGO (O LOOP PRINCIPAL) ===
while game:
    pos_mouse = pygame.mouse.get_pos()
    
    # (O Loop de Eventos Global continua o mesmo)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                tela_cheia = not tela_cheia
                if tela_cheia: janela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
                else: janela = pygame.display.set_mode((LARGURA, ALTURA))
        if estado_jogo == "tela_inicial":
            if botao_jogar.foi_clicado(event): reiniciar_jogo(); estado_jogo = "jogando"
            if botao_conquistas.foi_clicado(event): estado_jogo = "tela_conquistas"
            if botao_sair.foi_clicado(event): game = False
        elif estado_jogo == "tela_conquistas":
            if botao_voltar.foi_clicado(event): estado_jogo = "tela_inicial"
        elif estado_jogo == "jogando":
            if event.type == EVENTO_TIRO_BOSS:
                pos_y_tiro = random.randint(boss_rect.top, boss_rect.bottom); novo_tiro = pygame.Rect(boss_rect.left, pos_y_tiro, 20, 10); tiros_boss.append(novo_tiro)
        elif estado_jogo == "game_over":
            if botao_jogar_novamente.foi_clicado(event): reiniciar_jogo(); estado_jogo = "jogando"
            if botao_voltar_menu.foi_clicado(event): reiniciar_jogo(); estado_jogo = "tela_inicial"

    # --- LÓGICA DE ATUALIZAÇÃO E DESENHO DE CADA TELA ---
    if estado_jogo == "tela_inicial":
        janela.blit(fundoini, (0, 0)); janela.blit(logocomp, logo_rect); [b.checar_hover(pos_mouse) for b in botoes_menu]; [b.desenhar(janela) for b in botoes_menu]
    elif estado_jogo == "tela_conquistas":
        janela.blit(fundoini, (0, 0)); titulo_surf = fonte_titulo.render("Conquistas", True, BRANCO); titulo_rect = titulo_surf.get_rect(center=(LARGURA/2, 80)); janela.blit(titulo_surf, titulo_rect)
        pos_y_conquista = 180
        for id, conquista in conquistas.items():
            cor_nome = OURO if conquista["desbloqueada"] else BRANCO; cor_desc = BRANCO if conquista["desbloqueada"] else CINZA_CONQUISTA
            nome_surf = fonte_conquista.render(conquista["nome"], True, cor_nome); nome_rect = nome_surf.get_rect(topleft=(100, pos_y_conquista)); janela.blit(nome_surf, nome_rect)
            desc_surf = fonte_descricao.render(conquista["descricao"], True, cor_desc); desc_rect = desc_surf.get_rect(topleft=(100, pos_y_conquista + 40)); janela.blit(desc_surf, desc_rect)
            pygame.draw.line(janela, CINZA_CONQUISTA, (100, pos_y_conquista + 80), (LARGURA - 100, pos_y_conquista + 80), 1); pos_y_conquista += 100
        botao_voltar.checar_hover(pos_mouse); botao_voltar.desenhar(janela)

    elif estado_jogo == "jogando":
        tempo_sobrevivido = pygame.time.get_ticks() - tempo_inicio_partida
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] or teclas[pygame.K_w]: player_rect.y -= vel_player
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]: player_rect.y += vel_player
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: player_rect.x -= vel_player
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: player_rect.x += vel_player
        player_hitbox.center = player_rect.center
        if player_rect.top <= 0: player_rect.top = 0
        if player_rect.bottom >= ALTURA: player_rect.bottom = ALTURA
        if player_rect.left <= 0: player_rect.left = 0
        if player_rect.right >= boss_rect.left: player_rect.right = boss_rect.left
        
        for tiro in tiros_boss[:]:
            tiro.x -= velocidade_tiro_atual
            if tiro.right < 0: tiros_boss.remove(tiro); tiros_desviados_total += 1
        
        # --- AUMENTO PROGRESSIVO DA DIFICULDADE --- 
        if tempo_sobrevivido >= proximo_aumento_dificuldade:
            velocidade_tiro_atual += 1.5   # <-- AJUSTADO (era 1.2)
            pontos_por_segundo_atual += 1  # <-- AJUSTADO (era 3)
            proximo_aumento_dificuldade += 60000 # <-- AJUSTADO (era 15000), próximo aumento em 20s
            print(f"DIFICULDADE AUMENTOU! Velocidade Tiro: {velocidade_tiro_atual:.1f}, Pontos/Seg: {pontos_por_segundo_atual}")
        
        pontuacao_atual = int((tempo_sobrevivido / 1000) * pontos_por_segundo_atual)

        for tiro in tiros_boss:
            if player_hitbox.colliderect(tiro):
                pontuacao_final = pontuacao_atual; estado_jogo = "game_over"
        
        # (Rastreamento de conquistas e desenho continuam iguais)
        if not conquistas["SOBREVIVENTE_30S"]["desbloqueada"] and tempo_sobrevivido >= 30000: conquistas["SOBREVIVENTE_30S"]["desbloqueada"] = True; print("CONQUISTA: Sobrevivente!")
        if not conquistas["ESQUIVA_100"]["desbloqueada"] and tiros_desviados_total >= 100: conquistas["ESQUIVA_100"]["desbloqueada"] = True; print("CONQUISTA: Esquiva Rápida!")
        if not conquistas["MESTRE_DO_CAOS"]["desbloqueada"] and tiros_desviados_total >= 500: conquistas["MESTRE_DO_CAOS"]["desbloqueada"] = True; print("CONQUISTA: Mestre do Caos!")
        janela.blit(fundo, (0, 0)); janela.blit(player_img, player_rect); janela.blit(boss_img, boss_rect)
        for tiro in tiros_boss: pygame.draw.ellipse(janela, AMARELO, tiro)
        texto_pontos_surf = fonte_hud.render(f"Pontos: {pontuacao_atual}", True, BRANCO)
        texto_pontos_rect = texto_pontos_surf.get_rect(topleft=(20, 20)); janela.blit(texto_pontos_surf, texto_pontos_rect)

    elif estado_jogo == "game_over":
        # (Código da tela de Game Over continua o mesmo)
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA); overlay.fill((0, 0, 0, 180)); janela.blit(overlay, (0, 0))
        texto_surf = fonte_gameover.render("GAME OVER", True, VERMELHO); texto_rect = texto_surf.get_rect(center=(LARGURA / 2, ALTURA / 3)); janela.blit(texto_surf, texto_rect)
        texto_final_surf = fonte_botao.render(f"Sua pontuação: {pontuacao_final}", True, BRANCO); texto_final_rect = texto_final_surf.get_rect(center=(LARGURA/2, ALTURA/2)); janela.blit(texto_final_surf, texto_final_rect)
        for botao in botoes_gameover: botao.checar_hover(pos_mouse); botao.desenhar(janela)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()