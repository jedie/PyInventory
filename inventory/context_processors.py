from inventory import __version__


def inventory_version_string(request):
    return {'inventory_version_string': f'v{__version__}'}
