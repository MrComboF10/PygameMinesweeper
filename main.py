import sys
import ctypes
from game_functions import *
from utils import *

# ========== variables ==========


sys.setrecursionlimit(999999999)

pygame.init()

ctypes.windll.user32.SetProcessDPIAware()

screen_size = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

screen = pygame.display.set_mode((screen_size[0], screen_size[1]), pygame.FULLSCREEN)

coords_sizes = CoordsSizes(screen_size, settings.margin_factor, settings.number_squares)

# game_exit = False


# def main_menu():
#     options_ratio = OptionsRatio()
#
#     grid_size_options = ScreenOptions(options_ratio, (0, 0.20), screen_size, screen, "mario.png", list(range(5, 51, 5)))
#     grid_size_options.game_screen.fill((230, 230, 230))
#     grid_size_options.draw()
#
#     dificulty_options = ScreenOptions(options_ratio, (0, 0.60), screen_size, screen, "luigi.png", list(range(1, 10)))
#     dificulty_options.draw()
#
#     pygame.display.update()
#
#     exit_menu = False
#
#     while not exit_menu:
#         grid_size_options.mouse_coords = pygame.mouse.get_pos()
#         dificulty_options.mouse_coords = pygame.mouse.get_pos()
#
#         grid_size_options.detect_change_button_state()
#         dificulty_options.detect_change_button_state()
#
#         grid_size_options.mouse_click = False
#         dificulty_options.mouse_click = False
#
#         for event in pygame.event.get():
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     grid_size_options.mouse_click = True
#                     dificulty_options.mouse_click = True
#
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     exit_menu = True


def game_menu():

    text_display = DisplayNumbers(coords_sizes.timer_rect_coords, coords_sizes.timer_rect_sizes, screen)

    mines_display = DisplayNumbers(coords_sizes.mines_rect_coords, coords_sizes.mines_rect_sizes, screen)

    grid = Grid(coords_sizes.grid_size, coords_sizes.grid_coords, settings.number_squares, settings.margin_factor,
                coords_sizes.grid_block_side, settings.number_mines, screen)

    grid.game_screen.fill(background_color)

    text_display.draw(str(0))

    mines_display.draw(str(settings.number_mines))

    grid.draw()

    pygame.display.update()

    game_over = False
    recursion_time = 0
    start_timer = pygame.time.get_ticks()

    while not game_over:
        go_recursion = False
        # timer
        update_time(start_timer, recursion_time, text_display)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]
                for square in grid.squares:
                    square_x, square_y = square.grid_coord[0], square.grid_coord[1]
                    length = square.size
                    if square_x <= mouse_x <= square_x + length and square_y <= mouse_y <= square_y + length and \
                            not square.left_pressed:

                        initial_flag = square.have_flag

                        # detect left click
                        if event.button == 1:
                            square.right_pressed = False
                            square.left_pressed = True
                            if square.number == 0:
                                recursion_time_start = pygame.time.get_ticks()
                                grid.draw_square_neighbors(square, [])

                                # mines display
                                mines_display.update()
                                mines_display.draw(str(settings.current_mines))
                                pygame.display.update()

                                recursion_time = pygame.time.get_ticks() - recursion_time_start

                                go_recursion = True
                            elif square.number == -1:  # detect mine
                                square.left_pressed = False
                                grid.draw_all_squares()
                                pygame.display.update()
                            else:
                                square.draw(grid.images)
                                pygame.display.update()

                        # right click
                        elif event.button == 3:
                            square.right_pressed = True
                            square.draw(grid.images)
                            pygame.display.update()

                        final_flag = square.have_flag

                        if not go_recursion:
                            if initial_flag and not final_flag:
                                settings.current_mines += 1
                            elif not initial_flag and final_flag:
                                settings.current_mines -= 1
                            mines_display.update()
                            mines_display.draw(str(settings.current_mines))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True

            if event.type == pygame.QUIT:
                game_over = True


game_menu()
# main_menu()

# def main_menu():