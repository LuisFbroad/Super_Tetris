# ==========================================
# CONFIGURAÇÕES GERAIS E TELA
# ==========================================
LARGURA_BLOCO = 30
COLUNAS = 10
LINHAS = 20

LARGURA_TELA = COLUNAS * LARGURA_BLOCO
ALTURA_TELA = LINHAS * LARGURA_BLOCO
FPS = 60

# ==========================================
# CORES & PALETA NEON
# ==========================================
COR_FUNDO = (15, 15, 26)           # Azul bem escuro / Roxo
COR_GRADE = (30, 30, 50)           # Linhas sutis
COR_PAINEL = (22, 22, 38)          # Fundo do painel lateral
COR_TEXTO = (220, 220, 240)
COR_TEXTO_MUTED = (120, 120, 150)   # Texto secundário/suave

# Cores vibrantes para as peças padrão
CORES_PECAS = [
    (0, 240, 255),   # Cyan (I)
    (0, 80, 255),    # Azul (J)
    (255, 140, 0),   # Laranja (L)
    (255, 215, 0),   # Amarelo (O)
    (50, 205, 50),   # Verde (S)
    (160, 32, 240),  # Roxo (T)
    (255, 30, 80)    # Vermelho/Rosa (Z)
]

# ==========================================
# SUPER PEÇAS
# ==========================================
CHANCE_SUPER_PECA = 0.1
COR_SUPER_PECA = (255, 223, 0)
COR_BORDA_SUPER = (255, 255, 255)
MIN_BLOCOS_SUPER = 5   # <--- Adicionado
MAX_BLOCOS_SUPER = 8   # <--- Adicionado

# ==========================================
# FORMATOS DAS PEÇAS (MATRIZES)
# ==========================================
FORMATOS = [
    [[1, 1, 1, 1]],                  # I
    [[1, 0, 0], [1, 1, 1]],          # J
    [[0, 0, 1], [1, 1, 1]],          # L
    [[1, 1], [1, 1]],                # O
    [[0, 1, 1], [1, 1, 0]],          # S
    [[0, 1, 0], [1, 1, 1]],          # T
    [[1, 1, 0], [0, 1, 1]]           # Z
]

# ==========================================
# DIFICULDADES DO MENU
# ==========================================
DIFICULDADES = {
    "FACIL": {
        "nome": "Fácil",
        "velocidade_ms": 700,
        "chance_super": 0.20,
        "cor": (50, 205, 50)
    },
    "MEDIO": {
        "nome": "Médio",
        "velocidade_ms": 450,
        "chance_super": 0.10,
        "cor": (255, 180, 0)
    },
    "DIFICIL": {
        "nome": "Difícil",
        "velocidade_ms": 200,
        "chance_super": 0.03,
        "cor": (255, 50, 80)
    }
}