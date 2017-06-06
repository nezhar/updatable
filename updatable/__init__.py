import re
import argparse
import requests
import semantic_version

from datetime import datetime
from pip.operations import freeze

__author__ = "Harald Nezbeda (hn@nezhar.com)"
__version__ = "0.1.3"


def get_parsed_environment_package_list():
    """
    Get a parsed list of packages in the current environment

    :return:
    """
    return parse_requirements_list(
        get_environment_requirements_list()
    )


def get_environment_requirements_list():
    """
    Take the requirements list from the current running environment

    :return: string
    """
    requirement_list = []
    requirements = freeze.freeze()

    for requirement in requirements:
        requirement_list.append(requirement)

    return requirement_list


def parse_requirements_list(requirements_list):
    """
    Take a list and return a list of dicts with {package, versions) based on the requirements specs

    :param requirements_list: string
    :return: string
    """
    req_list = []

    for requirement in requirements_list:
        requirement_no_comments = requirement.split('#')[0].strip()

        # if matching requirement line (Thing==1.2.3), update dict, continue
        req_match = re.match(
            r'\s*(?P<package>[^\s\[\]]+)(?P<extras>\[\S+\])?==(?P<version>\S+)',
            requirement_no_comments
        )
        if req_match:
            req_list.append({
                'package': req_match.group('package'),
                'version': req_match.group('version'),
            })

    return req_list


def get_pypi_package_data(package_name):
    """
    Get package data from pypi by the package name

    https://wiki.python.org/moin/PyPIJSON

    :param package_name: string
    :return: dict
    """
    try:
        response = requests.get('https://pypi.python.org/pypi/%s/json' % package_name)
    except requests.ConnectionError:
        raise RuntimeError('Connection error!')

    # Package not available on pypi
    if not response.ok:
        return None

    return response.json()


def get_package_update_list(package_name, version):
    """
    Return update information of a package from a given version

    :param package_name: string
    :param version: string
    :return: dict
    """
    package_version = semantic_version.Version.coerce(version)
    data = get_pypi_package_data(package_name)

    major_updates = []
    minor_updates = []
    patch_updates = []
    non_semantic_versions = []

    if data:
        for release, info in data['releases'].items():
            upload_time = None
            if info:
                upload_time = datetime.strptime(info[0]['upload_time'], "%Y-%m-%dT%H:%M:%S")

            try:
                # Get semantic version of package
                release_version = semantic_version.Version.coerce(release)

                # Place package in the appropriate semantic visioning list
                if release_version in semantic_version.Spec(">=%s" % package_version.next_major()):
                    major_updates.append({
                        'version': release,
                        'upload_time': upload_time,
                    })
                elif release_version in semantic_version.Spec(">=%s,<%s" % (package_version.next_minor(), package_version.next_major())):
                    minor_updates.append({
                        'version': release,
                        'upload_time': upload_time,
                    })
                elif release_version in semantic_version.Spec(">=%s,<%s" % (package_version.next_patch(), package_version.next_minor())):
                    patch_updates.append({
                        'version': release,
                        'upload_time': upload_time,
                    })
            except ValueError:
                # Keep track of versions that could not be recognized as semantic
                non_semantic_versions.append({'version': release, 'upload_time': upload_time})

    # Get number of newer releases available for the given package
    newer_releases = len(major_updates + minor_updates + patch_updates)

    return {
        'latest_release': data['info']['version'],
        'newer_releases': newer_releases,
        'major_updates': sorted(major_updates, key=lambda x: semantic_version.Version.coerce(x['version']), reverse=True),
        'minor_updates': sorted(minor_updates, key=lambda x: semantic_version.Version.coerce(x['version']), reverse=True),
        'patch_updates': sorted(patch_updates, key=lambda x: semantic_version.Version.coerce(x['version']), reverse=True),
        'non_semantic_versions': non_semantic_versions,
    }


def __list_package_updates(package_name, version):
    """
    Function used to list all package updates in console

    :param package_name: string
    :param version: string
    """

    updates = get_package_update_list(package_name, version)

    if updates['newer_releases']:
        print('%s (%s)' % (package_name, version))
        __list_updates('Major releases', updates['major_updates'])
        __list_updates('Minor releases', updates['minor_updates'])
        __list_updates('Patch releases', updates['patch_updates'])
        __list_updates('Unknown releases', updates['non_semantic_versions'])
        print("___")


def __list_updates(update_type, update_list):
    """
    Function used to list package updates by update type in console

    :param update_type: string
    :param update_list: list
    """
    if len(update_list):
        print("  %s:" % update_type)
        for update_item in update_list:
            print("  -- %(version)s on %(upload_time)s" % update_item)


def __updatable():
    """
    Function used to output packages update information in the console
    """
    # Add argument for console
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', type=argparse.FileType(), default=None, help='Requirements file')
    args = parser.parse_args()

    # Get list of packages
    if args.file:
        packages = parse_requirements_list(args.file)
    else:
        packages = get_parsed_environment_package_list()

    # Output updates
    for package in packages:
        __list_package_updates(package['package'], package['version'])

if __name__ == '__main__':
    __updatable()
