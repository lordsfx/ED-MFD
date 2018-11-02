# Colors
COLOR_ORANGE = (255, 153,  51)
COLOR_GREEN  = ( 51, 255,  51)
COLOR_GREY   = (128, 128, 128)
COLOR_WHITE  = (255, 255, 255)
COLOR_SHADE  = ( 64,  64,  64)

# MFD Layout
#     X L C1 C2 C3 C4 C5 R       Y
# |28|    01 02 03 04 05    |21| T
# |27| 20                06 |22| C1
#      19                07      C2
#      18                08      C3
#      17                09      C4
# |26| 16                10 |23| C5
# |25|    15 14 13 12 11    |24| B

# MFD Button Map
MFD_SYS_FULL   = 1
MFD_ENG_FULL   = 2
MFD_WEP_FULL   = 3
MFD_ENG4_SYS2  = 4
MFD_WEP4_SYS2  = 5
MFD_HEATSINK   = 6
MFD_SILENTRUN  = 7
MFD_CHAFF      = 8
MFD_SHIELDCELL = 9
MFD_DISCOSCAN  = 10
MFD_ORBITLINES = 11
MFD_LIGHTS     = 12
MFD_LANDING    = 13
MFD_DOCKINGREQ = 18
MFD_CARGOSCOOP = 19
MFD_HARDPOINT  = 20

# Positions
MFD_XL1 = 2
MFD_XC1 = 100
MFD_XC2 = 224
MFD_XC3 = 346
MFD_XC4 = 464
MFD_XC5 = 582
MFD_XR1 = 676
MFD_YC1 = 151 #158
MFD_YC2 = 263 #270
MFD_YC3 = 375 #382
MFD_YC4 = 483 #490
MFD_YC5 = 593 #600
MFD_YT1 = 12
MFD_YB1 = 730

MFD_RP_X = 906
MFD_RP_Y = 0
MFD_RP_WIDTH = 374
MFD_RP_HEIGHT = 800

MFD_MP_X = 115
MFD_MP_Y = 100
MFD_MP_WIDTH = 560
MFD_MP_HEIGHT = 600

# Size
FONT_SIZE = 16
BTN_WIDTH = 112
BTN_HEIGHT = 50

# Coriolis images
IMAGE_CORIOLIS_LAYOUT = "images/coriolis-layout-clean.png"
IMAGE_CORIOLIS_PADNUM = "images/coriolis-layout-num.png"

# Coriolis pad positions
#      0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17
X = [ 40,  89, 146, 201, 255, 308, 370, 429, 489, 541, 557, 597, 626, 694, 757 ]
Y = [ 61, 107, 164, 193, 228, 257, 292, 349, 396, 434, 498, 544, 570, 591, 613, 644, 685, 717 ]
CORIOLIS_POS = [
    ( X[6], Y[16],  X[7], Y[17]),	# 01
    ( X[6], Y[14],  X[7], Y[15]),	# 02
    ( X[6], Y[11],  X[7], Y[13]),	# 03
    ( X[6],  Y[9],  X[7], Y[11]),	# 04
    ( X[3], Y[14],  X[5], Y[16]),	# 05
    ( X[3], Y[12],  X[5], Y[14]),	# 06
    ( X[4], Y[10],  X[6], Y[12]),	# 07
    ( X[5],  Y[9],  X[6], Y[10]),	# 08
    ( X[1], Y[10],  X[3], Y[11]),	# 09
    ( X[3],  Y[9],  X[5], Y[10]),	# 10
    ( X[0],  Y[7],  X[1],  Y[8]),	# 11
    ( X[1],  Y[7],  X[2],  Y[8]),	# 12
    ( X[2],  Y[7],  X[3],  Y[8]),	# 13
    ( X[3],  Y[7],  X[4],  Y[8]),	# 14
    ( X[4],  Y[7],  X[5],  Y[8]),	# 15
    ( X[1],  Y[3],  X[2],  Y[4]),	# 16
    ( X[2],  Y[4],  X[4],  Y[5]),	# 17
    ( X[3],  Y[5],  X[5],  Y[6]),	# 18
    ( X[4],  Y[6],  X[6],  Y[7]),	# 19
    ( X[3],  Y[0],  X[5],  Y[1]),	# 20
    ( X[3],  Y[1],  X[5],  Y[3]),	# 21
    ( X[4],  Y[3],  X[6],  Y[4]),	# 22
    ( X[5],  Y[4],  X[6],  Y[6]),	# 23
    ( X[6],  Y[0],  X[7],  Y[1]),	# 24
    ( X[6],  Y[3],  X[7],  Y[4]),	# 25
    ( X[9],  Y[0], X[11],  Y[1]),	# 26
    ( X[8],  Y[1], X[11],  Y[2]),	# 27
    ( X[7],  Y[2],  X[9],  Y[3]),	# 28
    ( X[7],  Y[3],  X[9],  Y[5]),	# 29
    ( X[7],  Y[5],  X[8],  Y[6]),	# 30
    (X[12],  Y[3], X[14],  Y[4]),	# 31
    (X[11],  Y[4], X[13],  Y[5]),	# 32
    ( X[9],  Y[5], X[11],  Y[6]),	# 33
    ( X[7],  Y[6],  X[9],  Y[7]),	# 34
    (X[13],  Y[7], X[14],  Y[8]),	# 35
    (X[12],  Y[7], X[13],  Y[8]),	# 36
    (X[10],  Y[7], X[12],  Y[8]),	# 37
    ( X[8],  Y[7], X[10],  Y[8]),	# 38
    (X[12], Y[10], X[13], Y[11]),	# 39
    ( X[8],  Y[9], X[11], Y[10]),	# 40
    ( X[8], Y[15], X[11], Y[16]),	# 41
    ( X[8], Y[13], X[11], Y[15]),	# 42
    ( X[7], Y[11],  X[9], Y[13]),	# 43
    ( X[7], Y[10],  X[9], Y[11]),	# 44
    ( X[7],  Y[9],  X[8], Y[10]) 	# 45
]

# EDDB data
EDDB_SYSTEMS_DATA  = "eddb/systems_populated.json"
EDDB_STATIONS_DATA = "eddb/stations_filtered.json"

