import cv2
import numpy as np


class ParkingLot:
    def __init__(self, cars, walls):
        self.obstacles = np.vstack([cars, walls])
        self.margin = 1
        self.background = np.ones((1000 + 20 * self.margin, 1000 + 20 * self.margin, 3))
        self.background[10:1000 + 20 * self.margin:10, :] = np.array([200, 200, 200]) / 255
        self.background[:, 10:1000 + 20 * self.margin:10] = np.array([200, 200, 200]) / 255
        self.generate_obstacles()

    def generate_obstacles(self):
        obstacles = np.concatenate([np.array([[0, i] for i in range(100 + 2 * self.margin)]),
                                    np.array([[100 + 2 * self.margin - 1, i] for i in range(100 + 2 * self.margin)]),
                                    np.array([[i, 0] for i in range(100 + 2 * self.margin)]),
                                    np.array([[i, 100 + 2 * self.margin - 1] for i in range(100 + 2 * self.margin)]),
                                    self.obstacles + np.array([self.margin, self.margin])]) * 10
        for ob in obstacles:
            self.background[ob[1]:ob[1] + 10, ob[0]:ob[0] + 10] = 0

    def render_frame(self):
        return self.background


class Cars:
    def __init__(self):
        self.car_object = self.create_car_object()
        self.end = None
        self.cars = {1: [[35, 20]], 2: [[65, 20]], 3: [[75, 20]], 4: [[95, 20]],
                     5: [[35, 32]], 6: [[65, 32]], 7: [[75, 32]], 8: [[95, 32]],
                     9: [[35, 44]], 10: [[65, 44]], 11: [[75, 44]], 12: [[95, 44]],
                     13: [[35, 56]], 14: [[65, 56]], 15: [[75, 56]], 16: [[95, 56]],
                     17: [[35, 68]], 18: [[65, 68]], 19: [[75, 68]], 20: [[95, 68]]}
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
        self.walls = [[70, i] for i in range(-5, 90)] + \
                     [[30, i] for i in range(10, 105)] + \
                     [[i, 10] for i in range(30, 36)] + \
                     [[i, 90] for i in range(70, 76)]
        self.walls = np.array(self.walls)

    def get_walls(self):
        return self.walls
