import sys
if sys.version_info[0] == 2:
    import easyfunc
    from easyfunc import *
elif sys.version_info[0] == 3:
    from . import easyfunc
    from easyfunc.easyfunc import *

name = 'easyfunc'
