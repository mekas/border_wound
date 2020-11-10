import os
import numpy as np


def get_filename_extension(path):
    return os.path.splitext(path)


def get_ground_truth_path(path):
    filename, ext = get_filename_extension(path)
    return filename + "_region" + ".png"


def merge_coordinates(p1, p2):
    points = [[p1[i], p2[i]] for i in range(len(p1))]
    return np.array(points)
