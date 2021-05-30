#!/usr/bin/python3
import random
import time
import pygame

# Commands
print("")
print("\033[36m📚 HOW TO PLAY?\033[0m")
print("\033[32m🟢 Move TETRIS PIECES using UP KEY 🔼, DOWN KEY 🔽, LEFT KEY ◀️  and RIGHT KEY ▶️ \033[0m")
print("\033[31m🔴 Press the \"ESCAPE\" KEY on the TETRIS \"GAME OVER\" screen to end the game! \033[0m")
print("")

pygame.font.init()

# Add music
pygame.mixer.init()
pygame.mixer.music.load('tetris.mp3')
pygame.mixer.music.play(-1, 0.0)

# Global variables

col = 10  # 10 Columns
row = 20  # 20 Rows
s_width = 800  # Screen width
s_height = 750  # Screen height
play_width = 300  # Play screen width; 300/10 = 30 width per block
play_height = 600  # Play screen height; 600/20 = 20 height per block
block_size = 30  # Size of block

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

filepath = 'highscore.txt'
font_title = 'font_title.ttf'
font_text = 'font_text.ttf'

# Tetriminos:
# 0 - S - Green
# 1 - Z - Red
# 2 - I - Cyan
# 3 - O - Yellow
# 4 - J - Blue
# 5 - L - Orange
# 6 - T - Purple

S = [['.....','.....','..00.','.00..','.....'],
     ['.....','..0..','..00.','...0.','.....']]

Z = [['.....','.....','.00..','..00.','.....'],
     ['.....','..0..','.00..','.0...','.....']]

I = [['.....','..0..','..0..','..0..','..0..'],
     ['.....','0000.','.....','.....','.....']]

O = [['.....','.....','.00..','.00..','.....']]

J = [['.....','.0...','.000.','.....','.....'],
     ['.....','..00.','..0..','..0..','.....'],
     ['.....','.....','.000.','...0.','.....'],
     ['.....','..0..','..0..','.00..','.....']]

L = [['.....','...0.','.000.','.....','.....'],
     ['.....','..0..','..0..','..00.','.....'],
     ['.....','.....','.000.','.0...','.....'],
     ['.....','.00..','..0..','..0..','.....']]

T = [['.....','..0..','.000.','.....','.....'],
     ['.....','..0..','..00.','..0..','.....'],
     ['.....','.....','.000.','..0..','.....'],
     ['.....','..0..','.00..','..0..','.....']]

# Index represents the shape
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

def run():
    screen = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')
    run = True
    while run:
        main(screen)

    pygame.quit()

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]  # Choose color from the shape_color list
        self.rotation = 0  # Chooses the rotation according to index

def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for x in range(col)] for y in range(row)]  # Grid represented rgb tuples

    # Locked_positions dictionary
    # (x,y):(r,g,b)
    for y in range(row):
        for x in range(col):
            if (x, y) in locked_pos:
                color = locked_pos[(x, y)] # Get the value color (r,g,b) from the locked_positions dictionary using key (x,y)
                grid[y][x] = color # Set grid position to color

    return grid

def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)] # Get the desired rotated shape from piece
    #e.g. ['.....','.....','..00.','.00..','.....']
    for i, line in enumerate(shape_format):  # i gives index; line gives string
        row = list(line)  # Makes a list of char from string
        for j, column in enumerate(row):  # j gives index of char; column gives char
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) # Offset according to the input given with dot and zero

    return positions

def check_piece_position(piece, grid):
    # Makes a 2D list of all the possible (x,y)
    accepted_pos = [[(x, y) for x in range(col) if grid[y][x] == (0, 0, 0)] for y in range(row)]
    # Removes sub lists and puts (x,y) in one list; easier to search
    accepted_pos = [x for item in accepted_pos for x in item]

    formatted_shape = convert_shape_format(piece)

    for pos in formatted_shape:
        if pos not in accepted_pos:
            if pos[1] >= 0:
                return False
    return True

# Check if piece is out of board
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

# Chooses a shape randomly from shapes list
def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_grid(surface):
    r = g = b = 0
    grid_color = (r, g, b)

    for i in range(row):
        # Draw grey horizontal lines
        pygame.draw.line(
            surface,
            grid_color,
            (top_left_x, top_left_y + i * block_size),
            (top_left_x + play_width, top_left_y + i * block_size)
        )
        for j in range(col):
            # Draw grey vertical lines
            pygame.draw.line(surface, grid_color, (top_left_x + j * block_size, top_left_y),
                             (top_left_x + j * block_size, top_left_y + play_height))

def clear_rows(grid, locked):
    # Need to check if row is clear then shift every other row above down one
    increment = 0
    for i in range(len(grid) - 1, -1, -1): # Start checking the grid backwards
        grid_row = grid[i] # Get the last row
        if (0, 0, 0) not in grid_row: # If there are no empty spaces (i.e. black blocks)
            increment += 1
            # Add positions to remove from locked
            index = i # Row index will be constant
            for j in range(len(grid_row)):
                try:
                    del locked[(j, i)] # Delete every locked element in the bottom row
                except ValueError:
                    continue

    # Shift every row one step down
    # Delete filled bottom row
    # Add another empty row on the top
    # Move down one step
    if increment > 0:
        # Sort the locked list according to y value in (x,y) and then reverse
        # Reversed because otherwise the ones on the top will overwrite the lower ones
        for key in sorted(list(locked), key=lambda a: a[1])[::-1]:
            x, y = key
            if y < index:                       # If the y value is above the removed index
                new_key = (x, y + increment)    # Shift position to down
                locked[new_key] = locked.pop(key)

    return increment

def draw_next_shape(piece, surface):
    font = pygame.font.Font(font_text, 30)
    label = font.render('Next shape', 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color, (start_x + j*block_size, start_y + i*block_size, block_size, block_size), 0)

    surface.blit(label, (start_x, start_y - 30))

def draw_screen(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.Font(font_title, 65, bold=True)
    label = font.render('TETRIS', 1, (255, 255, 255))
    surface.blit(label, ((top_left_x + play_width / 2) - (label.get_width() / 2), 30))

    # Current score
    font = pygame.font.Font(font_text, 30)
    label = font.render('SCORE   ' + str(score) , 1, (255, 255, 255))
    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)
    surface.blit(label, (start_x, start_y + 200))

    # Last score
    label_hi = font.render('HIGHSCORE   ' + str(last_score), 1, (255, 255, 255))
    start_x_hi = top_left_x - 240
    start_y_hi = top_left_y + 200
    surface.blit(label_hi, (start_x_hi + 20, start_y_hi + 200))

    # Draw content of the grid
    for i in range(row):
        for j in range(col):
            pygame.draw.rect(surface, grid[i][j],(top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    # Draw vertical and horizontal grid lines
    draw_grid(surface)

    # Draw rectangular border around play area
    border_color = (255, 255, 255)
    pygame.draw.rect(surface, border_color, (top_left_x, top_left_y, play_width, play_height), 4)

# Update the score txt file with high score
def update_score(new_score):
    score = get_max_score()

    with open(filepath, 'w') as file:
        if new_score > score:
            file.write(str(new_score))
        else:
            file.write(str(score))

# Get the high score from the file
def get_max_score():
    with open(filepath, 'r') as file:
        lines = file.readlines()        # Reads all the lines and puts in a list
        score = int(lines[0].strip())   # Remove \n

    return score

def main(screen):
    locked_positions = {}
    create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35
    level_time = 0
    score = 0
    last_score = get_max_score()

    while run:
        # Need to constantly make new grid as locked positions always change
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5: # Make the difficulty harder every 10 seconds
            level_time = 0
            if fall_speed > 0.15: # Until fall speed is 0.15
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not check_piece_position(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Move x position left
                    current_piece.x -= 1
                    if not check_piece_position(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    # Move x position right
                    current_piece.x += 1
                    if not check_piece_position(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    # Move shape down
                    current_piece.y += 1
                    if not check_piece_position(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    # Rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not check_piece_position(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        piece_pos = convert_shape_format(current_piece)

        # Draw the piece on the grid by giving color in the piece locations
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece: # If the piece is locked
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color # Add the key and value in the dictionary
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10 # Increment score by 10 for every row cleared
            update_score(score)

            if last_score < score:
                last_score = score

        draw_screen(screen, grid, score, last_score)
        draw_next_shape(next_piece, screen)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    font = pygame.font.Font(font_text, 40, bold=False, italic=True)
    label = font.render("GAME OVER", 1, (255, 255, 255))
    screen.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))

    pygame.display.update()
    time.sleep(1)

    while replay_or_quit() is None:
        clock.tick()

    main(screen)

def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                print("➡️  Thank you for using Ritchie CLI! 🆒")
                pygame.quit()
                quit()
        elif event.type == pygame.KEYDOWN:
            continue
        return event.key
    return None