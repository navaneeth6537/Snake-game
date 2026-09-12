import pygame
import random
import os

pygame.init()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")

pygame.mixer.music.load(os.path.join(ASSETS, "music.wav"))
pygame.mixer.music.play(-1)


WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

bg = pygame.image.load(os.path.join(ASSETS, "sky.png"))
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

head_img_up = pygame.image.load(os.path.join(ASSETS, "snake_head.png")).convert_alpha()
head_img_up = pygame.transform.scale(head_img_up, (CELL_SIZE, CELL_SIZE))

body_img = pygame.image.load(os.path.join(ASSETS, "snake_body.png")).convert_alpha()
body_img = pygame.transform.scale(body_img, (CELL_SIZE, CELL_SIZE))

food_img = pygame.image.load(os.path.join(ASSETS, "food.png")).convert_alpha()
food_img = pygame.transform.scale(food_img, (CELL_SIZE, CELL_SIZE))

eatsound = pygame.mixer.Sound(os.path.join(ASSETS, "eat.wav"))

HEAD_IMAGES = {
    (0, -1): head_img_up,
    (0, 1): pygame.transform.rotate(head_img_up, 180),
    (-1, 0): pygame.transform.rotate(head_img_up, 90),
    (1, 0): pygame.transform.rotate(head_img_up, -90),
}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
GREEN = (60, 220, 60)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)
big_font = pygame.font.SysFont(None, 70)

GRID_W = WIDTH // CELL_SIZE
GRID_H = HEIGHT // CELL_SIZE

MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"


def random_food_position(snake):
    while True:
        fx = random.randrange(0, GRID_W) * CELL_SIZE
        fy = random.randrange(0, GRID_H) * CELL_SIZE
        if (fx, fy) not in snake:
            return fx, fy


def new_game():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (1, 0)  # moving right
    food = random_food_position(snake)
    score = 0
    return snake, direction, food, score


def draw_text_center(text, font_obj, color, y):
    surf = font_obj.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)


def draw_game(snake, direction, food, score):
    screen.blit(bg, (0, 0))
    screen.blit(food_img, food)

    
    for segment in snake[1:]:
        screen.blit(body_img, segment)
    head_image = HEAD_IMAGES[direction]
    screen.blit(head_image, snake[0])
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def draw_menu():
    screen.blit(bg, (0, 0))
    draw_text_center("SNAKE", big_font, GREEN, HEIGHT // 2 - 60)
    draw_text_center("Press SPACE to start", font, WHITE, HEIGHT // 2 + 10)
    draw_text_center("Arrow keys to move  |  ESC to quit", font, WHITE, HEIGHT // 2 + 50)


def draw_game_over(score):
    screen.blit(bg, (0, 0))
    draw_text_center("GAME OVER", big_font, RED, HEIGHT // 2 - 60)
    draw_text_center(f"Score: {score}", font, WHITE, HEIGHT // 2)
    draw_text_center("Press SPACE to play again  |  ESC to quit", font, WHITE, HEIGHT // 2 + 40)


def main():
    state = MENU
    snake, direction, food, score = new_game()
    pending_direction = direction

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif state == MENU and event.key == pygame.K_SPACE:
                    snake, direction, food, score = new_game()
                    pending_direction = direction
                    state = PLAYING

                elif state == GAME_OVER and event.key == pygame.K_SPACE:
                    snake, direction, food, score = new_game()
                    pending_direction = direction
                    state = PLAYING

                elif state == PLAYING:
                    if event.key == pygame.K_UP and direction[1] == 0:
                        pending_direction = (0, -1)
                    elif event.key == pygame.K_DOWN and direction[1] == 0:
                        pending_direction = (0, 1)
                    elif event.key == pygame.K_LEFT and direction[0] == 0:
                        pending_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction[0] == 0:
                        pending_direction = (1, 0)

        if state == PLAYING:
            direction = pending_direction
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0] * CELL_SIZE, head_y + direction[1] * CELL_SIZE)

            if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
                state = GAME_OVER
            elif new_head in snake:
                state = GAME_OVER
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    eatsound.play()
                    food = random_food_position(snake)
                else:
                    snake.pop()

        if state == MENU:
            draw_menu()
        elif state == PLAYING:
            draw_game(snake, direction, food, score)
        elif state == GAME_OVER:
            draw_game(snake, direction, food, score)
            draw_game_over(score)

        pygame.display.update()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
