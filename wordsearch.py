import random
import string

from pprint import pprint

words = ["BROWNIE", "DODGEBALL", "SKIING", "CODING", "WATER", "HOUSEPLANT"]

grid_size = 20

# populate a grid_size x grid_size grid with underscores
grid = [['_' for _ in range(grid_size)] for _ in range(grid_size)]

def print_grid():
    for x in range(grid_size):
        print('\t'*5 + ' '.join(grid[x]))

orientations = ['leftright', 'rightleft', 'up', 'down', 'rightup', 'rightdown', 'leftup', 'leftdown']

for word in words:
    word_length = len(word)

    placed = False
    while not placed:
        orientation = random.choice(orientations)

        if orientation == 'leftright':
            step_x = 1
            step_y = 0
        if orientation == 'rightleft':
            step_x = -1
            step_y = 0
        if orientation == 'up':
            step_x = 0
            step_y = -1
        if orientation == 'down':
            step_x = 0
            step_y = 1
        if orientation == 'rightup':
            step_x = 1
            step_y = -1
        if orientation == 'rightdown':
            step_x = 1
            step_y = 1
        if orientation == 'leftup':
            step_x = -1
            step_y = -1
        if orientation == 'leftdown':
            step_x = -1
            step_y = 1

        # choosing random starting position for word
        x_pos = random.randint(0, grid_size)
        y_pos = random.randint(0, grid_size)

        # determine if word can fit in grid with it's starting position
        ending_x = x_pos + word_length*step_x
        ending_y = y_pos + word_length*step_y

        if ending_x < 0 or ending_x >= grid_size: continue
        if ending_y < 0 or ending_y >= grid_size: continue

        failed = False

        for i in range(word_length):
            character = word[i]

            curr_x = x_pos + i*step_x
            curr_y = y_pos + i*step_y

            character_curr_pos = grid[curr_x][curr_y]
            if character_curr_pos != '_':
                if character_curr_pos == character:
                    continue
                else:
                    failed = True
                    break
            
        if failed:
            continue
        else:
            # place word
            for i in range(word_length):
                character = word[i]

                curr_x = x_pos + i*step_x
                curr_y = y_pos + i*step_y

                grid[curr_x][curr_y] = ('\x1b[6;30;42m' + character + '\x1b[0m')

            placed = True

# fill rest of grid with random letters
for x in range(grid_size):
    for y in range(grid_size):
        if (grid[x][y] == '_'):
            grid[x][y] = random.choice(string.ascii_uppercase)

print_grid()
print("Words are: ")
pprint(words)