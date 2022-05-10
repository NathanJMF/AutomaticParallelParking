# Automatic Parallel Parking using A* algorithm
This program will allow an agent to drive to and parallel park into the users desired parking space.

The project makes use of 3 major libraries:
### 1. Numpy
   - Numpy arrays were used to store the aspects of the environment for the project. Such as obstacles and agent characteristics.
### 2. OpenCV
   - OpenCV was used in drawing the 2D environment. 
### 3. Scipy
   - Scipy had three uses in this project. First being to rotate any contours in the environment, such as the agent or its wheels.
   - Second is to interpolate the generated paths allowing for a higher resolution and smoother path for the agent to drive.
   - Lastly Scipy was used to optimise the agent's MPC controller allowing for a better performing system.

In the future I would like to try and implement a machine learning approach to achieve the same goal and compare performance between the two.

## Running the project

1. Make sure you have pipenv. This can be done by using the command `pip freeze` in a terminal window. If you already have it then continue. If not then run the command below to install it.
   - `pip install pipenv`
2. You will need to CD to the project directory in a terminal window.
3. When you are in the directory run the following commands:
   1. Open the virtual environment `pipenv shell`
   2. Install the project dependencies `pipenv sync`
4. You can now run the program with `python main.py`

After the program is up and running the user it prompted to choose between three options by entering the number 1, 2 or 3.

Option 1 will allow the user to run the program as intended by specifying their own start co-ordinates and desired parking spot.

Option 2 will run a short test where the program will run through parking in 4 predetermined parking spots.

Option 3 will run a long test where the program will run through all parking spots in the environment.

