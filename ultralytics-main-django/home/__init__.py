import sys
import os

# 获取 home 目录的绝对路径
HOME_DIR = os.path.dirname(os.path.abspath(__file__))

# 把 home 目录加入 sys.path
if HOME_DIR not in sys.path:
    sys.path.append(HOME_DIR)
