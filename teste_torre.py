import pygame

from config import (
    LARGURA_BLOCO,
    LARGURA_TELA,
    ALTURA_TELA
)

from models.peca import Peca
from physics.corpo_peca import CorpoPeca
from models.survival.torre import Torre
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
    "NEON SURVIVAL - TESTE DE DUAS PECAS"
)

clock = pygame.time.Clock()


# ============================================================
# TORRE
# ============================================================

torre = Torre(
    LARGURA_TELA,
    ALTURA_TELA
)


# ============================================================
# PRIMEIRA PEÇA
# ============================================================

peca1 = Peca(0, 0)

corpo1 = CorpoPeca(
    peca=peca1,
    tamanho_bloco=LARGURA_BLOCO,

    # Esquerda
    x=150,
    y=50
)

torre.adicionar_peca(corpo1)


# ============================================================
# SEGUNDA PEÇA
# ============================================================

peca2 = Peca(0, 0)

corpo2 = CorpoPeca(
    peca=peca2,
    tamanho_bloco=LARGURA_BLOCO,

    # Direita
    x=500,
    y=50
)

torre.adicionar_peca(corpo2)


# ============================================================
# TESTE NO TERMINAL
# ============================================================

print()
print("========================================")
print(" TESTE DA TORRE")
print("========================================")

print(
    "Quantidade de peças:",
    torre.quantidade_pecas()
)

for i, corpo in enumerate(
    torre.obter_pecas()
):

    print(
        f"Peça {i + 1}: "
        f"X={corpo.x} "
        f"Y={corpo.y} "
        f"Fixada={corpo.fixada}"
    )

print("========================================")
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
# LOOP
# ============================================================

rodando = True

while rodando:

    dt = clock.tick(60) / 1000.0

    # ========================================================
    # EVENTOS
    # ========================================================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

    # ========================================================
    # FÍSICA
    # ========================================================

    torre.atualizar(dt)

    # ========================================================
    # TELA
    # ========================================================

    tela.fill(
        (10, 10, 20)
    )

    # ========================================================
    # CHÃO
    # ========================================================

    pygame.draw.line(
        tela,
        (80, 80, 100),
        (0, ALTURA_TELA - 1),
        (LARGURA_TELA, ALTURA_TELA - 1),
        2
    )

    # ========================================================
    # DESENHAR PEÇAS
    # ========================================================

    for corpo in torre.obter_pecas():

        tela_survival.desenhar(
            tela,
            corpo
        )

    # ========================================================
    # ATUALIZAR
    # ========================================================

    pygame.display.flip()


pygame.quit()