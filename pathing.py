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


def pathing(new_end, x_start, y_start, mask, minimum_x, maximum_x, minimum_y, maximum_y, width):
    x_end = new_end[0]
    y_end = new_end[1]
    new_x, new_y = pathing_helper(x_start + 1, y_start + 1, x_end + 1, y_end + 1, mask, minimum_x, maximum_x, minimum_y,
                                  maximum_y, width)
    new_x = np.array(new_x) - 0.5
    new_y = np.array(new_y) - 0.5
    path = np.vstack([new_x, new_y]).T
    # path = np.flip(np.vstack([new_x, new_y])).T
    return path[::-1]


def parallel_park(obstacles):
    margin = 1
    obstacles = obstacles + np.array([margin, margin])
    obstacles = obstacles[(obstacles[:, 0] >= 0) & (obstacles[:, 1] >= 0)]
    # Fills walls?
    objects = np.concatenate([np.array([[0, i] for i in range(100 + margin)]),
                              np.array([[100 + 2 * margin, i] for i in range(100 + 2 * margin)]),
                              np.array([[i, 0] for i in range(100 + margin)]),
                              np.array([[i, 100 + 2 * margin] for i in range(100 + 2 * margin)]),
                              obstacles])
    # obstacles_x = np.empty(0, dtype=int)
    # obstacles_y = np.empty(0, dtype=int)
    # for item in obstacles:
    #     obstacles_x = np.append(obstacles_x, item[:, 0])
    #     obstacles_y = np.append(obstacles_y, item[:, 1])
    obstacles_x = [int(item) for item in objects[:, 0]]
    obstacles_y = [int(item) for item in objects[:, 1]]
    mask, minimum_x, maximum_x, minimum_y, maximum_y, width = obstacle_mask(obstacles_x, obstacles_y, 1, 4)
    return mask, minimum_x, maximum_x, minimum_y, maximum_y, width


def manoeuvre(x_start, y_start, x_end, y_end, mask, minimum_x, maximum_x, minimum_y, maximum_y, width, parking_spot):
    new_x, new_y = pathing_helper(x_start + 5, y_start + 5, x_end + 5, y_end + 5, mask, minimum_x, maximum_x, minimum_y,
                                  maximum_y, width)
    new_x = np.array(new_x) + 4.5
    new_y = np.array(new_y) + 4.5
    parking_manoeuvre = np.vstack([new_x, new_y]).T
    parking_manoeuvre = np.flip(parking_manoeuvre)
    # parking_manoeuvre = parking_manoeuvre[::-1]

    if 1 <= parking_spot <= 5 or 11 <= parking_spot <= 15:
        line_angle = calc_line_ang(parking_manoeuvre[-5][0], parking_manoeuvre[-5][1], parking_manoeuvre[-1][0],
                                   parking_manoeuvre[-1][1])
    else:
        line_angle = calc_line_ang(parking_manoeuvre[-1][0], parking_manoeuvre[-1][1], parking_manoeuvre[-1][0],
                                   parking_manoeuvre[-1][1])
    if -math.atan2(0, -1) < line_angle <= math.atan2(-1, 0):
        parking_manoeuvre, a_path, b_path, ax, ay = manoeuvre_back_right(x_end, y_end)
    elif math.atan2(-1, 0) <= line_angle <= math.atan2(0, 1):
        parking_manoeuvre, a_path, b_path, ax, ay = manoeuvre_back_left(x_end, y_end)
    elif math.atan2(0, 1) < line_angle <= math.atan2(1, 0):
        parking_manoeuvre, a_path, b_path, ax, ay = manoeuvre_forward_left(x_end, y_end)
    else:
        parking_manoeuvre, a_path, b_path, ax, ay = manoeuvre_forward_right(x_end, y_end)
    return parking_manoeuvre, a_path, b_path, np.array([ax, ay])


def manoeuvre_back_right(x_end, y_end):
    print("back right")
    ax = x_end + 6
    ay = y_end - 12
    a_path = np.vstack([np.repeat(ax, 3 / 0.25), np.flip(np.arange(ay - 3, ay, 0.25))]).T
    b_path = np.vstack([np.repeat(x_end, 3 / 0.25), np.flip(np.arange(y_end - 3, y_end, 0.25))]).T
    parking_manoeuvre = park(x_end, y_end, 1)
    return parking_manoeuvre, a_path, b_path, ax, ay


def manoeuvre_back_left(x_end, y_end):
    print("back left")
    ax = x_end - 6
    ay = y_end - 12
    a_path = np.vstack([np.repeat(ax, 3 / 0.25), np.flip(np.arange(ay - 3, ay, 0.25))]).T
    b_path = np.vstack([np.repeat(x_end, 3 / 0.25), np.flip(np.arange(y_end - 3, y_end, 0.25))]).T
    parking_manoeuvre = park(x_end, y_end, 2)
    return parking_manoeuvre, a_path, b_path, ax, ay


def manoeuvre_forward_left(x_end, y_end):
    print("forward left")
    ax = x_end - 6
    ay = y_end + 12
    a_path = np.vstack([np.repeat(ax, 3 / 0.25), np.arange(ay, ay + 3, 0.25)]).T
    b_path = np.vstack([np.repeat(x_end, 3 / 0.25), np.arange(y_end - 3, y_end, 0.25)]).T
    parking_manoeuvre = park(x_end, y_end, 3)
    return parking_manoeuvre, a_path, b_path, ax, ay


def manoeuvre_forward_right(x_end, y_end):
    print("forward right")
    ax = x_end + 6
    ay = y_end + 12
    a_path = np.vstack([np.repeat(ax, 3 / 0.25), np.arange(ay, ay + 3, 0.25)]).T
    b_path = np.vstack([np.repeat(x_end, 3 / 0.25), np.arange(y_end - 3, y_end, 0.25)]).T
    parking_manoeuvre = park(x_end, y_end, 4)
    return parking_manoeuvre, a_path, b_path, ax, ay


def park(x_end, y_end, option):
    x_function = np.array([])
    y_function = np.array([])
    if option == 1:
        ax = x_end + 6
        ay = y_end - 12
        y_temp = np.arange(ay, y_end + 1)
        circle = (6.9 ** 2 - (y_temp - ay) ** 2)
        x_temp = (np.sqrt(circle[circle >= 0]) + ax - 6.9)
    elif option == 2:
        ax = x_end - 6
        ay = y_end - 12
        y_temp = np.arange(ay, y_end + 1)
        circle = (6.9 ** 2 - (y_temp - ay) ** 2)
        x_temp = (np.sqrt(circle[circle >= 0]) + ax + 6.9)
    elif option == 3:
        ax = x_end - 6
        ay = y_end + 12
        y_temp = np.arange(y_end, ay + 1)
        circle = (6.9 ** 2 - (y_temp - ay) ** 2)
        x_temp = (np.sqrt(circle[circle >= 0]) + ax + 6.9)
    else:
        ax = x_end + 6
        ay = y_end + 12
        y_temp = np.arange(y_end, ay + 1)
        circle = (6.9 ** 2 - (y_temp - ay) ** 2)
        x_temp = (np.sqrt(circle[circle >= 0]) + ax - 6.9)

    y_temp = y_temp[circle >= 0]

    if option == 1:
        choice = x_temp > ax - 6.9 / 2
        x_temp = x_temp[choice]
        y_temp = y_temp[choice]
        x_function = np.append(x_function, x_temp)
        y_function = np.append(y_function, y_temp)
        y_temp = np.arange(ay, y_end + 1)
    elif option == 2:
        x_temp = (x_temp - 2 * (x_temp - (ax + 6.9)))
        choice = x_temp < ax + 6.9 / 2
        x_temp = x_temp[choice]
        y_temp = y_temp[choice]
        x_function = np.append(x_function, x_temp)
        y_function = np.append(y_function, y_temp)
        y_temp = np.arange(ay, y_end + 1)
    elif option == 3:
        x_temp = (x_temp - 2 * (x_temp - (ax + 6.9)))
        choice = x_temp < ax + 6.9 / 2
        x_temp = x_temp[choice]
        y_temp = y_temp[choice]
        x_function = np.append(x_function, x_temp[::-1])
        y_function = np.append(y_function, y_temp[::-1])
        y_temp = np.arange(y_end, ay + 1)
    else:
        choice = x_temp > ax - 6.9 / 2
        x_temp = x_temp[choice]
        y_temp = y_temp[choice]
        x_function = np.append(x_function, x_temp[::-1])
        y_function = np.append(y_function, y_temp[::-1])
        y_temp = np.arange(y_end, ay + 1)

    circle = (6.9 ** 2 - (y_temp - y_end) ** 2)

    if option == 1 or option == 4:
        x_temp = (np.sqrt(circle[circle >= 0]) + x_end + 6.9)
        x_temp = (x_temp - 2 * (x_temp - (x_end + 6.9)))
        y_temp = y_temp[circle >= 0]
        choice = x_temp < x_end + 6.9 / 2
    else:
        x_temp = (np.sqrt(circle[circle >= 0]) + x_end - 6.9)
        y_temp = y_temp[circle >= 0]
        choice = x_temp > x_end - 6.9 / 2

    x_temp = x_temp[choice]
    y_temp = y_temp[choice]

    if option == 1 or option == 2:
        x_function = np.append(x_function, x_temp)
        y_function = np.append(y_function, y_temp)
    else:
        x_function = np.append(x_function, x_temp[::-1])
        y_function = np.append(y_function, y_temp[::-1])
    parking_manoeuvre = np.vstack([x_function, y_function]).T
    return parking_manoeuvre


def pathing_helper(x_start, y_start, x_end, y_end, mask, minimum_x, maximum_x, minimum_y, maximum_y, width):
    start_set = dict()
    end_set = dict()
    start = node(calc_xy_index(x_start, minimum_x), calc_xy_index(y_start, minimum_y), 0.0, -1)
    end = node(calc_xy_index(x_end, minimum_x), calc_xy_index(y_end, minimum_y), 0.0, -1)
    start_set[calc_grid_index(start, minimum_x, minimum_y, width)] = start
    while True:
        if not bool(start_set):
            print("Empty starting set")
            break
        current_id = min(start_set, key=lambda o: start_set[o]["cost"] + calc_heuristic(end, start_set[o]))
        current_node = start_set[current_id]
        if current_node["x"] == end["x"] and current_node["y"] == end["y"]:
            end["cost"] = current_node["cost"]
            end["index"] = current_node["index"]
            break
        del start_set[current_id]
        end_set[current_id] = current_node
        for count in range(len(motion)):
            item = node(current_node["x"] + motion[count][0], current_node["y"] + motion[count][1],
                        current_node["cost"] + motion[count][2], current_id)
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


def grid_pos(index, pos):
    return index + pos


#     return index * resolution + pos


def obstacle_mask(obstacles_x, obstacles_y, resolution, agent_radius):
    minimum_x = round(min(obstacles_x))
    maximum_x = round(max(obstacles_x))
    minimum_y = round(min(obstacles_y))
    maximum_y = round(max(obstacles_y))
    mask = []
    x = round((maximum_x - minimum_x) / resolution)
    y = round((maximum_y - minimum_y) / resolution)

    for count in range(x):
        mask.append([])
        for count2 in range(y):
            mask[count].append(False)
    # mask = [[False for count in range(y)] for count in range(x)]
    for temp_x in range(x):
        xa = grid_pos(temp_x, minimum_x)
        for temp_y in range(y):
            ya = grid_pos(temp_y, minimum_y)
            for xb, yb in zip(obstacles_x, obstacles_y):
                if math.hypot(xb - xa, yb - ya) < agent_radius:
                    mask[temp_x][temp_y] = True
                    break
    return mask, minimum_x, maximum_x, minimum_y, maximum_y, x


# Rename!
def node(x, y, cost, index):
    return {"x": x, "y": y, "cost": cost, "index": index}


# Rename!
def calc_xy_index(coord, min_coord):
    return round(coord - min_coord)


# Rename!
def calc_grid_index(current, minimum_x, minimum_y, x):
    # current = (current["x"] - minimum_x) + (x * (current["y"] - minimum_y))
    current = (current["y"] - minimum_y) * x + (current["x"] - minimum_x)
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


def calc_line_ang(ax, ay, bx, by):
    angle = math.atan2(by - ay, bx - ax)
    return angle
