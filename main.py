import pygame
from modos.classico import iniciar_classico
from modos.fisico import iniciar_fisico


def menu():
    pygame.init()

    tela = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Super Tetris")

    fonte = pygame.font.Font(None, 50)

    rodando = True

    while rodando:
        tela.fill((20, 20, 20))

        titulo = fonte.render("SUPER TETRIS", True, (255, 255, 255))
        opcao1 = fonte.render("1 - Modo Clássico", True, (255, 255, 255))
        opcao2 = fonte.render("2 - Modo Físico", True, (255, 255, 255))

        tela.blit(titulo, (250, 100))
        tela.blit(opcao1, (230, 250))
        tela.blit(opcao2, (230, 320))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_1:
                    iniciar_classico()

                elif evento.key == pygame.K_2:
                    iniciar_fisico()

    pygame.quit()


if __name__ == "__main__":
    menu()