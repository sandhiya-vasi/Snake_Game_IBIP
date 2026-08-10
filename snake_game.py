import pygame
import random
import sys

pygame.init()

# ---------------- WINDOW ----------------
WIDTH = 720
HEIGHT = 1280

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
BLACK = (10, 16, 25)
BOARD = (20, 30, 45)
GREEN = (50, 220, 90)
LIGHT_GREEN = (100, 255, 140)
RED = (255, 70, 70)
WHITE = (245, 245, 245)
BUTTON = (45, 65, 90)
BORDER = (90, 110, 135)
GRAY = (130, 145, 160)
YELLOW = (255, 210, 70)

# ---------------- FONTS ----------------
title_font = pygame.font.Font(None, 68)
font = pygame.font.Font(None, 48)
button_font = pygame.font.Font(None, 55)
small_font = pygame.font.Font(None, 32)

# ---------------- BOARD ----------------
CELL = 30

BOARD_X = 30
BOARD_Y = 160
BOARD_W = 660
BOARD_H = 750

COLS = BOARD_W // CELL
ROWS = BOARD_H // CELL

# ---------------- DIFFICULTY ----------------
# Smaller delay = faster snake

DIFFICULTIES = {
    "EASY": 180,
    "MEDIUM": 110,
    "HARD": 65
}

difficulty = "EASY"
MOVE_DELAY = DIFFICULTIES[difficulty]

# ---------------- BUTTONS ----------------
CENTER = WIDTH // 2

EASY_BUTTON = pygame.Rect(50, 90, 190, 55)
MEDIUM_BUTTON = pygame.Rect(265, 90, 190, 55)
HARD_BUTTON = pygame.Rect(480, 90, 190, 55)

UP = pygame.Rect(CENTER - 55, 965, 110, 70)
LEFT = pygame.Rect(CENTER - 175, 1045, 110, 70)
DOWN = pygame.Rect(CENTER - 55, 1045, 110, 70)
RIGHT = pygame.Rect(CENTER + 65, 1045, 110, 70)

PLAY_AGAIN = pygame.Rect(CENTER - 150, 560, 300, 75)


# ---------------- FOOD ----------------
def create_food(snake):

    free_cells = []

    for x in range(COLS):
        for y in range(ROWS):

            if (x, y) not in snake:
                free_cells.append((x, y))

    if free_cells:
        return random.choice(free_cells)

    return None


# ---------------- RESET ----------------
def reset_game():

    x = COLS // 2
    y = ROWS // 2

    snake = [
        (x, y),
        (x - 1, y),
        (x - 2, y),
        (x - 3, y)
    ]

    direction = (1, 0)

    food = create_food(snake)

    score = 0

    game_over = False

    return snake, direction, food, score, game_over


# ---------------- DIRECTION ----------------
def change_direction(new_direction):

    global direction

    # Prevent reverse movement

    if (
        new_direction[0] + direction[0] == 0
        and
        new_direction[1] + direction[1] == 0
    ):
        return

    direction = new_direction


# ---------------- BUTTON ----------------
def draw_button(rect, text, selected=False):

    if selected:
        color = GREEN
    else:
        color = BUTTON

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        BORDER,
        rect,
        2,
        border_radius=15
    )

    text_surface = button_font.render(
        text,
        True,
        WHITE
    )

    screen.blit(
        text_surface,
        (
            rect.centerx -
            text_surface.get_width() // 2,

            rect.centery -
            text_surface.get_height() // 2
        )
    )


# ---------------- GAME ----------------
snake, direction, food, score, game_over = reset_game()

timer = 0

running = True

while running:

    dt = clock.tick(60)

    timer += dt

    # ---------------- EVENTS ----------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Keyboard
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                change_direction((0, -1))

            elif event.key == pygame.K_DOWN:
                change_direction((0, 1))

            elif event.key == pygame.K_LEFT:
                change_direction((-1, 0))

            elif event.key == pygame.K_RIGHT:
                change_direction((1, 0))

            elif event.key == pygame.K_r and game_over:

                snake, direction, food, score, game_over = reset_game()

        # Mouse / Touch
        elif event.type == pygame.MOUSEBUTTONDOWN:

            pos = event.pos

            # Difficulty buttons
            if EASY_BUTTON.collidepoint(pos):

                difficulty = "EASY"
                MOVE_DELAY = DIFFICULTIES[difficulty]

                snake, direction, food, score, game_over = reset_game()

            elif MEDIUM_BUTTON.collidepoint(pos):

                difficulty = "MEDIUM"
                MOVE_DELAY = DIFFICULTIES[difficulty]

                snake, direction, food, score, game_over = reset_game()

            elif HARD_BUTTON.collidepoint(pos):

                difficulty = "HARD"
                MOVE_DELAY = DIFFICULTIES[difficulty]

                snake, direction, food, score, game_over = reset_game()

            # Game controls
            elif not game_over:

                if UP.collidepoint(pos):
                    change_direction((0, -1))

                elif DOWN.collidepoint(pos):
                    change_direction((0, 1))

                elif LEFT.collidepoint(pos):
                    change_direction((-1, 0))

                elif RIGHT.collidepoint(pos):
                    change_direction((1, 0))

            # Restart
            elif game_over:

                if PLAY_AGAIN.collidepoint(pos):

                    snake, direction, food, score, game_over = reset_game()

    # ---------------- MOVE SNAKE ----------------

    if not game_over and timer >= MOVE_DELAY:

        timer = 0

        head_x, head_y = snake[0]

        dx, dy = direction

        new_head = (
            head_x + dx,
            head_y + dy
        )

        # Wall collision

        if (
            new_head[0] < 0
            or new_head[0] >= COLS
            or new_head[1] < 0
            or new_head[1] >= ROWS
        ):

            game_over = True

        # Self collision

        elif new_head in snake:

            game_over = True

        else:

            snake.insert(0, new_head)

            # Food

            if new_head == food:

                score += 1

                food = create_food(snake)

            else:

                snake.pop()

    # ---------------- DRAW ----------------

    screen.fill(BLACK)

    # Title

    title = title_font.render(
        "SNAKE GAME",
        True,
        LIGHT_GREEN
    )

    screen.blit(
        title,
        (
            WIDTH // 2 -
            title.get_width() // 2,
            15
        )
    )

    # Difficulty buttons

    draw_button(
        EASY_BUTTON,
        "EASY",
        difficulty == "EASY"
    )

    draw_button(
        MEDIUM_BUTTON,
        "MEDIUM",
        difficulty == "MEDIUM"
    )

    draw_button(
        HARD_BUTTON,
        "HARD",
        difficulty == "HARD"
    )

    # Board

    board = pygame.Rect(
        BOARD_X,
        BOARD_Y,
        BOARD_W,
        BOARD_H
    )

    pygame.draw.rect(
        screen,
        BOARD,
        board,
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        BORDER,
        board,
        3,
        border_radius=20
    )

    # Score

    score_text = font.render(
        "Score: " + str(score),
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (40, 175)
    )

    # Current difficulty

    level_text = small_font.render(
        "Level: " + difficulty,
        True,
        YELLOW
    )

    screen.blit(
        level_text,
        (
            WIDTH -
            level_text.get_width() -
            40,
            185
        )
    )

    # Food

    if food is not None:

        fx, fy = food

        pygame.draw.circle(
            screen,
            RED,
            (
                BOARD_X +
                fx * CELL +
                CELL // 2,

                BOARD_Y +
                fy * CELL +
                CELL // 2
            ),
            12
        )

    # Snake

    for i, (sx, sy) in enumerate(snake):

        rect = pygame.Rect(
            BOARD_X +
            sx * CELL + 2,

            BOARD_Y +
            sy * CELL + 2,

            CELL - 4,
            CELL - 4
        )

        if i == 0:
            color = LIGHT_GREEN
        else:
            color = GREEN

        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=8
        )

    # Instructions

    instruction = small_font.render(
        "Choose level • Use buttons or arrow keys",
        True,
        GRAY
    )

    screen.blit(
        instruction,
        (
            WIDTH // 2 -
            instruction.get_width() // 2,
            925
        )
    )

    # Movement buttons

    draw_button(UP, "↑")
    draw_button(LEFT, "←")
    draw_button(DOWN, "↓")
    draw_button(RIGHT, "→")

    # ---------------- GAME OVER ----------------

    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 190)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        text = title_font.render(
            "GAME OVER",
            True,
            RED
        )

        final_score = font.render(
            "Score: " + str(score),
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                CENTER -
                text.get_width() // 2,
                420
            )
        )

        screen.blit(
            final_score,
            (
                CENTER -
                final_score.get_width() // 2,
                495
            )
        )

        # Play again

        pygame.draw.rect(
            screen,
            GREEN,
            PLAY_AGAIN,
            border_radius=18
        )

        play_text = button_font.render(
            "PLAY AGAIN",
            True,
            WHITE
                PLAY_AGAIN.centery -
                play_text.get_height() // 2
            )
        )

    pygame.display.flip()


pygame.quit()
sys.exit()