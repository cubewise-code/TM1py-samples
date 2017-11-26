"""
Remove all objects in TM1 that match a list of regular expressions.

use with care!
"""


import re

from TM1py.Services import TM1Service


with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:

    # Regular expression for everything that starts with 'temp_', 'test' or 'TM1py'
    regex_list = ['^temp_*', '^test*', '^TM1py*']

    # Iterate through cubes
    cubes = tm1.cubes.get_all_names()
    for cube in cubes:
        for regex in regex_list:
            if re.match(regex, cube, re.IGNORECASE):
                tm1.cubes.delete(cube)
                break
            else:
                private_views, public_views = tm1.cubes.views.get_all(cube_name=cube)
                for view in private_views:
                    if re.match(regex, view.name, re.IGNORECASE):
                        tm1.cubes.views.delete(cube_name=cube, view_name=view.name, private=True)
                for view in public_views:
                    if re.match(regex, view.name, re.IGNORECASE):
                        tm1.cubes.views.delete(cube_name=cube, view_name=view.name, private=False)

    # Get Dimension names. Filter out }ElementAttributes and }Hierarchies Dimensions
    dimensions = [dimension for dimension in tm1.dimensions.get_all_names()
                  if not dimension.startswith('}ElementAttributes_') and not dimension.startswith('}Hierarchies_')]
    # Iterate through dimensions
    for dimension in dimensions:
        for regex in regex_list:
            if re.match(regex, dimension, re.IGNORECASE):
                tm1.dimensions.delete(dimension)
                break
            else:
                # Iterate through public subsets
                subsets = tm1.dimensions.subsets.get_all_names(dimension_name=dimension, hierarchy_name=dimension,
                                                               private=False)
                for subset in subsets:
                    if re.match(regex, subset, re.IGNORECASE):
                        tm1.dimensions.subsets.delete(dimension_name=dimension, subset_name=subset, private=False)

    # Iterate through Processes
    processes = tm1.processes.get_all_names()
    for process in processes:
        for regex in regex_list:
            if re.match(regex, process, re.IGNORECASE):
                tm1.processes.delete(process)

