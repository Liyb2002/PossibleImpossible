import random
import numpy as np

class Generic_object:
    def __init__(self, info):
        self.id = info['object_id']
        self.set_scope(info)
        self.connect_id = info['connect_id']
        self.canTerminate = info['canTerminate']
        self.rules = info['connect_rule']

    def get_nextType(self):
        if self.connect_id == []:
            print("terminate")
            return
        
        choice = random.choice(self.connect_id)
        return choice
    
    def set_scope(self, info):
        scope_x = info['scope_x']
        scope_y = info['scope_y']
        scope_z = info['scope_z']
        self.scope = np.array([scope_x,scope_y,scope_z])
    
    def execute_rule(self, next_id):
        rule = self.rules[str(next_id)]
        choice = random.choice(rule)
        return choice

    def get_nextType_with_direction(self, direction):
        possible_next = []
        for next_id in self.rules:
            if direction == self.rules[next_id][0]:
                possible_next.append(next_id)
        
        if len(possible_next) != 0:
            choice = possible_next[0]
            rule = direction
        else:
            choice = self.get_nextType()
            rule = self.execute_rule(choice)
        
        return (choice, rule)