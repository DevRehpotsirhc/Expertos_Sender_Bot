import os
import sys



def base_path(relative_path):
    base = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base, relative_path)

def resource_path(filename):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)
