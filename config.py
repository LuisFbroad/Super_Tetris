# Dimensões da grade
LARGURA_BLOCO = 30
COLUNAS = 10
LINHAS = 20

LARGURA_TELA = COLUNAS * LARGURA_BLOCO
ALTURA_TELA = LINHAS * LARGURA_BLOCO

FPS = 60
VELOCIDADE_QUEDA_MS = 350

# Cores
COR_FUNDO = (0, 0, 0)
COR_GRADE = (40, 40, 40)

# Formatos das peças padrão (Tetraminós)
FORMATOS = [
    [[1, 1, 1, 1]],         # I
    [[1, 0, 0], [1, 1, 1]], # L
    [[0, 0, 1], [1, 1, 1]], # J
    [[1, 1], [1, 1]],       # O
    [[0, 1, 1], [1, 1, 0]], # S
    [[1, 1, 0], [0, 1, 1]], # Z
    [[0, 1, 0], [1, 1, 1]]  # T
]

CORES_PECAS = [
    (0, 255, 255),  # Ciano
    (255, 165, 0),  # Laranja
    (0, 0, 255),    # Azul
    (255, 255, 0),  # Amarelo
    (0, 255, 0),    # Verde
    (255, 0, 0),    # Vermelho
    (128, 0, 128)   # Roxo
]

# Configurações da Super Peça
CHANCE_SUPER_PECA = 0.20          
COR_SUPER_PECA = (255, 215, 0)     
COR_BORDA_SUPER = (255, 255, 255)   
MIN_BLOCOS_SUPER = 5
MAX_BLOCOS_SUPER = 6