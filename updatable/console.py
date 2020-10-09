import argparse

from updatable import utils as updatable_utils


def _str_to_bool(value):
    """
    Converts a string into a bool

    :param pacvaluekage_name: string
    """
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected!')


def _list_package_updates(package_name, version, show_pre_releases=False):
    """
    Function used to list all package updates in console

    :param package_name: string
    :param version: string
    :param show_pre_releases bool
    """
    updates = updatable_utils.get_package_update_list(package_name, version)
    has_displayed_updates = updates['newer_releases'] or (show_pre_releases and updates['pre_releases'])
    current_release_license = updates["current_release_license"]

    if has_displayed_updates:
        print('%s (%s) - License: %s' % (package_name, version, current_release_license))

    if updates['newer_releases']:
        _list_updates('Major releases', updates['major_updates'], current_release_license)
        _list_updates('Minor releases', updates['minor_updates'], current_release_license)
        _list_updates('Patch releases', updates['patch_updates'], current_release_license)
        _list_updates('Unknown releases', updates['non_semantic_versions'], current_release_license)
        has_displayed_updates = True

    if show_pre_releases and updates['pre_releases']:
        _list_updates('Pre releases', updates['pre_release_updates'], current_release_license)
        has_displayed_updates = True

    if has_displayed_updates:
        print("___")


def _list_updates(update_type, update_list, current_release_license):
    """
    Function used to list package updates by update type in console

    :param update_type: string
    :param update_list: list
    :param current_release_license: string
    """
    if len(update_list):
        print("  %s:" % update_type)
        for update_item in update_list:
            print("  -- %s on %s - License: %s" % (update_item['version'], update_item['upload_time'],
                                                   current_release_license,))


def _updatable():
    """
    Function used to output packages update information in the console
    """
    # Add argument for console
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', nargs='?', type=argparse.FileType(), default=None, help='Requirements file')
    parser.add_argument('-pr', '--pre-releases', nargs='?', type=_str_to_bool, default=False, help='Show pre-releases')
    args = parser.parse_args()

    # Get list of packages
    if args.file:
        packages = updatable_utils.parse_requirements_list(args.file)
    else:
        packages = updatable_utils.get_parsed_environment_package_list()

    # Output updates
    for package in packages:
        _list_package_updates(package['package'], package['version'], args.pre_releases)
