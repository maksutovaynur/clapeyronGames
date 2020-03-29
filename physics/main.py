import cv2
import numpy as np
import time


class Bacterium:
    def __init__(self, skeleton=None):
        if not skeleton:
            self.skeleton = {
                "anchors": [
                    {
                        "fixed": False
                    },
                    {
                        "fixed": True
                    },
                    {
                        "fixed": False
                    },
                    {
                        "fixed": True
                    }
                ]
            }


class Environment:
    def __init__(self, size=(800, 800), ppu=20):

        self.size = size
        self.ppu = ppu  # pixels per unit
        self.canvas = 255 * np.ones((self.size[0], self.size[1], 3), dtype='uint8')

        self.bact_body_color = (32, 200, 128)
        self.bact_core_color = (32, 255, 255)
        self.bact_membrane_color = (82, 250, 178)
        self.bact_body_color_fixed = (100, 100, 255)

        self.food_color = (128, 200, 255)

        self.state = {
            "bacteria": [],
            "food": []
        }

    def add_bacterium(self, bacterium=Bacterium(), position=None):

        self.state["bacteria"].append({"object": bacterium})

        if not position:
            self.state["bacteria"][-1]["core_position"] = (self.size[0] // 2, self.size[1] // 2)
        else:
            self.state["bacteria"][-1]["core_position"] = position

        self.state["bacteria"][-1]["core_velocity"] = (0, 0)
        self.state["bacteria"][-1]["anchor_velocity"] = [(0, 0) for anchor in
                                                         self.state["bacteria"][-1]["object"].skeleton["anchors"]]

        self.state["bacteria"][-1]["anchor_position"] = \
            [(np.random.randint(-int(self.ppu * 5), int(self.ppu * 5)) + self.size[0] // 2,
              np.random.randint(-int(self.ppu * 5), int(self.ppu * 5)) + self.size[1] // 2)
             for anchor in self.state["bacteria"][-1]["object"].skeleton["anchors"]]

    def add_food(self, position=None, amount=None):
        if not position:
            self.state["food"].append({"position": (np.random.randint(0, self.size[0]),
                                                    np.random.randint(0, self.size[1]))})
        else:
            self.state["food"][-1]["position"] = position

        if not amount:
            self.state["food"][-1]["amount"] = 0.5 * np.random.random_sample() + 0.5
        else:
            self.state["food"][-1]["amount"] = amount

    def update(self):

        new_state = self.state
        self.canvas = 255 * np.ones((self.size[0], self.size[1], 3), dtype='uint8')

        # render bacteria
        for bacterium in self.state["bacteria"]:

            core_position = (bacterium["core_position"][0], bacterium["core_position"][1])

            core_acceleration_x = 0
            core_acceleration_y = 0

            # update coordinates
            for i in range(len(bacterium["anchor_position"])):
                anchor_position = bacterium["anchor_position"][i]

                if i == len(bacterium["anchor_position"]) - 1:
                    anchor_position_next = bacterium["anchor_position"][0]
                else:
                    anchor_position_next = bacterium["anchor_position"][i + 1]

                if i == 0:
                    anchor_position_prev = bacterium["anchor_position"][len(bacterium["anchor_position"]) - 1]
                else:
                    anchor_position_prev = bacterium["anchor_position"][i - 1]

                core_force = (np.linalg.norm(np.array(core_position) - np.array(anchor_position)) - int(5 * self.ppu))
                core_angle = np.arctan2((core_position[1] - anchor_position[1]),
                                        (core_position[0] - anchor_position[0]))

                anchor_next_force = (np.linalg.norm(np.array(anchor_position_next) - np.array(anchor_position)) - int(10 * self.ppu))
                anchor_next_angle = np.arctan2((anchor_position_next[1] - anchor_position[1]),
                                        (anchor_position_next[0] - anchor_position[0]))

                anchor_prev_force = (np.linalg.norm(np.array(anchor_position_prev) - np.array(anchor_position)) - int(10 * self.ppu))
                anchor_prev_angle = np.arctan2((anchor_position_prev[1] - anchor_position[1]),
                                        (anchor_position_prev[0] - anchor_position[0]))

                acceleration_x = 0.1 * np.cos(core_angle) * core_force   + \
                 0.1 * np.cos(anchor_next_angle) * anchor_next_force  + \
                 0.1 * np.cos(anchor_prev_angle) * anchor_prev_force

                acceleration_y = 0.1 * np.sin(core_angle) * core_force   + \
                 0.1 * np.sin(anchor_next_angle) * anchor_next_force  + \
                 0.1 * np.sin(anchor_prev_angle) * anchor_prev_force

                core_acceleration_x -= 0.1 * np.cos(core_angle) * core_force
                core_acceleration_y -= 0.1 * np.sin(core_angle) * core_force

                if self.state["bacteria"][-1]["object"].skeleton["anchors"][i]["fixed"] == False :

                    coord_x = new_state["bacteria"][-1]["anchor_position"][i][0] + \
                              new_state["bacteria"][-1]["anchor_velocity"][i][0] + int(acceleration_x/2)

                    coord_y = new_state["bacteria"][-1]["anchor_position"][i][1] + \
                              new_state["bacteria"][-1]["anchor_velocity"][i][1] + int(acceleration_y/2)

                    new_state["bacteria"][-1]["anchor_velocity"][i] = (int(acceleration_x), int(acceleration_y))
                    new_state["bacteria"][-1]["anchor_position"][i] = (coord_x, coord_y)

                else:
                    new_state["bacteria"][-1]["anchor_velocity"][i] = (0, 0)

            core_coord_x = new_state["bacteria"][-1]["core_position"][0] + \
                           new_state["bacteria"][-1]["core_velocity"][0] + int(core_acceleration_x / 2)

            core_coord_y = new_state["bacteria"][-1]["core_position"][1] + \
                           new_state["bacteria"][-1]["core_velocity"][1] + int(core_acceleration_y / 2)

            new_state["bacteria"][-1]["core_velocity"] = (int(core_acceleration_x), int(core_acceleration_y))
            new_state["bacteria"][-1]["core_position"] = (core_coord_x, core_coord_y)

            self.state = new_state

            core_position = new_state["bacteria"][-1]["core_position"]

            # draw core
            self.canvas = cv2.circle(self.canvas,
                                     core_position,
                                     self.ppu, self.bact_body_color, -1)

            # draw anchors and tubes
            for i in range(len(bacterium["anchor_position"])):

                anchor_position = bacterium["anchor_position"][i]

                if i == len(bacterium["anchor_position"]) - 1:
                    anchor_position_next = bacterium["anchor_position"][0]
                else:
                    anchor_position_next = bacterium["anchor_position"][i + 1]

                self.canvas = cv2.line(self.canvas,
                                       core_position,
                                       anchor_position,
                                       self.bact_body_color, int(self.ppu * 0.25))

                self.canvas = cv2.line(self.canvas,
                                       anchor_position,
                                       anchor_position_next,
                                       self.bact_membrane_color, int(self.ppu * 0.25))

                if self.state["bacteria"][-1]["object"].skeleton["anchors"][i]["fixed"] == False:
                    self.canvas = cv2.circle(self.canvas,
                                             anchor_position,
                                             int(self.ppu * 0.5),
                                             self.bact_body_color, -1)
                else:
                    self.canvas = cv2.circle(self.canvas,
                                             anchor_position,
                                             int(self.ppu * 0.5),
                                             self.bact_body_color_fixed, -1)

            # draw core
            self.canvas = cv2.circle(self.canvas,
                                     core_position,
                                     int(self.ppu * 0.5), self.bact_core_color, -1)

        # render food
        for food in self.state["food"]:
            self.canvas = cv2.circle(self.canvas,
                                     (food["position"][0], food["position"][1]),
                                     int(self.ppu * food["amount"]),
                                     self.food_color, -1)


if __name__ == '__main__':
    print("Hello, World!")

    env = Environment()

    for i in range(5):
        env.add_food()

    env.add_bacterium()

    cv2.namedWindow('canvas', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('canvas', 800, 800)

    print(env.state)

    while (True):
        key_flag = cv2.waitKey(1) & 0xFF

        if key_flag == ord('q'):
            break
        else:
            env.update()

        cv2.imshow('canvas', env.canvas)
        time.sleep(0.05)
