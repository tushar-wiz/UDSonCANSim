# Frame initialisation
fr = [0] * 8

# SID Definitions
SID = {
    "DSC": 0x10,    # Diagnostic Session Control
    "ER": 0x11,     # ECU Reset
    "SA": 0x27,
    "CC": 0x28,
    "TP": 0x3E,     # Tester Present
    "ATP": 0x83,
    "SDT": 0x84,
    "CDTCS": 0x85,  # Control DTC Setting
    "ROE": 0x86,
    "LC": 0x87,
    "RDBI": 0x22,   # Read Data By Identifier
    "RMBA": 0x23,   # Read Memory By Address
    "RSDBI": 0x24,
    "RDBPI": 0x2A,
    "DDDI": 0x2C,
    "WDBI": 0x2E,   # Write Data By Identifier
    "WMBA": 0x3D,   # Write Memory By Address
    "CDTCI": 0x14,  # Clear DTC Information
    "RDTCI": 0x19,  # Read DTC Information
    "IOCBI": 0x2F,
    "RC": 0x31,
    "RD": 0x34,
    "RU": 0x35,
    "TD": 0x36,
    "RTE": 0x37
}

# Subfunctions IDs
SUBFUNC = [
    0x00,
    0x01,
    0x02,
    0x03,
    0x04,
    0x05,
    0x06,
    0x07
]

# Display any 8 byte frame in the terminal


def displayFrame(frame):
    final_string = "\n"
    for i in range(0, 8):
        final_string += "0x{:02X} ".format(frame[i])
    print(final_string)
    return final_string

# Generate a (request) single frame with a DID


def single_frame_did(frame, pci_length, SID, DID, data):
    frame[0] = (0x00) | pci_length
    frame[1] = SID
    frame[2] = (DID >> 8) & 0xFF
    frame[3] = DID & 0xFF
    frame[4] = data[0]
    frame[5] = data[1]
    frame[6] = data[2]
    frame[7] = data[3]

# Generate (request) single frame with subfunction


def single_frame_subf(frame, pci_length, SID, subfunc, data):
    frame[0] = (0x00) | pci_length
    frame[1] = SID
    frame[2] = subfunc
    frame[3] = data[0]
    frame[4] = data[1]
    frame[5] = data[2]
    frame[6] = data[3]
    frame[7] = data[4]

# Generate flow control frames


def flow_control_frame(frame, mode, blockSize, separation_time):
    frame[0] = (0x3 << 4) | mode
    frame[1] = blockSize
    frame[2] = separation_time
    frame[3] = frame[4] = frame[5] = frame[6] = frame[7] = 0xAA

# Generate a negative response


def negative_response_frame(frame, NRC):
    frame[0] = 0x3
    frame[2] = frame[1]
    frame[1] = 0x7F
    frame[3] = NRC
    frame[4] = frame[5] = frame[6] = frame[7] = 0x00
