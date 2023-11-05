import pygame
import sys
import ui
import maze_generator
pygame.init()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ui.create_gradient_background()
    ui.screen.blit(ui.text_caption, ui.text_caption_rect)
    action = ui.create_gradient_button("DFS Generation", "choose_size")
    if action == "choose_size":
        maze_generator.choose_size(True)
    action = ui.create_gradient_button("Minimal Spanning Tree Generation", "choose_size")
    if action == "choose_size":
        maze_generator.choose_size(False)
    action = ui.create_gradient_button("Load", "Load")
    if action == "Load":
        grid = []
        my_file = open("Data.txt", "r")
        while True:
            line = my_file.readline()
            if not line:
                break
            grid.append(list(map(int, line.split())))
        my_file.close()
        print(grid)
        l = maze_generator.draw_grid(grid, len(grid[0]), ui.WIDTH // len(grid[0]))
        maze_generator.help_func(l, ui.WIDTH // len(grid[0]), len(grid[0]), grid)
    action = ui.create_gradient_button("Quit", "Quit")
    if action == "Quit":
        pygame.quit()
        sys.exit()
    pygame.display.update()

