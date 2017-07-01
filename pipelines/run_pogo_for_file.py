# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 01-07-2017 23:20
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module runs PoGo for a file, using the given GTF and FA reference files, it will produce the results in the same
folder where the input file is located
"""

import config_manager
import toolbox


__configuration_file = None
__configuration_manager = None


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not met to be run in stand alone mode")
