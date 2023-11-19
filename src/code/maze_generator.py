import pygame
import random
import sys
import ui
import maze_solver

def choose_size(generate_maze_algorythm):
    size = 0 
    input_text = ""
    generate_by_dfs = False
    generate_by_mst = False
    
    if (generate_maze_algorythm):
        generate_by_dfs = True
    else:
        generate_by_mst = True
        
    while True:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    size = min(10000, size + 1)
                elif event.key == pygame.K_DOWN:
                    size = max(1, size - 1)
                elif event.key == pygame.K_RETURN:
                    return size
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    if (input_text != ""):
                        size = int(input_text)
                    else:
                        size = 0
                else:
                    if event.unicode.isnumeric():
                        if (len(input_text) < 2):
                          input_text += event.unicode
                          size = int(input_text)
    
        ui.gui_for_choose_size(input_text, size)
        action = ui.create_gradient_button("OK", "generate")
        if action == "generate" and generate_by_dfs:
            try:
                if (input_text == ""):
                    generate_maze_DFS(size)
                else:
                  size = int(input_text)
                  size = max(1, min(500, size)) 
                  generate_maze_DFS(size)
            except ValueError:
                size = 50
                generate_maze_DFS(size)
        elif action == "generate" and generate_by_mst:
            try:
                if (input_text == ""):
                    generate_maze_MST(size)
                else:
                  size = int(input_text)
                  size = max(1, min(500, size)) 
                  generate_maze_MST(size)
            except ValueError:
                size = 50
                generate_maze_MST(size)

        pygame.display.update()



def draw_grid(grid, ROWS, CELL_SIZE):
    screen = pygame.display.set_mode((ROWS * CELL_SIZE, ROWS * CELL_SIZE + 50))
    ui.create_gradient_background()
    buffer_row = 0
    buffer_col = 0
    
    for row in range(ROWS):
        
        for col in range(ROWS):
            
            if grid[row][col] == 1:
                if (row == ROWS - 1 or col == ROWS - 1):
                    pygame.draw.rect(screen, 'Black', (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, 'Red', (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE + CELL_SIZE // 10, CELL_SIZE + CELL_SIZE // 10))
                    pygame.draw.rect(screen, 'Black', (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                buffer_row = row
                buffer_col = col
    pygame.draw.circle(screen, 'Orange', (buffer_col * CELL_SIZE + CELL_SIZE // 2, buffer_row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)
    return [buffer_row, buffer_col]


def help_func(l, CELL_SIZE, ROWS, grid):
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


def DFS(grid, row, col, ROWS, CELL_SIZE):
    grid[row][col] = 0
    pygame.draw.rect(ui.screen, 'White', (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update()
    current_time = pygame.time.get_ticks()
    
    while current_time % 30 != 0:
        current_time = pygame.time.get_ticks()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(directions)
    
    for dr, dc in directions:
        new_row, new_col = row + dr * 2, col + dc * 2
        if 0 < new_row < ROWS - 1 and 0 < new_col < ROWS - 1 and grid[new_row][new_col] == 1:
            grid[row + dr][col + dc] = 0
            pygame.draw.rect(ui.screen, 'White', ((col + dc) * CELL_SIZE, (row + dr) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.update()
            
            while current_time % 30 != 0:
                current_time = pygame.time.get_ticks()
            DFS(grid, new_row, new_col, ROWS, CELL_SIZE)



def generate_maze_DFS(SIZE):
    if (SIZE % 2 == 0):
        SIZE += 1
    CELL_SIZE = ui.WIDTH // SIZE
    ROWS = SIZE
    COLS = SIZE
    grid = [[1] * COLS for _ in range(ROWS)]
    screen = pygame.display.set_mode((ROWS * CELL_SIZE, ROWS * CELL_SIZE + 50))
    ui.create_gradient_background()
    
    for row in range(ROWS):
        
        for col in range(COLS):
            pygame.draw.rect(screen, 'Black', (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    DFS(grid, 1, 1, ROWS, CELL_SIZE)
    l = draw_grid(grid, ROWS, CELL_SIZE)
    help_func(l, CELL_SIZE, ROWS, grid)



def is_valid(x, y, ROWS):
    return 0 <= x < ROWS and 0 <= y < ROWS

def get_neighbors(x, y, ROWS):
    neighbors = [(x+dx, y+dy) for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]]
    random.shuffle(neighbors)
    return [(nx, ny) for nx, ny in neighbors if is_valid(nx, ny, ROWS)]

def generate_maze_MST(SIZE):
    if (SIZE % 2 == 0):
        SIZE += 1
    CELL_SIZE = ui.WIDTH // SIZE
    ROWS = SIZE
    COLS = SIZE

    grid = [[1] * COLS for _ in range(ROWS)]
    screen = pygame.display.set_mode((ROWS * CELL_SIZE, ROWS * CELL_SIZE + 50))
    ui.create_gradient_background()
    
    for row in range(ROWS):
        
        for col in range(COLS):
            pygame.draw.rect(screen, 'Black', (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    start_x, start_y = 1, 1
    grid[start_y][start_x] = 0
    pygame.draw.rect(screen, 'White', (CELL_SIZE, CELL_SIZE, CELL_SIZE, CELL_SIZE))

    stack = [(start_x, start_y)]

    while stack:
        x, y = stack[-1]
        neighbors = get_neighbors(x, y, ROWS)
        unvisited_neighbors = [(nx, ny) for nx, ny in neighbors if grid[ny][nx] == 1]
        if unvisited_neighbors:
            nx, ny = unvisited_neighbors[0]
            grid[ny][nx] = 0
            pygame.draw.rect(screen, 'White', (nx * CELL_SIZE, ny * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.update()
            current_time = pygame.time.get_ticks()
            
            while current_time % 30 != 0:
                current_time = pygame.time.get_ticks()
            grid[y + (ny - y) // 2][x + (nx - x) // 2] = 0
            pygame.draw.rect(screen, 'White', ((x + (nx - x) // 2) * CELL_SIZE, (y + (ny - y) // 2) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.update()
            current_time = pygame.time.get_ticks()
            
            while current_time % 30 != 0:
                current_time = pygame.time.get_ticks()
            stack.append((nx, ny))
        else:
            stack.pop()
    l = draw_grid(grid, ROWS, CELL_SIZE)
    help_func(l, CELL_SIZE, ROWS, grid)
