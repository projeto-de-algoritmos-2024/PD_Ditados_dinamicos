import pygame
import sys
import numpy as np

# Inicialização do Pygame
pygame.init()

# Definições de cores e tamanhos de tela
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
LIGHT_GREEN = (144, 238, 144)
LIGHT_BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 24

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alinhamento de Sequência")

font = pygame.font.SysFont("arial", FONT_SIZE)
input_box_font = pygame.font.SysFont("arial", FONT_SIZE, bold=True)
button_font = pygame.font.SysFont("arial", FONT_SIZE, bold=True)

# Função para desenhar texto na tela
def draw_text(text, x, y, color=BLACK, font=font):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Função para desenhar uma caixa de entrada de texto
def draw_input_box(x, y, w, h, text='', active=False):
    color = BLUE if active else GRAY
    pygame.draw.rect(screen, color, (x, y, w, h), 2)
    draw_text(text, x + 5, y + 5, BLACK, input_box_font)

# Função para desenhar um botão
def draw_button(x, y, w, h, text='', active=False):
    color = GREEN if active else GRAY
    pygame.draw.rect(screen, color, (x, y, w, h))
    draw_text(text, x + 5, y + 5, WHITE, button_font)

# Função para quebrar o texto em várias linhas
def wrap_text(text, font, max_width):
    wrapped_lines = []
    words = text.split(' ')
    current_line = ""

    for word in words:
        if font.size(current_line + word)[0] <= max_width:
            current_line += word + " "
        else:
            wrapped_lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        wrapped_lines.append(current_line.strip())

    return wrapped_lines

# Função para o alinhamento de sequência (mantendo o código original)
def sequence_alignment(x: str, y: str, pxy: int, pgap: int):
    m, n = len(x), len(y)
    dp = np.zeros([m + 1, n + 1], dtype=int)
    dp[0:m + 1, 0] = [i * pgap for i in range(m + 1)]
    dp[0, 0:n + 1] = [i * pgap for i in range(n + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j - 1] + pxy, dp[i - 1][j] + pgap, dp[i][j - 1] + pgap)

    alignment_x, alignment_y, colored_alignment_x, colored_alignment_y, mismatch_count, gap_count, match_count = reconstruct_alignment(x, y, dp, pgap, pxy)

    return dp[m][n], alignment_x, alignment_y, colored_alignment_x, colored_alignment_y, mismatch_count, gap_count, match_count

# Função para reconstruir o alinhamento
def reconstruct_alignment(x, y, M, gap_cost, mismatch_cost):
    i, j = len(x), len(y)
    alignment_x = []
    alignment_y = []
    colored_alignment_x = []
    colored_alignment_y = []
    mismatch_count = 0
    gap_count = 0
    match_count = 0
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and M[i][j] == M[i-1][j-1] + (mismatch_cost if x[i-1] != y[j-1] else 0):
            alignment_x.append(x[i-1])
            alignment_y.append(y[j-1])
            if x[i-1] == y[j-1]:
                colored_alignment_x.append((x[i-1], YELLOW))
                colored_alignment_y.append((y[j-1], YELLOW))
                match_count += 1
            else:
                colored_alignment_x.append((x[i-1], LIGHT_BLUE))
                colored_alignment_y.append((y[j-1], LIGHT_BLUE))
                mismatch_count += 1
            i -= 1
            j -= 1
        elif i > 0 and M[i][j] == M[i-1][j] + gap_cost:
            alignment_x.append(x[i-1])
            alignment_y.append('-')
            colored_alignment_x.append((x[i-1], LIGHT_GREEN))
            colored_alignment_y.append(('-', LIGHT_GREEN))
            gap_count += 1
            i -= 1
        else:
            alignment_x.append('-')
            alignment_y.append(y[j-1])
            colored_alignment_x.append(('-', LIGHT_GREEN))
            colored_alignment_y.append((y[j-1], LIGHT_GREEN))
            gap_count += 1
            j -= 1
    
    alignment_x.reverse()
    alignment_y.reverse()
    colored_alignment_x.reverse()
    colored_alignment_y.reverse()
    
    return ''.join(alignment_x), ''.join(alignment_y), colored_alignment_x, colored_alignment_y, mismatch_count, gap_count, match_count

# Função para encontrar a frase mais similar
def find_most_similar(phrases, user_input, gap_cost=50000, mismatch_cost=1):
    min_distance = float('inf')
    most_similar_phrase = ""
    best_alignment = ("", "")
    colored_alignment = ("", "")
    mismatch_count = gap_count = match_count = 0
    
    for phrase in phrases:
        distance, aligned_x, aligned_y, colored_x, colored_y, m_count, g_count, mt_count = sequence_alignment(user_input, phrase, gap_cost, mismatch_cost)
        if distance < min_distance:
            min_distance = distance
            most_similar_phrase = phrase
            best_alignment = (aligned_x, aligned_y)
            colored_alignment = (colored_x, colored_y)
            mismatch_count = m_count
            gap_count = g_count
            match_count = mt_count
    
    return most_similar_phrase, min_distance, best_alignment, colored_alignment, mismatch_count, gap_count, match_count

# Função para carregar frases de um arquivo
def load_phrases_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        phrases = [line.strip() for line in file.readlines()]
    return phrases

# Função para desenhar o alinhamento colorido na tela
def draw_colored_alignment(colored_alignment, start_x, start_y):
    for i, (char, color) in enumerate(colored_alignment):
        draw_text(char, start_x + i * FONT_SIZE, start_y, color)

# Função principal do Pygame
def main():
    # Variáveis de controle
    input_text = ''
    result_text = ''
    wrapped_result_text = []  # Inicializa wrapped_result_text como uma lista vazia
    aligned_result = [[], []]
    mismatch_count = gap_count = match_count = 0
    phrases = load_phrases_from_file('frases.txt')
    
    input_box_active = False  # Variável para controlar o estado da caixa de entrada
    button_active = False  # Variável para controlar o estado do botão "Nova Frase"

    # Dimensões da caixa de entrada
    input_box_rect = pygame.Rect(20, 60, 600, 40)
    # Dimensões do botão
    button_rect = pygame.Rect(630, 60, 150, 40)

    # Loop principal do Pygame
    while True:
        screen.fill(WHITE)

        # Eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Ativar/desativar a caixa de entrada quando o usuário clicar
                if input_box_rect.collidepoint(event.pos):
                    input_box_active = True
                else:
                    input_box_active = False

                # Verifica se o botão foi clicado
                if button_rect.collidepoint(event.pos) and button_active:
                    input_text = ''
                    result_text = ''
                    wrapped_result_text = []
                    aligned_result = [[], []]
                    mismatch_count = gap_count = match_count = 0
                    button_active = False
            elif event.type == pygame.KEYDOWN:
                if input_box_active:
                    if event.key == pygame.K_RETURN:
                        # Quando o usuário pressiona ENTER, encontra a frase mais similar
                        similar_phrase, distance, alignment, colored_alignment, m_count, g_count, mt_count = find_most_similar(phrases, input_text, gap_cost=5, mismatch_cost=3)
                        result_text = f"A frase mais semelhante é: '{similar_phrase}' com uma distância de {distance}."
                        
                        # Quebra o texto para caber na tela
                        wrapped_result_text = wrap_text(result_text, font, SCREEN_WIDTH - 40)
                        
                        aligned_result = [colored_alignment[0], colored_alignment[1]]
                        mismatch_count = m_count
                        gap_count = g_count
                        match_count = mt_count
                        button_active = True  # Ativa o botão para permitir nova entrada
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove o último caractere
                        input_text = input_text[:-1]
                    else:
                        # Adiciona o caractere pressionado ao texto de entrada
                        input_text += event.unicode

        # Desenha a interface gráfica
        draw_text("Digite uma frase:", 20, 20)
        draw_input_box(input_box_rect.x, input_box_rect.y, input_box_rect.width, input_box_rect.height, input_text, input_box_active)

        # Mostra o resultado na tela após a análise
        # Desenha cada linha do texto quebrado
        for i, line in enumerate(wrapped_result_text):
            draw_text(line, 20, 120 + i * (FONT_SIZE + 5), GREEN)
        
        draw_colored_alignment(aligned_result[0], 20, 160 + len(wrapped_result_text) * (FONT_SIZE + 5))  # Alinhamento 1
        draw_colored_alignment(aligned_result[1], 20, 200 + len(wrapped_result_text) * (FONT_SIZE + 5))  # Alinhamento 2

        # Desenha a lista de contagens de mismatches, gaps e matches
        if button_active:
            draw_text(f"Mismatch: {mismatch_count}", 20, 280 + len(wrapped_result_text) * (FONT_SIZE + 5), LIGHT_BLUE)
            draw_text(f"Gap: {gap_count}", 20, 310 + len(wrapped_result_text) * (FONT_SIZE + 5), LIGHT_GREEN)
            draw_text(f"Match: {match_count}", 20, 340 + len(wrapped_result_text) * (FONT_SIZE + 5), YELLOW)
            draw_button(button_rect.x, button_rect.y, button_rect.width, button_rect.height, "Nova Frase", True)

        # Atualiza a tela
        pygame.display.update()

if __name__ == "__main__":
    main()
