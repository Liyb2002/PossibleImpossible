import procedural_objects
import numpy as np

class Module:
    def __init__(self, position, size):
        self.type = 'A'
        self.position = position
        self.size = size
        self.age = 0

    def toProcedual(self):
        dummy_scope = [0.1, 0.1]

        tempt_obj = procedural_objects.Procedural_object(11, self.position,np.array([dummy_scope,dummy_scope,dummy_scope]), "00000", np.array([[0],[0],[0]]), np.array([0,0,0]))
        tempt_obj.arbitrary_set_length(np.array([float(self.size[0]),float(self.size[1]),float(self.size[2])]))
        return tempt_obj
    
    def execute(self, enviroment):
        new_size = self.size
        new_position = self.position + np.array([self.size[0], 0, 0]) + np.array([new_size[0], 0, 0])
        new_module = Module(new_position, new_size)
        return new_module
