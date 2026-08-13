import random
import pygame

from models.peca import(
    Peca, 
    SuperPeca
)
from models.tabuleiro import Tabuleiro
from views.tela import TelaJogo
from config import(
    FPS,
    VELOCIDADE_QUEDA_MS,
    CHANCE_SUPER_PECA
)

class GerenciadorJogo:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.tela = TelaJogo()

        self.peca_atual = self._gerar_nova_peca()

        self.relogio = pygame.time.Clock()
        self.tempo_queda = 0
        self.velocidade_atual - VELOCIDADE_QUEDA_MS

        self.pontuacao = 0
        self.game_over = False

    def _gerar_nova_peca(self):
        if random.random() < CHANCE_SUPER_PECA:
            return SuperPeca()
        return Peca()

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.KEYDOWN:
                # Reiniciar jogo se der Game Over
                if self.game_over:
                    if evento.key == pygame.K_r:
                        self._reiniciar()
                    return True

                # Movimentos laterais
                if evento.key == pygame.K_LEFT:
                    self.peca_atual.x -= 1
                    if not self.tabuleiro.posicao_valida(self.peca_atual):
                        self.peca_atual.x += 1

                elif evento.key == pygame.K_RIGHT:
                    self.peca_atual.x += 1
                    if not self.tabuleiro.posicao_valida(self.peca_atual):
                        self.peca_atual.x -= 1

                # Queda rápida (Soft Drop)
                elif evento.key == pygame.K_DOWN:
                    self.peca_atual.y += 1
                    if not self.tabuleiro.posicao_valida(self.peca_atual):
                        self.peca_atual.y -= 1

                # Rotação
                elif evento.key == pygame.K_UP:
                    formato_antigo = self.peca_atual.formato
                    self.peca_atual.rotacionar()
                    if not self.tabuleiro.posicao_valida(self.peca_atual):
                        self.peca_atual.formato = formato_antigo

                # Queda instantânea (Hard Drop)
                elif evento.key == pygame.K_SPACE:
                    while self.tabuleiro.posicao_valida(self.peca_atual):
                        self.peca_atual.y += 1
                    self.peca_atual.y -= 1  # Retorna 1 passo válido
                    self.tempo_queda = self.velocidade_atual  # Força a fixação no próximo tick

        return True

    def atualizar(self, dt):
        if self.game_over:
            return

        self.tempo_queda += dt
        if self.tempo_queda >= self.velocidade_atual:
            self.tempo_queda = 0
            self.peca_atual.y += 1

            # Se encontrou obstáculo abaixo, fixa a peça
            if not self.tabuleiro.posicao_valida(self.peca_atual):
                self.peca_atual.y -= 1
                self.tabuleiro.fixar_peca(self.peca_atual)
                
                # Bônus de pontuação por encaixar Super Peça com sucesso
                if getattr(self.peca_atual, 'is_super', False):
                    self.pontuacao += 50

                # Verifica se limpou linhas
                linhas_limpas = self.tabuleiro.limpar_linhas()
                if linhas_limpas > 0:
                    # Pontuação progressiva por combos de linhas
                    multiplicadores = {1: 100, 2: 300, 3: 500, 4: 800}
                    self.pontuacao += multiplicadores.get(linhas_limpas, linhas_limpas * 200)
                    
                    # Aumenta um pouco a velocidade a cada linha (limite mínimo de 100ms)
                    self.velocidade_atual = max(100, VELOCIDADE_QUEDA_MS - (self.pontuacao // 500) * 20)

                # Gera próxima peça
                self.peca_atual = self._gerar_nova_peca()

                # Se a nova peça já nasce colidindo = Game Over
                if not self.tabuleiro.posicao_valida(self.peca_atual):
                    self.game_over = True

    def _reiniciar(self):
        self.tabuleiro = Tabuleiro()
        self.peca_atual = self._gerar_nova_peca()
        self.pontuacao = 0
        self.velocidade_atual = VELOCIDADE_QUEDA_MS
        self.game_over = False

    def executar(self):
        rodando = True
        while rodando:
            dt = self.relogio.tick(FPS)
            rodando = self.processar_eventos()
            self.atualizar(dt)
            self.tela.desenhar(self.tabuleiro, self.peca_atual, self.pontuacao, self.game_over)

        pygame.quit()