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

        self.plane = find_plane(u, v, self.cam_lower_left_corner)

    def get_ray(self, u, v):
        r = self.cam_lower_left_corner + u * self.cam_horizontal + v * self.cam_vertical - self.cam_origin
        return r
    
    def get_ray_origin(self, u, v):
        screen_width = 800                  
        screen_height = 800                  
        world_width = 10.0                    
        world_height = (screen_height / screen_width) * world_width 

        direction = self.lookat - self.lookfrom
        direction /= np.linalg.norm(direction)
        right = np.cross(direction, self.vup)
        right /= np.linalg.norm(right)
        up = np.cross(right, direction)

        ndc_x = (2 * u) - 1
        ndc_y = 1 - (2 * v)

        world_x = self.lookfrom[0] + (ndc_x * world_width * 0.5 * right[0])
        world_y = self.lookfrom[1] + (ndc_y * world_height * 0.5 * up[1])
        world_z = self.lookfrom[2] + (self.lookat[2] - self.lookfrom[2])

        # Create the ray from the camera to the current pixel
        ray_origin = np.array([world_x, world_y, world_z])
        return ray_origin

    
    def get_uv(self, point):
        intersection_pt = find_intersection(self.cam_origin, point, self.plane)
        v = (intersection_pt[1] - self.cam_lower_left_corner[1]) / self.cam_vertical[1]
        u = (intersection_pt[0] - (self.cam_lower_left_corner[0] + v*self.cam_vertical[0])) / self.cam_horizontal[0]
        return (u*800, v*800)

    def get_camera_origin(self):
        return self.cam_origin
    

    # Function to find the equation of a plane given two lines
def find_plane(dir1, dir2, point):

    dir1 = dir1 / np.linalg.norm(dir1)    
    dir2 = dir2 / np.linalg.norm(dir2)    

    # Take the cross product of the direction vectors to find the normal vector of the plane
    normal_vector = np.cross(dir1, dir2)

    # Calculate the constant term in the plane equation
    constant = -np.dot(normal_vector, point)
    
    # Return the coefficients of the plane equation
    return np.append(normal_vector, constant)

# Function to find the intersection of a line and a plane
def find_intersection(camera_origin, target_point , plane):
    # Extract the coefficients of the plane equation
    a, b, c, d = plane
    
    # Calculate the direction vector of the line
    dir_vector = target_point - camera_origin
    
    # Calculate the parameter t at the intersection point
    t = (-d - np.dot(plane[:3], camera_origin)) / np.dot(plane[:3], dir_vector)
    
    # Calculate the coordinates of the intersection point
    intersection_point = camera_origin + t * dir_vector
    
    return intersection_point
