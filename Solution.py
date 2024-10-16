import time

def visualise_input_so_far(grid):
    rows = len(grid)
    columns = len(grid[0])
    out = ''
    for i in range(9):
        row = '\n'
        for j in range(9):
            if (i < rows) and (j < columns):
                row += str(grid[i][j]) + ' '
            else:
                row += '_ '
        out = out + row
    print(out)
    
def read_input():
    print('\nHello! Thank you for choosing to use this program to solve the LinkedIn Queen puzzle.')
    print('The algorithm was designed by Mmesomachi Nwachukwu. Contact at nwachukwummesomachi@gmail.com :).')
    print('The computer is expecting 9 colours. We ask you to map this 9 colours to integers from 1 to 9 inclusive.')
    print('If no solution exists, it prints the puzzle without any Queen position.')
    print('Time to input the colours row by row')
    grid = []
    for r in range(9):
        row = []
        for c in range(9):
            colour = input(f'What colour from 1, 2, 3, 4, 5, 6, 7, 8, 9, is in row {r+1} and column {c+1}? ')
            while colour not in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                colour = input(f'What colour from 1, 2, 3, 4, 5, 6, 7, 8, 9, is in row {r+1} and column {c+1}? ')
            row.append(int(colour))
        ifend = input('If you made a mistake and would like to start from beginning, press 0. To continue input as usual, press 1: ')
        if ifend == '0':
            return
        grid.append(row)
        visualise_input_so_far(grid)
    return grid

grid = read_input()
    
if not grid:
    read_input()

colour_dict = {}
position_dict = {}
for i in range(9):
    for j in range(9):
        key = grid[i][j]
        position_dict[(i, j)] = key
        if grid[i][j] in colour_dict:
            colour_dict[key].add((i, j))
        else:
            colour_dict[key] = {(i, j)}

LEFT_BOUNDARY  = 0
RIGHT_BOUNDARY = 8
UP_BOUNDARY    = 0
DOWN_BOUNDARY  = 8

def neighbours(position):
    row = position[0]
    col = position[1]
    neighbours = set()
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if (i == row and j == col):
                continue
            if (UP_BOUNDARY   <= i <= DOWN_BOUNDARY and
                LEFT_BOUNDARY <= j <= RIGHT_BOUNDARY):
                neighbours.add((i, j))
    return neighbours

def same_rowcolumn(position): # Returns set of positions in same row or column
    same = set()
    for i in range(9):
        for j in range(9):
            if (position[0] == i) or (position[1] == j):
                same.add((i, j))
    return same

# colour_dict = {}   # colours (int) as keys and positions it occupies
# position_dict = {} # position as keys and colours (int) as values

# Input is the list[list]. You should type the colour per row (comma seperated)
# Example
# Type the colours on row 1 :
# purple, blue, blue, purple, orange, purple, green, green, purple

def place_queen(position, old_dict):
    '''
    old_dict and possibilities are colour encoding dictionaries like colour_dict.
    return remaining possible positions and next_colour to search.
    '''
    i = position[0]
    j = position[1]
    check_set = (neighbours(position) | same_rowcolumn(position))
    if not old_dict:
        return -1, {}
    possibilities = {}
    colour = position_dict[(i, j)]
    next_colour = 9
    for key in old_dict:
        if key != colour:                               # Remove colour
            possibilities[key] = old_dict[key].copy()
            possibilities[key] -= check_set             # Remove positions on same row or column or are neighbour of occupied position
            next_colour = min(key, next_colour)
    return next_colour, possibilities
    
def listing(possibilities): # get set of possible positions
    possible_coordinates = set()
    for colour in possibilities:
        temp = list(possibilities[colour])
        for position in temp:
            possible_coordinates.add(position)
    return possible_coordinates

def visualise(possibilities):
    out = ''
    possible_coordinates = listing(possibilities)
    for i in range(9):
        row = '\n'
        for j in range(9):
            if (i, j) not in possible_coordinates:
                row += '0'
            else:
                row += str(position_dict[(i, j)])
        out = out + row
    return out
    
def play_game(colour = 1):
    positions = list(colour_dict[colour])
    path = set() # Keep track of visited positions
    
    def DFS(old_position, old_possibilities):
        l1 = len(old_possibilities)
        if len(path) == 9:
            return True, path
        next_colour, next_possibilities = place_queen(old_position, old_possibilities)
        l2 = len(next_possibilities)
        if not next_possibilities:
            path.add(old_position)
            if len(path) == 9:
                return True, path
            return False, set()
        if ((l1 - l2) > 1) or (old_position in path): # A colour is prematurely eliminated or we encounter a position in path
            return False, set()
        recursion = list(next_possibilities[next_colour])
        condition = False
        path.add(old_position)
        for next_position in recursion:
            condition = condition or DFS(next_position, next_possibilities)[0]
            if len(path) == 9:
                return True, path
        path.remove(old_position)
        if condition:
            return True, path
        return False, set()
    
    for position in positions:
        if DFS(position, colour_dict)[0]:
            return DFS(position, colour_dict)[1]

def visualise_solution(visited):
    out = ''
    for i in range(9):
        row = '\n'
        for j in range(9):
            if (i, j) in visited:
                row += 'Q '
            else:
                row += str(position_dict[(i, j)]) + ' '
        out = out + row
    print(out)

sol = play_game()
print('\nSolving...')
time.sleep(1)
print('Q represents Queen position')
visualise_solution(sol)
print('For more enquiries, please contact me at nwachukwummesomachi@gmail.com')
