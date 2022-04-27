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


def pathing(obstacles):
    pass


def parallel_park(obstacles):
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
    mask, minimum_x, maximum_x, minimum_y, maximum_y = obstacle_mask(obstacles_x, obstacles_y, 1, 4)
    return mask, minimum_x, maximum_x, minimum_y, maximum_y


def grid_pos(index, resolution, pos):
    return index * resolution + pos


def obstacle_mask(obstacles_x, obstacles_y, resolution, agent_radius):
    minimum_x = round(min(obstacles_x))
    maximum_x = round(max(obstacles_x))
    minimum_y = round(min(obstacles_y))
    maximum_y = round(max(obstacles_y))
    x = round((maximum_x - minimum_x) / resolution)
    y = round((maximum_y - minimum_y) / resolution)
    mask = [[False for count in range(y)] for count in range(x)]
    for temp_x in range(x):
        xa = grid_pos(temp_x, 1, round(min(obstacles_x)))
        for temp_y in range(y):
            ya = grid_pos(temp_y, 1, round(min(obstacles_y)))
            for xb, yb in zip(obstacles_x, obstacles_y):
                if math.hypot(xb - x, yb - y) < agent_radius:
                    mask[xa][ya] = True
                    break
    return mask, minimum_x, maximum_x, minimum_y, maximum_y


def manoeuvre(x_start, y_start, x_end, y_end, mask, minimum_x, maximum_x, minimum_y, maximum_y):
    new_x, new_y = pathing_helper(x_start + 1, y_start + 1, x_end + 1, y_end + 1, mask, minimum_x, maximum_x, minimum_y, maximum_y)


def pathing_helper(x_start, y_start, x_end, y_end, mask, minimum_x, maximum_x, minimum_y, maximum_y):
    new_x = None
    new_y = None
    start = node(calc_xy_index(x_start, minimum_x), calc_xy_index(y_start, minimum_y), 0.0, -1)
    end = node(calc_xy_index(x_end, minimum_x), calc_xy_index(y_end, minimum_y), 0.0, -1)
    
    return new_x, new_y


# Rename!
def node(x, y, cost, index):
    return str(x + "," + y + "," + cost + "," + index)


# Rename!
def calc_xy_index(coord, min_coord):
    return round(coord - min_coord)


# Rename!
def calc_heuristic():
    


# Rename!
def calc_grid_index():
    