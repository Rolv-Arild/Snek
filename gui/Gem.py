import sys, os, pygame

from snek.Snake import Snek, UP, DOWN, LEFT, RIGHT, NONE, EMPTY, FOOD, HEAD, SNAKE

pygame.init()

clock = pygame.time.Clock()

scrsize = width, height = 400, 400
black = (0, 0, 0)

# to get the true full-screen size, do this BEFORE pygame.display.set_mode:
fullscreen_sz = pygame.display.Info().current_w, pygame.display.Info().current_h

# ---------- This works under Windows Vista, no promises elsewhere! ----------
# initially center the pygame window by setting %SDL_VIDEO_WINDOW_POS%
win_pos_left = 1 + ((fullscreen_sz[0] - width) // 2)
win_pos_top = 1 + ((fullscreen_sz[1] - height) // 2)
os.environ['SDL_VIDEO_WINDOW_POS'] = '{0},{1}'.format(win_pos_left, win_pos_top)
# ----------------------------------------------------------------------------

screen = pygame.display.set_mode(scrsize, pygame.RESIZABLE)
pygame.display.set_caption("Snake")

# ----------------------------------------------------------------------------
os.environ['SDL_VIDEO_WINDOW_POS'] = ''
# if you don't clear the environment variable, the window will reposition
# every time pygame.display.set_mode() gets called due to a VIDEORESIZE event.
# ----------------------------------------------------------------------------

arial = pygame.font.SysFont('arial,microsoftsansserif,courier', 14)
txt2display = arial.render("Snake", True, (255, 255, 255))
txt2display_w = txt2display.get_size()[0]

high_score: int = 0

rect = pygame.Rect(0, 0, 20, 20)

game_width = 20
game_height = 20
snake_length = 5

while True:
    clock.tick(1)
    s: Snek = Snek(game_width, game_height, snake_length, RIGHT)
    while s.move():
        changed = False
        move_lock: bool = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.VIDEORESIZE:
                scrsize = event.size  # or event.w, event.h
                screen = pygame.display.set_mode(scrsize, pygame.RESIZABLE)
                changed = True
            elif event.type == pygame.KEYDOWN:
                if not move_lock:
                    move = {
                        pygame.K_w: UP,
                        pygame.K_s: DOWN,
                        pygame.K_a: LEFT,
                        pygame.K_d: RIGHT,
                        pygame.K_UP: UP,
                        pygame.K_DOWN: DOWN,
                        pygame.K_LEFT: LEFT,
                        pygame.K_RIGHT: RIGHT,
                        pygame.K_p: NONE,
                        pygame.K_ESCAPE: NONE
                    }.get(event.key, None)
                    if move is not None:
                        s.set_direction(move)  # TODO fix being able to turn on the spot
                        move_lock = True

        width, height = screen.get_size()

        grid = s.snake_coordinates()  # TODO move over to more efficient data structure

        screen.fill(black)


        def change_pixel(color, x, y):
            rect = pygame.Rect(x * width // s.width, (s.height - y - 1) * height // s.height, width // s.width,
                               height // s.height)
            screen.fill(color, rect)


        first: bool = True
        for x, y in grid:
            if first:
                change_pixel((0, 200, 0), x, y)
            else:
                change_pixel((0, 255, 0), x, y)
            first = False

        change_pixel((255, 0, 0), s.food_x, s.food_y)

        pygame.display.set_caption(
            "Score: " + (s.length - snake_length).__str__() + " High score: " + high_score.__str__())

        screen.blit(txt2display, ((scrsize[0] + 1 - txt2display_w) // 2, 1))  # at top-center of screen
        pygame.display.update()
        if not changed:
            clock.tick(10)
    if s.length - snake_length > high_score:
        high_score = s.length - snake_length
