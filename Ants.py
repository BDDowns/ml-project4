from DataHandler import DataPoints as pnt
import random
from bidict import bidict
from scipy.spatial import distance as dst
class Ant:
    def __init__(self, farm, x_init=0, y_init=0, sense_range=10, ):
        self.farm = farm
        self.pos = [x_init, y_init]
        self.sense_range= sense_range
        self.data_loc_sensed = []
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
        for i in range(-self.sense_range, self.sense_range):
            for j in range(-self.sense_range, self.sense_range):
                point = [self.pos[0]+i, self.pos[1]+j]
                # Check if collection of points in search radius contain data
                # To do this, check Antfarm's list of points containing data
                if (self.farm.occupied_space.count(point)>0):#If scanned position contains data
                    points_in_range.append(point)
        self.data_loc_sensed = points_in_range

    def evaluate_env(self):
        #if an ant can not sense any data nearby
        if(len(self.data_loc_sensed)<=3):
            return False
        else: return True



    """
    evaluate_fit method
    """
    def evaluate_fit(self):
        #local list of datapoints [location, data]
        data = []
        least_fitness = None
        index = None
        for each in self.data_loc_sensed:
            data.append([each, self.farm.data_map.inv[each].data])
        data = sorted(data, key=lambda x: (abs(self.pos[0]-x[0]) +abs(self.pos[1]-x[1])))
        for i in range(0, len(data)):
            if(self.carrying is None):
                compared_point = data[i][1]
            else: compared_point = self.carrying
            # compute cosine similiarity between compared point and next 2 points closest to ant
            if (i < len(data)-2):
                mean = (1/2)*(data[i+1][1] + data[i+2][1])
                score = dst.cosine(compared_point, mean)
            else:
                mean = (1 / 2) * (data[i - 1][1] + data[i + 2][1])
                score = dst.cosine(compared_point, mean)
            #update if new least fit found and meets dissimilarity tolerance
            if (score>least_fitness and score>.27):
                least_fitness = score
                index = i
        if(index is not None):
            return data[index]




class AntFarm:
    def __init__(self, num_ants, datapoints, sense_radius=None, dimensions=None, max_iterations=10000):
        if(dimensions is None):
            dimensions = [700, 700]
        self.dimensions = dimensions
        self.max_iterations = max_iterations
        self.occupied_space = [None]
        self.data_map = bidict({})#dictionary for space by data point
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
                    self.data_map[point] = point.loc
                    placed = True
        self.occupied_space.sort()

    def update_data_map(self, datapoint, loc):
        self.data_map[datapoint] = loc
        datapoint.loc = loc


