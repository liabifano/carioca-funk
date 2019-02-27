import os
import shutil


def clean_folder(path):
    """
    Delete folder if exists and creates a new folder with no data

    :param path: string with the path
    """
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)
