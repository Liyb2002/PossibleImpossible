import random
import numpy as np

class Generic_object:
    def __init__(self, info):
        self.id = info['object_id']
        self.set_scope(info)
        self.connect_id = info['connect_id']
        self.canTerminate = info['canTerminate']
        self.rules = info['connect_rule']

    def get_nextType(self, unavailable_dirs):
        if self.connect_id == []:
            print("terminate")
            return

        count = 0
        while count <3:
            count += 1
            choice = random.choice(self.connect_id)
            direction = self.execute_rule(choice)
            available_next = True

            for unavailable_dir in unavailable_dirs:
                if direction == unavailable_dir:
                    available_next = False

            if available_next: 
                return choice
            
        return None
    
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
            for i in range(len(self.rules[next_id])):
                if direction == self.rules[next_id][i]:
                    possible_next.append(next_id)
        
        if len(possible_next) != 0:
            choice = possible_next[0]
            rule = direction
        else:
            return (False, [], [])
            # print("wtf")
            # choice = self.get_nextType()
            # rule = self.execute_rule(choice)
        
        return (True,choice, rule)
        
    def able_next_direction(self, direction):
        for next_id in self.rules:
            for i in range(len(self.rules[next_id])):
                if direction == self.rules[next_id][i]:
                    return True

        return False    

    def test(self):
        print("hello")
    
    def generate_hash(self):
        gen_hash = self.id + random.uniform(0, 1)
        return gen_hash
