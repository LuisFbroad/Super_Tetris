import pygame
import random

class Particula:
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.cor = cor
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-6, 2)
        self.gravidade = 0.25
        self.tamanho = random.randint(3, 6)
        self.vida = 255  # Opacidade (Alfa)

    def atualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravidade
        self.vida -= 10  # Desaparece aos poucos
        if self.tamanho > 0.1:
            self.tamanho -= 0.1

    def desenhar(self, superficie):
        if self.vida > 0:
            surf_particula = pygame.Surface((int(self.tamanho * 2), int(self.tamanho * 2)), pygame.SRCALPHA)
            cor_com_alfa = (*self.cor[:3], max(0, int(self.vida)))
            pygame.draw.circle(surf_particula, cor_com_alfa, (int(self.tamanho), int(self.tamanho)), int(self.tamanho))
            superficie.blit(surf_particula, (int(self.x), int(self.y)))


class GerenciadorParticulas:
    def __init__(self):
        self.particulas = []

    def criar_explosao_linha(self, y_linha, largura, cor=(255, 255, 255)):
        for x in range(0, largura, 10):
            for _ in range(3):
                self.particulas.append(Particula(x, y_linha, cor))

    def atualizar_e_desenhar(self, superficie):
        for p in self.particulas[:]:
            p.atualizar()
            p.desenhar(superficie)
            if p.vida <= 0:
                self.particulas.remove(p)