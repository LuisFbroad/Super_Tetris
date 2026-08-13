import random
from config import FORMATOS, CORES_PECAS, MIN_BLOCOS_SUPER, MAX_BLOCOS_SUPER, COR_SUPER_PECA

class Peca:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.indice_tipo = random.randint(0, len(FORMATOS) - 1)
        self.formato = [linha[:] for linha in FORMATOS[self.indice_tipo]]
        self.cor = CORES_PECAS[self.indice_tipo]
        self.is_super = False

    def girar(self, tabuleiro):
        """Gira a matriz no sentido horário com suporte a Wall Kick."""
        formato_antigo = self.formato
        # Rotacionar matriz 90 graus
        self.formato = [list(linha) for linha in zip(*self.formato[::-1])]

        # Tentar posicionar na posição original
        if not tabuleiro.verificar_colisao(self):
            return True

        # --- WALL KICK: Tenta deslocar a peça para permitir o giro ---
        deslocamentos = [(-1, 0), (1, 0), (0, -1), (-2, 0), (2, 0)]
        for dx, dy in deslocamentos:
            self.x += dx
            self.y += dy
            if not tabuleiro.verificar_colisao(self):
                return True
            # Reverte o deslocamento testado
            self.x -= dx
            self.y -= dy

        # Se nenhum deslocamento funcionou, desfaz a rotação
        self.formato = formato_antigo
        return False


class SuperPeca(Peca):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_super = True
        self.cor = COR_SUPER_PECA
        self.formato = self._gerar_formato_aleatorio()

    def _gerar_formato_aleatorio(self):
        num_blocos = random.randint(MIN_BLOCOS_SUPER, MAX_BLOCOS_SUPER)
        blocos = {(0, 0)}
        vizinhos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while len(blocos) < num_blocos:
            base_x, base_y = random.choice(list(blocos))
            dx, dy = random.choice(vizinhos)
            blocos.add((base_x + dx, base_y + dy))

        min_x = min(b[0] for b in blocos)
        max_x = max(b[0] for b in blocos)
        min_y = min(b[1] for b in blocos)
        max_y = max(b[1] for b in blocos)

        largura = max_x - min_x + 1
        altura = max_y - min_y + 1

        matriz = [[0] * largura for _ in range(altura)]
        for bx, by in blocos:
            matriz[by - min_y][bx - min_x] = 1

        return matriz