import pygame
#import os
#current_directory = os.path.dirname(os.path.abspath(__file__))
#font_path = os.path.join(current_directory, 'Project', 'MyFont.ttf')
pygame.init()

WIDTH, HEIGHT = 800, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

def create_gradient_rect(surface, color1, color2, rect):
    for y in range(rect.height):
        color = (
            int(color1[0] + (color2[0] - color1[0]) * (y / rect.height)),
            int(color1[1] + (color2[1] - color1[1]) * (y / rect.height)),
            int(color1[2] + (color2[2] - color1[2]) * (y / rect.height))
        )
        pygame.draw.line(surface, color, (rect.left, rect.top + y), (rect.right, rect.top + y))

font = pygame.font.Font('MyFont.ttf', 36)
font_yet = pygame.font.Font('MyFont.ttf', 70)
font_another_yet = pygame.font.Font('MyFont.ttf', 12)

pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

text_caption = font_yet.render("MIPT Maze", False, (156, 31, 77))
text_caption_rect = text_caption.get_rect(center = (WIDTH // 2, 100))


text_caption_another = font_another_yet.render("*** To change the size of the maze press KEYUP and KEYDOWN or enter the size manually in a special text field ***", False, (156, 31, 77))
text_caption_rect_another = text_caption_another.get_rect(center = (WIDTH // 2, 600))

BACKGROUND_GRADIENT_START = (190, 230, 240)
BACKGROUND_GRADIENT_END = (50, 120, 160)
BUTTON_GRADIENT_START = (170, 170, 170)
BUTTON_GRADIENT_END = (120, 110, 140)

def create_gradient_button(text, action, length_of_screen = 0):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    button_width = text_rect.width + 20
    button_height = text_rect.height + 20
    button_x = WIDTH // 2 - button_width // 2
    button_y = 0
    if text == "DFS Generation" :
        button_y = 225
    elif text == "Minimal Spanning Tree Generation":
        button_y = 350
    elif text == "OK":
        button_y = 450
    elif text == "Save":
        button_x = length_of_screen // 2 - button_width // 2
        button_y = length_of_screen
    elif text == "Load":
        button_y = 475
    elif text == "Quit":
        button_y = 600
    if action == "Quit1":
        button_y = length_of_screen
        button_x = length_of_screen // 2 + 2 * button_width

    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    create_gradient_rect(screen, BUTTON_GRADIENT_START, BUTTON_GRADIENT_END, button_rect)

    if button_rect.collidepoint(pygame.mouse.get_pos()):
        create_gradient_rect(screen, BUTTON_GRADIENT_END, BUTTON_GRADIENT_START, button_rect)
        text_surface = font.render(text, True, (255, 0, 0))
        text_rect = text_surface.get_rect()
        if pygame.mouse.get_pressed()[0]:
            return action

    text_rect.center = button_rect.center
    screen.blit(text_surface, text_rect)

def create_gradient_background():
    background_rect = pygame.Rect(0, 0, WIDTH, HEIGHT + 50)
    create_gradient_rect(screen, BACKGROUND_GRADIENT_START, BACKGROUND_GRADIENT_END, background_rect)

def gui_for_choose_size(input_text, size):
    create_gradient_background()
    screen.blit(text_caption_another, text_caption_rect_another)
    input_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 40)
    input_rect.x = WIDTH // 2 - 100
    pygame.draw.rect(screen, (255, 255, 255), input_rect)
    pygame.draw.rect(screen, (0, 0, 0), input_rect, 2)
    text_surface = font.render(input_text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2 + 25)
    screen.blit(text_surface, text_rect)

    text_surface = font.render(f"Size: {size}", True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
    screen.blit(text_surface, text_rect)

def gui_in_generate_window(l, CELL_SIZE, ROWS, grid):
    pygame.draw.circle(ui.screen, 'Red', (CELL_SIZE + CELL_SIZE // 2, CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lenth = maze_solver.FindAPath(ROWS, grid, l[0], l[1], CELL_SIZE)
                    text_of_len = ui.font.render(f"Length: {lenth}", False, 'Red')
                    rect_of_len = text_of_len.get_rect(topleft = (0, ROWS * CELL_SIZE + 10))
                    ui.screen.blit(text_of_len, rect_of_len)

        action = ui.create_gradient_button("Save", "Save", ROWS * CELL_SIZE)
        if (action == "Save"):
            my_file = open("Data.txt", "w+")
            for i in range(len(grid[0])):
                for j in range(len(grid[0])):
                    my_file.write(f"{grid[i][j]} ")
                my_file.write("\n")
            my_file.close()
        action = ui.create_gradient_button("Quit", "Quit1", ROWS * CELL_SIZE)
        if (action == "Quit1"):
            pygame.quit()
            sys.exit()
        pygame.display.update()
