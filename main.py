import numpy as np
import cv2

from environment import ParkingLot, Agent, Cars, Walls
from pathing import parallel_park, manoeuvre, pathing, path_interpolation
from agent_movement import AgentMovement
from agent_control import MPC


def get_start_vars(lower, upper, prompt):
    value = int
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a valid input.")
            continue
        if lower <= value <= upper:
            break
        else:
            print("Please enter a valid input.")
    return value


def main(test_spot, selection):
    if selection == 1:
        x = get_start_vars(5, 30, "Starting X co-ordinate:\nPlease enter a number from 5 to 30\n")
        y = get_start_vars(5, 30, "Starting Y co-ordinate:\nPlease enter a number from 5 to 30\n")
        parking_spot = get_start_vars(1, 20, "Desired parking spot:\nPlease enter a number from 1 to 20\n")
    else:
        x = 15
        y = 15
        parking_spot = test_spot
    angle = 90
    agent = Agent()
    car = Cars()
    end, cars = car.generate_cars(parking_spot)
    wall = Walls()
    parkinglot = ParkingLot(cars, wall.get_walls())
    parkinglot.generate_obstacles()

    mask, minimum_x, maximum_x, minimum_y, maximum_y, width = parallel_park(parkinglot.obstacles)
    parking_manoeuvre, a_path, b_path, new_end = manoeuvre(x, y, end[0], end[1], mask, minimum_x, maximum_x, minimum_y,
                                                           maximum_y, width, parking_spot)
    mask, minimum_x, maximum_x, minimum_y, maximum_y, width = parallel_park(parkinglot.obstacles)
    path = pathing(new_end, x, y, mask, minimum_x, maximum_x, minimum_y, maximum_y, width)

    interpolated_pathing = path_interpolation(path, 10)
    interpolated_parking = path_interpolation(parking_manoeuvre, 1)
    interpolated_parking = np.vstack([a_path, interpolated_parking, b_path])

    if 5 < parking_spot < 9 or 15 < parking_spot < 19:
        last_element = len(interpolated_pathing) - 10
        interpolated_pathing = interpolated_pathing[:last_element]
    if parking_spot in [9, 10, 19, 20]:
        last_element = len(interpolated_pathing) - 20
        interpolated_pathing = interpolated_pathing[:last_element]

    parkinglot.path(interpolated_pathing)
    parkinglot.path(interpolated_parking)
    r = parkinglot.render_frame(agent, x, y, angle, 0)
    cv2.imshow("Parallel Parking", r)
    cv2.waitKey(1)

    agent_path = np.vstack([interpolated_pathing, interpolated_parking])
    agent_car = AgentMovement(x, y, 0, np.deg2rad(angle))
    agent_controller = MPC()

    for count, coordinate in enumerate(agent_path):
        vel, steer_angle = agent_controller.optimisation(agent_car, agent_path[count:count+5])
        agent_car.update_agent(agent_car.drive(vel, steer_angle))
        agent_car.x = agent_car.x + 1
        agent_car.y = agent_car.y + 1
        r = parkinglot.render_frame(agent, agent_car.x, agent_car.y, np.rad2deg(agent_car.angle),
                                    np.rad2deg(steer_angle))
        cv2.imshow("Parallel Parking", r)
        cv2.waitKey(1)

    r = parkinglot.render_frame(agent, agent_car.x, agent_car.y, 90, 0)
    cv2.imshow("Parallel Parking", r)
    cv2.waitKey(1)


def tester(selection):
    if selection == 2:
        parking_spots = [1, 5, 6, 10]
    else:
        parking_spots = []
        for count in range(1, 21):
            parking_spots.append(count)
    for count in range(0, len(parking_spots)):
        print("Parking spot", parking_spots[count], "!\n")
        main(parking_spots[count], 2)


def start():
    selection = get_start_vars(1, 3, "1) Run normal\n2) Run short test\n3) Run long test\n")
    if selection == 1:
        main(0, 1)
    elif selection == 2:
        tester(2)
    else:
        tester(3)


if __name__ == "__main__":
    start()
