import procedural_objects
import numpy as np

class Module:
    def __init__(self, position, size, rotation):
        self.type = 11
        self.position = position
        self.size = size
        self.age = 0
        self.rotation = rotation

    def toProcedual(self):
        dummy_scope = [0.1, 0.1]

        tempt_obj = procedural_objects.Procedural_object(11, self.position,np.array([dummy_scope,dummy_scope,dummy_scope]), "00000", np.array([[self.rotation[0]],[self.rotation[1]],[self.rotation[2]]]), np.array([0,0,0]))
        tempt_obj.arbitrary_set_length(np.array([float(self.size[0]),float(self.size[1]),float(self.size[2])]))
        return tempt_obj
    
    def execute(self, enviroment, rules):
        #chose a rule to execute
        execute_rule =  None
        new_modules = []
        
        for rule in rules:
            if rule.lhs_type == self.type:
                execute_rule = rule
                break
        
        for i in range(len(execute_rule.rhs_types)):
            new_type = execute_rule.rhs_types[i]
            new_size = np.array([self.size[0] * execute_rule.rhs_size_multiplier[i][0], self.size[1] * execute_rule.rhs_size_multiplier[i][1], self.size[2] * execute_rule.rhs_size_multiplier[i][2]])
            new_rotation = self.rotation + execute_rule.rhs_rotations[i]
            new_direction = execute_rule.rhs_directions[i]
            new_offsets = execute_rule.rhs_offsets[i]

            new_position = self.get_new_position(new_direction, new_size, new_offsets)
            new_module = Module(new_position, new_size, new_rotation)
            new_modules.append(new_module)

        return new_modules


    def get_new_position(self, new_direction, new_size, new_offsets):
        new_position = new_offsets
        if new_direction == "top":
            new_position += self.position + np.array([0, self.size[1], 0]) + np.array([0, new_size[1], 0])
        
        if new_direction == "bot":
            new_position += self.position - np.array([0, self.size[1], 0]) - np.array([0, new_size[1], 0])

        return new_position