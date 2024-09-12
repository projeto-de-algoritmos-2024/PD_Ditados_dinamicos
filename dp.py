from colorama import Fore, Style, init
import numpy as np

init(autoreset=True)


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

    alignment_x, alignment_y, colored_alignment_x, colored_alignment_y = reconstruct_alignment(x, y, dp, pgap, pxy)

    return dp[m][n], alignment_x, alignment_y, colored_alignment_x, colored_alignment_y


def reconstruct_alignment(x, y, M, gap_cost, mismatch_cost):
    i, j = len(x), len(y)
    alignment_x = []
    alignment_y = []
    colored_alignment_x = []
    colored_alignment_y = []
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and M[i][j] == M[i-1][j-1] + (mismatch_cost if x[i-1] != y[j-1] else 0):
    
            alignment_x.append(x[i-1])
            alignment_y.append(y[j-1])
            if x[i-1] == y[j-1]:
        
                colored_alignment_x.append(Fore.LIGHTYELLOW_EX + x[i-1] + Style.RESET_ALL)
                colored_alignment_y.append(Fore.LIGHTYELLOW_EX + y[j-1] + Style.RESET_ALL)
            else:
        
                colored_alignment_x.append(Fore.LIGHTBLUE_EX + x[i-1] + Style.RESET_ALL)
                colored_alignment_y.append(Fore.LIGHTBLUE_EX + y[j-1] + Style.RESET_ALL)
            i -= 1
            j -= 1
        elif i > 0 and M[i][j] == M[i-1][j] + gap_cost:
    
            alignment_x.append(x[i-1])
            alignment_y.append('-')
            colored_alignment_x.append(Fore.LIGHTGREEN_EX + x[i-1] + Style.RESET_ALL)
            colored_alignment_y.append(Fore.LIGHTGREEN_EX + '-' + Style.RESET_ALL)
            i -= 1
        else:
    
            alignment_x.append('-')
            alignment_y.append(y[j-1])
            colored_alignment_x.append(Fore.LIGHTGREEN_EX + '-' + Style.RESET_ALL)
            colored_alignment_y.append(Fore.LIGHTGREEN_EX + y[j-1] + Style.RESET_ALL)
            j -= 1
    
    alignment_x.reverse()
    alignment_y.reverse()
    colored_alignment_x.reverse()
    colored_alignment_y.reverse()
    
    return ''.join(alignment_x), ''.join(alignment_y), ''.join(colored_alignment_x), ''.join(colored_alignment_y)

def find_most_similar(phrases, user_input, gap_cost=50000, mismatch_cost=1):
    min_distance = float('inf')
    most_similar_phrase = ""
    best_alignment = ("", "")
    colored_alignment = ("", "")
    
    for phrase in phrases:
        distance, aligned_x, aligned_y, colored_x, colored_y = sequence_alignment(user_input, phrase, gap_cost, mismatch_cost)
        if distance < min_distance:
            min_distance = distance
            most_similar_phrase = phrase
            best_alignment = (aligned_x, aligned_y)
            colored_alignment = (colored_x, colored_y)
    
    return most_similar_phrase, min_distance, best_alignment, colored_alignment
def load_phrases_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        phrases = [line.strip() for line in file.readlines()]
    return phrases
phrases = load_phrases_from_file('frases.txt')
user_input = input("Digite uma frase: ")
similar_phrase, distance, alignment, colored_alignment = find_most_similar(phrases, user_input, gap_cost=5, mismatch_cost=3)
print(f"A frase mais semelhante é: '{similar_phrase}' com uma distância de {distance}.")
print("Alinhamento:")
print(colored_alignment[1])
print(colored_alignment[0])
