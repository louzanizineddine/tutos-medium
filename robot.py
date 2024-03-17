#!/usr/bin/python3

from time import sleep
from enum import Enum


class Direction(Enum):
    SENSOR_NORTH = 1
    SENSOR_EAST = 2
    SENSOR_SOUTH = 3
    SENSOR_WEST = 4

class Robot:
    def __init__(self, width=20, height=20, rect_x=5, rect_y=5, rect_width=5, rect_height=5):
        self.matrix = [[]]
        self.width = width
        self.height = height
        self.r_x_pos = 10  # artificial position of the robot
        self.r_y_pos = 10  # artificial position of the robot
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.T = False  # to indicate if the robot found the red rectangle or not
        self.AN = False
        self.AE = True  # initialized to True to start the search in the east direction with escargo
        self.AS = False
        self.AW = False
        self.long = 1
        self.temp = 1

    def build_matrix(self):
        self.matrix = [['E' for _ in range(self.width)]
                       for _ in range(self.height)]

        for i in range(self.rect_height):
            for j in range(self.rect_width):
                self.matrix[self.rect_y + i][self.rect_x + j] = 'R'

        self.matrix[self.r_y_pos][self.r_x_pos] = 'G'

    def production_system(self):
        while not self.T:
            self.search_red_rec()
            print("\033c", end="")
            self.print_matrix()
            sleep(1)
        print("\033c", end="")
        self.AE = self.AN = self.AS = self.AW = False
        while self.T:
            self.make_tour()
            print("\033c", end="")
            self.print_matrix()
            sleep(1)

    def make_tour(self):
        dir = self.sensors()
        if dir == Direction.SENSOR_NORTH:
            self.AO = True
            # move west
            self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
            self.matrix[self.r_y_pos][self.r_x_pos - 1] = 'G'
            self.r_x_pos -= 1
            return

        if dir == Direction.SENSOR_EAST:
            self.AN = True
            # move north
            self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
            self.matrix[self.r_y_pos - 1][self.r_x_pos] = 'G'
            self.r_y_pos -= 1
            return

        if dir == Direction.SENSOR_SOUTH:
            self.AE = True
            # move east
            self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
            self.matrix[self.r_y_pos][self.r_x_pos + 1] = 'G'
            self.r_x_pos += 1
            return

        if dir == Direction.SENSOR_WEST:
            self.AS = True
            # move south
            self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
            self.matrix[self.r_y_pos + 1][self.r_x_pos] = 'G'
            self.r_y_pos += 1
            return

        if dir is None and self.AN == True:
            self.AN = False
            self.AE = True
            # move east
            self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
            self.matrix[self.r_y_pos][self.r_x_pos + 1] = 'G'
            self.r_x_pos += 1
            return

        if dir is None and self.AE == True:
            self.AE = False
            self.AS = True
            # move south
            self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
            self.matrix[self.r_y_pos + 1][self.r_x_pos] = 'G'
            self.r_y_pos += 1
            return

        if dir is None and self.AS == True:
            self.AS = False
            self.AO = True
            # move west
            self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
            self.matrix[self.r_y_pos][self.r_x_pos - 1] = 'G'
            self.r_x_pos -= 1
            return

        if dir is None and self.AO == True:
            self.AO = False
            self.AN = True
            # move north
            self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
            self.matrix[self.r_y_pos - 1][self.r_x_pos] = 'G'
            self.r_y_pos -= 1
            return

    def search_red_rec(self):
        dir = self.sensors()
        print("dir: ", dir)
        if dir is None:
            if self.AE == True:
                if self.long == self.temp:
                    print("AE")
                    self.AE = False
                    self.AS = True
                    # move south
                    self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
                    self.matrix[self.r_y_pos + 1][self.r_x_pos] = 'G'
                    self.r_y_pos += 1  # update the position of the robot
                    self.long = self.long + 1
                    self.temp = 1
                    return
                else:
                    print("AE")
                    self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
                    self.matrix[self.r_y_pos][self.r_x_pos + 1] = 'G'
                    self.r_x_pos += 1
                    self.temp = self.temp + 1
                    return

            elif self.AS == True:
                if self.long == self.temp:
                    print("AS")
                    self.AS = False
                    self.AW = True
                    # move west
                    self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
                    self.matrix[self.r_y_pos][self.r_x_pos - 1] = 'G'
                    self.r_x_pos -= 1
                    self.temp = 1
                    self.long = self.long + 1
                    return
                else:
                    print("AS")
                    self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
                    self.matrix[self.r_y_pos + 1][self.r_x_pos] = 'G'
                    self.r_y_pos += 1
                    self.temp = self.temp + 1
                    return

            elif self.AW == True:
                if self.long == self.temp:
                    print("AW")
                    self.AW = False
                    self.AN = True
                    # move north
                    self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
                    self.matrix[self.r_y_pos - 1][self.r_x_pos] = 'G'
                    self.r_y_pos -= 1
                    self.temp = 1
                    return
                else:
                    print("AW")
                    self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
                    self.matrix[self.r_y_pos][self.r_x_pos - 1] = 'G'
                    self.r_x_pos -= 1
                    self.temp = self.temp + 1
                    return

            elif self.AN == True:
                if self.long == self.temp:
                    print("AN")
                    self.AN = False
                    self.AE = True
                    # move east
                    self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
                    self.matrix[self.r_y_pos][self.r_x_pos + 1] = 'G'
                    self.r_x_pos += 1
                    self.temp = 1
                    self.long = self.long + 1
                    return
                else:
                    print("AN")
                    self.matrix[self.r_y_pos][self.r_x_pos] = 'E'
                    self.matrix[self.r_y_pos - 1][self.r_x_pos] = 'G'
                    self.r_y_pos -= 1
                    self.temp = self.temp + 1
                    return

        else:  # if the robot found the red rectangle
            self.T = True
            print("The robot found the red rectangle")

    def sensors(self):
        if self.matrix[self.r_y_pos - 1][self.r_x_pos] == 'R':
            return Direction.SENSOR_NORTH
        elif self.matrix[self.r_y_pos][self.r_x_pos + 1] == 'R':
            return Direction.SENSOR_EAST
        elif self.matrix[self.r_y_pos + 1][self.r_x_pos] == 'R':
            return Direction.SENSOR_SOUTH
        elif self.matrix[self.r_y_pos][self.r_x_pos - 1] == 'R':
            return Direction.SENSOR_WEST
        else:
            return None

    def print_matrix(self):
        robot_emoji = '🤖'
        rectangle_emoji = '🟥'
        grass_green = '🌿'
    
        for i in range(self.height):
            for j in range(self.width):
                if self.matrix[i][j] == 'R':
                    print(rectangle_emoji, end=' ')
                elif self.matrix[i][j] == 'G':
                    print(robot_emoji, end=' ')
                elif self.matrix[i][j] == 'E':
                    print(grass_green, end=' ')
                else:
                    print(self.matrix[i][j], end=' ')
            print()
        print()

        print("Robot position: ", self.r_x_pos, self.r_y_pos)


if __name__ == '__main__':
    robot = Robot()
    robot.build_matrix()
    robot.production_system()
