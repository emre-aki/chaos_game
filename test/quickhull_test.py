import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hull.quickhull import quickhull
from hull.convex_hull import sort_radially
from numpy import random, uint16
from PIL import Image, ImageDraw


def main():
    print(' _____       _      _    _   _       _ _ ')
    print('|  _  |     (_)    | |  | | | |     | | |')
    print('| | | |_   _ _  ___| | _| |_| |_   _| | |')
    print('| | | | | | | |/ __| |/ /  _  | | | | | |')
    print('\ \/\' / |_| | | (__|   <| | | | |_| | | |')
    print(' \_/\_\\\\__,_|_|\___|_|\_\_| |_/\__,_|_|_|')
    print('')
    game_size = uint16(input("game_size> "))
    num_epoch = uint16(input("number_of_iterations> "))
    run(game_size, num_epoch)


def run(game_size, num_epoch):
    print('Generating %d random points...'%(num_epoch))
    the_grid = generate_random_points(num_epoch, game_size, game_size)
    print('Plotting %dx%d grid...'%(game_size, game_size))
    file_suffix = plot_grid(game_size, the_grid, save=True)
    print('Calculating the convex hull...')
    ch = sort_radially(quickhull(the_grid))
    plot_convex_hull(game_size, ch, save=True, file_suffix=file_suffix)


def generate_random_points(n, high_x, high_y, low_x=0, low_y=0):
    """
    Generates a number of n 2-D points on a square grid
    :param low_x: Lower bound the points will have on the x-axis
    :param low_y: Lower bound the points will have on the y-axis
    :param high_x: Upper bound the points will have on the x-axis
    :param high_y: Upper bound the points will have on the y-axis
    :param n: The number of points to generate
    :return: The list of 2-D points generated
    """
    points = []
    for i in range(n):
        p = ((random.randint(low_x, high_x)), (random.randint(low_y, high_y)))
        points.append(p)
    return points


def plot_convex_hull(size, convex_hull, save=False, file_suffix=None):
    """
    Plots the set of points in the given grid
    :param grid: The grid to plot
    :param save: Specifies whether the plotted image will be saved or not
    :return: None
    """
    img_convhull = Image.new("RGB", (size, size))
    draw_convhull = ImageDraw.Draw(img_convhull, "RGBA")
    for p in convex_hull:
        draw_convhull.ellipse((p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2), fill=(0, 0, 255, 255))
        draw_convhull.text((p[0], p[1]), (('(%d, %d)') % (p[0], p[1])), (0, 0, 255, 255))
    convex_hull.append(convex_hull[0])
    draw_convhull.line(convex_hull, fill=(0, 0, 255, 255), width=1)
    convex_hull.pop(-1)
    if save and file_suffix is not None:
        img_convhull.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plot",
                                       ("quickhull_%d.png" % (file_suffix))), "PNG")
    elif file_suffix is None:
        raise IOError('Error while saving file.')
    img_convhull.show(title='Quickhull')
    del draw_convhull


def plot_grid(size, grid, save=False):
    """
    Plots the set of points in the given grid
    :param grid: The grid to plot
    :param save: Specifies whether the plotted image will be saved or not
    :return: None
    """
    lines = []
    img_grid = Image.new("RGB", (size, size))
    draw_grid = ImageDraw.Draw(img_grid, "RGBA")
    for p in grid:
        draw_grid.ellipse((p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2), fill=(255, 255, 0, 255))
        draw_grid.text((p[0], p[1]), (('(%d, %d)')%(p[0], p[1])), (255, 255, 0, 255))
    if save:
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "latest.log"), mode="rb") as log:
            for line in log:
                lines.append(line) # each line read is a byte-like
            prep_file = uint16(lines[1].decode(encoding="utf-8")) # reading and converting prep_file to int
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "latest.log"), mode="wb") as log:
            log.seek(0)
            for i, line in enumerate(lines):
                if i == 1:                                                    # if the line is the one we are interested
                    log.write(str(uint16(line) + 1).encode(encoding="utf-8")) # in, then update it
                else: # if not, just write it as is
                    log.write(line)
        img_grid.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plot",
                                   ("grid_qh%d.png"%(prep_file))), "PNG")
        return prep_file
    img_grid.show(title='The Grid')
    del draw_grid


if __name__ == '__main__':
    main()