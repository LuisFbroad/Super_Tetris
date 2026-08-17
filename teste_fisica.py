import pygame

from physics.fisica import CorpoFisico
from physics.colisao import Colisor


pygame.init()

LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode(
    (LARGURA, ALTURA)
)

pygame.display.set_caption(
    "Teste de Física"
)

clock = pygame.time.Clock()

bloco = CorpoFisico(
    x=350,
    y=50,
    largura=40,
    altura=40
)

rodando = True

while rodando:

    dt = clock.tick(60) / 1000.0

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

    # Física
    bloco.atualizar(dt)

    # Colisão com chão
    Colisor.colisao_com_chao(
        bloco,
        ALTURA
    )

    # Tela
    tela.fill(
        (10, 10, 20)
    )

    pygame.draw.rect(
        tela,
        (0, 240, 255),
        (
            int(bloco.x),
            int(bloco.y),
            bloco.largura,
            bloco.altura
        )
    )

    pygame.display.flip()


pygame.quit()