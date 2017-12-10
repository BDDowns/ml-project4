from DataHandler import DataPoints as pnt
import random
from bidict import bidict #bi-directional dictionary mapping
from scipy.spatial import distance as dst
class Ant:
    def __init__(self, farm, x_init=0, y_init=0, sense_range=10, ):
        self.farm = farm
        self.pos = [x_init, y_init]
        self.sense_range= sense_range
        self.data_loc_sensed = []
        self.carrying = None

    def move(self, vector=None, dropoff=False):
        moved = False
        #If ant is moving to determined location, check that location is valid and move
        if(vector is not None):
            new_vector = [self.pos[0] + vector[0], self.pos[1] + vector[1]]
            if(self.check_valid_pos(new_vector, dropoff=dropoff)):
                self.pos = new_vector
            else:
                #If the position chosen is not valid, check immediately adjacent positions
                for i in range(-1, 1):
                    for j in range(-1, 1):
                        if(self.check_valid_pos([new_vector[0] + i, new_vector[1] + j], dropoff=dropoff) is not False):
                            self.pos = [new_vector[0] + i, new_vector[1] + j]
                            i=5
                            j=5
                            moved = True
                #if no position in the immediate vicinity are viable, move to new random location
                if(moved is False):
                    while(moved is False):
                        x = random.randint(-15, 15) + self.pos[0]
                        y = random.randint(-15, 15) + self.pos[1]
                        if (self.check_valid_pos([x, y], dropoff=dropoff) is not False):
                            self.pos = [x, y]
                            moved = True
        else:
            while(moved is False):
                x = random.randint(-50,50)+ self.pos[0]
                y = random.randint(-50, 50) + self.pos[1]
                if (self.check_valid_pos([x, y], dropoff=dropoff) is not False):
                    self.pos = [x, y]
                    moved=True

    def pickup(self):
        datapoint = self.farm.data_map.inv[self.pos]
        self.carrying = datapoint
        del(self.farm.data_map[datapoint])

    def setdown(self):
        self.farm.data_map[self.carrying] = self.pos
        self.carrying = None

    def check_valid_pos(self, pos, dropoff=False):
        valid = False
        x, y = pos[0], pos[1]
        #check if position is within bounds of ant farm
        if(x>0 and x<self.farm.x_max) and (y>0 and y<self.farm.y_max):
            valid = True
        else: return False
        #check that no other data points occupy that position
        if(self.farm.occupied_space.count([x, y])>0 and dropoff is not False):
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


    def steps_per_iteration(self):
        self.scan()
        if(self.carrying is not None):
            while(len(self.data_loc_sensed)<3):
                self.move()
                self.scan()
            target = self.evaluate_fit()
            if (target is not None):
                self.move(target, dropoff=True)
                self.setdown()
        else



    """
    evaluate_fit method evaluates the fitness of the datapoints within an ant's percetion range
    The fitness is computed by calculating the cosine similarity of a datapoint and two other sensed datapoints
    datapoints are ordered by their distance from the ant's position

    returns best position for dropoff if ant is carrying data
    or best point to move if not carrying data

    """
    def evaluate_fit(self):
        #local list of datapoints [location, data]
        datum = []
        least_fitness = 0
        best_fitness = 1
        target = None
        for each in self.data_loc_sensed:
            datum.append([each, self.farm.data_map.inv[each]])
            #sort list of locally sensed data in order of Manhattan distance from ant
        datum = sorted(datum, key=lambda x: (abs(self.pos[0]-x.data[0]) + abs(self.pos[1]-x.data[1])))
        for i in range(0, len(datum)):
            if(self.carrying is None):
                compared_point = datum[i][1]
            else: compared_point = self.carrying
            # compute cosine similiarity between compared point and next 2 points closest to ant
            if (i < len(datum)-3):
                mean = (1/2)*(datum[i+1][1].data + datum[i+2][1].data)
                mean_pos = [((datum[i + 1][0][0] + datum[i + 2][0][0])//2),
                            ((datum[i + 1][0][1] + datum[i + 2][0][1])//2)]
                score = dst.cosine(compared_point.data, mean)
            else:
                mean = (1 / 2) * (datum[i - 1].data + datum[i + 2].data)
                mean_pos = [((datum[i - 1][0][0] + datum[i - 2][0][0]) // 2),
                            ((datum[i - 1][0][1] + datum[i - 2][0][1]) // 2)]
                score = dst.cosine(compared_point.data, mean)
            #update if new least fit found and meets dissimilarity tolerance
            if (self.carrying is None):
                if(score>least_fitness and score>.33 ):
                    least_fitness = score
                    target = datum[i][0]
            elif( self.carrying is not None ):
                if(score<.33 and score<best_fitness):
                    best_fitness = score
                    target = mean_pos

        if(target is not None):
            return target
        else: return None




class AntFarm:
    def __init__(self, num_ants, datapoints, sense_radius=None, dimensions=None, max_iterations=10000):
        if(dimensions is None):
            dimensions = [700, 700]
        self.dimensions = dimensions
        self.max_iterations = max_iterations
        self.occupied_space = [None]
        self.data_map = bidict({})#bi-directional dictionary for space and data point
        #                          # { Datapoint : [x, y] }
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



