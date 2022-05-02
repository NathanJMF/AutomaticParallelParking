import numpy as np
import cv2

from environment import ParkingLot, Agent, Cars, Walls
from pathing import parallel_park, manoeuvre, pathing


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


def main():
    print("Start!")
    x = get_start_vars(0, 100, "Starting X co-ordinate:\nPlease enter a number from 0 and 100\n")
    y = get_start_vars(0, 100, "Starting Y co-ordinate:\nPlease enter a number from 0 and 100\n")
    angle = get_start_vars(0, 360, "Starting angle:\nPlease enter a number from 0 to 360\n")
    parking_spot = get_start_vars(1, 20, "Desired parking spot:\nPlease enter a number from 1 to 20\n")
    # Environment
    # start_pos = np.array([x, y])
    agent = Agent()
    car = Cars()
    end, cars = car.generate_cars(parking_spot)
    wall = Walls()
    parkinglot = ParkingLot(cars, wall.get_walls())
    parkinglot.generate_obstacles()
    r = parkinglot.render_frame(agent, x, y, angle, 45)
    # cv2.imshow("test", r)
    # cv2.waitKey(0)
    # Path planning

    # Generate obstacle mask
    mask, minimum_x, maximum_x, minimum_y, maximum_y, width = parallel_park(parkinglot.obstacles)

    parking_manoeuvre, a_path, b_path, new_end = manoeuvre(x, y, end[0], end[1], mask, minimum_x, maximum_x, minimum_y,
                                                           maximum_y, width)

    mask, minimum_x, maximum_x, minimum_y, maximum_y, width = parallel_park(parkinglot.obstacles)

    path = pathing(new_end, x, y, mask, minimum_x, maximum_x, minimum_y, maximum_y, width)
    path = np.vstack([path, a_path, b_path])
    parkinglot.path(path)
    parkinglot.path(parking_manoeuvre)
    r = parkinglot.render_frame(agent, x, y, angle, 45)
    cv2.imshow("test", r)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
