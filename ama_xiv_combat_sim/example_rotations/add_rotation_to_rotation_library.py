def add_to_rotation_library(rotation_name_and_rb, rotation_library):
    rotation_name, rb = rotation_name_and_rb
    if rotation_name in rotation_library:
        print('Updating rotation "{}" in the rotation library.'.format(rotation_name))
    rotation_library[rotation_name] = rb