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
    obstacles = obstacles + np.array([margin, margin])
    obstacles = obstacles[(obstacles[:, 0] >= 0) & (obstacles[:, 1] >= 0)]
    # obstacles = obstacles[obstacles[:, 0] >= 0 & obstacles[:, 1] >= 0]
    obstacles = np.concatenate([np.array([[0, i] for i in range(100 + 2 * margin)]),
                                np.array([[100 + 2 * margin - 1, i] for i in range(100 + 2 * margin)]),
                                np.array([[i, 0] for i in range(100 + 2 * margin)]),
                                np.array([[i, 100 + 2 * margin - 1] for i in range(100 + 2 * margin)]),
                                obstacles + np.array([margin, margin])]) * 10
    # obstacles_x = np.empty(0, dtype=int)
    # obstacles_y = np.empty(0, dtype=int)
    # for item in obstacles:
    #     obstacles_x = np.append(obstacles_x, item[:, 0])
    #     obstacles_y = np.append(obstacles_y, item[:, 1])
    obstacles_x = [int(item) for item in obstacles[:, 0]]
    obstacles_y = [int(item) for item in obstacles[:, 1]]
    mask, minimum_x, maximum_x, minimum_y, maximum_y = obstacle_mask(obstacles_x, obstacles_y, 1, 4)
    return mask, minimum_x, maximum_x, minimum_y, maximum_y


# def grid_pos(index, resolution, pos):
#     return index * resolution + pos


def grid_pos(index, pos):
    return index + pos


def obstacle_mask(obstacles_x, obstacles_y, resolution, agent_radius):
    minimum_x = round(min(obstacles_x))
    maximum_x = round(max(obstacles_x))
    minimum_y = round(min(obstacles_y))
    maximum_y = round(max(obstacles_y))
    x = round((maximum_x - minimum_x) / resolution)
    y = round((maximum_y - minimum_y) / resolution)
    mask = [[False for count in range(y)] for count in range(x)]
    for temp_x in range(x):
        xa = grid_pos(temp_x, round(min(obstacles_x)))
        for temp_y in range(y):
            ya = grid_pos(temp_y, round(min(obstacles_y)))
            for xb, yb in zip(obstacles_x, obstacles_y):
                if math.hypot(xb - x, yb - y) < agent_radius:
                    mask[xa][ya] = True
                    break
    return mask, minimum_x, maximum_x, minimum_y, maximum_y


def manoeuvre(x_start, y_start, x_end, y_end, mask, minimum_x, maximum_x, minimum_y, maximum_y, width):
    new_x, new_y = pathing_helper(x_start + 1, y_start + 1, x_end + 1, y_end + 1, mask, minimum_x, maximum_x, minimum_y,
                                  maximum_y, width)


def pathing_helper(x_start, y_start, x_end, y_end, mask, minimum_x, maximum_x, minimum_y, maximum_y, width):
    # route_x = None
    # route_y = None
    start_set = dict()
    end_set = dict()
    # width = round((maximum_x - minimum_x) / 1)
    start = node(calc_xy_index(x_start, minimum_x), calc_xy_index(y_start, minimum_y), 0.0, -1)
    end = node(calc_xy_index(x_end, minimum_x), calc_xy_index(y_end, minimum_y), 0.0, -1)
    start_set[calc_grid_index(start, minimum_x, minimum_y, width)] = start
    while True:
        if not bool(start_set):
            print("Empty starting set")
            break
        current_id = min(start_set, key=lambda o: start_set[o]["cost"] + calc_heuristic(end, start_set[o]))
        current_node = start_set[current_id]
        if current_node["x"] == end["x"] and current_node["x"] == end["x"]:
            end["cost"] = current_node["cost"]
            end["index"] = current_node["index"]
            break
        del start_set[current_id]
        end_set[current_id] = current_node
        for count in range(len(motion)):
            item = node(current_node["x"] + motion[count][0], current_node["y"] + motion[count][1], current_node["cost"] + motion[count][2], current_id)
            node_id = calc_grid_index(item, minimum_x, minimum_y, width)
            if not verify_node(minimum_x, minimum_y, maximum_x, maximum_y, item, mask):
                continue
            if node_id in end_set:
                continue
            if node_id not in start_set:
                start_set[node_id] = item
            elif start_set[node_id]["cost"] > item["cost"]:
                start_set[node_id] = item
            else:
                continue
    route_x, route_y = calc_final_path(end, end_set, minimum_x, minimum_y)
    return route_x, route_y


# Rename!
def node(x, y, cost, index):
    return {"x": x, "y": y, "cost": cost, "index": index}


# Rename!
def calc_xy_index(coord, min_coord):
    return round(coord - min_coord)


# Rename!
def calc_grid_index(current, minimum_x, minimum_y, x):
    current = (current["x"] - minimum_x) + (x * (current["y"] - minimum_y))
    return current


# Rename!
def calc_heuristic(a, b):
    opposite = a["x"] - b["x"]
    adjacent = a["y"] - b["y"]
    return math.hypot(opposite, adjacent)


# Rename!
def verify_node(minimum_x, minimum_y, maximum_x, maximum_y, current, mask):
    cx = grid_pos(current["x"], minimum_x)
    cy = grid_pos(current["y"], minimum_y)
    if cx >= maximum_x or cx < minimum_x or cy >= maximum_y or cy < minimum_y:
        return False
    if mask[current["x"]][current["y"]]:
        return False
    return True


# Rename and check logic!
def calc_final_path(end, closed, minimum_x, minimum_y):
    final_x = [grid_pos(end["x"], minimum_x)]
    final_y = [grid_pos(end["y"], minimum_y)]
    index = end["index"]
    while index != -1:
        temp = closed[index]
        final_x.append(grid_pos(temp["x"], minimum_x))
        final_y.append(grid_pos(temp["y"], minimum_y))
        index = temp["index"]
    return final_x, final_y
