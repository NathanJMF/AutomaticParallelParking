from copy import copy
import numpy as np
import scipy.optimize


class MPC:
    def __init__(self):
        self.horizon = None
        self.input_cost = np.diag([0.01, 0.01])
        self.delta_cost = np.diag([0.01, 1.0])
        self.state_cost = np.diag([1.0, 1.0])
        self.matrix = self.state_cost

    def controller(self, new_horizon, agent, path):
        agent_cost = 0
        agent = copy(agent)
        new_horizon = new_horizon.reshape(self.horizon, 2).T
        path = path.T
        for count in range(self.horizon):
            agent.update_agent(agent.drive(new_horizon[0, count], new_horizon[1, count]))
            coordinate = np.zeros((2, self.horizon + 1))
            coordinate[:, count] = [agent.x, agent.y]
            agent_cost = agent_cost + np.sum(self.input_cost @ (new_horizon[:, count] ** 2)) + \
                np.sum(self.state_cost @ ((path[:, count] - coordinate[:, count]) ** 2))
            if count < self.horizon - 1:
                agent_cost = agent_cost + np.sum(self.delta_cost @ ((new_horizon[:, count + 1] -
                                                                     new_horizon[:, count]) ** 2))
        return agent_cost

    def optimisation(self, agent, path):
        self.horizon = path.shape[0]
        agent_state = scipy.optimize.minimize(self.controller, args=(agent, path), x0=np.zeros(2 * self.horizon),
                                              method="SLSQP",
                                              bounds=[(-5, 5), (np.deg2rad(-60), np.deg2rad(60))] * self.horizon)
        return agent_state.x[0], agent_state.x[1]
