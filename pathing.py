import numpy as np
import math
import scipy.interpolate

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
    return np.vstack([new_x, new_y]).T[::-1]


def parallel_park(obstacles):
    obstacles_x = []
    obstacles_y = []
    margin = 1

    objects = np.concatenate([np.array([[0, i] for i in range(100 + margin)]),
                              np.array([[100 + 2 * margin, i] for i in range(100 + 2 * margin)]),
                              np.array([[i, 0] for i in range(100 + margin)]),
                              np.array([[i, 100 + 2 * margin] for i in range(100 + 2 * margin)]),
                              (obstacles + np.array([margin, margin]))])

    for item in objects:
        obstacles_x.append(int(item[0]))
        obstacles_y.append(int(item[1]))

    mask, minimum_x, maximum_x, minimum_y, maximum_y, width = obstacle_mask(obstacles_x, obstacles_y, 1, 4)
    return mask, minimum_x, maximum_x, minimum_y, maximum_y, width


def manoeuvre(x_start, y_start, x_end, y_end, mask, minimum_x, maximum_x, minimum_y, maximum_y, width, parking_spot):
    new_x, new_y = pathing_helper(x_start + 1, y_start + 1, x_end + 1, y_end + 1, mask, minimum_x, maximum_x, minimum_y,
                                  maximum_y, width)
    new_x = np.array(new_x) - 0.5
    new_y = np.array(new_y) - 0.5

    parking_manoeuvre = np.flip(np.vstack([new_x, new_y]).T)

    if 1 <= parking_spot <= 5 or 11 <= parking_spot <= 15:
        line_angle = angle_calc(parking_manoeuvre[-5][0], parking_manoeuvre[-5][1], parking_manoeuvre[-1][0],
                                parking_manoeuvre[-1][1])
    else:
        line_angle = angle_calc(parking_manoeuvre[-1][0], parking_manoeuvre[-1][1], parking_manoeuvre[-1][0],
                                parking_manoeuvre[-1][1])

    if -math.atan2(0, -1) < line_angle <= math.atan2(-1, 0) or math.atan2(1, 0) < line_angle <= math.atan2(0, -1):
        parking_manoeuvre, a_path, b_path, ax, ay = manoeuvre_left(x_end, y_end)
    else:
        parking_manoeuvre, a_path, b_path, ax, ay = manoeuvre_right(x_end, y_end)
    return parking_manoeuvre, a_path, b_path, np.array([ax, ay])


def manoeuvre_left(x_end, y_end):
    ax = x_end + 6
    ay = y_end - 12
    a_path = np.vstack([np.repeat(ax, 3 / 0.25), np.flip(np.arange(ay - 3, ay, 0.25))]).T
    b_path = np.vstack([np.repeat(x_end, 3 / 0.25), np.flip(np.arange(y_end, y_end + 3, 0.25))]).T
    parking_manoeuvre = park(x_end, y_end, 1)
    return parking_manoeuvre, a_path, b_path, ax, ay


def manoeuvre_right(x_end, y_end):
    ax = x_end - 6
    ay = y_end - 12
    a_path = np.vstack([np.repeat(ax, 3 / 0.25), np.flip(np.arange(ay - 3, ay, 0.25))]).T
    b_path = np.vstack([np.repeat(x_end, 3 / 0.25), np.flip(np.arange(y_end, y_end + 3, 0.25))]).T
    parking_manoeuvre = park(x_end, y_end, 2)
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
    else:
        ax = x_end - 6
        ay = y_end - 12
        y_temp = np.arange(ay, y_end + 1)
        circle = (6.9 ** 2 - (y_temp - ay) ** 2)
        x_temp = (np.sqrt(circle[circle >= 0]) + ax + 6.9)

    y_temp = y_temp[circle >= 0]

    if option == 1:
        choice = x_temp > ax - 6.9 / 2
        x_temp = x_temp[choice]
        y_temp = y_temp[choice]
        x_function = np.append(x_function, x_temp)
        y_function = np.append(y_function, y_temp)
        y_temp = np.arange(ay, y_end + 1)
    else:
        x_temp = (x_temp - 2 * (x_temp - (ax + 6.9)))
        choice = x_temp < ax + 6.9 / 2
        x_temp = x_temp[choice]
        y_temp = y_temp[choice]
        x_function = np.append(x_function, x_temp)
        y_function = np.append(y_function, y_temp)
        y_temp = np.arange(ay, y_end + 1)

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
    x_function = np.append(x_function, x_temp)
    y_function = np.append(y_function, y_temp)
    parking_manoeuvre = np.vstack([x_function, y_function]).T

    return parking_manoeuvre


def pathing_helper(x_start, y_start, x_end, y_end, mask, minimum_x, maximum_x, minimum_y, maximum_y, width):
    # This is the A* search algorithm.
    start_dict = dict()
    end_dict = dict()
    # Manipulates the passed in data into a dictionary for ease of calculation.
    # Does this for both starting and ending co-ordinates.
    start = get_node_dict(coord_index_calc(x_start, minimum_x), coord_index_calc(y_start, minimum_y), 0.0, -1)
    end = get_node_dict(coord_index_calc(x_end, minimum_x), coord_index_calc(y_end, minimum_y), 0.0, -1)
    # Populates the start_dict by calling grid_calc and placing the start dictionary inside it.
    start_dict[grid_calc(start, minimum_x, minimum_y, width)] = start
    # Runs until start_dict is empty.
    while True:
        # Check if start_dict is empty. If it is then the loop is exited.
        if not bool(start_dict):
            break
        # Places the current lowest cost + distance from the end point in current_id
        current_id = min(start_dict, key=lambda o: start_dict[o]["cost"] + hypotenuse_calc(end, start_dict[o]))
        # Finds the full item in start_dict and places it into current_node.
        current_node = start_dict[current_id]
        # This checks if the current node that is being looked at is the same as the goal node.
        # If it is, cost and index are then updated and the loop is left.
        if current_node["x"] == end["x"] and current_node["y"] == end["y"]:
            end["cost"] = current_node["cost"]
            end["index"] = current_node["index"]
            break
        # Removes the current item from the start_dict.
        del start_dict[current_id]
        # The current item is then added to the end_dict.
        end_dict[current_id] = current_node
        # This loop uses the motion global variable to look at the next move the agent is able to perform.
        # Using the available agent motions, the search is expanded.
        for count in range(len(motion)):
            item = get_node_dict(current_node["x"] + motion[count][0], current_node["y"] + motion[count][1],
                                 current_node["cost"] + motion[count][2], current_id)
            node_id = grid_calc(item, minimum_x, minimum_y, width)
            # Continue if the node is not of a valid move.
            if not node_verification(minimum_x, minimum_y, maximum_x, maximum_y, item, mask):
                continue
            # Continue if the node already exists in end_dict.
            if node_id in end_dict:
                continue
            # Checks to see if the node exists yet.
            # If it is a new node it is placed into the start_dict.
            if node_id not in start_dict:
                start_dict[node_id] = item
            # Checks if the new item cost is lower than the current node cost.
            # If it is then, current node is replaced by the new item.
            elif start_dict[node_id]["cost"] > item["cost"]:
                start_dict[node_id] = item
            else:
                continue
    # Returns two lists, holding the X and Y co-ordinates of the path found.
    route_x, route_y = path_calc(end, end_dict, minimum_x, minimum_y)
    return route_x, route_y


def grid_pos_calc(index, pos):
    return index + pos


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

    for temp_x in range(x):
        xa = grid_pos_calc(temp_x, minimum_x)
        for temp_y in range(y):
            ya = grid_pos_calc(temp_y, minimum_y)
            for xb, yb in zip(obstacles_x, obstacles_y):
                if hypotenuse_calc({"x": xb, "y": yb}, {"x": xa, "y": ya}) < agent_radius:
                    mask[temp_x][temp_y] = True
                    break
    return mask, minimum_x, maximum_x, minimum_y, maximum_y, x


def get_node_dict(x, y, cost, index):
    return {"x": x, "y": y, "cost": cost, "index": index}


def coord_index_calc(coord, min_coord):
    return round(coord - min_coord)


def grid_calc(current, minimum_x, minimum_y, x):
    current = (current["x"] - minimum_x) + (x * (current["y"] - minimum_y))
    return current


def hypotenuse_calc(a, b):
    opposite = a["x"] - b["x"]
    adjacent = a["y"] - b["y"]
    return math.hypot(opposite, adjacent)


def node_verification(minimum_x, minimum_y, maximum_x, maximum_y, current, mask):
    current_x = grid_pos_calc(current["x"], minimum_x)
    current_y = grid_pos_calc(current["y"], minimum_y)
    if current_x >= maximum_x or current_x < minimum_x or current_y >= maximum_y or current_y < minimum_y:
        return False
    if mask[current["x"]][current["y"]]:
        return False
    return True


def path_calc(end, closed, minimum_x, minimum_y):
    final_x = [grid_pos_calc(end["x"], minimum_x)]
    final_y = [grid_pos_calc(end["y"], minimum_y)]
    index = end["index"]
    while index != -1:
        temp = closed[index]
        final_x.append(grid_pos_calc(temp["x"], minimum_x))
        final_y.append(grid_pos_calc(temp["y"], minimum_y))
        index = temp["index"]
    return final_x, final_y


def angle_calc(ax, ay, bx, by):
    angle = math.atan2(by - ay, bx - ax)
    return angle


def path_interpolation(path, rate):
    path_length = len(path)
    current = np.arange(0, path_length, rate)
    if path_length - 1 not in current:
        current = np.append(current, path_length - 1)
    x = path[current, 0]
    y = path[current, 1]

    interpolated_x = scipy.interpolate.make_interp_spline(np.linspace(0.0, len(x) - 1, len(x)), x, k=3)
    interpolated_y = scipy.interpolate.make_interp_spline(np.linspace(0.0, len(x) - 1, len(x)), y, k=3)

    final_x = interpolated_x(np.linspace(0.0, len(x) - 1, len(path) * 3))
    final_y = interpolated_y(np.linspace(0.0, len(x) - 1, len(path) * 3))
    return np.vstack([final_x, final_y]).T
