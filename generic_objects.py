import random

class Generic_object:
    def __init__(self, info):
        self.id = info['object_id']
        self.scope_x = info['scope_x']
        self.scope_y = info['scope_y']
        self.scope_z = info['scope_z']
        self.connect_id = info['connect_id']

    def get_next(self):
        if self.connect_id == []:
            print("terminate")
            return
        
        choice = random.choice(self.connect_id)
        return choice