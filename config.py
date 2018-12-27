import logging

# Debug Level
LOG_LEVEL = logging.DEBUG
LOG_FILE = "mfd-debug.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Version
MFD_VER = "1.5.0 (E:D 3.3)"

# Fonts
#DEFAULT_FONT = "fonts/Eurostile.ttf"
DEFAULT_FONT = "fonts/Calibri.ttf"
DEFAULT_FONT_BOLD = "fonts/Calibri Bold.ttf"

# Default display size
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 800

# MFD images
IMAGE_WALLPAPER = "images/MFD-Display-wallpaper.png"
IMAGE_BUTTON = "images/MFD-Display-button-s1.png"
IMAGE_MODE = "images/MFD-Display-mode-status.png"
IMAGE_MODE_DARK = "images/MFD-Display-mode-status-dark.png"
IMAGE_STICK_BUTTON = "images/MFD-Display-stick-button.png"
IMAGE_FSS = "images/MFD-Display-FSS.png"
IMAGE_ED_LOGO = "images/EliteDangerous_Logo.png"

# Coriolis images
IMAGE_CORIOLIS_LAYOUT = "images/coriolis-layout-clean.png"
IMAGE_CORIOLIS_PADNUM = "images/coriolis-layout-num.png"

# EDDB source
EDDB_SYSTEMS_SOURCE  = "https://eddb.io/archive/v5/systems_populated.json"
EDDB_STATIONS_SOURCE = "https://eddb.io/archive/v5/stations.json"

# EDDB data
EDDB_PATH = "eddb"
EDDB_SYSTEMS_DATA  = "systems_populated.json"
EDDB_STATIONS_PRE  = "stations.json"
EDDB_STATIONS_DATA = "stations_filtered.json"
