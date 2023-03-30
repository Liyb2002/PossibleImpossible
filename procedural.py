import json
import generic_objects

objects = []
if __name__ == "__main__":
    with open('objects.json', 'r') as object_file:
        objects_data = json.load(object_file)

        for object_data in objects_data:
            print("hi")
            new_object = generic_objects.Generic_object(object_data)

