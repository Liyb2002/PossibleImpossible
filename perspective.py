import math 
import numpy as np
import math

PI = 3.14

class Camera:
    def __init__(self, fov=60, aspect_ratio=1.0):
        # Camera parameters
        self.lookfrom = np.array([5.0, 5.0, 5.0])
        self.lookat = np.array([0.0, 0.0, 0.0])
        self.vup = np.array([0.0, 1.0, 0.0])
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        
        theta = self.fov * (PI / 180.0)
        half_height = math.tan(theta / 2.0)
        half_width = self.aspect_ratio * half_height
        self.cam_origin = self.lookfrom
        
        w = self.lookfrom - self.lookat
        w = w / np.linalg.norm(w)
        u = np.cross(self.vup,w)
        u = u / np.linalg.norm(u)
        v = np.cross(w,u)
        
        self.cam_lower_left_corner = self.cam_origin - half_width * u - half_height * v - w
        self.cam_horizontal = 2 * half_width * u
        self.cam_vertical = 2 * half_height * v


    def get_ray(self, u, v):
        r = self.cam_lower_left_corner + u * self.cam_horizontal + v * self.cam_vertical - self.cam_origin
        return r
    
    def get_camera_origin(self):
        return self.cam_origin
    