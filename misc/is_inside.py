from hull import quickhull
from hull.convex_hull import sort_radially
from misc.mergesort import mergesort


def is_inside(set, p):
    """
    Returns `True` if point `p` is inside the convex hull
    defined by the points in `set`, otherwise returns `False`.
    """
    print(str(mergesort))
    ch = sort_radially(quickhull(set))
    print('Convex hull: %s'%(str(ch)))

    """
    #TODO: 
        1. Derive convex hull from set using quickhull.
        2. Sort vertices in the convex hull radially
        3. Each adjacent pair of points in the convex hull defines 
           a line. 
           For each line:
               if p lies to the right of the line:
                   return False
           return True
    """
    return True