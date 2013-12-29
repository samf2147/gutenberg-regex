import re
import os

def file_paths(directory):
    file_names = os.listdir(directory)
    all_files = [os.path.join(directory,file_name) for file_name in file_names]
    return filter(lambda file_name : file_name[-4:] == '.txt', all_files)