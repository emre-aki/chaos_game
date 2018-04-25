############################################################################################
# Must keep in mind that the coordinates (0, 0) defines the pixel that is the top leftmost #
# pixel on the screen. However, it is the bottom leftmost point in the coordinate system.  #
# Also, y-axis corresponds to rows, whereas x-axis corresponds to columns in a 2-D array.  #
############################################################################################

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hull.convex_hull import dist, convex_hull, slope, sort_radially
from hull.quickhull import quickhull
from numpy import random, uint16
from PIL import Image, ImageDraw


def main():
    print("      _")
    print("  ___| |__   __ _  ___  ___      __ _  __ _ _ __ ___   ___")
    print(" / __| '_ \ / _` |/ _ \/ __|    / _` |/ _` | '_ ` _ \ / _ \\")
    print("| (__| | | | (_| | (_) \__ \   | (_| | (_| | | | | | |  __/")
    print(" \___|_| |_|\__,_|\___/|___/____\__, |\__,_|_| |_| |_|\___|")
    print("                          |_____|___/")
    game_size = uint16(input("game_size> "))
    num_epochs = uint16(input("number_of_iterations> "))
    r_pointer = uint16(input("tracer_radius> "))
    run(game_size=game_size, num_iters=num_epochs, r_tracer=r_pointer)


def run(game_size, num_iters, r_tracer):

    # handling log files
    lines = []
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "latest.log"), mode="rb") as log:
        for line in log:
            lines.append(line)  # each line read is a byte-like
        prep_file = uint16(lines[0].decode(encoding="utf-8"))  # reading and converting prep_file to int
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "latest.log"), mode="wb") as log:
        log.seek(0)
        for (i, line) in enumerate(lines):
            if i == 0:                                                                # if the line is the one we are interested
                log.write(("%s\n"%(str(uint16(line) + 1))).encode(encoding="utf-8"))  # in, then update it
            else:  # if not, just write it as is
                log.write(line)
    # end_handling_log

    init = Image.new("RGB", (game_size, game_size))
    img_grid = Image.new("RGB", (game_size, game_size))
    draw_init = ImageDraw.Draw(init, "RGBA")
    draw_grid = ImageDraw.Draw(img_grid, "RGBA")
    grid = []

    # initializing_the_base-points
    A = {"x" :random.randint(0, game_size), "y" :random.randint(0, game_size)}
    B = {"x" :random.randint(0, game_size), "y" :random.randint(0, game_size)}
    C = {"x" :random.randint(0, game_size), "y" :random.randint(0, game_size)}
    while not is_triangle((A["x"], A["y"]), (B["x"], B["y"]), (C["x"], C["y"])):
        A = {"x" :random.randint(0, game_size), "y" :random.randint(0, game_size)}
        B = {"x" :random.randint(0, game_size), "y" :random.randint(0, game_size)}
        C = {"x" :random.randint(0, game_size), "y" :random.randint(0, game_size)}
    grid.append((A["x"], A["y"]))
    grid.append((B["x"], B["y"]))
    grid.append((C["x"], C["y"]))
    # end_initializing

    # initializing_the_dot within the bounds of the triangle
    d = {"x" : random.randint(low=0, high=game_size), "y" : random.randint(low=0, high=game_size)}
    while not is_inside((d["x"], d["y"]), (A["x"], A["y"]), (B["x"], B["y"]), (C["x"], C["y"])):
        d = {"x" :random.randint(low=0, high=game_size), "y" :random.randint(low=0, high=game_size)}
    grid.append((d["x"], d["y"]))
    # end_initializing_the_dot

    # plot_initial_grid
    for i, dot in enumerate(grid):
        if i == 0 or i == 1 or i == 2:
            fill = (255, 255, 0, 255)
            if i == 0:
                foo = "A"
            if i == 1:
                foo = "B"
            if i == 2:
                foo = "C"
        elif i == 3:
            fill = (255, 0, 0, 255)
            foo = "d"
        draw_init.ellipse((dot[0] - r_tracer, dot[1] - r_tracer, dot[0] + r_tracer, dot[1] + r_tracer),
                                           fill=fill)
        draw_init.text((dot[0], dot[1]), (("%s(%d, %d)") % (foo, dot[0], dot[1])), (0, 0, 255, 255))
    init.show(title="The Grid")
    del draw_init
    # end_plot

    # the_Game
    for e in range(num_iters):
        die = random.randint(low=1, high=4)
        towards = "A"
        if die == 1:    #move towards A
            if d["x"] > A["x"]:
                d["x"] -= uint16(abs(d["x"] - A["x"]) / 2)
            elif d["x"] < A["x"]:
                d["x"] += uint16(abs(d["x"] - A["x"]) / 2)
            if d["y"] > A["y"]:
                d["y"] -= uint16(abs(d["y"] - A["y"]) / 2)
            elif d["y"] < A["y"]:
                d["y"] += uint16(abs(d["y"] - A["y"]) / 2)
        elif die == 2:  #move towards B
            towards = "B"
            if d["x"] > B["x"]:
                d["x"] -= uint16(abs(d["x"] - B["x"]) / 2)
            elif d["x"] < B["x"]:
                d["x"] += uint16(abs(d["x"] - B["x"]) / 2)
            if d["y"] > B["y"]:
                d["y"] -= uint16(abs(d["y"] - B["y"]) / 2)
            elif d["y"] < B["y"]:
                d["y"] += uint16(abs(d["y"] - B["y"]) / 2)
        else:           #move towards C
            towards = "C"
            if d["x"] > C["x"]:
                d["x"] -= uint16(abs(d["x"] - C["x"]) / 2)
            elif d["x"] < C["x"]:
                d["x"] += uint16(abs(d["x"] - C["x"]) / 2)
            if d["y"] > C["y"]:
                d["y"] -= uint16(abs(d["y"] - C["y"]) / 2)
            elif d["y"] < B["y"]:
                d["y"] += uint16(abs(d["y"] - C["y"]) / 2)
        grid.append((d["x"], d["y"]))
        print("epoch %d>"%(e))
        print("pointer\t\ttowards\n(%d, %d)\t%s\n"%(d["x"], d["y"], towards))
    # end_the_Game

    # determining the convex hull of the resulting grid of 2-D points, i.e., the corners of the triangle
    #conv_hull = convex_hull(grid)
    conv_hull = sort_radially(quickhull(grid))
    # end_convex_hull

    # plotting_the_grid
    for i, d in enumerate(grid):
        if i == 0 or i == 1 or i == 2:
            draw_grid.ellipse((d[0] - r_tracer * 2, d[1] - r_tracer * 2, d[0] + r_tracer * 2,
                                                 d[1] + r_tracer * 2), fill=(255, 255, 0, 255))
        elif i == 3:
            draw_grid.ellipse((d[0] - r_tracer * 2, d[1] - r_tracer*2, d[0] + r_tracer * 2,
                                                 d[1] + r_tracer * 2), fill=(255, 0, 0, 255))
        elif i == (len(grid) - 1):
            draw_grid.ellipse((d[0] - r_tracer * 2, d[1] - r_tracer * 2, d[0] + r_tracer * 2,
                                                 d[1] + r_tracer * 2), fill=(0, 255, 0, 255))
        else:
            draw_grid.ellipse((d[0] - r_tracer, d[1] - r_tracer, d[0] + r_tracer, d[1] + r_tracer),
                                                fill=(255, 255, 255, 75))
            # draw_grid.text((d[0], d[1]), str(i),(0, 0, 255, 255))
    img_grid.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plot", ("grid_%d.png"%(prep_file))), "PNG")
    img_grid.show(title="The Grid")
    del draw_grid
    img_convhull = Image.new("RGB", (game_size, game_size))
    draw_convhull = ImageDraw.Draw(img_convhull, "RGBA")
    for d in conv_hull:
        draw_convhull.ellipse((d[0] - r_tracer, d[1] - r_tracer, d[0] + r_tracer, d[1] + r_tracer),
                                            fill=(0, 0, 255, 255))
        draw_convhull.text((d[0], d[1]), (("(%d, %d)\n%s") % (d[0], d[1], str(slope(conv_hull[0], d)))),
                                         (0, 0, 255, 255))
    conv_hull.append(conv_hull[0])
    draw_convhull.line(conv_hull, fill=(0, 0, 255, 255), width=1)
    conv_hull.pop(-1)
    img_convhull.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plot",
                                   ("convex_hull_%d.png"%(prep_file))), "PNG")
    img_convhull.show(title="Convex Hull")
    del draw_convhull
    # end_plotting_the_grid

    print("s(conv_hull) = %d"%len(conv_hull))


def is_triangle(v0, v1, v2):
    """
    Checks if the points v0, v1 and v2 define a valid triangle
    """
    dist_01 = dist(v0, v1)
    dist_02 = dist(v0, v2)
    dist_12 = dist(v1, v2)
    if ((abs(dist_01 - dist_02) < dist_12) and (dist_12 < (dist_01 + dist_02)))\
        and ((abs(dist_01 - dist_12) < dist_02) and (dist_02 < (dist_01 + dist_12)))\
        and ((abs(dist_02 - dist_12) < dist_01) and (dist_01 < (dist_02 + dist_12))):
        return True
    return False


def is_inside(v, v0, v1, v2):
    """
    Checks if the point v is inside the bounds defined by the triangle v0v1v2
    :return: True if v is inside the triangle v0v1v2
    """
    if len(convex_hull([v0, v1, v2])) == len(convex_hull([v, v0, v1, v2])):
        # Checking for the exceptional case where point v is NOT inside the triangle v0v1v2,
        # YET STILL, it WON'T increase the length of the convex_hull([v0, v1, v2]).
        # This case could only be caused by point v being aligned with one of the segments v0, v1 or v2.
        # The following if block checks for this special case.
        # Ex: (v)    v0 *--------* v1, or v0 *--------* v1     (v)
        if (dist(v, v1) > dist(v0, v1)) or (dist(v, v2) > dist(v0, v2)) \
                or (dist(v, v0) > dist(v0, v1)) or (dist(v, v2) > dist(v1, v2))\
                or (dist(v, v0) > dist(v0, v2)) or (dist(v, v1) > dist(v1, v2)):
            return False
        return True
    return False


if __name__ == "__main__":
    main()