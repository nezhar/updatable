import re
import sys
import requests
from datetime import datetime
from subprocess import check_output
from packaging.version import parse

import semantic_version

__all__ = [
    'is_major_update',
    'is_minor_update',
    'is_patch_update',
    'sorted_versions',
    'get_categorized_package_data',
    'get_parsed_environment_package_list',
    'get_environment_requirements_list',
    'parse_requirements_list',
    'get_pypi_package_data',
    'get_package_update_list',
]


def is_major_update(release, package):
    """
    Checks if the release is a major update compared to the package

    :param release: semantic_version.Version
    :param package: semantic_version.Version
    :return: bool
    """
    return release in semantic_version.Spec(">=%s" % package.next_major())


def is_minor_update(release, package):
    """
    Checks if the release is a minor update compared to the package

    :param release: semantic_version.Version
    :param package: semantic_version.Version
    :return: bool
    """
    return release in semantic_version.Spec(">=%s,<%s" % (package.next_minor(), package.next_major()))


def is_patch_update(release, package):
    """
    Checks if the release is a patch update compared to the package

    :param release: semantic_version.Version
    :param package: semantic_version.Version
    :return: bool
    """
    return release in semantic_version.Spec(">=%s,<%s" % (package.next_patch(), package.next_minor()))


def sorted_versions(versions):
    """
    Returns the list of Versions in ascending order

    :param versions: semantic_version.Version[]
    :return: semantic_version.Version[]
    """
    return sorted(versions, key=lambda x: semantic_version.Version.coerce(x['version']), reverse=True)


def get_categorized_package_data(package_data, package_version):
    """
    Returns all Versions grouped by type compared to the current package version

    :param package_data: dict
    :param package_version: semantic_version.Version
    :return: {
        major_updates: semantic_version.Version[]
        minor_updates: semantic_version.Version[]
        patch_updates: semantic_version.Version[]
        pre_release_updates: semantic_version.Version[]
        non_semantic_versions: semantic_version.Version[]
    }
    """
    major_updates = []
    minor_updates = []
    patch_updates = []
    pre_release_updates = []
    non_semantic_versions = []

    for release, info in package_data['releases'].items():
        parsed_release = parse(release)

        upload_time = None
        if info:
            upload_time = datetime.strptime(info[0]['upload_time'], "%Y-%m-%dT%H:%M:%S")

        try:
            # Get semantic version of package
            release_version = semantic_version.Version.coerce(release)

            if not parsed_release.is_prerelease:
                # Place package in the appropriate semantic visioning list
                if is_major_update(release_version, package_version):
                    major_updates.append({
                        'version': release,
                        'upload_time': upload_time,
                    })
                elif is_minor_update(release_version, package_version):
                    minor_updates.append({
                        'version': release,
                        'upload_time': upload_time,
                    })
                elif is_patch_update(release_version, package_version):
                    patch_updates.append({
                        'version': release,
                        'upload_time': upload_time,
                    })
            else:
                pre_release_updates.append({
                    'version': release,
                    'upload_time': upload_time
                })
        except ValueError:
            # Keep track of versions that could not be recognized as semantic
            non_semantic_versions.append({'version': release, 'upload_time': upload_time})

    return {
        'major_updates': sorted_versions(major_updates),
        'minor_updates': sorted_versions(minor_updates),
        'patch_updates': sorted_versions(patch_updates),
        'pre_release_updates': sorted_versions(pre_release_updates),
        'non_semantic_versions': non_semantic_versions,
    }


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
    requirements = check_output([sys.executable, '-m', 'pip', 'freeze'])

    for requirement in requirements.split():
        requirement_list.append(requirement.decode("utf-8"))

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


def get_pypi_package_data(package_name, version=None):
    """
    Get package data from pypi by the package name

    https://wiki.python.org/moin/PyPIJSON

    :param package_name: string
    :param version: string
    :return: dict
    """
    pypi_url = 'https://pypi.org/pypi'

    if version:
        package_url = '%s/%s/%s/json' % (pypi_url, package_name, version, )
    else:
        package_url = '%s/%s/json' % (pypi_url, package_name, )

    try:
        response = requests.get(package_url)
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

    # Get package and version data from pypi
    package_data = get_pypi_package_data(package_name)
    version_data = get_pypi_package_data(package_name, version)

    # Current release specific information
    current_release = ''
    current_release_license = ''

    # Latest release specific information
    latest_release = ''
    latest_release_license = ''

    # Information about packages
    newer_releases = 0
    pre_releases = 0
    categorized_package_data = {
        'major_updates': [],
        'minor_updates': [],
        'patch_updates': [],
        'pre_release_updates': [],
        'non_semantic_versions': [],
    }

    if package_data:
        latest_release = package_data['info']['version']
        latest_release_license = package_data['info']['license'] if package_data['info']['license'] else ''
        categorized_package_data = get_categorized_package_data(package_data, package_version)

        # Get number of newer releases available for the given package, excluding pre_releases and non semantic versions
        newer_releases = len(
            categorized_package_data['major_updates'] +
            categorized_package_data['minor_updates'] +
            categorized_package_data['patch_updates']
        )
        pre_releases = len(categorized_package_data['pre_release_updates'])

    if version_data:
        current_release = version_data['info']['version']
        current_release_license = version_data['info']['license'] if version_data['info']['license'] else ''

    return {
        'current_release': current_release,
        'current_release_license': current_release_license,
        'latest_release': latest_release,
        'latest_release_license': latest_release_license,
        'newer_releases': newer_releases,
        'pre_releases': pre_releases,
        **categorized_package_data,
    }
