from DataHandler import DataPoints as pnt
import random
class Ant:
    def __init__(self, farm, x_init=0, y_init=0, range=10, ):
        self.farm = farm
        self.pos = [x_init, y_init]
        self.range = range
        self.carrying = None
    def pickup(self, datapoint):
        self.carrying = datapoint
        self.carrying.pick_up(self)
    def setdown(self):
        self.carrying.set_down()
        self.carrying = None
    def check_valid_pos(self, pos):
        valid = False
        x, y = pos[0], pos[1]
        #check if position is within bounds of ant farm
        if(x>0 and x<self.farm.x_max) and (y>0 and y<self.farm.y_max):
            valid = True
        else: return False
        #check that no other data points occupy that position
        if(self.farm.occupied_space.count([x, y])>0):
            return False
        return valid


class AntFarm:
    def __init__(self, num_ants, datapoints, sense_radius=None, dimensions=[700, 700]):
        self.dimensions = dimensions
        self.occupied_space = [None]
        self.x_max = dimensions[0]
        self.y_max = dimensions[1]
        self.colony = []
        for i in range(num_ants):
            x = random.randint(0, self.dimensions[0])
            y = random.randint(0, self.dimensions[1])
            ant = Ant(self, x, y, sense_radius)
