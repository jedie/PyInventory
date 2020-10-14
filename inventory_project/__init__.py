import sys

from inventory import __version__


if __name__ == "inventory_project":
    #
    # This will be called before the click cli
    #
    if "--version" not in sys.argv:
        print(f"PyInventory v{__version__}")

    if len(sys.argv) == 1:
        # FIXME: How can be a "default" action set in click?
        sys.argv.append("run-server")
