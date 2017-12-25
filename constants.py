# Colors
COLOR_ORANGE = (255, 153,  51)
COLOR_GREEN  = ( 51, 255,  51)
COLOR_GREY   = (128, 128, 128)
COLOR_WHITE  = (255, 255, 255)

# MFD Layout
#     X L C1 C2 C3 C4 C5 R       Y
# |28|    01 02 03 04 05    |21| T
# |27| 20                06 |22| C1
#      19                07      C2
#      18                08      C3
#      17                09      C4
# |26| 16                10 |23| C5
# |25|    15 14 13 12 11    |24| B

# Positions
MFD_XL1 = 2
MFD_XC1 = 100
MFD_XC2 = 224
MFD_XC3 = 346
MFD_XC4 = 464
MFD_XC5 = 582
MFD_XR1 = 676
MFD_YC1 = 158
MFD_YC2 = 270
MFD_YC3 = 382
MFD_YC4 = 490
MFD_YC5 = 600
MFD_YT1 = 12
MFD_YB1 = 730
MFD_RP_X = 906
MFD_RP_Y = 0
MFD_RP_WIDTH = 380
MFD_RP_HEIGHT = 800

# Size
FONT_SIZE = 16

# Coriolis pad positions
# X = 41, 91, 146, 206, 259, 310, 375, 421, 486, 513, 538, 567, 597, 626, 703, 757
# Y = 65, 108, 164, 194, 228, 258, 293, 350, 396, 497, 551, 584, 643, 685, 716
CORIOLIS_POS = [
    (375, 685, 421, 716)
]
