import pygame
import random
import sys

pygame.init()

# =========================================================
# WINDOW
# =========================================================

WIDTH = 720
HEIGHT = 1280

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# =========================================================
# COLORS
# =========================================================

BG = (10, 16, 25)
BOARD = (20, 30, 45)

GREEN = (50, 220, 90)
LIGHT_GREEN = (100, 255, 140)

RED = (255, 70, 70)

WHITE = (245, 245, 245)

BLUE = (45, 65, 90)
BLUE_LIGHT = (70, 95, 125)

GRAY = (130, 145, 160)

YELLOW = (255, 210, 70)

# =========================================================
# FONTS
# =========================================================

title_font = pygame.font.Font(None, 80)
large_font = pygame.font.Font(None, 65)
font = pygame.font.Font(None, 48)
button_font = pygame.font.Font(None, 55)
small_font = pygame.font.Font(None, 32)

# =========================================================
# GAME BOARD
# =========================================================

CELL = 30

BOARD_X = 30
BOARD_Y = 160

BOARD_W = 660
BOARD_H = 750

COLS = BOARD_W // CELL
ROWS = BOARD_H // CELL

# =========================================================
# GAME MODES
# =========================================================
# Higher delay = slower snake

MODES = {
    "EASY": 180,
    "MEDIUM": 110,
    "HARD": 65
}

selected_mode = "EASY"

# =========================================================
# MENU BUTTONS
# =========================================================

EASY_BUTTON = pygame.Rect(
    120, 320, 480, 75
)

MEDIUM_BUTTON = pygame.Rect(
    120, 420, 480, 75
)

HARD_BUTTON = pygame.Rect(
    120, 520, 480, 75
)

START_BUTTON = pygame.Rect(
    170, 680, 380, 90
)

EXIT_MENU = pygame.Rect(
    170, 790, 380, 75
)

# =========================================================
# GAME CONTROL BUTTONS
# =========================================================

CENTER = WIDTH // 2

UP = pygame.Rect(
    CENTER - 55, 965, 110, 70
)

LEFT = pygame.Rect(
    CENTER - 175, 1045, 110, 70
)

DOWN = pygame.Rect(
    CENTER - 55, 1045, 110, 70
)

RIGHT = pygame.Rect(
    CENTER + 65, 1045, 110, 70
)

EXIT_GAME = pygame.Rect(
    CENTER - 100, 1130, 200, 60
)

# =========================================================
# GAME OVER BUTTON
# =========================================================

PLAY_AGAIN = pygame.Rect(
    CENTER - 150, 600, 300, 75
)

EXIT_OVER = pygame.Rect(
    CENTER - 150, 700, 300, 70
)


# =========================================================
# CREATE FOOD
# =========================================================

def create_food(snake):

    free_cells = []

    for x in range(COLS):

        for y in range(ROWS):

            if (x, y) not in snake:

                free_cells.append((x, y))

    if free_cells:

        return random.choice(free_cells)

    return None


# =========================================================
# RESET GAME
# =========================================================

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


# =========================================================
# CHANGE DIRECTION
# =========================================================

def change_direction(new_direction):

    global direction

    # Prevent the snake from moving directly backwards

    if (
        new_direction[0] + direction[0] == 0
        and
        new_direction[1] + direction[1] == 0
    ):
        return

    direction = new_direction


# =========================================================
# DRAW BUTTON
# =========================================================

def draw_button(rect, text, selected=False):

    if selected:

        color = GREEN

    else:

        color = BLUE

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=18
    )

    pygame.draw.rect(
        screen,
        BLUE_LIGHT,
        rect,
        3,
        border_radius=18
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


# =========================================================
# VARIABLES
# =========================================================

snake = []

direction = (1, 0)

food = None

score = 0

game_over = False

game_started = False

timer = 0

running = True


# =========================================================
# MAIN GAME LOOP
# =========================================================

while running:

    dt = clock.tick(60)

    timer += dt

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        # -------------------------------------------------
        # CLOSE WINDOW
        # -------------------------------------------------

        if event.type == pygame.QUIT:

            running = False

        # =================================================
        # KEYBOARD
        # =================================================

        elif event.type == pygame.KEYDOWN:

            # ---------------- MENU ----------------

            if not game_started:

                if event.key == pygame.K_1:

                    selected_mode = "EASY"

                elif event.key == pygame.K_2:

                    selected_mode = "MEDIUM"

                elif event.key == pygame.K_3:

                    selected_mode = "HARD"

                elif event.key == pygame.K_RETURN:

                    snake, direction, food, score, game_over = reset_game()

                    game_started = True

            # ---------------- GAME ----------------

            else:

                if not game_over:

                    if event.key == pygame.K_UP:

                        change_direction((0, -1))

                    elif event.key == pygame.K_DOWN:

                        change_direction((0, 1))

                    elif event.key == pygame.K_LEFT:

                        change_direction((-1, 0))

                    elif event.key == pygame.K_RIGHT:

                        change_direction((1, 0))

                    elif event.key == pygame.K_ESCAPE:

                        pygame.quit()

                        sys.exit()

                else:

                    if event.key == pygame.K_r:

                        snake, direction, food, score, game_over = reset_game()

                    elif event.key == pygame.K_ESCAPE:

                        pygame.quit()

                        sys.exit()

        # =================================================
        # MOUSE / TOUCH
        # =================================================

        elif event.type == pygame.MOUSEBUTTONDOWN:

            position = event.pos

            # =================================================
            # MENU SCREEN
            # =================================================

            if not game_started:

                # Easy

                if EASY_BUTTON.collidepoint(position):

                    selected_mode = "EASY"

                # Medium

                elif MEDIUM_BUTTON.collidepoint(position):

                    selected_mode = "MEDIUM"

                # Hard

                elif HARD_BUTTON.collidepoint(position):

                    selected_mode = "HARD"

                # Start

                elif START_BUTTON.collidepoint(position):

                    snake, direction, food, score, game_over = reset_game()

                    game_started = True

                # Exit

                elif EXIT_MENU.collidepoint(position):

                    pygame.quit()

                    sys.exit()

            # =================================================
            # GAME SCREEN
            # =================================================

            else:

                # ---------------- PLAYING ----------------

                if not game_over:

                    # EXIT

                    if EXIT_GAME.collidepoint(position):

                        pygame.quit()

                        sys.exit()

                    # UP

                    elif UP.collidepoint(position):

                        change_direction((0, -1))

                    # DOWN

                    elif DOWN.collidepoint(position):

                        change_direction((0, 1))

                    # LEFT

                    elif LEFT.collidepoint(position):

                        change_direction((-1, 0))

                    # RIGHT

                    elif RIGHT.collidepoint(position):

                        change_direction((1, 0))

                # ---------------- GAME OVER ----------------

                else:

                    # Play Again

                    if PLAY_AGAIN.collidepoint(position):

                        snake, direction, food, score, game_over = reset_game()

                    # Exit

                    elif EXIT_OVER.collidepoint(position):

                        pygame.quit()

                        sys.exit()

    # =====================================================
    # MOVE SNAKE
    # =====================================================

    if game_started and not game_over:

        move_delay = MODES[selected_mode]

        if timer >= move_delay:

            timer = 0

            head_x, head_y = snake[0]

            dx, dy = direction

            new_head = (
                head_x + dx,
                head_y + dy
            )

            # ------------------------------------------------
            # WALL COLLISION
            # ------------------------------------------------

            if (
                new_head[0] < 0
                or
                new_head[0] >= COLS
                or
                new_head[1] < 0
                or
                new_head[1] >= ROWS
            ):

                game_over = True

            # ------------------------------------------------
            # SELF COLLISION
            # ------------------------------------------------

            elif new_head in snake:

                game_over = True

            # ------------------------------------------------
            # NORMAL MOVEMENT
            # ------------------------------------------------

            else:

                snake.insert(
                    0,
                    new_head
                )

                # ------------------------------------------------
                # FOOD
                # ------------------------------------------------

                if new_head == food:

                    score += 1

                    food = create_food(snake)

                else:

                    snake.pop()

    # =====================================================
    # DRAW SCREEN
    # =====================================================

    screen.fill(BG)

    # =====================================================
    # MENU
    # =====================================================

    if not game_started:

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
                100
            )
        )

        # Select mode

        select_text = large_font.render(
            "SELECT GAME MODE",
            True,
            WHITE
        )

        screen.blit(
            select_text,
            (
                WIDTH // 2 -
                select_text.get_width() // 2,
                220
            )
        )

        # Mode buttons

        draw_button(
            EASY_BUTTON,
            "EASY",
            selected_mode == "EASY"
        )

        draw_button(
            MEDIUM_BUTTON,
            "MEDIUM",
            selected_mode == "MEDIUM"
        )

        draw_button(
            HARD_BUTTON,
            "HARD",
            selected_mode == "HARD"
        )

        # Start button

        pygame.draw.rect(
            screen,
            GREEN,
            START_BUTTON,
            border_radius=20
        )

        start_text = large_font.render(
            "START",
            True,
            WHITE
        )

        screen.blit(
            start_text,
            (
                START_BUTTON.centerx -
                start_text.get_width() // 2,

                START_BUTTON.centery -
                start_text.get_height() // 2
            )
        )

        # Exit button

        pygame.draw.rect(
            screen,
            RED,
            EXIT_MENU,
            border_radius=20
        )

        exit_text = large_font.render(
            "EXIT",
            True,
            WHITE
        )

        screen.blit(
            exit_text,
            (
                EXIT_MENU.centerx -
                exit_text.get_width() // 2,

                EXIT_MENU.centery -
                exit_text.get_height() // 2
            )
        )

        # Selected mode

        mode_text = font.render(
            "Selected: " + selected_mode,
            True,
            YELLOW
        )

        screen.blit(
            mode_text,
            (
                WIDTH // 2 -
                mode_text.get_width() // 2,
                900
            )
        )

    # =====================================================
    # GAME SCREEN
    # =====================================================

    else:

        # Title

        title = title_font.render(
            "SNAKE",
            True,
            LIGHT_GREEN
        )

        screen.blit(
            title,
            (30, 25)
        )

        # Score

        score_text = font.render(
            "Score: " + str(score),
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (
                WIDTH -
                score_text.get_width() -
                30,
                35
            )
        )

        # -------------------------------------------------
        # BOARD
        # -------------------------------------------------

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
            BLUE_LIGHT,
            board,
            3,
            border_radius=20
        )

        # -------------------------------------------------
        # MODE
        # -------------------------------------------------

        mode_text = small_font.render(
            "MODE: " + selected_mode,
            True,
            YELLOW
        )

        screen.blit(
            mode_text,
            (
                WIDTH // 2 -
                mode_text.get_width() // 2,
                920
            )
        )

        # -------------------------------------------------
        # FOOD
        # -------------------------------------------------

        if food is not None:

            fx, fy = food

            food_center = (
                BOARD_X +
                fx * CELL +
                CELL // 2,

                BOARD_Y +
                fy * CELL +
                CELL // 2
            )

            pygame.draw.circle(
                screen,
                RED,
                food_center,
                13
            )

        # -------------------------------------------------
        # SNAKE
        # -------------------------------------------------

        for index, (sx, sy) in enumerate(snake):

            rectangle = pygame.Rect(
                BOARD_X +
                sx * CELL + 2,

                BOARD_Y +
                sy * CELL + 2,

                CELL - 4,
                CELL - 4
            )

            if index == 0:

                color = LIGHT_GREEN

            else:

                color = GREEN

            pygame.draw.rect(
                screen,
                color,
                rectangle,
                border_radius=8
            )

        # -------------------------------------------------
        # CONTROL BUTTONS
        # -------------------------------------------------

        draw_button(
            UP,
            "↑"
        )

        draw_button(
            LEFT,
            "←"
        )

        draw_button(
            DOWN,
            "↓"
        )

        draw_button(
            RIGHT,
            "→"
        )

        # -------------------------------------------------
        # EXIT BUTTON INSIDE GAME
        # -------------------------------------------------

        pygame.draw.rect(
            screen,
            RED,
            EXIT_GAME,
            border_radius=15
        )

        exit_game_text = button_font.render(
            "EXIT",
            True,
            WHITE
        )

        screen.blit(
            exit_game_text,
            (
                EXIT_GAME.centerx -
                exit_game_text.get_width() // 2,

                EXIT_GAME.centery -
                exit_game_text.get_height() // 2
            )
        )

        # =================================================
        # GAME OVER
        # =================================================

        if game_over:

            # Dark overlay

            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 200)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            # Game over text

            game_over_text = title_font.render(
                "GAME OVER",
                True,
                RED
            )

            screen.blit(
                game_over_text,
                (
                    WIDTH // 2 -
                    game_over_text.get_width() // 2,
                    400
                )
            )

            # Score

            final_score = font.render(
                "Final Score: " + str(score),
                True,
                WHITE
            )

            screen.blit(
                final_score,
                (
                    WIDTH // 2 -
                    final_score.get_width() // 2,
                    490
                )
            )

            # Play Again

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
            )

            screen.blit(
                play_text,
                (
                    PLAY_AGAIN.centerx -
                    play_text.get_width() // 2,

                    PLAY_AGAIN.centery -
                    play_text.get_height() // 2
                )
            )

            # Exit after Game Over

            pygame.draw.rect(
                screen,
                RED,
                EXIT_OVER,
                border_radius=18
            )

            exit_over_text = button_font.render(
                "EXIT",
                True,
                WHITE
            )

            screen.blit(
                exit_over_text,
                (
                    EXIT_OVER.centerx -
                    exit_over_text.get_width() // 2,

                    EXIT_OVER.centery -
                    exit_over_text.get_height() // 2
                )
            )

    pygame.display.flip()


# =========================================================
# EXIT
# =========================================================

pygame.quit()
sys.exit()
