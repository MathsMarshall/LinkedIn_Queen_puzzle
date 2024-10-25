import time
  
def read_input():
    print('\nHello! Thank you for choosing to use this program to solve the LinkedIn Queen puzzle.')
    print('The algorithm was designed by Mmesomachi Nwachukwu. Contact at nwachukwummesomachi@gmail.com :).')
    temp = input('What is the size of the grid? Expecting a square grid. Please enter the number of rows. ')
    while not temp.isdigit():
        temp = input('What is the size of the grid? Expecting a square grid. Please enter the number of rows. ')
    DOWN_BOUNDARY  = RIGHT_BOUNDARY = int(temp)
    
    def visualise_input_so_far(grid):
        rows = len(grid)
        columns = len(grid[0])
        shutter = len(str(RIGHT_BOUNDARY))
        shutter += 1
        out = ''
        for i in range(RIGHT_BOUNDARY):
            row = '\n'
            for j in range(RIGHT_BOUNDARY):
                if (i < rows) and (j < columns):
                    row += str(grid[i][j]) + ' '*(shutter - len(str(grid[i][j])))
                else:
                    row += '_' + ' '*(shutter - 1)
            out = out + row
        print(out)
    
    print(f'The computer is expecting {RIGHT_BOUNDARY} colours. We ask you to map this {RIGHT_BOUNDARY} colours to integers from 1 to {RIGHT_BOUNDARY} inclusive.')
    print('If no solution exists, it prints the puzzle without any Queen position.')
    print('Time to input the colours row by row')
    grid = []
    check_set_input = set()
    statement = 'What colour from'
    for n in range(RIGHT_BOUNDARY):
        check_set_input.add(str(n+1))
        statement += ' ' + str(n+1) + ','
    statement = statement[:-1] + ' is in '
    for r in range(RIGHT_BOUNDARY):
        row = []
        for c in range(RIGHT_BOUNDARY):
            colour = input(statement + f'row {r+1} and column {c+1}? ')
            while colour not in check_set_input:
                colour = input(statement + f'row {r+1} and column {c+1}? Check again. ')
            row.append(int(colour))
        grid.append(row)
        ifend = input('If you made a mistake and would like to repeat the row, press 0. To start from the beginning, input -1. To continue input as usual, press enter: ')
        if ifend == '0':
            grid = grid[:-1]
            row = []
            for c in range(RIGHT_BOUNDARY):
                colour = input(statement + f'row {r+1} and column {c+1}? ')
                while colour not in check_set_input:
                    colour = input(statement + f'row {r+1} and column {c+1}? Check again. ')
                row.append(int(colour))
            grid.append(row)
        elif ifend == '-1':
            return None, RIGHT_BOUNDARY
        visualise_input_so_far(grid)
    return grid, RIGHT_BOUNDARY

grid, RIGHT_BOUNDARY = read_input()
    
while not grid:
    grid, RIGHT_BOUNDARY = read_input()

colour_dict = {}
position_dict = {}
for i in range(RIGHT_BOUNDARY):
    for j in range(RIGHT_BOUNDARY):
        key = grid[i][j]
        position_dict[(i, j)] = key
        if grid[i][j] in colour_dict:
            colour_dict[key].add((i, j))
        else:
            colour_dict[key] = {(i, j)}

def neighbours(position):
    row = position[0]
    col = position[1]
    neighbours = set()
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if (i == row and j == col):
                continue
            if (0 <= i < RIGHT_BOUNDARY and
                0 <= j < RIGHT_BOUNDARY):
                neighbours.add((i, j))
    return neighbours

def same_rowcolumn(position): # Returns set of positions in same row or column
    same = set()
    for i in range(RIGHT_BOUNDARY):
        for j in range(RIGHT_BOUNDARY):
            if (position[0] == i) or (position[1] == j):
                same.add((i, j))
    return same

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
    next_colour = RIGHT_BOUNDARY
    for key in old_dict:
        if key != colour:                               # Remove colour
            possibilities[key] = old_dict[key].copy()
            possibilities[key] -= check_set             # Remove positions on the same row or column or are neighbours of occupied position
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
    for i in range(RIGHT_BOUNDARY):
        row = '\n'
        for j in range(RIGHT_BOUNDARY):
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
        if len(path) == RIGHT_BOUNDARY:
            return True, path
        next_colour, next_possibilities = place_queen(old_position, old_possibilities)
        l2 = len(next_possibilities)
        if not next_possibilities:
            path.add(old_position)
            if len(path) == RIGHT_BOUNDARY:
                return True, path
            return False, set()
        if ((l1 - l2) > 1) or (old_position in path): # A colour is prematurely eliminated or we encounter a position in path
            return False, set()
        recursion = list(next_possibilities[next_colour])
        condition = False
        path.add(old_position)
        for next_position in recursion:
            condition = condition or DFS(next_position, next_possibilities)[0]
            if len(path) == RIGHT_BOUNDARY:
                return True, path
        path.remove(old_position)
        if condition:
            return True, path
        return False, set()
    
    for position in positions:
        if DFS(position, colour_dict)[0]:
            return DFS(position, colour_dict)[1]
    return path

def visualise_solution(visited):
    out = ''
    shutter = len(str(RIGHT_BOUNDARY))
    for i in range(RIGHT_BOUNDARY):
        row = '\n'
        for j in range(RIGHT_BOUNDARY):
            if (i, j) in visited:
                row += 'Q' + ' '*(shutter)
            else:
                row += str(position_dict[(i, j)]) + ' '*(shutter + 1 - len(str(position_dict[(i, j)])))
        out = out + row
    print(out)

sol = play_game()
print('\nSolving...')
time.sleep(1)
print('Q represents a Queen position')
visualise_solution(sol)
print('\nFor more enquiries, please contact me at nwachukwummesomachi@gmail.com')
