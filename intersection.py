import numpy as np
import argparse
import random

import perspective

class Scene:
    def __init__(self, startPos):
        self.possible_intersects = []
        self.max_screen = []
        self.min_screen = []

        self.x_start = startPos[0]
        self.y_start = startPos[1]
        self.image_height = 800
        self.image_width = 800

        self.screen_height = 10.0
        self.screen_width = 10.0

        self.camera = perspective.Camera()
        self.get_impossible_intersection()
        

    def get_impossible_intersection(self):
        u = (self.x_start) / self.image_width
        v = (self.y_start) / self.image_height
        camera_pos = self.camera.get_camera_origin()
        ray = self.camera.get_ray(u, u)
        ro_x = camera_pos[0] + (2 * u - 1) * self.screen_width
        ro_y = camera_pos[1] + (1 - 2 * v) * self.screen_height
        ro = np.array([ro_x, ro_y, camera_pos[2]])

        for k in range(0,40):
            x = ro[0] + ray[0] * (k*0.5)
            y = ro[1] + ray[1] * (k*0.5)
            z = ro[2] + ray[2] * (k*0.5)
            pos = np.array([x, y,z])
            self.possible_intersects.append(pos)

    def get_intersection_t(self, screenPos, worldPos):
        u = (screenPos[0]) / self.image_width
        v = (screenPos[1]) / self.image_height
        camera_pos = self.camera.get_camera_origin()
        ray = self.camera.get_ray(u, v)

        t = (worldPos[2] - camera_pos[2]) / ray[2]
        x = camera_pos[0] + ray[0] * t
        y = camera_pos[1] + ray[1] * t

        return np.array([x, y, worldPos[2]])

    def get_uv(self, point):
        return self.camera.get_uv(point)
        
    def get_max_screen(self, k):
        return np.array([self.max_screen[k][0], self.max_screen[k][1]])
    
    def get_min_screen(self, k):
        return np.array([self.min_screen[k][0], self.min_screen[k][1]])
    
    def get_possible_intersects(self, k):
        return np.array([self.possible_intersects[k][0], self.possible_intersects[k][1], self.possible_intersects[k][2]])

    def get_arbitrary_pos(self, k, uv):
        u = uv[0] / self.image_width
        v = uv[1] / self.image_height
        camera_pos = self.camera.get_camera_origin()
        ray = self.camera.get_ray(u, v)

        x = camera_pos[0] + ray[0] * (k*0.5)
        y = camera_pos[1] + ray[1] * (k*0.5)
        z = camera_pos[2] + ray[2] * (k*0.5)
        pos = np.array([x, y,z])

        return pos