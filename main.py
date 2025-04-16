import pygame
import random
pygame.init()
WHITE = (250, 250, 250)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GOLD = (255, 205, 200)
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()
SNAKE_SPEED = 8
font = pygame.font.SysFont("bahnschrift", 25)
snake_head_img = pygame.image.load("eng/zmeika.png")
snake_head_img = pygame.transform.scale(snake_head_img, (CELL_SIZE, CELL_SIZE))
apple_sound = pygame.mixer.Sound("eng/apple_eat.wav")
game_over_sound = pygame.mixer.Sound("eng/game_over.wav")
snake_colors = [GREEN, YELLOW, ORANGE, PURPLE]
snake_color = GREEN
fruit_count = 3
def draw_snake(snake_body, color):
    for i, pos in enumerate(snake_body):
        if i == len(snake_body) - 1:
            screen.blit(snake_head_img, (pos[0], pos[1]))
        else:
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE),
                border_radius=5,
            )
def draw_fruits(fruits):
    for fruit in fruits:
        pygame.draw.ellipse(
            screen, fruit[2], pygame.Rect(fruit[0], fruit[1], CELL_SIZE, CELL_SIZE)
        )
def show_score(score):
    value = font.render(f"Счет: {score}", True, WHITE)
    screen.blit(value, [10, 10])
def start_menu():
    selecting = True
    options = ["Играть", "Выйти"]
    selected = 0
    while selecting:
        screen.fill(BLUE)
        for i, option in enumerate(options):
            color = WHITE if i != selected else (255, 0, 0)
            msg = font.render(f"{i + 1}. {option}", True, color)
            screen.blit(msg, [WIDTH // 3, HEIGHT // 3 + i * 40])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        selecting = False
                    else:
                        pygame.quit()
                        quit()
def select_snake_color():
    global snake_color
    options = ["Зеленый", "Желтый", "Оранжевый", "Фиолетовый"]
    selected = 0
    selecting = True
    while selecting:
        screen.fill(BLUE)
        for i, option in enumerate(options):
            color = WHITE if i != selected else (255, 0, 0)
            msg = font.render(f"{i + 1}. {option}", True, color)
            screen.blit(msg, [WIDTH // 10, HEIGHT // 3 + i * 40])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    snake_color = snake_colors[selected]
                    selecting = False
def select_fruit_count():
    global fruit_count
    options = ["3 яблока", "5 яблок", "7 яблок"]
    selected = 0
    selecting = True
    while selecting:
        screen.fill(BLUE)
        for i, option in enumerate(options):
            color = WHITE if i != selected else (255, 0, 0)
            msg = font.render(f"{i + 1}. {option}", True, color)
            screen.blit(msg, [WIDTH // 3, HEIGHT // 3 + i * 40])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    fruit_count = [3, 5, 7][selected]
                    selecting = False
def game_loop():
    game_over = False
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = CELL_SIZE, 0
    snake_body = [[x, y]]
    snake_length = 1
    fruits = generate_fruits(fruit_count)
    speed = SNAKE_SPEED
    score = 0
    normal_apple_count = 0
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -CELL_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = CELL_SIZE, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -CELL_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, CELL_SIZE
        x += dx
        y += dy
        if x >= WIDTH and x < 0 and y >= HEIGHT and y < 0 or [x, y] in snake_body:
            game_over_sound.play()
            pygame.time.delay(1500)
            start_menu()
            return game_loop()
        screen.fill(BLUE)
        draw_fruits(fruits)
        snake_body.append([x, y])
        if len(snake_body) > snake_length:
            del snake_body[0]
        for fruit in fruits[:]:
            if x == fruit[0] and y == fruit[1]:
                apple_sound.play()
                if fruit[2] == GOLD:
                    score += 10
                    snake_length += 10
                    normal_apple_count = 0
                else:
                    score += 1
                    snake_length += 1
                    normal_apple_count += 1
                if normal_apple_count == 10:
                    normal_apple_count = 0
                    fruits.append(generate_fruit(True))
                fruits.append(generate_fruit(False))
        draw_snake(snake_body, snake_color)
        show_score(score)
        pygame.display.flip()
        clock.tick(int(speed))
def generate_fruit(is_gold=False):
    if is_gold:
        return [
            random.randrange(0, WIDTH - CELL_SIZE, CELL_SIZE),
            random.randrange(0, HEIGHT - CELL_SIZE, CELL_SIZE),
            GOLD,
        ]
    else:
        return [
            random.randrange(0, WIDTH - CELL_SIZE, CELL_SIZE),
            random.randrange(0, HEIGHT - CELL_SIZE, CELL_SIZE),
            BLUE,
        ]
def generate_fruits(count):
    return [generate_fruit(False) for _ in range(count)]
start_menu()
select_snake_color()
select_fruit_count()
game_loop()


