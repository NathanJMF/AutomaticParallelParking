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
        obs = np.concatenate([np.array([[0, i] for i in range(100 + 2 * self.margin)]),
                              np.array([[100 + 2 * self.margin - 1, i] for i in range(100 + 2 * self.margin)]),
                              np.array([[i, 0] for i in range(100 + 2 * self.margin)]),
                              np.array([[i, 100 + 2 * self.margin - 1] for i in range(100 + 2 * self.margin)]),
                              self.obstacles + np.array([self.margin, self.margin])]) * 10
        for ob in obs:
            self.background[ob[1]:ob[1] + 10, ob[0]:ob[0] + 10] = 0

    def render_frame(self, car, x, y, angle, steer_angle):
        x = int(10 * x)
        y = int(10 * y)

        agent_body = car.car_body
        agent_body = self.rotate_contours(agent_body, self.ar([0.5, 0.5]), self.rad(angle))
        agent_body = agent_body + np.array([x, y])
        self.frame = cv2.fillPoly(self.background.copy(), np.int32([agent_body]), car.car_colour)

        agent_wheel_base = car.wheel_base
        agent_wheel = car.wheel_layout
        agent_wheel_base = self.rotate_contours(agent_wheel_base, self.ar([0.5, 0.5]), self.rad(angle))
        for count, wheel in enumerate(agent_wheel_base):
            if count <= 1:
                tire = self.rotate_contours(agent_wheel, self.ar([0.5, 0.5]), self.rad(angle + steer_angle))
            else:
                tire = self.rotate_contours(agent_wheel, self.ar([0.5, 0.5]), self.rad(angle))
            tire = tire + np.array([x, y]) + wheel
            self.frame = cv2.fillPoly(self.frame, np.int32([tire]), car.wheel_colour)
        self.frame = cv2.resize(np.flip(self.frame, axis=0), (700, 700))
        return self.frame

    def path(self, path):
        path = np.array(path) * 10
        color = np.random.randint(0, 150, 3) / 255
        path = path.astype(int)
        for p in path:
            self.background[p[1] + 10 * self.margin:p[1] + 10 * self.margin + 3,
            p[0] + 10 * self.margin:p[0] + 10 * self.margin + 3] = color

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
        self.wheel_base = np.array([[25, 15], [25, -15], [-25, 15], [-25, -15]])
        self.wheel_layout = np.array([[+self.wheel_diameter / 2, +self.wheel_width / 2],
                                      [+self.wheel_diameter / 2, -self.wheel_width / 2],
                                      [-self.wheel_diameter / 2, -self.wheel_width / 2],
                                      [-self.wheel_diameter / 2, +self.wheel_width / 2]])


class Cars:
    def __init__(self):
        self.car_object = self.create_car_object()
        self.end = None
        self.cars = {1: [[37, 15]],
                     2: [[37, 27]],
                     3: [[37, 39]],
                     4: [[37, 51]],
                     5: [[37, 63]],
                     6: [[63, 15]],
                     7: [[63, 27]],
                     8: [[63, 39]],
                     9: [[63, 51]],
                     10: [[63, 63]],
                     11: [[70, 15]],
                     12: [[70, 27]],
                     13: [[70, 39]],
                     14: [[70, 51]],
                     15: [[70, 63]],
                     16: [[97, 15]],
                     17: [[97, 27]],
                     18: [[97, 39]],
                     19: [[97, 51]],
                     20: [[97, 63]]}
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
        object_x, object_y = np.meshgrid(np.arange(-2, 2), np.arange(-4, 4))
        car = np.dstack([object_x, object_y])
        car = car.reshape(-1, 2)
        return car


class Walls:
    def __init__(self):
        self.walls = [[33, i] for i in range(0, 70)] + [[66, i] for i in range(0, 70)]
        self.walls = np.array(self.walls)

    def get_walls(self):
        return self.walls
