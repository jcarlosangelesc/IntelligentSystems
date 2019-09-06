from search import *
import copy
import random
import time

class State:
    def __init__(self, agent_pos, obstacles, movables, target, goal):
        self.rows = 5
        self.cols = 5
        self.agent_pos = agent_pos
        self.obstacles = obstacles
        self.movables = movables
        self.target = target
        self.goal = goal
        self.free_spaces = [[x, y] for x in range(self.rows) for y in range(self.cols) if [x, y] not in (self.obstacles + self.movables + [self.target])]

    def show(self):
        print('\n[ STATE ]')
        for r in range(self.rows):
            for c in range(self.cols):
                if [r, c] == self.agent_pos:
                    print('A' + ' ', end = '')
                elif [r, c] in self.obstacles:
                    print('O' + ' ', end = '')
                elif [r, c] in self.movables:
                    print('M' + ' ', end = '')
                elif [r, c] == self.target:
                    print('T' + ' ', end = '')
                elif [r, c] == self.goal:
                    print('X' + ' ', end = '')
                else:
                    print('-' + ' ', end = '')
            print()
        print()

    def get_neighbors(self):
        U, D, L, R = DIRECTIONS = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        neighbors = []
        for [dx, dy] in DIRECTIONS:
            [nx, ny] = [self.agent_pos[0] + dx, self.agent_pos[1] + dy]
            if [nx, ny] not in self.obstacles and 0 <= nx < self.rows and 0 <= ny < self.cols:
                neighbors.append([nx, ny])
        return neighbors


class PushPull(Problem):
    def actions(self, state):
        actions = []
        # Posible actions:
        #   1. Move (N, S, E, W)
        #   2. Push (Must be besides the target and there should be a free space immediately after the target)
        #   3. Pull (Must be besides the target and there should be a free space immediately before the agent)

        # Get neighbor cells
        neighbors = state.get_neighbors()

        # For each neighbor deetermine which action can be performed
        for cell in neighbors:
            r = state.agent_pos[0]
            c = state.agent_pos[1]
            # Si la celda de arriba esta vacia puedes moverte hacia arriba
            if cell == [r - 1, c] and cell in state.free_spaces and cell not in (state.movables + [state.target]):
                actions.append('move_up')
            # Si la celda de la izquierda esta vacia puedes moverte hacia la izquierda
            if cell == [r, c - 1] and cell in state.free_spaces and cell not in (state.movables + [state.target]):
                actions.append('move_left')
            # Si la celda de la derecha esta vacia puedes moverte hacia la derecha
            if cell == [r, c + 1] and cell in state.free_spaces and cell not in (state.movables + [state.target]):
                actions.append('move_right')
            # Si la celda de abajo esta vacia puedes moverte hacia abajo
            if cell == [r + 1, c] and cell in state.free_spaces and cell not in (state.movables + [state.target]):
                actions.append('move_down')
            # Si la celda de arriba esta vacia y la celda de abajo es movible puedes jalar hacia arriba
            if cell == [r - 1, c] and cell in state.free_spaces and [r + 1, c] in (state.movables + [state.target]):
                actions.append('pull_up')
            # Si la celda de la izquierda esta vacia y la celda de la derecha es movible puedes jalar hacia la izquierda
            if cell == [r, c - 1] and cell in state.free_spaces and [r, c + 1] in (state.movables + [state.target]):
                actions.append('pull_left')
            # Si la celda de abajo esta vacia y la celda de arriba es movible puedes jalar hacia abajo
            if cell == [r + 1, c] and cell in state.free_spaces and [r - 1, c] in (state.movables + [state.target]):
                actions.append('pull_down')
            # Si la celda de la derecha esta vacia y la celda de la izquierda es movible puedes jalar hacia la derecha
            if cell == [r, c + 1] and cell in state.free_spaces and [r, c - 1] in (state.movables + [state.target]):
                actions.append('pull_right')
            # Si la celda de arriba es movible y la celda dos posiciones arriba esta vacia puedes empujar hacia arriba
            if cell == [r - 1, c] and cell in (state.movables + [state.target]) and [r - 2, c] in state.free_spaces:
                actions.append('push_up')
            # Si la celda de la izquierda es movible y la celda dos posiciones a la izquierda esta vacia puedes empujar hacia la izquierda
            if cell == [r, c - 1] and cell in (state.movables + [state.target]) and [r, c - 2] in state.free_spaces:
                actions.append('push_left')
            # Si la celda de abajo es movible y la celda dos posiciones abajo esta vacia puedes empujar hacia abajo
            if cell == [r + 1, c] and cell in (state.movables + [state.target]) and [r + 2, c] in state.free_spaces:
                actions.append('push_down')
            # Si la celda de la derecha es movible y la celda dos posiciones a la derecha esta vacia puedes empujar hacia la derecha
            if cell == [r, c + 1] and cell in (state.movables + [state.target]) and [r, c + 2] in state.free_spaces:
                actions.append('push_right')
        return actions

    def result(self, state, action):
        new_state = copy.deepcopy(state)
        r_pos = new_state.agent_pos[0]
        c_pos = new_state.agent_pos[1]

        if action == 'move_up':
            new_state.agent_pos = [r_pos - 1, c_pos]
        elif action == 'move_down':
            new_state.agent_pos = [r_pos + 1, c_pos]
        elif action == 'move_left':
            new_state.agent_pos = [r_pos, c_pos - 1]
        elif action == 'move_right':
            new_state.agent_pos = [r_pos, c_pos + 1]
        elif action == 'pull_up':
            # If the position below the agent is the target piece
            if new_state.target == [r_pos+1, c_pos]:
                new_state.target = [r_pos, c_pos]
            # Or if it is other movable piece
            else:
                new_state.movables[new_state.movables.index([r_pos + 1, c_pos])] = [r_pos, c_pos]
            new_state.agent_pos = [r_pos - 1, c_pos]
        elif action == 'pull_down':
            # If the position above the agent is the target piece
            if [r_pos - 1, c_pos] == new_state.target:
                new_state.target = [r_pos, c_pos]
            # Or if it is other movable piece
            else:
                new_state.movables[new_state.movables.index([r_pos - 1, c_pos])] = [r_pos, c_pos]
            new_state.agent_pos = [r_pos + 1, c_pos]
        elif action == 'pull_left':
            # If the position to the right the agent is the target piece
            if [r_pos, c_pos + 1] == new_state.target:
                new_state.target = [r_pos, c_pos]
            # Or if it is other movable piece
            else:
                new_state.movables[new_state.movables.index([r_pos, c_pos + 1])] = [r_pos, c_pos]
            new_state.agent_pos = [r_pos, c_pos - 1]
        elif action == 'pull_right':
            # If the position to the left of the agent is the target piece
            if [r_pos, c_pos - 1] == new_state.target:
                new_state.target = [r_pos, c_pos]
            # Or if it is other movable piece
            else:
                new_state.movables[new_state.movables.index([r_pos, c_pos - 1])] = [r_pos, c_pos]
            new_state.agent_pos = [r_pos, c_pos + 1]
        elif action == 'push_up':
            # If the position above the agent is the target piece
            if [r_pos - 1, c_pos] == new_state.target:
                new_state.target = [r_pos - 2, c_pos]
            # Or if it is other movable piece
            else:
                new_state.movables[new_state.movables.index([r_pos - 1, c_pos])] = [r_pos - 2, c_pos]
            new_state.agent_pos = [r_pos - 1, c_pos]
        elif action == 'push_down':
            # If the position below the agent is the target piece
            if [r_pos + 1, c_pos] == new_state.target:
                new_state.target = [r_pos + 2, c_pos]
            # Or if it is other movable piece
            else:
                idx = new_state.movables.index([r_pos + 1, c_pos])
                new_state.movables[idx] = [r_pos + 2, c_pos]
                # new_state.movables[new_state.movables.index((r_pos + 1, c_pos))] = (r_pos + 2, c_pos)
            new_state.agent_pos = [r_pos + 1, c_pos]
        elif action == 'push_left':
            # If the position to the left of the agent is the target piece
            if [r_pos, c_pos - 1] == new_state.target:
                new_state.target = [r_pos, c_pos - 2]
            # Or if it is other movable piece
            else:
                new_state.movables[new_state.movables.index([r_pos, c_pos - 1])] = [r_pos, c_pos - 2]
            new_state.agent_pos = [r_pos, c_pos - 1]
        elif action == 'push_right':
            # If the position to the right of the agent is the target piece
            if [r_pos, c_pos + 1] == new_state.target:
                new_state.target = [r_pos, c_pos + 2]
            # Or if it is other movable piece
            else:
                new_state.movables[new_state.movables.index([r_pos, c_pos + 1])] = [r_pos, c_pos + 2]
            new_state.agent_pos = [r_pos, c_pos + 1]
        return new_state

    def goal_test(self, state):
        return state.target == state.goal

# Easy test
agent_pos = [4,1]
obstacles = [[2,0], [2,1], [2,2], [2,3], [2,4]]
movables = []#[[4,1]] #[[2,2]]#, [2,2], [2,3]]
target = [4,0]
goal = [4,4]

state = State(agent_pos, obstacles, movables, target, goal)
state.show()
prob = PushPull(state, goal)

frontier = FIFOQueue()
start_time = time.time()
result, visited = tree_search(prob, frontier)
print("<SOLUTION>\n")
solution = result.solution()
for step, action in enumerate(solution):
    print("  Step %s" % str(step+1))
    print(action)
    state = prob.result(state, action)
    state.show()
print("< END >\n")
print ("This algorithm took", (time.time() - start_time), "seconds to run")
print("%s nodes were visited in the process" % visited)
print("The maximum depth reached for this solution was %s\n" % result.depth)
# print("Solution: %s" % solution)
