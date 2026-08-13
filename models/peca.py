import random
from config import (
    FORMATOS,
    CORES_PECAS,
    CHANCE_SUPER_PECA,
    COR_SUPER_PECA,
    COR_BORDA_SUPER,
    MIN_BLOCOS_SUPER,
    MAX_BLOCOS_SUPER
)

class Peca:
    def __init__(self, x=3, y= 0):
        self.x = x
        self.y = y
        indice = random.randint(0, len(FORMATOS) - 1)
        self.formato = FORMATOS[indice]
        self.cor = CORES_PECAS[indice]

    def obter_posicoes_globais(self):

        posicoes = []
        for i, linha in enumerate(self.formato):
            for j, bloco in enumerate(linha):
                if bloco:
                    posicoes.append((self.x + j, self.y + i))
        return posicoes

    def rotacionar(self):
        self.formato = [list(linha) for linha in zip(*self.formato[::-1])]

class Superpeca(Peca):
    def __init__(self, x=3, y=0):
        super().__init__(x, y)

        self.is_super = True
        self.cor = COR_SUPER_PECA

        qtd_blocos = random.randint(MIN_BLOCOS_SUPER, MAX_BLOCOS_SUPER)
        self.formato = self._gerar_formato_aleatorio(qtd_blocos)

        def _gerar_formato_aleatorio(self, num_blocos):
            tamanho = 4
            grid = [[0 for _ in range(tamanho)] for _ in range(tamanho)]

            cx, cy = 1, 1
            grid[cx][cy] = 1
            posicoes = [(cx, cy)]
            blocos_criados = 1

            while blocos_criados < num_blocos:
                bx, by = random.choice(posicoes)
                dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                nx, ny = bx + dx, by + dy

                if 0 <= nx < tamanho and 0 <= tamanho and grid[ny][nx] == 0:
                    grid[ny][nx] = 1
                    posicoes.append((nx,ny))
                    blocos_criados += 1


        def _recortar_matriz(self, grid):
            grid_filtrado = [linha for linha in grid if any(linha)]
            colunas = [j for j in range(len(grid_filtrado[0])) if any(grid_filtrado[i][j] for i in range(len(grid_filtrado)))]
            min_c, max_c = min(colunas), max(colunas)
            return [linha[min_c:max_c + 1] for linha in grid_filtrado]