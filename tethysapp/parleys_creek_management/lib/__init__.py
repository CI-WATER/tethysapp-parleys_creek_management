# Utility functions for app

import os

from tethys_apps.utilities import get_dataset_engine


CKAN_ENGINE = get_dataset_engine('default')


def get_package_name():
    """
    Retrieve the package name that will be used to store results.
    Create it if it doesn't exist.
    """
    DEFAULT_PACKAGE_NAME = 'parleys-creek-management-dataset'
    INVALID_CHARS = '~`!@#$%^&*(){}[]_+=?/\\.,:;><|\'\"\t'

    # Context dict
    context = {}

    # Set default package name
    package_name = DEFAULT_PACKAGE_NAME

    for char in INVALID_CHARS:
        package_name = package_name.replace(char, '')

    if package_name == '':
        package_name = DEFAULT_PACKAGE_NAME

    # Check to see if package name already exists
    result = CKAN_ENGINE.get_dataset(DEFAULT_PACKAGE_NAME, console=True)

    # if package_name not in package_list:
    #     package_options = {'name': package_name,
    #                        'notes': 'Dataset that stores results from the Parley\'s Creek Management Tool app.'}
    #     t.get_action('package_create')(context, package_options)

    return package_name


def is_number(s):
    """
    Validate string as a number
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_valid_name(s):
    """
    Validate name strings
    """
    INVALID_CHARS = '~`!$%^&*{}+=?/\\.,:;><|\'\"'
    
    for char in INVALID_CHARS:
        if char in s:
            return False
    
    return True


def is_valid_description(s):
    """
    Validate description strings
    """
    INVALID_CHARS = '~`^*{}_+=/\\><|\'\"'
    
    if s == '':
        return True
    
    for char in INVALID_CHARS:
        if char in s:
            return False
    
    return True