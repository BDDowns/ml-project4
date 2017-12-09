from DataHandler import DataPoints as pnt
import random
class Ant:
    def __init__(self, farm, x_init=0, y_init=0, sense_range=10, ):
        self.farm = farm
        self.pos = [x_init, y_init]
        self.sene_range= sense_range
        self.data_sensed = None
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
    def scan(self):
        #create collection of x-y coordinates in Ant's seach radius
        points_in_range = []
        for i in range(-self.sense_range, self.sene_range):
            for j in range(-self.sense_range, self.sene_range):
                point = [self.pos[0]+i, self.pos[1]+j]
        #Check if collection of points in search radius contain data
        #To do this, check Antfarm's list of points containing data
        for point in points_in_range:
            if (self.farm.occupied_space.count(point)<1):
                points_in_range.remove(point)
            self.data_sensed = points_in_range
    def

class AntFarm:
    def __init__(self, num_ants, datapoints, sense_radius=None, dimensions=[700, 700]):
        self.dimensions = dimensions
        self.occupied_space = [None]
        self.x_max = dimensions[0]
        self.y_max = dimensions[1]
        self.colony = []
        #Initialize ants
        for i in range(num_ants):
            x = random.randint(0, self.dimensions[0])
            y = random.randint(0, self.dimensions[1])
            ant = Ant(self, x, y, sense_radius)
            self.colony.append(ant)
        #set position for datapoints in 2-D space
        for point in datapoints:
            placed = False
            while(placed is False):
                x = random.randint(0, self.dimensions[0])
                y = random.randint(0, self.dimensions[1])
                #check that no other datapoint is already in this position
                if self.occupied_space.count([x, y]<1):
                    self.occupied_space.append([x, y])
                    point.loc = [x, y]
                    placed = True


