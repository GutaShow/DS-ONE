import pygame, sys, random

# === PREPARANDO O BÁSICO ===
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

# === CARREGANDO IMAGENS (COM TRATAMENTO DE ERRO) ===
def carregar_imagem_com_erro(caminho, alpha=True, resize=None):
    try:
        img = pygame.image.load(caminho)
        if alpha: img = img.convert_alpha()
        else: img = img.convert()
        if resize: img = pygame.transform.scale(img, resize)
        return img
    except pygame.error as e:
        print(f"ERRO: Não foi possível carregar a imagem '{caminho}': {e}")
        fallback_surface = pygame.Surface((64, 64) if not resize else resize, pygame.SRCALPHA)
        fallback_surface.fill((255, 0, 255))
        return fallback_surface

logo = carregar_imagem_com_erro('img/DS-One_Logomini.png'); pygame.display.set_icon(logo)
fundoini = carregar_imagem_com_erro('img/fundoini.gif', alpha=False); logocomp = carregar_imagem_com_erro('img/DS-One_Logo.png')
logo_rect = logocomp.get_rect(center=(LARGURA / 2, 230)); fundo = carregar_imagem_com_erro('img/fundo.jpg', alpha=False)
player_img = carregar_imagem_com_erro('img/nave.png')
boss_img_original = carregar_imagem_com_erro('img/boss_atenun.png')
powerup_item_img = carregar_imagem_com_erro('img/powerup_peido.png')
tiro_peido_img = carregar_imagem_com_erro('img/nuvem_peido.png')

# --- Ícones existentes ---
icon_sobrevivente_base = carregar_imagem_com_erro('img/icon_sobrevivente.png', resize=(64, 64)) # Este será o base
icon_esquiva = carregar_imagem_com_erro('img/icon_esquiva.png', resize=(64, 64))
icon_bloqueada = carregar_imagem_com_erro('img/icon_bloqueada.png', resize=(64, 64))

# --- Ícones de Sobrevivência (que você já gerou ou vai gerar) ---
icon_sobrevivente_1m = carregar_imagem_com_erro('img/icon_sobrevivente_1m.png', resize=(64, 64)) or icon_sobrevivente_base
icon_sobrevivente_5m = carregar_imagem_com_erro('img/icon_sobrevivente_5m.png', resize=(64, 64)) or icon_sobrevivente_base
icon_sobrevivente_10m = carregar_imagem_com_erro('img/icon_sobrevivente_10m.png', resize=(64, 64)) or icon_sobrevivente_base
icon_sobrevivente_20m = carregar_imagem_com_erro('img/icon_sobrevivente_20m.png', resize=(64, 64)) or icon_sobrevivente_base
icon_sobrevivente_1hr = carregar_imagem_com_erro('img/icon_sobrevivente_1hr.png', resize=(64, 64)) or icon_sobrevivente_base

# --- Ícones de Pontuação (que você já gerou ou vai gerar) ---
icon_pontos_100 = carregar_imagem_com_erro('img/icon_pontos_100.png', resize=(64, 64)) or icon_bloqueada 
icon_pontos_250 = carregar_imagem_com_erro('img/icon_pontos_250.png', resize=(64, 64)) or icon_bloqueada
icon_pontos_500 = carregar_imagem_com_erro('img/icon_pontos_500.png', resize=(64, 64)) or icon_bloqueada
icon_pontos_2000 = carregar_imagem_com_erro('img/icon_pontos_2000.png', resize=(64, 64)) or icon_bloqueada
icon_pontos_10000 = carregar_imagem_com_erro('img/icon_pontos_10000.png', resize=(64, 64)) or icon_bloqueada

# --- NOVOS ÍCONES PARA AS CONQUISTAS RECÉM-ADICIONADAS ---
icon_bixao = carregar_imagem_com_erro('img/icon_bixao.png', resize=(64, 64)) or icon_bloqueada
icon_que_ota = carregar_imagem_com_erro('img/icon_que_ota.png', resize=(64, 64)) or icon_bloqueada
icon_fim = carregar_imagem_com_erro('img/icon_fim.png', resize=(64, 64)) or icon_bloqueada
icon_abemsuado = carregar_imagem_com_erro('img/icon_abemsuado.png', resize=(64, 64)) or icon_bloqueada


# === DICIONÁRIO DE CONQUISTAS ATUALIZADO COM TODAS AS NOVAS ENTRADAS ===
conquistas = {
    "SOBREVIVENTE_30S": {"nome": "A LENDAAA!", "descricao": "Sobreviva por 30 segundos. Você é quase um meme.", "desbloqueada": False, "icon": icon_sobrevivente_base},
    "SOBREVIVENTE_1M": {"nome": "UMA MÁQUINAA!", "descricao": "Sobreviva por 1 minuto. Impressionante, agora descanse.", "desbloqueada": False, "icon": icon_sobrevivente_1m},
    "SOBREVIVENTE_5M": {"nome": "Só mais 5 minutinhos...", "descricao": "Sobreviva por 5 minutos. Igual àquele cochilo antes da aula.", "desbloqueada": False, "icon": icon_sobrevivente_5m},
    "SOBREVIVENTE_10M": {"nome": "A Prova não era tão difícil", "descricao": "Sobreviva por 10 minutos. Ou era?", "desbloqueada": False, "icon": icon_sobrevivente_10m},
    "SOBREVIVENTE_20M": {"nome": "Me formei (em enrolação)", "descricao": "Sobreviva por 20 minutos. Merece um diploma!", "desbloqueada": False, "icon": icon_sobrevivente_20m},
    "SOBREVIVENTE_1HR": {"nome": "Platinado no jogo da vida", "descricao": "Sobreviva por 1 hora. Parabéns, você é um veterano!", "desbloqueada": False, "icon": icon_sobrevivente_1hr},

    "ESQUIVA_100": {"nome": "Cadê o lag?", "descricao": "Desvie de 100 tiros. Sua internet está boa hoje!", "desbloqueada": False, "icon": icon_esquiva},
    "MESTRE_DO_CAOS": {"nome": "Manejo de Crises (e tiros)", "descricao": "Desvie de 500 tiros. O seu RH aprovaria.", "desbloqueada": False, "icon": icon_esquiva},
    
    "RECORDISTA_100P": {"nome": "Fui aprovado no estágio!", "descricao": "Alcance 100 pontos em uma única partida. O primeiro salário a gente nunca esquece.", "desbloqueada": False, "icon": icon_pontos_100},
    "RECORDISTA_250P": {"nome": "Meti o louco no FGTS", "descricao": "Alcance 250 pontos em uma única partida. O risco compensou.", "desbloqueada": False, "icon": icon_pontos_250},
    "RECORDISTA_500P": {"nome": "O pai tá on (com PIX)", "descricao": "Alcance 500 pontos em uma única partida. A grana chegou!", "desbloqueada": False, "icon": icon_pontos_500},
    "RECORDISTA_2000P": {"nome": "Comprei uma NFT (de foguete)", "descricao": "Alcance 2000 pontos em uma única partida. Investimento do futuro.", "desbloqueada": False, "icon": icon_pontos_2000},
    "RECORDISTA_10000P": {"nome": "Monopólio Intergalático", "descricao": "Alcance 10.000 pontos em uma única partida. Você é o novo Elon Musk do caos!", "desbloqueada": False, "icon": icon_pontos_10000},

    # --- NOVAS CONQUISTAS ---
    "BIXAO": {"nome": "Cê é o bixão mesmo", "descricao": "Alcance 750 pontos sem coletar power-ups.", "desbloqueada": False, "icon": icon_bixao},
    "QUE_OTA": {"nome": "Que ota?", "descricao": "Derrote o chefe.", "desbloqueada": False, "icon": icon_que_ota},
    "O_FIM": {"nome": "O fim?", "descricao": "Finalize o game (Sobreviva 1 hora e derrote o chefe).", "desbloqueada": False, "icon": icon_fim}, # Condição ajustada
    "ABEMSUADO": {"nome": "Abemsuado", "descricao": "Conquiste todas as conquistas.", "desbloqueada": False, "icon": icon_abemsuado},
}


# === CRIAÇÃO DOS BOTÕES ===
LARGURA_BOTAO, ALTURA_BOTAO = 320, 70
botao_jogar = Button(LARGURA/2 - LARGURA_BOTAO/2, 450, LARGURA_BOTAO, ALTURA_BOTAO, 'Jogar', CINZA_ESCURO, CINZA_CLARO)
botao_conquistas = Button(LARGURA/2 - LARGURA_BOTAO/2, 450 + 80, LARGURA_BOTAO, ALTURA_BOTAO, 'Conquistas', CINZA_ESCURO, CINZA_CLARO)
botao_sair = Button(LARGURA/2 - LARGURA_BOTAO/2, 450 + 160, LARGURA_BOTAO, ALTURA_BOTAO, 'Sair', CINZA_ESCURO, CINZA_CLARO)
botoes_menu = [botao_jogar, botao_conquistas, botao_sair]
botao_jogar_novamente = Button(LARGURA/2 - LARGURA_BOTAO/2, ALTURA / 2 + 50, LARGURA_BOTAO, ALTURA_BOTAO, 'Jogar Novamente', CINZA_ESCURO, CINZA_CLARO)
botao_voltar_menu = Button(LARGURA/2 - LARGURA_BOTAO/2, ALTURA / 2 + 50 + 80, LARGURA_BOTAO, ALTURA_BOTAO, 'Voltar ao Menu', CINZA_ESCURO, CINZA_CLARO)
botoes_gameover = [botao_jogar_novamente, botao_voltar_menu]
botao_voltar = Button(LARGURA/2 - LARGURA_BOTAO/2, ALTURA - 90, LARGURA_BOTAO, ALTURA_BOTAO, 'Voltar', CINZA_ESCURO, CINZA_CLARO)

# === CONFIGURAÇÃO DOS OBJETOS DO JOGO ===
player_rect = player_img.get_rect(center=(150, ALTURA / 2)); vel_player = 10; HITBOX_LARGURA, HITBOX_ALTURA = 80, 40
player_hitbox = pygame.Rect(0, 0, HITBOX_LARGURA, HITBOX_ALTURA); player_hitbox.center = player_rect.center
altura_original_boss = boss_img_original.get_height(); largura_original_boss = boss_img_original.get_width()
nova_largura_boss = int(largura_original_boss * (ALTURA / altura_original_boss)); boss_img = pygame.transform.scale(boss_img_original, (nova_largura_boss, ALTURA))
boss_rect = boss_img.get_rect(topright=(LARGURA, 0)); tiros_boss = []
EVENTO_TIRO_BOSS = pygame.USEREVENT + 1; pygame.time.set_timer(EVENTO_TIRO_BOSS, 250)
EVENTO_SPAWN_POWERUP = pygame.USEREVENT + 2; pygame.time.set_timer(EVENTO_SPAWN_POWERUP, 10000)
VELOCIDADE_TIRO_INICIAL = 9; PONTOS_POR_SEGUNDO_INICIAL = 1; velocidade_tiro_atual = VELOCIDADE_TIRO_INICIAL
pontos_por_segundo_atual = PONTOS_POR_SEGUNDO_INICIAL; proximo_aumento_dificuldade = 60000; tempo_inicio_partida = 0
tiros_desviados_total = 0; pontuacao_atual = 0; pontuacao_final = 0; powerups_na_tela = []; jogador_tem_arma = False; tiro_peido_ativo = None

# --- NOVAS VARIÁVEIS DE CONTROLE PARA AS CONQUISTAS ---
coletou_powerup_na_partida = False
chefe_derrotado_na_partida = False


def reiniciar_jogo():
    global tempo_inicio_partida, pontuacao_atual, velocidade_tiro_atual, pontos_por_segundo_atual, proximo_aumento_dificuldade, tiros_desviados_total, jogador_tem_arma, tiro_peido_ativo
    global coletou_powerup_na_partida, chefe_derrotado_na_partida # Reinicia as novas flags
    
    player_rect.center = (150, ALTURA / 2); player_hitbox.center = player_rect.center; tiros_boss.clear(); powerups_na_tela.clear()
    tempo_inicio_partida = pygame.time.get_ticks(); pontuacao_atual = 0; velocidade_tiro_atual = VELOCIDADE_TIRO_INICIAL
    pontos_por_segundo_atual = PONTOS_POR_SEGUNDO_INICIAL; proximo_aumento_dificuldade = 60000; tiros_desviados_total = 0
    jogador_tem_arma = False; tiro_peido_ativo = None
    
    coletou_powerup_na_partida = False # Reinicia
    chefe_derrotado_na_partida = False # Reinicia

game = True; estado_jogo = "tela_inicial"; tela_cheia = False
scroll_y = 0; velocidade_scroll = 30

# === O CORAÇÃO DO JOGO (O LOOP PRINCIPAL) ===
while game:
    pos_mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                tela_cheia = not tela_cheia
                if tela_cheia: janela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
                else: janela = pygame.display.set_mode((LARGURA, ALTURA))
            if estado_jogo == "jogando" and event.key == pygame.K_SPACE and jogador_tem_arma and tiro_peido_ativo is None:
                jogador_tem_arma = False; tiro_peido_ativo = tiro_peido_img.get_rect(midleft=player_rect.midright)
        
        if estado_jogo == "tela_inicial":
            if botao_jogar.foi_clicado(event): reiniciar_jogo(); estado_jogo = "jogando"
            if botao_conquistas.foi_clicado(event): estado_jogo = "tela_conquistas"; scroll_y = 0
            if botao_sair.foi_clicado(event): game = False
        elif estado_jogo == "tela_conquistas":
            if botao_voltar.foi_clicado(event): estado_jogo = "tela_inicial"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: scroll_y += velocidade_scroll
                elif event.button == 5: scroll_y -= velocidade_scroll
        elif estado_jogo == "jogando":
            if event.type == EVENTO_TIRO_BOSS:
                pos_y_tiro = random.randint(boss_rect.top + 5, boss_rect.bottom - 5); novo_tiro = pygame.Rect(boss_rect.left, pos_y_tiro, 20, 10); tiros_boss.append(novo_tiro)
            if event.type == EVENTO_SPAWN_POWERUP:
                if not powerups_na_tela and not jogador_tem_arma and tiro_peido_ativo is None:
                    pos_x = random.randint(100, boss_rect.left - 50); pos_y = random.randint(50, ALTURA - 50)
                    novo_powerup = powerup_item_img.get_rect(center=(pos_x, pos_y)); powerups_na_tela.append(novo_powerup)
        elif estado_jogo == "game_over":
            if botao_jogar_novamente.foi_clicado(event): reiniciar_jogo(); estado_jogo = "jogando"
            if botao_voltar_menu.foi_clicado(event): reiniciar_jogo(); estado_jogo = "tela_inicial"

    # --- LÓGICA DE ATUALIZAÇÃO E DESENHO DE CADA TELA ---
    if estado_jogo == "tela_inicial":
        janela.blit(fundoini, (0, 0)); janela.blit(logocomp, logo_rect); [b.checar_hover(pos_mouse) for b in botoes_menu]; [b.desenhar(janela) for b in botoes_menu]
    
    elif estado_jogo == "tela_conquistas":
        janela.blit(fundoini, (0, 0))
        titulo_surf = fonte_titulo.render("Conquistas", True, BRANCO)
        titulo_rect = titulo_surf.get_rect(center=(LARGURA/2, 60))
        janela.blit(titulo_surf, titulo_rect)

        viewport_rect = pygame.Rect(LARGURA/2 - 450, 120, 900, 480)
        painel_fundo = pygame.Surface(viewport_rect.size, pygame.SRCALPHA)
        painel_fundo.fill((CINZA_ESCURO[0], CINZA_ESCURO[1], CINZA_ESCURO[2], 150))
        pygame.draw.rect(painel_fundo, (BRANCO[0], BRANCO[1], BRANCO[2], 200), painel_fundo.get_rect(), 2, border_radius=15)
        janela.blit(painel_fundo, viewport_rect.topleft)

        card_altura = 100; espacamento = 20
        altura_total_conteudo = len(conquistas) * card_altura + (len(conquistas) - 1) * espacamento

        if altura_total_conteudo > viewport_rect.height:
            limite_scroll_inferior = viewport_rect.height - altura_total_conteudo - (2 * espacamento)
            scroll_y = max(limite_scroll_inferior, scroll_y)
            scroll_y = min(0, scroll_y)
        else:
            scroll_y = 0

        janela.set_clip(viewport_rect)

        card_largura = 800; pos_y_inicial = viewport_rect.top + espacamento; card_pos_x = LARGURA/2 - card_largura/2
        for i, (id, conquista) in enumerate(conquistas.items()):
            pos_y_atual = pos_y_inicial + i * (card_altura + espacamento)
            card_rect_desenho = pygame.Rect(card_pos_x, pos_y_atual + scroll_y, card_largura, card_altura)

            if card_rect_desenho.bottom > viewport_rect.top and card_rect_desenho.top < viewport_rect.bottom:
                card_surf = pygame.Surface((card_largura, card_altura), pygame.SRCALPHA)
                desbloqueada = conquista["desbloqueada"]
                
                if desbloqueada:
                    card_surf.fill((CINZA_CLARO[0], CINZA_CLARO[1], CINZA_CLARO[2], 180))
                    cor_nome, cor_desc, icone = OURO, BRANCO, conquista["icon"]
                else:
                    card_surf.fill((CINZA_ESCURO[0], CINZA_ESCURO[1], CINZA_ESCURO[2], 180))
                    cor_nome, cor_desc, icone = BRANCO, CINZA_CONQUISTA, icon_bloqueada

                pygame.draw.rect(card_surf, BRANCO, card_surf.get_rect(), 2, border_radius=10)
                icone_rect = icone.get_rect(centery=card_altura/2, left=20)
                card_surf.blit(icone, icone_rect)
                nome_surf = fonte_conquista.render(conquista["nome"], True, cor_nome)
                nome_rect = nome_surf.get_rect(topleft=(icone_rect.right + 20, 25))
                card_surf.blit(nome_surf, nome_rect)
                desc_surf = fonte_descricao.render(conquista["descricao"], True, cor_desc)
                desc_rect = desc_surf.get_rect(topleft=(icone_rect.right + 20, 55))
                card_surf.blit(desc_surf, desc_rect)
                janela.blit(card_surf, card_rect_desenho.topleft)

        janela.set_clip(None)
        botao_voltar.checar_hover(pos_mouse); botao_voltar.desenhar(janela)

    elif estado_jogo == "jogando":
        tempo_sobrevivido = pygame.time.get_ticks() - tempo_inicio_partida; teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] or teclas[pygame.K_w]: player_rect.y -= vel_player
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]: player_rect.y += vel_player
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: player_rect.x -= vel_player
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: player_rect.x += vel_player
        player_hitbox.center = player_rect.center
        player_rect.top = max(0, player_rect.top); player_rect.bottom = min(ALTURA, player_rect.bottom)
        player_rect.left = max(0, player_rect.left); player_rect.right = min(boss_rect.left, player_rect.right)
        for tiro in tiros_boss[:]:
            tiro.x -= velocidade_tiro_atual
            if tiro.right < 0: tiros_boss.remove(tiro); tiros_desviados_total += 1
        if tempo_sobrevivido >= proximo_aumento_dificuldade:
            velocidade_tiro_atual += 1.5; pontos_por_segundo_atual += 1; proximo_aumento_dificuldade += 60000
        pontuacao_atual = int((tempo_sobrevivido / 1000) * pontos_por_segundo_atual)
        
        # Detecta coleta de power-up para a conquista "Cê é o bixão mesmo"
        for powerup_rect in powerups_na_tela[:]:
            if player_hitbox.colliderect(powerup_rect):
                powerups_na_tela.remove(powerup_rect); jogador_tem_arma = True
                coletou_powerup_na_partida = True # Marca que o jogador pegou um power-up
        
        if tiro_peido_ativo:
            tiro_peido_ativo.x += 8
            if tiro_peido_ativo.colliderect(boss_rect):
                tiros_boss.clear(); tiro_peido_ativo = None
                chefe_derrotado_na_partida = True # Marca que o chefe foi derrotado
            elif tiro_peido_ativo.left > LARGURA: tiro_peido_ativo = None
        
        for tiro in tiros_boss:
            if player_hitbox.colliderect(tiro): pontuacao_final = pontuacao_atual; estado_jogo = "game_over"

        # === LÓGICA DE VERIFICAÇÃO DAS CONQUISTAS ===
        # Sobrevivência
        if not conquistas["SOBREVIVENTE_30S"]["desbloqueada"] and tempo_sobrevivido >= 30000: conquistas["SOBREVIVENTE_30S"]["desbloqueada"] = True; print("CONQUISTA: A LENDAAA!")
        if not conquistas["SOBREVIVENTE_1M"]["desbloqueada"] and tempo_sobrevivido >= 60000: conquistas["SOBREVIVENTE_1M"]["desbloqueada"] = True; print("CONQUISTA: UMA MÁQUINAA!")
        if not conquistas["SOBREVIVENTE_5M"]["desbloqueada"] and tempo_sobrevivido >= 300000: conquistas["SOBREVIVENTE_5M"]["desbloqueada"] = True; print("CONQUISTA: Só mais 5 minutinhos...")
        if not conquistas["SOBREVIVENTE_10M"]["desbloqueada"] and tempo_sobrevivido >= 600000: conquistas["SOBREVIVENTE_10M"]["desbloqueada"] = True; print("CONQUISTA: A Prova não era tão difícil")
        if not conquistas["SOBREVIVENTE_20M"]["desbloqueada"] and tempo_sobrevivido >= 1200000: conquistas["SOBREVIVENTE_20M"]["desbloqueada"] = True; print("CONQUISTA: Me formei (em enrolação)")
        if not conquistas["SOBREVIVENTE_1HR"]["desbloqueada"] and tempo_sobrevivido >= 3600000: conquistas["SOBREVIVENTE_1HR"]["desbloqueada"] = True; print("CONQUISTA: Platinado no jogo da vida")

        # Esquiva
        if not conquistas["ESQUIVA_100"]["desbloqueada"] and tiros_desviados_total >= 100: conquistas["ESQUIVA_100"]["desbloqueada"] = True; print("CONQUISTA: Cadê o lag?")
        if not conquistas["MESTRE_DO_CAOS"]["desbloqueada"] and tiros_desviados_total >= 500: conquistas["MESTRE_DO_CAOS"]["desbloqueada"] = True; print("CONQUISTA: Manejo de Crises (e tiros)")

        # Pontuação
        if not conquistas["RECORDISTA_100P"]["desbloqueada"] and pontuacao_atual >= 100: conquistas["RECORDISTA_100P"]["desbloqueada"] = True; print("CONQUISTA: Fui aprovado no estágio!")
        if not conquistas["RECORDISTA_250P"]["desbloqueada"] and pontuacao_atual >= 250: conquistas["RECORDISTA_250P"]["desbloqueada"] = True; print("CONQUISTA: Meti o louco no FGTS")
        if not conquistas["RECORDISTA_500P"]["desbloqueada"] and pontuacao_atual >= 500: conquistas["RECORDISTA_500P"]["desbloqueada"] = True; print("CONQUISTA: O pai tá on (com PIX)")
        if not conquistas["RECORDISTA_2000P"]["desbloqueada"] and pontuacao_atual >= 2000: conquistas["RECORDISTA_2000P"]["desbloqueada"] = True; print("CONQUISTA: Comprei uma NFT (de foguete)")
        if not conquistas["RECORDISTA_10000P"]["desbloqueada"] and pontuacao_atual >= 10000: conquistas["RECORDISTA_10000P"]["desbloqueada"] = True; print("CONQUISTA: Monopólio Intergalático")

        # --- NOVAS CONQUISTAS ---
        # "Cê é o bixão mesmo"
        if not conquistas["BIXAO"]["desbloqueada"] and pontuacao_atual >= 750 and not coletou_powerup_na_partida:
            conquistas["BIXAO"]["desbloqueada"] = True; print("CONQUISTA: Cê é o bixão mesmo!")
        
        # "Que ota?"
        if not conquistas["QUE_OTA"]["desbloqueada"] and chefe_derrotado_na_partida:
            conquistas["QUE_OTA"]["desbloqueada"] = True; print("CONQUISTA: Que ota?!")

        # "O fim?" (Sobreviver 1 hora E derrotar o chefe)
        if not conquistas["O_FIM"]["desbloqueada"] and conquistas["SOBREVIVENTE_1HR"]["desbloqueada"] and chefe_derrotado_na_partida:
            conquistas["O_FIM"]["desbloqueada"] = True; print("CONQUISTA: O fim?!")
            
        # "Abemsuado" (Todas as conquistas)
        todas_desbloqueadas = True
        for id_conquista in conquistas:
            if not conquistas[id_conquista]["desbloqueada"]:
                todas_desbloqueadas = False
                break
        if not conquistas["ABEMSUADO"]["desbloqueada"] and todas_desbloqueadas:
            conquistas["ABEMSUADO"]["desbloqueada"] = True; print("CONQUISTA: Abemsuado!")

        janela.blit(fundo, (0, 0)); janela.blit(player_img, player_rect); janela.blit(boss_img, boss_rect)
        for tiro in tiros_boss: pygame.draw.ellipse(janela, AMARELO, tiro)
        for powerup_rect in powerups_na_tela: janela.blit(powerup_item_img, powerup_rect)
        if tiro_peido_ativo: janela.blit(tiro_peido_img, tiro_peido_ativo)
        texto_pontos_surf = fonte_hud.render(f"Pontos: {pontuacao_atual}", True, BRANCO)
        texto_pontos_rect = texto_pontos_surf.get_rect(midtop=(LARGURA / 2, 20))
        janela.blit(texto_pontos_surf, texto_pontos_rect)
        if jogador_tem_arma:
            powerup_hud_rect = powerup_item_img.get_rect(topleft=(20, 20))
            janela.blit(powerup_item_img, powerup_hud_rect)

    elif estado_jogo == "game_over":
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA); overlay.fill((0, 0, 0, 180)); janela.blit(overlay, (0, 0))
        texto_surf = fonte_gameover.render("GAME OVER", True, VERMELHO); texto_rect = texto_surf.get_rect(center=(LARGURA / 2, ALTURA / 3)); janela.blit(texto_surf, texto_rect)
        texto_final_surf = fonte_botao.render(f"Sua pontuação: {pontuacao_final}", True, BRANCO)
        texto_final_rect = texto_final_surf.get_rect(center=(LARGURA/2, ALTURA/2 - 80))
        janela.blit(texto_final_surf, texto_final_rect)
        for botao in botoes_gameover: botao.checar_hover(pos_mouse); botao.desenhar(janela)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()