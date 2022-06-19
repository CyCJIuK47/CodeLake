import sys
from os.path import dirname

sys.path.append(dirname(__file__))

import widgets
from settings_menu import SettingsMenu, Settings

__all__ = ["SettingsMenu", "Settings", "widgets"]
__version__ = "1.0"
__author__ = "CyCJIuK47"