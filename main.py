import pygame

from controllers.gerenciador_menu import GerenciadorMenu
from controllers.gerenciador_jogo import GerenciadorJogo
from controllers.modos.modo_classic import ModoClassic
from controllers.modos.modo_survival import ModoSurvival


def main():

    pygame.init()

    tela = pygame.display.set_mode((800, 800))

    pygame.display.set_caption("Super Tetris")

    menu = GerenciadorMenu(tela)

    rodando = True

    while rodando:

        escolha = menu.executar()

        if escolha == "CLASSIC":

            jogo = GerenciadorJogo()

            modo = ModoClassic(jogo)

            modo.executar()

        elif escolha == "SURVIVAL":

            survival = ModoSurvival(tela)

            resultado = survival.executar()

            if resultado == "MENU":
                continue

        elif escolha == "SAIR":

            rodando = False

    pygame.quit()


if __name__ == "__main__":
    main()