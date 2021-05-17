import os


def create_directory(path_file):
    if not os.path.exists(path_file):
        os.makedirs(path_file)

#def create_file():