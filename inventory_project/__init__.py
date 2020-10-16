"""
    Just print version line on every call from commandline ;)
"""

import sys

from inventory import __version__


if __name__ == "inventory_project":
    if "--version" not in sys.argv:
        print(f"PyInventory v{__version__}")
