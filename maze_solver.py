import pygame
import ui

def MakeStep(ROWS, grid, k, m):
  for i in range(ROWS):
    for j in range(ROWS):
      if m[i][j] == k:
        if i>0 and m[i-1][j] == 0 and grid[i-1][j] == 0:
          m[i-1][j] = k + 1
        if j>0 and m[i][j-1] == 0 and grid[i][j-1] == 0:
          m[i][j-1] = k + 1
        if i<len(m)-1 and m[i+1][j] == 0 and grid[i+1][j] == 0:
          m[i+1][j] = k + 1
        if j<len(m[i])-1 and m[i][j+1] == 0 and grid[i][j+1] == 0:
           m[i][j+1] = k + 1



def FindAPath(ROWS, grid, buffer_row, buffer_col, CELL_SIZE):
    m = []
    for i in range(ROWS):
      m.append([])
      for j in range(ROWS):
        m[i].append(0)
    m[1][1] = 1
    k = 0
    while m[buffer_row][buffer_col] == 0:
        k += 1
        MakeStep(ROWS, grid, k, m)
    i, j = buffer_row, buffer_col
    k = m[i][j]
    the_path = [(i,j)]
    while k > 1:
      if i > 0 and m[i - 1][j] == k-1:
        i, j = i-1, j
        the_path.append((i, j))
        k-=1
      elif j > 0 and m[i][j - 1] == k-1:
        i, j = i, j-1
        the_path.append((i, j))
        k-=1
      elif i < len(m) - 1 and m[i + 1][j] == k-1:
        i, j = i+1, j
        the_path.append((i, j))
        k-=1
      elif j < len(m[i]) - 1 and m[i][j + 1] == k-1:
        i, j = i, j+1
        the_path.append((i, j))
        k -= 1
    color = 0
    colors = []
    color_another = 50
    for i in range(len(the_path)):
        color += 1        
        colors.append((min(color, 255), color_another, min(color // 2, 255)))
        if (color == 510):
            color = 0
            color_another += 50
        if (color_another > 255):
            color_another == 50
        pygame.draw.rect(ui.screen, colors[i], (the_path[i][1] * CELL_SIZE, the_path[i][0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()
        current_time = pygame.time.get_ticks()
        while current_time % 30 != 0:
            current_time = pygame.time.get_ticks()

    return len(the_path)