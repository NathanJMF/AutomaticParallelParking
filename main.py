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


def main():
    print("Start!")
    x = get_start_vars(5, 30, "Starting X co-ordinate:\nPlease enter a number from 5 to 30\n")
    y = get_start_vars(5, 30, "Starting Y co-ordinate:\nPlease enter a number from 5 to 30\n")
    parking_spot = get_start_vars(1, 20, "Desired parking spot:\nPlease enter a number from 1 to 20\n")

    angle = 90
    agent = Agent()
    car = Cars()
    end, cars = car.generate_cars(parking_spot)
    wall = Walls()
    parkinglot = ParkingLot(cars, wall.get_walls())
    parkinglot.generate_obstacles()
    # r = parkinglot.render_frame(agent, x, y, angle, 0)

    mask, minimum_x, maximum_x, minimum_y, maximum_y, width = parallel_park(parkinglot.obstacles)
    parking_manoeuvre, a_path, b_path, new_end = manoeuvre(x, y, end[0], end[1], mask, minimum_x, maximum_x, minimum_y,
                                                           maximum_y, width, parking_spot)
    mask, minimum_x, maximum_x, minimum_y, maximum_y, width = parallel_park(parkinglot.obstacles)
    path = pathing(new_end, x, y, mask, minimum_x, maximum_x, minimum_y, maximum_y, width)
    # path = np.vstack([path, a_path])

    interpolated_pathing = path_interpolation(path, 10)
    interpolated_parking = path_interpolation(parking_manoeuvre, 1)
    interpolated_parking = np.vstack([a_path, interpolated_parking, b_path])

    parkinglot.path(interpolated_pathing)
    parkinglot.path(interpolated_parking)
    r = parkinglot.render_frame(agent, x, y, angle, 0)
    cv2.imshow("test", r)
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
        cv2.imshow("test", r)
        cv2.waitKey(1)

    r = parkinglot.render_frame(agent, agent_car.x, agent_car.y, 90, 0)
    cv2.imshow("test", r)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
