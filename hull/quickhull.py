from numpy import abs
from time import time


def quickhull(set_of_points):
    """
    Calculates the convex hull of the given set of points using
    the 'Quickhull' algorithm.
    :param set_of_points: The set of points from which the convex hull will be derived
    :return: A subset containing the points which make up the convex hull
    """
    if len(set_of_points) < 2:
        raise ValueError('The provided set has to be comprised of at least 2 distinct points.')
    else:
        start = time()
        convex_hull = []
        r = __get_rightmost(set_of_points)
        l = __get_leftmost(set_of_points)
        convex_hull.extend((r, l))
        subset_rl = []
        subset_lr = []
        for (idx, p) in enumerate(set_of_points):
            if __shortest_distance(p, r, l) > 0: # if on one side, append to a subset (top portion)
                subset_rl.append(p)
            elif __shortest_distance(p, r, l) < 0: # if on the other side, append to the other subset (bottom portion)
                subset_lr.append(p)
        __find_hull(r, l, subset_rl, convex_hull)
        __find_hull(l, r, subset_lr, convex_hull)
        print('Completed in %.2f seconds.'%(time() - start))
        return convex_hull


def __find_hull(v0, v1, set_of_points, convex_hull):
    """
    Calculates the points on the convex hull for the given set of
    points that lie on the right side of the line segment oriented
    from the point v0 to point v1.
    """
    if len(set_of_points) <= 0:
        return
    else:
        furthest_dist = 0
        furthest_idx = -1
        for (i, p) in enumerate(set_of_points):
            current_dist = abs(__shortest_distance(p, v0, v1))
            if current_dist > furthest_dist:
                furthest_dist = current_dist
                furthest_idx = i
        furthest_point = set_of_points[furthest_idx]
        convex_hull.append(furthest_point)
        subset_0 = []
        subset_1 = []
        for (i, p) in enumerate(set_of_points):
            if __shortest_distance(p, furthest_point, v1) > 0:
                subset_0.append(p)
            if __shortest_distance(p, v0, furthest_point) > 0:
                subset_1.append(p)
        __find_hull(furthest_point, v1, subset_0, convex_hull)
        __find_hull(v0, furthest_point, subset_1, convex_hull)


def __shortest_distance(v, v0, v1):
    """
    Calculates the shortest pseudo-distance from the line segment v0v1 to point v.
    """
    return ((v0[0] - v[0]) * (v0[1] - v1[1])) + ((v0[1] - v[1]) * (v1[0] - v0[0]))


def __get_leftmost(set_of_points):
    """
    Returns the point that is located at the leftmost portion
    of the 2-D plane.
    """
    min = float('inf')
    idx = -1
    for (i, p) in enumerate(set_of_points):
        if p[0] <= min:
            min = p[0]
            idx = i
    return set_of_points[idx]


def __get_rightmost(set_of_points):
    """
    Returns the point that is located at the rightmost portion
    of the 2-D plane.
    """
    max = 0
    idx = -1
    for (i, p) in enumerate(set_of_points):
        if p[0] >= max:
            max = p[0]
            idx = i
    return set_of_points[idx]