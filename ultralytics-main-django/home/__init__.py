import sys
import os

# Obtain the absolute path of the home directory
HOME_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the home directory to sys.path
if HOME_DIR not in sys.path:
    sys.path.append(HOME_DIR)
