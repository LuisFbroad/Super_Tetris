import pygame

from config import (
    LARGURA_BLOCO,
    LARGURA_TELA,
    ALTURA_TELA
)

from models.peca import Peca
from physics.corpo_peca import CorpoPeca
from views.tela_survival import TelaSurvival


pygame.init()


# ============================================================
# TELA
# ============================================================

tela = pygame.display.set_mode(
    (
        LARGURA_TELA,
        ALTURA_TELA
    )
)

pygame.display.set_caption(
    "TESTE - DUAS PECAS"
)

clock = pygame.time.Clock()


# ============================================================
# PEÇA 1
# ============================================================

peca1 = Peca(0, 0)

corpo1 = CorpoPeca(
    peca=peca1,
    tamanho_bloco=LARGURA_BLOCO,
    x=150,
    y=100
)


# ============================================================
# PEÇA 2
# ============================================================

peca2 = Peca(0, 0)

corpo2 = CorpoPeca(
    peca=peca2,
    tamanho_bloco=LARGURA_BLOCO,
    x=500,
    y=100
)


# ============================================================
# DEBUG
# ============================================================

print()
print("================================")
print("PEÇA 1")
print("================================")

print("Formato:", corpo1.formato)
print("Cor:", corpo1.cor)
print("X:", corpo1.x)
print("Y:", corpo1.y)
print("Largura:", corpo1.largura)
print("Altura:", corpo1.altura)

print()
print("================================")
print("PEÇA 2")
print("================================")

print("Formato:", corpo2.formato)
print("Cor:", corpo2.cor)
print("X:", corpo2.x)
print("Y:", corpo2.y)
print("Largura:", corpo2.largura)
print("Altura:", corpo2.altura)

print()
print("================================")
print()


# ============================================================
# VIEW
# ============================================================

tela_survival = TelaSurvival(
    LARGURA_TELA,
    ALTURA_TELA,
    LARGURA_BLOCO
)


# ============================================================
# LISTA DE PEÇAS
# ============================================================

pecas = [
    corpo1,
    corpo2
]


# ============================================================
# LOOP
# ============================================================

rodando = True

while rodando:

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

    for corpo in pecas:

        corpo.atualizar_fisica(
            dt
        )

        # Chão
        limite_y = (
            ALTURA_TELA
            - corpo.altura
        )

        if corpo.y >= limite_y:

            corpo.y = limite_y
            corpo.fixar()

    # --------------------------------------------------------
    # DESENHO
    # --------------------------------------------------------

    tela.fill(
        (10, 10, 20)
    )

    # Chão
    pygame.draw.line(
        tela,
        (80, 80, 100),
        (0, ALTURA_TELA - 1),
        (LARGURA_TELA, ALTURA_TELA - 1),
        2
    )

    # Peças
    for corpo in pecas:

        tela_survival.desenhar(
            tela,
            corpo
        )

    pygame.display.flip()


pygame.quit()