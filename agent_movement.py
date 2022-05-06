import numpy as np


class AgentMovement:
    def __init__(self, x, y, velocity, angle):
        self.clock = 0.2
        self.agent_length = 4
        self.x = x
        self.y = y
        self.velocity = velocity
        self.angle = angle
        self.current = np.array([[self.x, self.y, self.velocity, self.angle]]).T

    def update_agent(self, update):
        self.current = self.current + self.clock * update
        self.x = self.current[0, 0]
        self.y = self.current[1, 0]
        self.velocity = self.current[2, 0]
        self.angle = self.current[3, 0]

    def drive(self, velocity, angle_diff):
        return np.array([[self.velocity*np.cos(self.angle), self.velocity*np.sin(self.angle), velocity,
                          self.velocity*np.tan(angle_diff)/self.agent_length]]).T
