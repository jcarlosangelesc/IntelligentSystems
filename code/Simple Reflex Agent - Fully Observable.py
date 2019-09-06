from agents import *
from random import randrange

#Declaring the grid environment
class Grid(Environment):
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
                qtty = qtty - 1

    def show(self):
        print("ENVIRONMENT")
        for row in range(len(self.map)):
            for col in range(len(self.map)):
                print(self.map[row][col] + ' ', end = '')
            print()
        print()

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
            opt = randrange(4)
            if opt == 0:
                self.agent.move_up(self.map)
                self.execute_action()
            if opt == 1:
                self.agent.move_down(self.map)
                self.execute_action()
            if opt == 2:
                self.agent.move_left(self.map)
                self.execute_action()
            if opt == 3:
                self.agent.move_right(self.map)
                self.execute_action()
            self.show()
            step = step + 1
            steps -= 1

    def is_done(self):
        percepts = self.percept()
        hasTreas1 = len(percepts['treas1'])
        hasTreas2 = len(percepts['treas2'])
        if hasTreas1 == 0 and hasTreas2 == 0:
            return True
        else:
            return False

class Explorer(Agent):
    def __init__(self):
        self.row = None
        self.col = None
        self.prev_cell = '-'
        self.tools = []
        self.score = 50

    def __repr__(self):
        return "Explorer{\nRow:%s \nCol:%s \nTools:%s \nScore:%s}" % (self.row, self.col, self.tools, self.score)

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

    def move_up(self, grid):
        try:
            target_row = self.row - 1
            target_col = self.col
            self.update_map(target_row, target_col, grid)
        except:
            self.score -= 5
        print('Moved up. Last cell: %s' % self.prev_cell)

    def move_down(self, grid):
        try:
            target_row = self.row + 1
            target_col = self.col
            self.update_map(target_row, target_col, grid)
        except:
            self.score -= 5
        print('Moved down. Last cell: %s' % self.prev_cell)

    def move_right(self, grid):
        try:
            target_row = self.row
            target_col = self.col + 1
            self.update_map(target_row, target_col, grid)
        except:
            self.score -= 5
        print('Moved right. Last cell: %s' % self.prev_cell)

    def move_left(self, grid):
        try:
            target_row = self.row
            target_col = self.col - 1
            self.update_map(target_row, target_col, grid)
        except:
            self.score -= 5
        print('Moved left. Last cell: %s' % self.prev_cell)

    def no_op():
        pass

    def g_reuse(self, grid):
        if self.prev_cell == 'H':
            self.tools.append('H')
            self.prev_cell = '-'
            self.score -= 2
            print('Grabbed reusable tool')

    def g_dispos(self, grid):
        if self.prev_cell == 'h':
            self.tools.append('h')
            self.prev_cell = '-'
            self.score -= 2
            print('Grabbed disposable tool')

    def g_treas1(self):
        if self.prev_cell == 'T' and 'H' in self.tools:
            self.prev_cell = '-'
            self.score += 20
            print('Grabbed type 1 treasure')

    def g_treas2(self):
        if self.prev_cell == 't' and 'h' in self.tools:
            self.prev_cell = '-'
            self.tools.remove('h')
            self.score += 40
            print('Grabbed type 2 treasure')


'''Main Program'''

if __name__ == '__main__':
    explorer = Explorer()
    grid = Grid(explorer)
    grid.add('walls', 6)
    grid.add('treas1', 2)
    grid.add('reus', 2)
    grid.add('treas2', 2)
    grid.add('dispos', 2)
    grid.run(200)
    # grid.percept()
    print('Done')
