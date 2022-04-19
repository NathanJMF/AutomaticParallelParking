import cv2
import numpy as np
import scipy


class ParkingLot:
    def __init__(self, cars, walls):
        self.frame = None
        self.obstacles = np.vstack([cars, walls])
        self.margin = 1
        self.background = np.ones((1000 + 20 * self.margin, 1000 + 20 * self.margin, 3))
        self.generate_obstacles()

        self.ar = scipy.array
        self.rad = lambda ang: ang * self.pi / 180
        self.pi = scipy.pi
        self.sin = scipy.sin
        self.cos = scipy.cos
        self.dot = scipy.dot

    def generate_obstacles(self):
        obstacles = np.concatenate([np.array([[0, i] for i in range(100 + 2 * self.margin)]),
                                    np.array([[100 + 2 * self.margin - 1, i] for i in range(100 + 2 * self.margin)]),
                                    np.array([[i, 0] for i in range(100 + 2 * self.margin)]),
                                    np.array([[i, 100 + 2 * self.margin - 1] for i in range(100 + 2 * self.margin)]),
                                    self.obstacles + np.array([self.margin, self.margin])]) * 10
        for ob in obstacles:
            self.background[ob[1]:ob[1] + 10, ob[0]:ob[0] + 10] = 0

    def render_frame(self, car, x, y, angle):
        x = int(10 * x)
        y = int(10 * y)

        agent_body = car.car_body
        agent_body = self.rotate_contours(agent_body, self.ar([0.5, 0.5]), self.rad(angle))
        agent_body = agent_body + np.array([x, y])
        self.frame = cv2.fillPoly(self.background.copy(), np.int32([agent_body]), car.car_colour)

        agent_wheels = car.wheel_layout
        agent_wheels = agent_wheels + np.array([x, y])
        self.frame = cv2.fillPoly(self.frame, np.int32([agent_wheels]), car.wheel_colour)
        return self.frame

    def rotate_contours(self, pts, cnt, ang):
        return self.dot(pts - cnt, self.ar([[self.cos(ang), self.sin(ang)], [-self.sin(ang), self.cos(ang)]])) + cnt


class Agent:
    def __init__(self):
        self.car_length = 80
        self.car_width = 40
        self.car_colour = np.array([255, 0, 0]) / 255
        self.car_body = np.array([[+self.car_length / 2, +self.car_width / 2],
                                  [+self.car_length / 2, -self.car_width / 2],
                                  [-self.car_length / 2, -self.car_width / 2],
                                  [-self.car_length / 2, +self.car_width / 2]])
        self.wheel_width = 10
        self.wheel_diameter = 20
        self.wheel_colour = np.array([0, 0, 0]) / 255
        self.wheel_layout = np.array([[+self.wheel_diameter / 2, +self.wheel_width / 2],
                                      [+self.wheel_diameter / 2, -self.wheel_width / 2],
                                      [-self.wheel_diameter / 2, -self.wheel_width / 2],
                                      [-self.wheel_diameter / 2, +self.wheel_width / 2]])


class Cars:
    def __init__(self):
        self.car_object = self.create_car_object()
        self.end = None
        self.cars = {1: [[15, 37]],
                     2: [[27, 37]],
                     3: [[39, 37]],
                     4: [[51, 37]],
                     5: [[63, 37]],
                     6: [[15, 63]],
                     7: [[27, 63]],
                     8: [[39, 63]],
                     9: [[51, 63]],
                     10: [[63, 63]],
                     11: [[15, 70]],
                     12: [[27, 70]],
                     13: [[39, 70]],
                     14: [[51, 70]],
                     15: [[63, 70]],
                     16: [[15, 97]],
                     17: [[27, 97]],
                     18: [[39, 97]],
                     19: [[51, 97]],
                     20: [[63, 97]]}
        self.car_obstacles = np.empty(0, dtype=int)

    def generate_cars(self, parking_spot):
        self.end = self.cars[parking_spot][0]
        self.cars.pop(parking_spot)
        for key in self.cars.keys():
            for count in range(len(self.cars[key])):
                obstacle = self.car_object + self.cars[key]
                self.car_obstacles = np.append(self.car_obstacles, obstacle)
                self.car_obstacles = np.array(self.car_obstacles).reshape(-1, 2)
        return self.end, self.car_obstacles

    @staticmethod
    def create_car_object():
        object_x, object_y = np.meshgrid(np.arange(-4, 4), np.arange(-2, 2))
        car = np.dstack([object_x, object_y])
        car = car.reshape(-1, 2)
        return car


class Walls:
    def __init__(self):
        self.walls = [[i, 33] for i in range(0, 70)] + [[i, 66] for i in range(0, 70)]
        self.walls = np.array(self.walls)

    def get_walls(self):
        return self.walls
