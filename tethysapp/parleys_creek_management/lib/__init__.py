# Utility functions for app

import os, ConfigParser


# def get_package_name():
#     """
#     Retrieve the package name that will be used to store results.
#     Create it if it doesn't exist.
#     """
#     DEFAULT_PACKAGE_NAME = 'parleys-creek-management-app-dataset'
#     CONFIG_NAME = 'app.ini'
#     CONFIG_DATASET_SECTION = 'dataset'
#     DATASET_NAME_PARAMETER = 'ckan_dataset_name'
#     INVALID_CHARS = '~`!@#$%^&*(){}[]_+=?/\\.,:;><|\'\"     '
#
#     # Context dict
#     context = {}
#
#     # Get package name from app.ini
#     app_config = ConfigParser.SafeConfigParser()
#     config_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), CONFIG_NAME)
#     app_config.read(config_path)
#
#     # Set default package name
#     package_name = DEFAULT_PACKAGE_NAME
#
#     # Attempt to get user defined package name if not in config
#     if app_config.has_option(CONFIG_DATASET_SECTION, DATASET_NAME_PARAMETER):
#         package_name = app_config.get(CONFIG_DATASET_SECTION, DATASET_NAME_PARAMETER)
#
#     for char in INVALID_CHARS:
#         package_name = package_name.replace(char, '')
#
#     if package_name == '':
#         package_name = DEFAULT_PACKAGE_NAME
#
#     # Check to see if package name already exists
#     package_list_options = {}
#     package_list = t.get_action('package_list')(context, package_list_options)
#
#     if package_name not in package_list:
#         package_options = {'name': package_name,
#                            'notes': 'Dataset that stores results from the Parley\'s Creek Management Tool app.'}
#         t.get_action('package_create')(context, package_options)
#
#     return package_name


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