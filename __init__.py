import os

parent_dir_name = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)
sys.path.append(parent_dir_name + "/url_tools")
