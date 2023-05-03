from headerfile import *

# General definition
# PCI = 0x00
DATA_ARRAY = [0]*6

# Sub function definitions
# SUBFUNCTION = 0xFF
suppressPosRspMsgIndicationBit = 0

# Flow control definitions
# MODE = 0
# BLOCKSIZE = 0
# ST = 0

# ----------------------------------------------------


def example_sessionControl():
    PCI = 0x2
    DATA_ARRAY[0] = DATA_ARRAY[1] = DATA_ARRAY[2] = DATA_ARRAY[3] = DATA_ARRAY[4] = DATA_ARRAY[5] = 0x00
    SUBFUNCTION = SUBFUNC[1] | (suppressPosRspMsgIndicationBit << 7)
    single_frame_subf(fr, PCI, SID["DSC"], SUBFUNCTION, DATA_ARRAY)


def example_singleFrame1():
    PCI = 0x3
    single_frame_did(fr, PCI, SID["RDBI"], 0x1402, DATA_ARRAY)

# ----------------------------------------------------

# File operations


def writeMessage():
    with open('message.txt', 'w+') as filehandle:
        for item in fr:
            filehandle.write(f'{item}\n')
