import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from util import *
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from matplotlib.pyplot import imread
from skimage.color import rgb2gray, rgba2rgb


def define_circle(center, radius, density=400):
    s = np.linspace(0, 2*np.pi, density)
    r = center[0] + radius*np.sin(s)
    c = center[1] + radius*np.cos(s)
    points = np.array([r, c]).T
    return points


def plot_snake(img, start_snake, snake):
    dpi = matplotlib.rcParams['figure.dpi']
    figsize = img.shape[1] / float(dpi), img.shape[0] / float(dpi)
    fig = plt.figure(frameon=False, figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img, cmap=plt.cm.gray)
    ax.plot(start_snake[:, 1], start_snake[:, 0], '--r', lw=3)
    ax.plot(snake[:, 1], snake[:, 0], '-b', lw=3)

    fig.patch.set_visible(False)
    ax.axis('off')
    # comment this line if you want to show axes coordinates
    ax.set_xticks([]), ax.set_yticks([])
    ax.axis([0, img.shape[1], img.shape[0], 0])



def run_active_contour(dirpath, df):
    """
    :param dirpath: dir to scan for input images
    :param df: dataframe containing list of file to be processed inside dirpath
    :return: None, this function store processing results as images in directory
    """"img""img"
    for index, row in df.iterrows():
        path = dirpath + "/" + row['path']
        img = imread(path)
        print(img.shape)
        if len(img.shape) > 2:
            if img.shape[2] > 3:
                img = rgb2gray(rgba2rgb(img))
            else:
                img = rgb2gray(img)

        center = (row['x_center'], row['y_center'])
        radius = row['radius']

        points = define_circle(center, radius, 400)

        blur_width = 3
        # smooth the image with gaussian blur of window range
        sm_image = gaussian(img, blur_width)

        # run basic snake on smoothed image
        snake = active_contour(sm_image,
                               points, alpha=0.015, beta=10, gamma=0.0001, boundary_condition='periodic', coordinates='rc')

        plot_snake(img, points, snake)
        filename, ext = get_filename_extension(path)
        plt.savefig(filename + "_res" + ext)
        # plt.show()
