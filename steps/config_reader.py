from json import load as _load


def read_config(path):
    """
    Reads configuration from json file
    :param path: path of the json file
    :return: python dict of the json configuration
    """
    with open(path, "r") as config_file:
        return _load(config_file)