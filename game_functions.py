# import pygame
import random
import settings
from utils import *

# ========== constants ==========

# colors
black = (0, 0, 0)
background_color = (200, 200, 200)

# text colors
unpressed_text_color = (150, 150, 150)
pressed_text_color = (100, 100, 100)

# buttons colors
button_unpressed_color = (200, 200, 200)
button_pressed_color = (150, 150, 150)


class CoordsSizes:
    def __init__(self, screen_size, margin_factor, grid_number_squares):
        self.screen_size = screen_size
        self.margin_factor = margin_factor
        self.grid_number_squares = grid_number_squares
        self.grid_size = self.get_size_grid()
        self.grid_coords = self.get_grid_coords()
        self.grid_block_side = self.get_grid_block_side()
        self.timer_rect_coords = 0, 0
        self.timer_rect_sizes = self.get_timer_sizes()
        self.mines_rect_coords = self.get_mines_coords()
        self.mines_rect_sizes = self.timer_rect_sizes
        self.again_button_coords = 0, screen_size[1] - self.timer_rect_sizes[1]
        self.again_button_sizes = self.timer_rect_sizes
        self.exit_button_coords = self.mines_rect_coords[0], self.again_button_coords[1]
        self.exit_button_sizes = self.timer_rect_sizes

    def get_size_grid(self):
        screen_size_x, screen_size_y = self.screen_size[0], self.screen_size[1]
        # maximize grid size
        if screen_size_x > screen_size_y:
            return screen_size_y, screen_size_y
        return screen_size_x, screen_size_x

    def get_grid_coords(self):
        screen_size_x, screen_size_y = self.screen_size[0], self.screen_size[1]
        grid_size = self.grid_size[0]  # grid_size_x = grid_size_y
        return (screen_size_x - grid_size) // 2, 0

    def get_grid_block_side(self):
        grid_size = self.grid_size[0]  # grid_size_x = grid_size_y
        return grid_size / (self.grid_number_squares + (self.grid_number_squares + 1) * self.margin_factor)

    def get_timer_sizes(self):
        grid_x = self.grid_coords[0]
        return grid_x, grid_x // 2

    def get_mines_coords(self):
        grid_x = self.grid_coords[0]
        grid_size = self.grid_size[0]
        return grid_x + grid_size, 0


class Image:
    def __init__(self, square_size):
        self.image_size = (square_size, square_size)

        # # name number images
        # self.name_img_one = "1_square.png"
        # self.name_img_two = "2_square.png"
        # self.name_img_three = "3_square.png"
        # self.name_img_four = "4_square.png"
        # self.name_img_five = "5_square.png"
        # self.name_img_six = "6_square.png"
        # self.name_img_seven = "7_square.png"
        # self.name_img_eight = "8_square.png"
        #
        # # name unpressed image
        # self.name_unpressed_image = "square.png"
        #
        # # name empty square image
        # self.name_empty_square_image = "empty_square.png"
        #
        # # name flag image
        # self.name_flag_image = "flag_square.png"
        #
        # # name mine image
        # self.name_mine_image = "mine_square.png"

        self.flag_image = open_image(self.image_size, settings.name_image_flag)
        self.mine_image = open_image(self.image_size, settings.name_image_mine)
        self.empty_image = open_image(self.image_size, settings.name_image_empty_square)
        self.unpressed_image = open_image(self.image_size, settings.name_image_unpressed_square)
        self.number_images = self.get_number_images()
        self.number_images.insert(0, self.empty_image)

    def get_number_images(self):
        return [open_image(self.image_size, settings.name_image_one), open_image(self.image_size, settings.name_image_two),
                open_image(self.image_size, settings.name_image_three), open_image(self.image_size, settings.name_image_four),
                open_image(self.image_size, settings.name_image_five), open_image(self.image_size, settings.name_image_six),
                open_image(self.image_size, settings.name_image_seven), open_image(self.image_size, settings.name_image_eight)]


class Square:
    def __init__(self, square_size, square_coord, grid_coord, number, game_screen):
        self.size = square_size
        self.square_coord = square_coord
        self.grid_coord = grid_coord
        self.number = number
        self.have_flag = False

        self.have_mine = False
        if self.number == -1:
            self.have_mine = True

        self.left_pressed = False
        self.right_pressed = False

        self.game_screen = game_screen

    def draw(self, image):
        if self.right_pressed and not self.left_pressed:
            # draw flag
            if not self.have_flag:
                self.game_screen.blit(image.flag_image, self.grid_coord)
                self.have_flag = True
            # clear flag
            else:
                self.game_screen.blit(image.unpressed_image, self.grid_coord)
                self.have_flag = False

        elif self.left_pressed:
            # draw mine
            if self.have_mine:
                self.game_screen.blit(image.mine_image, self.grid_coord)
                self.have_flag = False
            # draw number
            else:
                self.game_screen.blit(image.number_images[self.number], self.grid_coord)
                self.have_flag = False
        else:
            self.game_screen.blit(image.unpressed_image, self.grid_coord)
            self.have_flag = False


class DisplayNumbers:
    def __init__(self, coords, sizes, game_screen):
        self.game_screen = game_screen
        self.coords = coords
        self.sizes = sizes
        self.color = unpressed_text_color
        self.font = pygame.font.Font(None, 100)

    def draw(self, message):
        font = self.font
        self.text = font.render(message, False, self.color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.coords[0] + self.sizes[0] // 2, self.coords[1] + self.sizes[1] // 2
        self.game_screen.blit(self.text, self.text_rect)

    def update(self):
        pygame.draw.rect(self.game_screen, background_color, self.text_rect)


class Grid:
    def __init__(self, size_grid, coords_grid, number_squares_grid, margin_factor, side_square, number_mines, game_screen):
        self.game_screen = game_screen
        self.size = size_grid
        self.coords = coords_grid
        self.number_squares = number_squares_grid
        self.margin_factor = margin_factor
        self.number_mines = number_mines
        self.mine_coord_list = []
        self.create_mine_list()
        self.side_square = side_square
        self.margin = self.margin_factor * self.side_square
        self.squares = []  # list all squares objects
        self.create_square_list()

        images = Image(self.side_square)
        self.images = images

    def calculate_grid_coord_square(self, square_coord):
        grid_x, grid_y = self.coords
        x, y = square_coord[0], square_coord[1]
        return grid_x + int((x + 1) * self.margin + x * self.side_square), \
               grid_y + int((y + 1) * self.margin + y * self.side_square)

    def create_mine_list(self):
        i = 0
        while i < self.number_mines:
            x, y = random.randint(0, self.number_squares - 1), random.randint(0, self.number_squares - 1)
            if (x, y) not in self.mine_coord_list:
                self.mine_coord_list.append((x, y))
                i += 1

    def create_square_list(self):
        for line in range(self.number_squares):
            for col in range(self.number_squares):
                number_mines_arround = 0
                if (line, col) in self.mine_coord_list:
                    number_mines_arround = -1
                else:
                    for x in range(max(line - 1, 0), min(line + 1, self.number_squares - 1) + 1):
                        for y in range(max(col - 1, 0), min(col + 1, self.number_squares - 1) + 1):
                            if x != line or y != col:
                                if (x, y) in self.mine_coord_list:
                                    number_mines_arround += 1
                square = Square(self.side_square, (line, col), self.calculate_grid_coord_square((line, col)),
                                number_mines_arround, self.game_screen)
                self.squares.append(square)

    def draw(self):
        for i in range(self.number_squares ** 2):
            self.squares[i].draw(self.images)

    def draw_all_squares(self):
        for square in self.squares:
            if not square.left_pressed:
                square.left_pressed = True
                square.right_pressed = False
                square.draw(self.images)

    def draw_square_neighbors(self, center_square, visited_squares):
        center_square.right_pressed = False
        center_square.left_pressed = True
        if center_square.have_flag:
            settings.current_mines += 1
        center_square.draw(self.images)
        square_x, square_y = center_square.square_coord[0], center_square.square_coord[1]
        for x in range(max(square_x - 1, 0), min(square_x + 1, self.number_squares - 1) + 1):
            for y in range(max(square_y - 1, 0), min(square_y + 1, self.number_squares - 1) + 1):
                if x != square_x or y != square_y:
                    for square in self.squares:
                        if (x, y) == square.square_coord:
                            if square not in visited_squares:
                                visited_squares.append(square)
                                if square.number == 0:
                                    self.draw_square_neighbors(square, visited_squares)
                                    pygame.display.update()
                                elif square.number > 0:
                                    # square.right_pressed = False
                                    square.left_pressed = True
                                    if square.have_flag:
                                        settings.current_mines += 1
                                    square.draw(self.images)
                                    pygame.display.update()


# class OptionsRatio:
#     def __init__(self):
#         self.size_ratio = 0.50, 0.40
#         self.border_ratio = 0.10, 0.40
#         self.image_ratio = 0.20, 0.20
#         self.button_ratio = 0.10, 0.20
#         self.text_ratio = 0.40, 0.20


# class ScreenOptions:
#     def __init__(self, options_ratio, screen_options_ratio, screen_size, game_screen, image_name, list_numbers):
#
#         # position options in game screen
#         screen_options_coords = screen_options_ratio[0] * screen_size[0], screen_options_ratio[1] * screen_size[1]
#
#         # sides size of surface options
#         options_size = options_ratio.size_ratio[0] * screen_size[1], options_ratio.size_ratio[1] * screen_size[1]
#
#         # constant
#         y = screen_options_coords[1] + options_size[1] * options_ratio.border_ratio[1]
#
#         # sides size of objects in options surface
#         ranges_1 = options_ratio.border_ratio[0]
#         ranges_2 = 2 * ranges_1 + options_ratio.image_ratio[0]
#         ranges_3 = ranges_2 + options_ratio.button_ratio[0]
#         ranges_4 = ranges_3 + options_ratio.text_ratio[0]
#
#         # position options components in game screen
#         self.image_coords = screen_options_coords[0] + options_size[0] * ranges_1, y
#         self.left_button_coords = screen_options_coords[0] + options_size[0] * ranges_2, y
#         self.text_coords = screen_options_coords[0] + options_size[0] * ranges_3, y
#         self.right_button_coords = screen_options_coords[0] + options_size[0] * ranges_4, y
#
#         # size objects
#         self.image_sizes = options_size[0] * options_ratio.image_ratio[0], options_size[1] * options_ratio.image_ratio[1]
#         self.left_button_sizes = options_size[0] * options_ratio.button_ratio[0], options_size[1] * options_ratio.button_ratio[1]
#         self.text_sizes = options_size[0] * options_ratio.text_ratio[0], options_size[1] * options_ratio.text_ratio[1]
#         self.right_button_sizes = self.left_button_sizes
#
#         # surface buttons
#         self.image_button_left_unpressed = open_image(self.left_button_sizes, "left_triangle_unpressed.png")
#         self.image_button_left_pressed = open_image(self.left_button_sizes, "left_triangle_pressed.png")
#         self.image_button_right_unpressed = open_image(self.right_button_sizes, "right_triangle_unpressed.png")
#         self.image_button_right_pressed = open_image(self.right_button_sizes, "right_triangle_pressed.png")
#
#         # buttons states
#         self.left_button_pressed = False
#         self.right_button_pressed = False
#         self.left_button_click = False
#         self.right_button_click = False
#
#         # mouse state
#         self.mouse_click = False
#         self.mouse_coords = (0, 0)
#
#         self.image = open_image(self.image_sizes, image_name)
#
#         self.game_screen = game_screen
#
#         # all possible numbers to appear between buttons
#         self.list_number = list_numbers
#         self.index = 0
#
#         # text font
#         self.font = pygame.font.Font(None, 100)
#
#     # verify if mouse is over button and if was clicked
#     def verify_mouse_over_button(self):
#         mouse_x, mouse_y = self.mouse_coords
#         left_button_x, left_button_y = self.left_button_coords
#         left_button_size_x, left_button_size_y = self.left_button_sizes
#         right_button_x, right_button_y = self.right_button_coords
#         right_button_size_x, right_button_size_y = self.right_button_sizes
#
#         # verify if mouse is over left button
#         if left_button_x < mouse_x < left_button_x + left_button_size_x and \
#                 left_button_y < mouse_y < left_button_y + left_button_size_y:
#
#             # verify if left button pressed
#             if self.mouse_click:
#                 self.left_button_click = True
#             else:
#                 self.left_button_click = False
#
#             self.left_button_pressed = True
#         else:
#             self.left_button_pressed = False
#
#         # verify if mouse is over right button
#         if right_button_x < mouse_x < right_button_x + right_button_size_x and \
#                 right_button_y < mouse_y < right_button_y + right_button_size_y:
#
#             # verify if left button pressed
#             if self.mouse_click:
#                 self.right_button_click = True
#             else:
#                 self.right_button_click = False
#
#             self.right_button_pressed = True
#         else:
#             self.right_button_pressed = False
#
#     # update screen options
#     def detect_change_button_state(self):
#         left_button_last_state = self.left_button_pressed
#         right_button_last_state = self.right_button_pressed
#
#         last_index = self.index
#
#         self.verify_mouse_over_button()
#         self.update_index()
#
#         left_button_new_state = self.left_button_pressed
#         right_button_new_state = self.right_button_pressed
#
#         new_index = self.index
#
#         # verify left button state
#         if left_button_last_state != left_button_new_state:
#             self.draw_button_left()
#             pygame.display.update()
#
#         # verify right button state
#         if right_button_last_state != right_button_new_state:
#             self.draw_button_right()
#             pygame.display.update()
#
#         # verify index
#         if last_index != new_index:
#             self.draw_number()
#             pygame.display.update()
#
#             self.mouse_click = False
#             self.right_button_click = False
#             self.left_button_click = False
#
#     def draw_image(self):
#         self.game_screen.blit(self.image, self.image_coords)
#
#     def draw_button_left(self):
#         if self.left_button_pressed:
#             self.game_screen.blit(self.image_button_left_pressed, self.left_button_coords)
#         else:
#             self.game_screen.blit(self.image_button_left_unpressed, self.left_button_coords)
#
#     def draw_button_right(self):
#         if self.right_button_pressed:
#             self.game_screen.blit(self.image_button_right_pressed, self.right_button_coords)
#         else:
#             self.game_screen.blit(self.image_button_right_unpressed, self.right_button_coords)
#
#     # def draw_buttons(self):
#     #     self.draw_button_left()
#     #     self.draw_button_right()
#
#     def update_index(self):
#         if self.right_button_click:
#             if self.index == len(self.list_number) - 1:
#                 self.index = 0
#             else:
#                 self.index += 1
#
#         if self.left_button_click:
#             if self.index == 0:
#                 self.index = len(self.list_number) - 1
#             else:
#                 self.index -= 1
#
#     def get_number(self):
#         return self.list_number[self.index]
#
#     def draw_number(self):
#         text_x, text_y = self.text_coords
#         text_size_x, text_size_y = self.text_sizes
#
#         self.update_number()
#
#         str_number = str(self.get_number())
#         number_surface = self.font.render(str_number, False, background_color)
#         number_rect = number_surface.get_rect()
#         number_rect.center = text_x + text_size_x // 2, text_y + text_size_y // 2
#         self.game_screen.blit(number_surface, number_rect)
#
#     def update_number(self):
#         number_rect = (self.text_coords[0], self.text_coords[1], self.text_sizes[0], self.text_sizes[1])
#         pygame.draw.rect(self.game_screen, (230, 230, 230), number_rect)
#
#     def draw(self):
#         self.draw_image()
#         self.draw_button_left()
#         self.draw_number()
#         self.draw_button_right()
