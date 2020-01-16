import pygame


def open_image(image_size, image_name):
    try:
        image = pygame.image.load(image_name)
        image = pygame.transform.scale(image, (int(image_size[0]), int(image_size[1])))
    except pygame.error:
        print("Image not found: " + image_name)
        exit()
    else:
        return image


def update_time(start_timer, recursion_time, text_display):
    if (pygame.time.get_ticks() - start_timer) % 1000 == 0:
        new_time = (pygame.time.get_ticks() - start_timer - recursion_time) // 1000
        text_display.update()
        text_display.draw(str(new_time))
        pygame.display.update()

# def draw_text(text_coords):
#     text_surface = pygame.font
