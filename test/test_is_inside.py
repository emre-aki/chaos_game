import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from misc.is_inside import is_inside

set = [(1, 1), (2, 2), (3, 3)]
is_inside(set, (2, 3))