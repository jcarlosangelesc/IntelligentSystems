from agents import *
from random import randrange

# Declaring the Fully Observable Environment
class FO_Grid(Environment):
    # Initialize the FO_Grid object
    def __init__(self, agent):
        self.agent = agent
        self.map = [['-']*7 for i in range(7)]

        # Set the row and column numbers
        self.map[0] = ['*','1', '2', '3', '4', '5', '6']
        for row in range(len(self.map)):
            if row != 0:
                self.map[row][0] = str(row)

        # Add new explorer
        self.add('explorer', 1)

    # This method lets you insert elements randomly to the grid
    def add(self, thing, qtty):
        ##### REVISAR QUE HAYA CELDAS LIBRES PARA AGREGAR COSAS ####
        while qtty > 0:
            rand_row = randrange(6) + 1
            rand_col = randrange(6) + 1
            if self.map[rand_row][rand_col] == '-':
                if thing == 'walls':
                    self.map[rand_row][rand_col] = '#'
                elif thing == 'treas1':
                    self.map[rand_row][rand_col] = 'T'
                elif thing == 'reus':
                    self.map[rand_row][rand_col] = 'H'
                elif thing == 'treas2':
                    self.map[rand_row][rand_col] = 't'
                elif thing == 'dispos':
                    self.map[rand_row][rand_col] = 'h'
                elif thing == 'explorer':
                    self.agent.row = rand_row
                    self.agent.col = rand_col
                    self.map[rand_row][rand_col] = 'E'
                    if hasattr(self.agent, 'state'):
                        self.agent.state = self.map
                        # self.agent.state[rand_row][rand_col] = 'E'
                qtty = qtty - 1

    # Print the current state of the environment
    def show(self):
        print("ENVIRONMENT")
        for row in range(len(self.map)):
            for col in range(len(self.map)):
                print(self.map[row][col] + ' ', end = '')
            print()
        print()

    # This function returns what the agent is able to 'see'
    def percept(self):
        # In the case of the fully observable environment, you know the locations of all elements in the map
        # as well as the locaton of the agent in the map.
        map_elements = {'walls' : [],
                        'treas1': [],
                        'reus'  : [],
                        'treas2': [],
                        'dispos': []}
        for row in range(len(self.map)):
            for col in range(len(self.map)):
                if self.map[row][col] == '#':
                    map_elements['walls'].append((row, col))
                elif self.map[row][col] == 'T':
                    map_elements['treas1'].append((row, col))
                elif self.map[row][col] == 'H':
                    map_elements['reus'].append((row, col))
                elif self.map[row][col] == 't':
                    map_elements['treas2'].append((row, col))
                elif self.map[row][col] == 'h':
                    map_elements['dispos'].append((row, col))
                elif self.map[row][col] == 'E':
                    explorer_location = (row, col)
        return map_elements

    def execute_action(self):
        if self.agent.prev_cell == 'H':
            self.agent.g_reuse(self.map)
        elif self.agent.prev_cell == 'h':
            self.agent.g_dispos(self.map)
        elif self.agent.prev_cell == 'T':
            self.agent.g_treas1()
        elif self.agent.prev_cell == 't':
            self.agent.g_treas2()

    # This function allows the agent to move and perform actions for a determined number of steps
    # or untill all treasures are collected (since you know where and how many treasures there are)
    def run(self, steps):
        step = 1
        print('<STARTING>')
        print('Agent Location:', str((self.agent.row, self.agent.col)))
        print('Agent Tools: %s' % str(self.agent.tools))
        print('Score: %s\n' % self.agent.score)
        self.show()

        while steps > 0 and not self.is_done():
            print('<STEP %s>\n' % step)
            percepts = self.percept()
            print('PERCEPT:\n%s' % str(percepts))
            print('Agent Location:', str((self.agent.row, self.agent.col)))
            print('Agent Tools: %s' % str(self.agent.tools))
            print('Score: %s' % self.agent.score)

            surrounding_cells = []
            curr_r = self.agent.row
            curr_c = self.agent.col

            if curr_r > 1 and curr_c > 1 and curr_r < 6 and curr_c < 6:
                surrounding_cells = [(curr_r-1, curr_c), (curr_r,   curr_c-1), (curr_r,   curr_c+1), (curr_r+1, curr_c)]
            elif curr_r == 1 and curr_c > 1 and curr_c < 6:
                surrounding_cells = [(curr_r,   curr_c-1), (curr_r,   curr_c+1), (curr_r+1, curr_c)]
            elif curr_r > 1 and curr_c < 6 and curr_c == 1:
                surrounding_cells = [(curr_r-1,   curr_c), (curr_r,   curr_c+1), (curr_r+1, curr_c)]
            elif curr_r == 6 and curr_c > 1 and curr_c < 6:
                surrounding_cells = [(curr_r-1,   curr_c), (curr_r,   curr_c-1), (curr_r, curr_c+1)]
            elif curr_r > 1 and curr_r < 6 and curr_c == 6:
                surrounding_cells = [(curr_r-1, curr_c), (curr_r, curr_c-1), (curr_r+1, curr_c)]
            elif curr_r == 1 and curr_c == 1:
                surrounding_cells = [(curr_r, curr_c+1), (curr_r+1, curr_c)]
            elif curr_r == 1 and curr_c == 6:
                surrounding_cells = [(curr_r, curr_c-1), (curr_r+1, curr_c)]
            elif curr_r == 6 and curr_c == 1:
                surrounding_cells = [(curr_r-1, curr_c), (curr_r, curr_c+1)]
            elif curr_r == 6 and curr_c == 6:
                surrounding_cells = [(curr_r, curr_c-1), (curr_r-1, curr_c)]

            print(surrounding_cells)
            for cell in surrounding_cells:
                try:
                    if self.map[cell[0]][cell[1]] == '#':
                        surrounding_cells.remove(cell)
                except:
                    pass

            opt = random.choice(surrounding_cells)

            #Check where the chosen cell is located with respect of the current cell and move
            if opt[0] < self.agent.row and opt[1] == self.agent.col:
                self.agent.move_up(self.map, percepts)
                self.execute_action()
            elif opt[0] > self.agent.row and opt[1] == self.agent.col:
                self.agent.move_down(self.map, percepts)
                self.execute_action()
            elif opt[0] == self.agent.row and opt[1] < self.agent.col:
                self.agent.move_left(self.map, percepts)
                self.execute_action()
            elif opt[0] == self.agent.row and opt[1] > self.agent.col:
                self.agent.move_right(self.map, percepts)
                self.execute_action()

            self.show()
            if hasattr(self.agent, 'state'):
                self.agent.show_state()
            step = step + 1
            steps -= 1
        print("DONE!!!")

    # In the case of the Fully Observable Environment, the agent knows when to stop hunting for treasures.
    # This function stops the agent once all treasures are collected
    def is_done(self):
        percepts = self.percept()
        hasTreas1 = len(percepts['treas1'])
        hasTreas2 = len(percepts['treas2'])
        if hasTreas1 == 0 and hasTreas2 == 0:
            return True
        else:
            return False

# Declaring the Partially Observable Environment
class PO_Grid(Environment):
    # Initialize the PO_Grid object
    def __init__(self, agent):
        self.agent = agent
        self.map = [['-']*7 for i in range(7)]

        #Set the row and column numbers
        self.map[0] = ['*','1', '2', '3', '4', '5', '6']
        for row in range(len(self.map)):
            if row != 0:
                self.map[row][0] = str(row)

        #Add empty explorer
        self.add('explorer', 1)

    # This method lets you insert elements to the grid
    def add(self, thing, qtty):
        ##### REVISAR QUE HAYA CELDAS LIBRES PARA AGREGAR COSAS ####
        while qtty > 0:
            rand_row = randrange(6) + 1
            rand_col = randrange(6) + 1
            if self.map[rand_row][rand_col] == '-':
                if thing == 'walls':
                    self.map[rand_row][rand_col] = '#'
                elif thing == 'treas1':
                    self.map[rand_row][rand_col] = 'T'
                elif thing == 'reus':
                    self.map[rand_row][rand_col] = 'H'
                elif thing == 'treas2':
                    self.map[rand_row][rand_col] = 't'
                elif thing == 'dispos':
                    self.map[rand_row][rand_col] = 'h'
                elif thing == 'explorer':
                    self.agent.row = rand_row
                    self.agent.col = rand_col
                    self.map[rand_row][rand_col] = 'E'
                    if hasattr(self.agent, 'state'):
                        self.agent.state[rand_row][rand_col] = 'E'
                qtty = qtty - 1

    # Print the current state of the environment
    def show(self):
        print("ENVIRONMENT")
        for row in range(len(self.map)):
            for col in range(len(self.map)):
                print(self.map[row][col] + ' ', end = '')
            print()
        print()

    # This function returns what the agent is able to 'see'
    def percept_PO(self, agent):
        # In the case of the partially observable environment, the agent only knows the locations of the elements around it
        map_elements = {'walls' : [],
                        'treas1': [],
                        'reus'  : [],
                        'treas2': [],
                        'dispos': []}
        curr_r = self.agent.row
        curr_c = self.agent.col

        # Here you define the cells that surround the agent for later inspection
        surrounding_cells = [(curr_r-1, curr_c-1),
                             (curr_r-1, curr_c),
                             (curr_r-1, curr_c+1),
                             (curr_r,   curr_c-1),
                             (curr_r,   curr_c+1),
                             (curr_r+1, curr_c-1),
                             (curr_r+1, curr_c),
                             (curr_r+1, curr_c+1)]

        for cell in surrounding_cells:
            try:
                if self.map[cell[0]][cell[1]] == '#':
                    map_elements['walls'].append((cell[0], cell[1]))
                elif self.map[cell[0]][cell[1]] == 'T':
                    map_elements['treas1'].append((cell[0], cell[1]))
                elif self.map[cell[0]][cell[1]] == 'H':
                    map_elements['reus'].append((cell[0], cell[1]))
                elif self.map[cell[0]][cell[1]] == 't':
                    map_elements['treas2'].append((cell[0], cell[1]))
                elif self.map[cell[0]][cell[1]] == 'h':
                    map_elements['dispos'].append((cell[0], cell[1]))
            except:
                pass
        return map_elements

    def execute_action(self):
        if self.agent.prev_cell == 'H':
            self.agent.g_reuse(self.map)
        elif self.agent.prev_cell == 'h':
            self.agent.g_dispos(self.map)
        elif self.agent.prev_cell == 'T':
            self.agent.g_treas1()
        elif self.agent.prev_cell == 't':
            self.agent.g_treas2()

    # This function allows the agent to move and perform actions for a determined number of steps
    def run(self, steps):
        step = 1
        print('<STARTING>')
        print('Agent Location:', str((self.agent.row, self.agent.col)))
        print('Agent Tools: %s' % str(self.agent.tools))
        print('Score: %s\n' % self.agent.score)
        self.show()

        while steps > 0:# and not self.is_done():
            print('<STEP %s>\n' % step)
            percepts = self.percept_PO(self.agent)
            print('PERCEPT:\n%s' % str(percepts))
            print('Agent Location:', str((self.agent.row, self.agent.col)))
            print('Agent Tools: %s' % str(self.agent.tools))
            print('Score: %s' % self.agent.score)

            surrounding_cells = []
            curr_r = self.agent.row
            curr_c = self.agent.col

            if curr_r > 1 and curr_c > 1 and curr_r < 6 and curr_c < 6:
                surrounding_cells = [(curr_r-1, curr_c), (curr_r,   curr_c-1), (curr_r,   curr_c+1), (curr_r+1, curr_c)]
            elif curr_r == 1 and curr_c > 1 and curr_c < 6:
                surrounding_cells = [(curr_r,   curr_c-1), (curr_r,   curr_c+1), (curr_r+1, curr_c)]
            elif curr_r > 1 and curr_c < 6 and curr_c == 1:
                surrounding_cells = [(curr_r-1,   curr_c), (curr_r,   curr_c+1), (curr_r+1, curr_c)]
            elif curr_r == 6 and curr_c > 1 and curr_c < 6:
                surrounding_cells = [(curr_r-1,   curr_c), (curr_r,   curr_c-1), (curr_r, curr_c+1)]
            elif curr_r > 1 and curr_r < 6 and curr_c == 6:
                surrounding_cells = [(curr_r-1, curr_c), (curr_r, curr_c-1), (curr_r+1, curr_c)]
            elif curr_r == 1 and curr_c == 1:
                surrounding_cells = [(curr_r, curr_c+1), (curr_r+1, curr_c)]
            elif curr_r == 1 and curr_c == 6:
                surrounding_cells = [(curr_r, curr_c-1), (curr_r+1, curr_c)]
            elif curr_r == 6 and curr_c == 1:
                surrounding_cells = [(curr_r-1, curr_c), (curr_r, curr_c+1)]
            elif curr_r == 6 and curr_c == 6:
                surrounding_cells = [(curr_r, curr_c-1), (curr_r-1, curr_c)]

            for cell in surrounding_cells:
                try:
                    if self.map[cell[0]][cell[1]] == '#':
                        surrounding_cells.remove(cell)
                except:
                    pass

            opt = random.choice(surrounding_cells)

            #Check where the chosen cell is located with respect of the current cell and move
            if opt[0] < self.agent.row and opt[1] == self.agent.col:
                self.agent.move_up(self.map, percepts)
                self.execute_action()
            elif opt[0] > self.agent.row and opt[1] == self.agent.col:
                self.agent.move_down(self.map, percepts)
                self.execute_action()
            elif opt[0] == self.agent.row and opt[1] < self.agent.col:
                self.agent.move_left(self.map, percepts)
                self.execute_action()
            elif opt[0] == self.agent.row and opt[1] > self.agent.col:
                self.agent.move_right(self.map, percepts)
                self.execute_action()

            self.show()
            if hasattr(self.agent, 'state'):
                self.agent.show_state()
            step = step + 1
            steps -= 1
        print('DONE!!!')

# Declaring the Simple Reflex Agent
class SR_Explorer(Agent):
    # Initialize the SR_Agent object
    def __init__(self):
        self.row = None
        self.col = None
        self.prev_cell = '-'
        self.tools = []
        self.score = 50

    # Just a simple helper method to print the content of the object
    def __repr__(self):
        return "Explorer{\nRow:%s \nCol:%s \nTools:%s \nScore:%s}" % (self.row, self.col, self.tools, self.score)

    # This function translates the agent's actions into the map, updating it on every step
    # This function also updates the agent's score for every movement.
    def update_map(self, target_row, target_col, grid):
        target_cell = grid[target_row][target_col]
        if target_cell == '#':
            self.score -= 1
        elif target_row < 1 or target_col < 1:
            self.score -= 5
        else:
            self.score -= 1
            grid[self.row][self.col] = self.prev_cell
            self.row = target_row
            self.col = target_col
            self.prev_cell = grid[target_row][target_col]
            grid[target_row][target_col] = 'E'

    # Moves the agent one cell up (if possible)
    def move_up(self, grid, percepts):
        try:
            target_row = self.row - 1
            target_col = self.col
            self.update_map(target_row, target_col, grid)
        except:
            self.score -= 5
        print('Moved up. Last cell: %s' % self.prev_cell)

    # Moves the agent one cell down (if possible)
    def move_down(self, grid, percepts):
        try:
            target_row = self.row + 1
            target_col = self.col
            self.update_map(target_row, target_col, grid)
        except:
            self.score -= 5
        print('Moved down. Last cell: %s' % self.prev_cell)

    # Moves the agent one cell to the right (if possible)
    def move_right(self, grid, percepts):
        try:
            target_row = self.row
            target_col = self.col + 1
            self.update_map(target_row, target_col, grid)
        except:
            self.score -= 5
        print('Moved right. Last cell: %s' % self.prev_cell)

    # Moves the agent one cell to the left (if possible)
    def move_left(self, grid, percepts):
        try:
            target_row = self.row
            target_col = self.col - 1
            self.update_map(target_row, target_col, grid)
        except:
            self.score -= 5
        print('Moved left. Last cell: %s' % self.prev_cell)

    # This function does nothing
    def no_op():
        pass

    # Allows the user to grab a reusable tool if its current cell has such tool
    def g_reuse(self, grid):
        if self.prev_cell == 'H':
            # Stop grabbing this kind of tools if you already have one
            if not 'H' in self.tools:
                self.tools.append('H')
                self.prev_cell = '-'
                self.score -= 2
                print('Grabbed reusable tool')

    # Allows the user to grab a disposable tool if its current cell has such tool
    def g_dispos(self, grid):
        if self.prev_cell == 'h':
            self.tools.append('h')
            self.prev_cell = '-'
            self.score -= 2
            print('Grabbed disposable tool')

    # Allows the user to grab a type 1 treasure if its current cell has such treasure
    def g_treas1(self):
        if self.prev_cell == 'T' and 'H' in self.tools:
            self.prev_cell = '-'
            self.score += 20
            print('Grabbed type 1 treasure')

    # Allows the user to grab a type 2 treasure if its current cell has such treasure
    def g_treas2(self):
        if self.prev_cell == 't' and 'h' in self.tools:
            self.prev_cell = '-'
            self.tools.remove('h')
            self.score += 40
            print('Grabbed type 2 treasure')

# Declaring the Model Based Agent
class MB_Explorer(Agent):
    # Initialize the MB_Agent object.
    # The main difference from the SR_Agent is that this type of agent 'remembers' the state of environment
    def __init__(self):
        self.row = None
        self.col = None
        self.prev_cell = '-'
        self.tools = []
        self.score = 50
        self.state = [['?']*7 for i in range(7)]

        #Set the row and column numbers
        self.state[0] = ['*','1', '2', '3', '4', '5', '6']
        for row in range(len(self.state)):
            if row != 0:
                self.state[row][0] = str(row)
    # Just a simple helper method to print the content of the object
    def __repr__(self):
        return "Explorer{\nRow:%s \nCol:%s \nTools:%s \nScore:%s}" % (self.row, self.col, self.tools, self.score)

    # Prints the content of the Internal State
    def show_state(self):
        print('INTERNAL STATE')
        for row in range(len(self.state)):
            for col in range(len(self.state)):
                print(self.state[row][col] + ' ', end = '')
            print()
        print()

    # Updates the content of the internal state according to the percepts
    def update_state(self, percepts):
        curr_r = self.row
        curr_c = self.col
        things_at = []
        keys = {'walls':  '#',
                'treas1': 'T',
                'reus':   'H',
                'treas2': 't',
                'dispos': 'h'}
        if curr_r > 1 and curr_c > 1:
            surrounding_cells = [(curr_r-1, curr_c-1), (curr_r-1, curr_c),  (curr_r-1, curr_c+1),
                                 (curr_r,   curr_c-1),                      (curr_r,   curr_c+1),
                                 (curr_r+1, curr_c-1), (curr_r+1, curr_c),  (curr_r+1, curr_c+1)]

        elif curr_r == 1 and curr_c > 1:
            surrounding_cells = [(curr_r,   curr_c-1),                      (curr_r,   curr_c+1),
                                 (curr_r+1, curr_c-1), (curr_r+1, curr_c),  (curr_r+1, curr_c+1)]

        elif curr_r > 1 and curr_c == 1:
            surrounding_cells = [(curr_r-1,   curr_c), (curr_r-1, curr_c+1),
                                                       (curr_r,   curr_c+1),
                                 (curr_r+1, curr_c),   (curr_r+1, curr_c+1)]
        else:
            surrounding_cells = [                      (curr_r,   curr_c+1),
                                 (curr_r+1, curr_c),   (curr_r+1, curr_c+1)]

        for element, locations in percepts.items():
            if len(locations) != 0:
                for location in locations:
                    self.state[location[0]][location[1]] = keys[str(element)]
                    things_at.append(location)

        for cell in surrounding_cells:
            if not cell in things_at:
                try:
                    self.state[cell[0]][cell[1]] = '-'
                except:
                    pass

    # This function translates the agent's actions into the map, updating it on every step
    # This function also updates the agent's score for every movement.
    def update_map(self, target_row, target_col, grid):
        target_cell = grid[target_row][target_col]
        if target_cell == '#':
            self.score -= 1
        elif target_row < 1 or target_col < 1:
            self.score -= 5
        else:
            self.score -= 1
            grid[self.row][self.col] = self.prev_cell
            self.state[self.row][self.col] = self.prev_cell
            self.row = target_row
            self.col = target_col
            self.prev_cell = grid[target_row][target_col]
            grid[target_row][target_col] = 'E'
            self.state[target_row][target_col] = 'E'

    # Moves the agent one cell up (if possible)
    def move_up(self, grid, percepts):
        #Add percepts to the internal state
        self.update_state(percepts)
        try:
            target_row = self.row - 1
            target_col = self.col
            self.update_map(target_row, target_col, grid)

        except:
            self.score -= 5
        print('Moved up. Last cell: %s' % self.prev_cell)

    # Moves the agent one cell down (if possible)
    def move_down(self, grid, percepts):
        #Add percepts to the internal state
        self.update_state(percepts)
        try:
            target_row = self.row + 1
            target_col = self.col
            self.update_map(target_row, target_col, grid)
        except:
            self.score -= 5
        print('Moved down. Last cell: %s' % self.prev_cell)

    # Moves the agent one cell to the right (if possible)
    def move_right(self, grid, percepts):
        #Add percepts to the internal state
        self.update_state(percepts)
        try:
            target_row = self.row
            target_col = self.col + 1
            self.update_map(target_row, target_col, grid)
        except:
            self.score -= 5
        print('Moved right. Last cell: %s' % self.prev_cell)

    # Moves the agent one cell to the left (if possible)
    def move_left(self, grid, percepts):
        #Add percepts to the internal state
        self.update_state(percepts)
        try:
            target_row = self.row
            target_col = self.col - 1
            self.update_map(target_row, target_col, grid)
        except:
            self.score -= 5
        print('Moved left. Last cell: %s' % self.prev_cell)

    # This function does nothing
    def no_op():
        pass

    # Allows the user to grab a reusable tool if its current cell has such tool
    def g_reuse(self, grid):
        if self.prev_cell == 'H':
            # Stop grabbing this kind of tools if you already have one
            if not 'H' in self.tools:
                self.tools.append('H')
                self.prev_cell = '-'
                self.score -= 2
                print('Grabbed reusable tool')

    # Allows the user to grab a disposable tool if its current cell has such tool
    def g_dispos(self, grid):
        if self.prev_cell == 'h':
            self.tools.append('h')
            self.prev_cell = '-'
            self.score -= 2
            print('Grabbed disposable tool')

    # Allows the user to grab a disposable tool if its current cell has such tool
    def g_treas1(self):
        if self.prev_cell == 'T' and 'H' in self.tools:
            self.prev_cell = '-'
            self.score += 20
            print('Grabbed type 1 treasure')

    # Allows the user to grab a type 2 treasure if its current cell has such treasure
    def g_treas2(self):
        if self.prev_cell == 't' and 'h' in self.tools:
            self.prev_cell = '-'
            self.tools.remove('h')
            self.score += 40
            print('Grabbed type 2 treasure')


'''Main Program'''
if __name__ == '__main__':
    # Choose the type of explorer.
    # 'SR_Explorer' for a Simple Reflex Agent
    # 'MB_Agent' for a Model Based Agent
    explorer = MB_Explorer()

    # Choose the type of environment.
    # 'FO_Grid' for a Fully Observable Environment
    # 'PO_Environment' for a Partially Observable Environment
    grid = FO_Grid(explorer)

    # Add a number of different elements to the map.
    # Be careful not to add too many elements or the program will loop infinitely (to patch later)
    grid.add('walls',  6)
    grid.add('treas1', 2)
    grid.add('reus',   2)
    grid.add('treas2', 2)
    grid.add('dispos', 2)

    # Specify the maximum number of steps for the program to run
    grid.run(100)
