import pygame
from sys import exit
import math

from util.gerador import gera_numeros
from settings import WIDTH, HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ninja")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)

# Variável de controle do loop do jogo
running = True

# Número sorteados
numbers = gera_numeros()

# Estados do jogo
game_state = {
    'menu': True,
    'playing': False,
    'game_over': False
}

# Blocos
block_visible = [True, True, True]
block_rects = [
    pygame.Rect((WIDTH/2-50, HEIGHT-150), (100, 100)),
    pygame.Rect((WIDTH/2-50, HEIGHT-250), (100, 100)),
    pygame.Rect((WIDTH/2-50, HEIGHT-350), (100, 100)),
]
block_colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]

# Chão
ground = pygame.Rect((0, HEIGHT-50), (WIDTH, 50))

# Respostas
correct = font.render("Certo!", True, (0, 255, 0))
wrong = font.render("Errado!", True, (255, 0, 0))

# Botão de jogar
play_button = pygame.Rect((WIDTH/2-100, HEIGHT/2-50), (200, 100))
play_button_text = font.render("Jogar", True, (0, 0, 0))

# Pontuação
correct_answers = 0

# Vidas
lives = 3
has_clicked = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if game_state['menu']:
                if play_button.collidepoint(mouse_pos):
                    game_state['menu'] = False
                    game_state['playing'] = True
                    start_time_game = pygame.time.get_ticks()
                    
            elif game_state['playing']:
                for i, rect in enumerate(block_rects):
                    if rect.collidepoint(mouse_pos) and block_visible.count(True) == 3:
                        current_time = pygame.time.get_ticks()
                        block_visible[i] = False
                        has_clicked = True

    screen.fill("white")

    if game_state['menu']:
        pygame.draw.rect(screen, (200, 200, 200), play_button)
        screen.blit(play_button_text, play_button_text.get_rect(center=(WIDTH/2, HEIGHT/2)))

    elif game_state['game_over']:
        score_text = font.render(f"Você teve {correct_answers} respostas corretas", True, (0, 0, 0))
        screen.blit(score_text, score_text.get_rect(center=(WIDTH/2, HEIGHT/2)))

    elif game_state['playing']:
        current_time_game = pygame.time.get_ticks()
        elapsed_time = current_time_game - start_time_game
        
        if elapsed_time >= 60000:
            game_state['playing'] = False
            game_state['game_over'] = True

        # Timer
        elapsed_text = font.render(f"{math.ceil((60000-elapsed_time)/1000)}", True, (0, 0, 0))
        screen.blit(elapsed_text, (WIDTH-65, 20))

        # Números dos blocos
        text_numbers = [
            font.render(f"{numbers[0]}", True, (0, 0, 0)),
            font.render(f"{numbers[1]}", True, (0, 0, 0)),
            font.render(f"{numbers[2]}", True, (0, 0, 0))
        ]
        
        # Número alvo
        target = font.render(f"{numbers[-1]}", True, (0, 0, 0))
        screen.blit(target, (25, 25))

        # Chão
        pygame.draw.rect(screen, (200, 200, 200), ground)

        # Blocos e números
        for i, block in enumerate(block_rects):
            if (block_visible[i]):
                pygame.draw.rect(screen, block_colors[i], block)
                screen.blit(text_numbers[i], text_numbers[i].get_rect(center=(block.center)))
            else:
                if (sum(numbers[:-1]) - numbers[i] == numbers[-1]):
                    screen.blit(correct, correct.get_rect(center=(block.center)))
                    if has_clicked:
                        correct_answers += 1
                        has_clicked = False
                else:
                    screen.blit(wrong, wrong.get_rect(center=(block.center)))
                    if has_clicked:
                        lives -= 1
                        has_clicked = False

        # Verifica se algum bloco não está visível (foi clicado)
        if block_visible.count(True) < 3:
            start_time = pygame.time.get_ticks()
            elapsed_time = start_time - current_time
            
            if elapsed_time >= 1000:
                if lives == 0:
                    game_state['playing'] = False
                    game_state['game_over'] = True
                else:
                    block_visible = [True, True, True]
                    numbers = gera_numeros()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
