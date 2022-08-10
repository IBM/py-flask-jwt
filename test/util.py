import pkg_resources


def read_file(path):
    file = open(pkg_resources.resource_filename('test.resource', path), 'r')
    return file.read().strip()
