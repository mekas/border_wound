import matplotlib.pyplot as plt
import matplotlib
from util import *
from skimage.segmentation import active_contour
from matplotlib.pyplot import imread
from skimage.color import rgb2gray, rgba2rgb
from skimage.filters import gaussian, threshold_otsu
from skimage.morphology import closing, square
from skimage.feature import canny


def define_circle(center, radius, density=400):
    """
    Define a circle given center, radius, and density
    :param center: A pair tuple of x,y center of the circle
    :param radius: Integer define the radius of the circle
    :param density: How many you want to sample the circle perimeter
    :return:
    """
    s = np.linspace(0, 2*np.pi, density)
    r = center[0] + radius*np.sin(s)
    c = center[1] + radius*np.cos(s)
    points = np.array([r, c]).T
    return points


def plot_thresholding(path, img, suffix_path):
    dpi = matplotlib.rcParams['figure.dpi']
    figsize = img.shape[1] / float(dpi), img.shape[0] / float(dpi)
    fig = plt.figure(frameon=False, figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img, cmap=plt.cm.gray)

    fig.patch.set_visible(False)
    ax.axis('off')
    # comment this line if you want to show axes coordinates
    ax.set_xticks([]), ax.set_yticks([])
    ax.axis([0, img.shape[1], img.shape[0], 0])

    filename, ext = get_filename_extension(path)
    plt.savefig(filename + suffix_path + ext)


def plot_snake(path, img, start_snake, snake, edges, suffix_path):
    """
    This function draw the snake path in overlay mode with input image,
    drawn circle and ground truth
    :param path: Image path
    :param img: Image matrix
    :param start_snake: Drawn circle
    :param snake: Result of snake operation
    :param suffix_path: suffix filename to append as output filename
    :return:
    """

    dpi = matplotlib.rcParams['figure.dpi']
    figsize = img.shape[1] / float(dpi), img.shape[0] / float(dpi)
    fig = plt.figure(frameon=False, figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img, cmap=plt.cm.gray)
    ax.plot(start_snake[:, 1], start_snake[:, 0], '--r', lw=3)
    ax.plot(snake[:, 1], snake[:, 0], '-b', lw=3)
    # with edge map we can't plot with plot, since the indexes are unordered
    # (not clockwise rotation)
    ax.scatter(edges[:, 1], edges[:, 0], s=0.5, facecolor='green')

    fig.patch.set_visible(False)
    ax.axis('off')
    # comment this line if you want to show axes coordinates
    ax.set_xticks([]), ax.set_yticks([])
    ax.axis([0, img.shape[1], img.shape[0], 0])

    filename, ext = get_filename_extension(path)
    plt.savefig(filename + suffix_path + ext)
    # plt.show()


def thresholding(img):
    tres = threshold_otsu(img)
    return closing(img > tres, square(3))


def run_active_contour(dirpath, df, alpha, beta, gamma, blur_width, density):
    """
    :param dirpath: dir to scan for input images
    :param df: dataframe containing list of file to be processed inside dirpath
    :param alpha: Snake length shape parameter, higher values make snake contract faster
    :param beta: Snake smoothness shape parameter. Higher values makes snake smoother.
    :param gamma: Explicit time stepping parameter. Higher values makes 
    converge faster at the expense of precision.
    :param blur_width: Gaussian smoothing parameter. Must be odd.
    :param density: How many sample wanted for the snake
    :return: None, this function store processing results as images in directory
    """"img""img"
    for index, row in df.iterrows():
        path = os.path.join(dirpath, row['path'])
        try:
            img = imread(path)
            gt_path = get_ground_truth_path(path)
            gt_img = imread(gt_path)
            edge_map = canny(rgb2gray(rgba2rgb(gt_img)))
            edge_locations = np.where(edge_map == True)
            edge_locations = merge_coordinates(edge_locations[0],
                                               edge_locations[1])
            if len(img.shape) > 2:
                if img.shape[2] > 3:
                    img = rgb2gray(rgba2rgb(img))
                else:
                    img = rgb2gray(img)

            # smooth the image with gaussian blur of window range
            sm_image = gaussian(img, blur_width)
            # apply Otsu thresholding to the smoothed image
            bw_image = thresholding(sm_image)

            center = (row['x_center'], row['y_center'])
            radius = row['radius']

            points = define_circle(center, radius, density)

            blur_width = blur_width

            max_iteration_def = 10000
            gamma_def = 0.01
            max_iter = max_iteration_def * gamma_def / gamma

            # run basic snake on smoothed image
            snake = active_contour(bw_image, points, alpha=alpha, beta=beta, gamma=gamma,
                                   max_iterations=max_iter,
                                   coordinates='rc')

            # dump the processed image to the input directory with extra suffix
            plot_snake(path, img, points, snake, edge_locations, '_res')
            plot_thresholding(path, bw_image, '_thres')
        except IOError:
            print("Can't read either input or ground truth image, skip " + path)
