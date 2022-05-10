import numpy as np
import cv2

from environment import ParkingLot, Agent, Cars, Walls
from pathing import parallel_park, manoeuvre, pathing, path_interpolation
from agent_movement import AgentMovement
from agent_control import MPC


def get_start_vars(lower, upper, prompt):
    # Will prompt the user for a value and ensure it is in a given range.
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
    # Initialising angle and objects.
    angle = 90
    agent = Agent()
    car = Cars()
    wall = Walls()
    # Sets the starting x and y co-ordinates for the agent and the desired parking spot.
    if selection == 1:
        x = get_start_vars(5, 30, "Starting X co-ordinate:\nPlease enter a number from 5 to 30\n")
        y = get_start_vars(5, 30, "Starting Y co-ordinate:\nPlease enter a number from 5 to 30\n")
        parking_spot = get_start_vars(1, 20, "Desired parking spot:\nPlease enter a number from 1 to 20\n")
    else:
        x = 15
        y = 15
        parking_spot = test_spot
    # Gets the agents end co-ordinates and pops the car from the list of cars obstacles.
    end, cars = car.generate_cars(parking_spot)
    # Initialises the parkinglot environment and places the obstacles.
    parkinglot = ParkingLot(cars, wall.get_walls())
    parkinglot.generate_obstacles()
    # Generates the obstacle mask.
    mask, minimum_x, maximum_x, minimum_y, maximum_y, width = parallel_park(parkinglot.obstacles)
    # Obstacle mask is then used to generate the path and parking manoeuvre.
    parking_manoeuvre, a_path, b_path, new_end = manoeuvre(x, y, end[0], end[1], mask, minimum_x, maximum_x, minimum_y,
                                                           maximum_y, width, parking_spot)
    path = pathing(new_end, x, y, mask, minimum_x, maximum_x, minimum_y, maximum_y, width)
    # Interpolates the generated paths.
    interpolated_pathing = path_interpolation(path, 10)
    interpolated_parking = path_interpolation(parking_manoeuvre, 1)
    interpolated_parking = np.vstack([a_path, interpolated_parking, b_path])
    # Cleans up the ends of the paths for certain parking scenarios.
    if 5 < parking_spot < 9 or 15 < parking_spot < 19:
        last_element = len(interpolated_pathing) - 10
        interpolated_pathing = interpolated_pathing[:last_element]
    if parking_spot in [9, 10, 19, 20, 5, 15]:
        last_element = len(interpolated_pathing) - 20
        interpolated_pathing = interpolated_pathing[:last_element]
    # Draws the paths in the parkinglot environment.
    parkinglot.path(interpolated_pathing)
    parkinglot.path(interpolated_parking)
    # Renders a window with the starting state of the current run.
    r = parkinglot.render_frame(agent, x, y, angle, 0)
    cv2.imshow("Parallel Parking", r)
    cv2.waitKey(1)
    # Puts together the generated paths for the agent to drive along.
    agent_path = np.vstack([interpolated_pathing, interpolated_parking])
    # Initialises the agent MPC controller and movement.
    agent_car = AgentMovement(x, y, 0, np.deg2rad(angle))
    agent_controller = MPC()
    # This loop is responsible for iterating through the co-ordinates of the path and driving the agent along it.
    for count, coordinate in enumerate(agent_path):
        vel, steer_angle = agent_controller.optimisation(agent_car, agent_path[count:count+5])
        agent_car.update_agent(agent_car.drive(vel, steer_angle))
        # Adding 1 to both the x and y co-ordinates of the agent fixes an issue where the agent was off path slightly.
        agent_car.x = agent_car.x + 1
        agent_car.y = agent_car.y + 1
        # Renders the new frame and displays it to the user.
        r = parkinglot.render_frame(agent, agent_car.x, agent_car.y, np.rad2deg(agent_car.angle),
                                    np.rad2deg(steer_angle))
        cv2.imshow("Parallel Parking", r)
        cv2.waitKey(1)
    # Lines the agent and its wheels up at the end of the parking manoeuvre.
    r = parkinglot.render_frame(agent, agent_car.x, agent_car.y, 90, 0)
    cv2.imshow("Parallel Parking", r)
    cv2.waitKey(1)


def tester(selection):
    # Will run either a short or long test depending on user selection.
    # Tests all parking spots or a small list of important parking scenarios.
    if selection == 2:
        parking_spots = [1, 5, 6, 10]
    else:
        parking_spots = []
        for count in range(1, 21):
            parking_spots.append(count)
    for count in range(0, len(parking_spots)):
        print("Testing parking spot", str(parking_spots[count]) + "!")
        main(parking_spots[count], 2)


def start():
    # Asks the user how they'd like the program to run.
    selection = get_start_vars(1, 3, "1) Run normal\n2) Run short test  (4 parking scenarios)\n"
                                     "3) Run long test (All parking scenarios)\n")
    if selection == 1:
        main(0, 1)
    elif selection == 2:
        tester(2)
    else:
        tester(3)


if __name__ == "__main__":
    start()
