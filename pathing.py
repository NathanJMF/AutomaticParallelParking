import numpy as np
import math

motion = [[1, 0, 1],
          [0, 1, 1],
          [-1, 0, 1],
          [0, -1, 1],
          [-1, -1, math.sqrt(2)],
          [-1, 1, math.sqrt(2)],
          [1, -1, math.sqrt(2)],
          [1, 1, math.sqrt(2)]]


def path_planning(obstacles):
    pass


def parallel_park(obstacles, x_start, y_start, x_end, y_end):
    margin = 1
    obstacles_x = np.empty(0, dtype=int)
    obstacles_y = np.empty(0, dtype=int)
    obstacles = obstacles + np.array([margin, margin])
    obstacles = obstacles[obstacles[:, 0] > -1 & obstacles[:, 1] > -1]
    obstacles = np.concatenate([np.array([[0, i] for i in range(100 + 2 * margin)]),
                                np.array([[100 + 2 * margin - 1, i] for i in range(100 + 2 * margin)]),
                                np.array([[i, 0] for i in range(100 + 2 * margin)]),
                                np.array([[i, 100 + 2 * margin - 1] for i in range(100 + 2 * margin)]),
                                obstacles + np.array([margin, margin])]) * 10
    for item in obstacles:
        obstacles_x = np.append(obstacles_x, item[:, 0])
        obstacles_y = np.append(obstacles_y, item[:, 1])
    # call other functions


def grid_pos(index, resolution, pos):
    return index * resolution + pos


def obstacle_mask(obstacles_x, obstacles_y, resolution, agent_radius):
    x = round((round(max(obstacles_x)) - round(min(obstacles_x))) / resolution)
    y = round((round(max(obstacles_y)) - round(min(obstacles_y))) / resolution)
    mask = [[False for count in range(y)] for count in range(x)]
    for temp_x in range(x):
        xa = grid_pos(temp_x, 1, round(min(obstacles_x)))
        for temp_y in range(y):
            ya = grid_pos(temp_y, 1, round(min(obstacles_y)))
            for xb, yb in zip(obstacles_x, obstacles_y):
                if math.hypot(xb - x, yb - y) < agent_radius:
                    mask[xa][ya] = True
                    break
    return mask
