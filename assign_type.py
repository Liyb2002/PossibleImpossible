import copy

def assign(procedural_objects):
    for obj in procedural_objects:
        
        if obj.type == 1:
            assign_available = True
            for dir in obj.connected:
                if dir == "+y":
                    assign_available = False
            
            if assign_available:
                obj.type = 9
    
    return procedural_objects
