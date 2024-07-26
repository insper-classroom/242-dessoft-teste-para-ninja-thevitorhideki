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
running = True

numbers = gera_numeros()

game_state = {
    'menu': True,
    'playing': False,
    'result': False,
    'game_over': False
}

block1_visible = True
block2_visible = True
block3_visible = True

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
hasClicked = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state['menu']:
            mouse_pos = pygame.mouse.get_pos()
            if play_button.collidepoint(mouse_pos):
                start_time_game = pygame.time.get_ticks()
                game_state['menu'] = False
                game_state['playing'] = True
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state['playing']:
            mouse_pos = pygame.mouse.get_pos()
            if block1_rect.collidepoint(mouse_pos):
                current_time = pygame.time.get_ticks()
                block1_visible = False
                hasClicked = True
                game_state['result'] = True
                game_state['playing'] = False
            elif block2_rect.collidepoint(mouse_pos):
                current_time = pygame.time.get_ticks()
                block2_visible = False
                hasClicked = True
                game_state['result'] = True
                game_state['playing'] = False
            elif block3_rect.collidepoint(mouse_pos):
                current_time = pygame.time.get_ticks()
                block3_visible = False
                hasClicked = True
                game_state['result'] = True
                game_state['playing'] = False

    screen.fill("white")

    if game_state['menu']:
        pygame.draw.rect(screen, (200, 200, 200), play_button)
        screen.blit(play_button_text, play_button_text.get_rect(
            center=(WIDTH/2, HEIGHT/2)))
    elif game_state['game_over']:
        score_text = font.render(
            f"Você teve {correct_answers} respostas corretas", True, (0, 0, 0))
        screen.blit(score_text, score_text.get_rect(
            center=(WIDTH/2, HEIGHT/2)))
    else:
        current_time_game = pygame.time.get_ticks()
        elapsed_time = current_time_game - start_time_game
        if elapsed_time >= 60000:
            game_state['playing'] = False
            game_state['game_over'] = True

        elapsed_text = font.render(
            f"{math.ceil((60000-elapsed_time)/1000)}", True, (0, 0, 0))
        screen.blit(elapsed_text, (WIDTH-65, 20))

        text_numbers = [font.render(f"{numbers[i]}", True, (0, 0, 0))
                        for i in range(0, 3)]
        target = font.render(f"{numbers[-1]}", True, (0, 0, 0))
        block1_rect = pygame.Rect((WIDTH/2-50, HEIGHT-150), (100, 100))
        block2_rect = pygame.Rect((WIDTH/2-50, HEIGHT-250), (100, 100))
        block3_rect = pygame.Rect((WIDTH/2-50, HEIGHT-350), (100, 100))

        # Chão
        pygame.draw.rect(screen, (200, 200, 200),
                         pygame.Rect((0, HEIGHT-50), (WIDTH, 50)))

        # Blocos e números
        if (block1_visible):
            pygame.draw.rect(screen, (0, 0, 255), block1_rect)
            screen.blit(text_numbers[0], text_numbers[0].get_rect(
                center=(block1_rect.center)))
        else:
            if (numbers[1] + numbers[2] == numbers[3]):
                screen.blit(correct, correct.get_rect(
                    center=(block1_rect.center)))
                if hasClicked:
                    correct_answers += 1
                    hasClicked = False
            else:
                screen.blit(wrong, wrong.get_rect(
                    center=(block1_rect.center)))
                if hasClicked:
                    lives -= 1
                    hasClicked = False

        if (block2_visible):
            pygame.draw.rect(screen, (0, 255, 0), block2_rect)
            screen.blit(text_numbers[1], text_numbers[1].get_rect(
                center=(block2_rect.center)))
        else:
            if (numbers[0] + numbers[2] == numbers[3]):
                screen.blit(correct, correct.get_rect(
                    center=(block2_rect.center)))
                if hasClicked:
                    correct_answers += 1
                    hasClicked = False
            else:
                screen.blit(wrong, wrong.get_rect(
                    center=(block2_rect.center)))
                if hasClicked:
                    lives -= 1
                    hasClicked = False

        if (block3_visible):
            pygame.draw.rect(screen, (255, 0, 0), block3_rect)
            screen.blit(text_numbers[2], text_numbers[2].get_rect(
                center=(block3_rect.center)))
        else:
            if (numbers[0] + numbers[1] == numbers[3]):
                screen.blit(correct, correct.get_rect(
                    center=(block3_rect.center)))
                if hasClicked:
                    correct_answers += 1
                    hasClicked = False
            else:
                screen.blit(wrong, wrong.get_rect(
                    center=(block3_rect.center)))
                if hasClicked:
                    lives -= 1
                    hasClicked = False

        # Alvo
        screen.blit(target, (25, 25))

        if game_state['result']:
            start_time = pygame.time.get_ticks()
            elapsed_time = start_time - current_time
            if elapsed_time >= 1000:
                if lives == 0:
                    game_state['result'] = False
                    game_state['game_over'] = True
                else:
                    block1_visible = True
                    block2_visible = True
                    block3_visible = True
                    game_state['result'] = False
                    game_state['playing'] = True
                    numbers = gera_numeros()

    pygame.display.flip()
    clock.tick(60)
