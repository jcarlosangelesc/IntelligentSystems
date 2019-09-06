from agents import *

#Declaring the grid environment
class Grid(Environment):
    def __init__(self, walls, treas1, reus, treas2, dispos):
        self.walls = walls
        self.treas1 = treas1
        self.reus = reus
        self.treas2 = treas2
        self.dispos = dispos

    def percept(self, agent):
        #regresa informacion de donde están las cosas en el grid
        pass

    def execute_action(self, agent, action):
        #Execute action modifica el ambiente

        if action == "move_up":
            agent.move_up()
        elif action == "move_down":
            agent.move_down()
        elif action == "move_right":
            agent.move_right()
        elif action == "move_left":
            agent.move_left()
        elif action == "no_op":
            agent.no_op()
        elif action == "g_reuse":
            agent.g_reuse()
        elif action == "g_dispos":
            agent.g_dispos()
        elif action == "g_treas1":
            agent.g_treas1()
        elif action == "g_treas2":
            agent.g_treas2()

    def run(self, steps):
        pass

    def is_done(self):
        pass

class Explorer(Agent):
    pass

def program(percepts):
    #Aquí va el Simple Reflex Agent o La otra cosa
    pass

'''Main Program'''

if __name__ == 'main':
    print('Done')
