import pygame

from config import (
    LARGURA_BLOCO,
    LARGURA_TELA,
    ALTURA_TELA
)

from models.peca import Peca

from physics.corpo_peca import CorpoPeca

from views.tela_survival import TelaSurvival


# ============================================================
# INICIALIZAÇÃO
# ============================================================

pygame.init()

tela = pygame.display.set_mode(
    (
        LARGURA_TELA,
        ALTURA_TELA
    )
)

pygame.display.set_caption(
    "NEON SURVIVAL - Teste de Física"
)

clock = pygame.time.Clock()


# ============================================================
# CRIAR PEÇA
# ============================================================

peca = Peca(
    0,
    0
)

print("Formato da peça:")
print(peca.formato)

print("Cor da peça:")
print(peca.cor)


# ============================================================
# TRANSFORMAR EM CORPO FÍSICO
# ============================================================

corpo = CorpoPeca(
    peca=peca,

    tamanho_bloco=LARGURA_BLOCO,

    # Centro da tela
    x=(
        LARGURA_TELA // 2
        - LARGURA_BLOCO
    ),

    y=50
)


# ============================================================
# VIEW
# ============================================================

tela_survival = TelaSurvival(
    LARGURA_TELA,
    ALTURA_TELA,
    LARGURA_BLOCO
)


# ============================================================
# LOOP
# ============================================================

rodando = True

while rodando:

    # Tempo entre frames
    dt = clock.tick(60) / 1000.0

    # --------------------------------------------------------
    # EVENTOS
    # --------------------------------------------------------

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

    # --------------------------------------------------------
    # FÍSICA
    # --------------------------------------------------------

    corpo.atualizar_fisica(
        dt
    )

    # --------------------------------------------------------
    # CHÃO
    # --------------------------------------------------------

    limite_y = (
        ALTURA_TELA
        - corpo.altura
    )

    if corpo.y >= limite_y:

        corpo.y = limite_y

        corpo.fixar()

    # --------------------------------------------------------
    # TELA
    # --------------------------------------------------------

    tela.fill(
        (10, 10, 20)
    )

    # Desenha uma linha indicando o chão
    pygame.draw.line(
        tela,
        (50, 50, 80),
        (0, ALTURA_TELA - 1),
        (LARGURA_TELA, ALTURA_TELA - 1),
        2
    )

    # Desenha a peça
    tela_survival.desenhar(
        tela,
        corpo
    )

    pygame.display.flip()


pygame.quit()