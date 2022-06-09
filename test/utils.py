import os

PATH = os.path.dirname(os.path.realpath(__file__))
TEST_REQUIREMENTS_PATH = os.path.join(PATH, "fixtures/requirements-initial.txt")


def get_environment_requirements_list_monkey(*args, **kwargs):
    with open(TEST_REQUIREMENTS_PATH) as f:
        content = f.readlines()

    return content
