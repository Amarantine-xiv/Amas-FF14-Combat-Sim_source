def add_to_rotation_library(rotation_name_and_rb, rotation_library):
    if rotation_name_and_rb is None:        
        return
    rotation_name, rb = rotation_name_and_rb
    if rotation_name in rotation_library:
        print(f'Updating rotation "{rotation_name}" in the rotation library.')
    rotation_library[rotation_name] = rb