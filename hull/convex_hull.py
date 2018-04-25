"""
a = float("-inf")
b = -9999

print(str(b > a))
if b > a:
    print("%.2f > %.2f"%(b, a))
"""

import copy
from numpy import sqrt

def convex_hull(set_of_points):
    """
    Returns the convex hull of the given set 2-D points
    :param set_of_points: The set of points from which the convex hull will be derived
    :return: The convex hull set
    """
    sorted_set_of_points = sort_radially(set_of_points)
    stack = []
    stack.append(sorted_set_of_points[0])
    stack.append(sorted_set_of_points[1])
    i = 2
    while i < len(set_of_points):
        curr_vert = sorted_set_of_points[i]
        stack.append(curr_vert)
                                                                          #stack[-1]
        if not __is_left_turn(stack[len(stack) - 3], stack[len(stack) - 2], stack[len(stack) - 1]):
            # back-track
            stack.pop(len(stack) - 2)
                                                                                 #stack[-1]
            while (len(stack) > 3) and\
                    (not __is_left_turn(stack[len(stack) - 3], stack[len(stack) - 2], stack[len(stack) - 1])):
                stack.pop(len(stack) - 2)
        i += 1
    return stack


def __is_left_turn(v0, v1, v2):
    """
    Checks if the point v2 is on the left of the line segment v0v1
    :return: True v lies on the left of the line segment v0v1
    """
    return ((v1[0] - v0[0]) * (v2[1] - v0[1]) - (v2[0] - v0[0]) * (v1[1] - v0[1])) > 0


def sort_radially(set_of_points):
    """
    Sorts the given set of points/vertices radially with respect to the slope they make
    with the rightmost vertex in the set.
    Beware: This function does not sort in-place.
    :param set_of_points: The set of points/vertices to sort radially
    :return: The sorted set of points
    """
    slopes_increasing = []
    rightmost_idx = __rightmost_vertex(set_of_points) # the index of the rightmost vertex
    slopes_increasing.append(set_of_points[rightmost_idx]) # the coordinates of the rightmost vertex is appended to
                                                           # the sorted list as the first item
    cp_sop = copy.deepcopy(set_of_points)
    cp_sop.pop(rightmost_idx) # the rightmost vertex (that is already in the sorted list) is removed
    while len(cp_sop) > 0:
        min_slope = float("inf")
        idx = 0
        for i, p in enumerate(cp_sop):
            curr_slope = slope(set_of_points[rightmost_idx], p) # calculating the slope p makes with rightmost vertex
            if curr_slope <= min_slope:
                min_slope = curr_slope
                idx = i
        slopes_increasing.append(cp_sop[idx])
        #print("min_slope = %.2f"%(min_slope))
        cp_sop.pop(idx)
    return slopes_increasing


def slope(v0, v1):
    """
    Calculates the slope of 2 given vertices. However, if the two vertices are vertically aligned, the slope is
    returned a `float("inf")` or `float("-inf")` depending on the ???
    :param v0: first of the 2 vertices
    :param v1: second of the 2 vertices
    :return: the slope of 2 vertices
    """
    if v0[0] != v1[0]:
        return ((v0[1] - v1[1]) / (v0[0] - v1[0]))
    else:
        if v0[1] < v1[1]:
            return float("-inf")
        elif v0[1] == v1[1]:
            return 0
        else:
            return float("inf")


def __rightmost_vertex(set_of_points):
    """
    Returns the index of the rightmost vertex in a given set of points
    :param set_of_points: the set of points
    :return: the index of the rightmost vertex in the given set
    """
    rightmost_x = 0
    idx = 0
    for i, p in enumerate(set_of_points):
        if p[0] > rightmost_x:
            rightmost_x = p[0]
            idx = i
    return idx


def dist(v0, v1):
    """
    Calculates the Euclidean distance between points v0 and v1.
    :return: The Euclidean distance
    """
    return sqrt(((v1[0] - v0[0]) ** 2) + ((v1[1] - v0[1]) ** 2))