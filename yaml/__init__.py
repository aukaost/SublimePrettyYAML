import sys

if sys.version_info[0] < 3:
	from _yaml2 import *
else:
	from ._yaml3 import *