from headerfile import *

# General definitions
currentSession = 0x01  # Default session

# Define all valid SIDs for this server
stored_SID = [0x22, 0x3E, 0x2E, 0x10, 0x11]

# All valid DIDs with corresponding virual register values


class registerBank:
    def __init__(self, stored_DID, data, session_requirement):
        self.stored_DID = stored_DID
        self.data = data
        self.session_requirement = session_requirement


m = []
m.append(registerBank(0x01401, 0x1F, 0x01))
m.append(registerBank(0x01402, 0x2F, 0x01))
m.append(registerBank(0x01403, 0x3F, 0x01))
m.append(registerBank(0x01404, 0x4F, 0x03))
m.append(registerBank(0x01405, 0x5F, 0x03))

# Test cases


def ecu_reset_sequence():
    for i in range(0, 5):
        m[i].data = 16*(i+1) + 0xF
    fr[2] = 0x1
    writeSession()

    fr[0] = 0x3
    fr[1] = fr[1] + 0x40
    fr[3] = 0x5
    fr[4] = fr[5] = fr[6] = fr[7] = 0x00

    return "\nPositive response : ECU will be reset, power down time is 5s"


def service_present_RDBI():
    flagD = 0
    searchDID = (fr[2] << 8) | fr[3]
    for i in range(0, 5):
        if m[i].stored_DID == searchDID:
            flagD = i+1
            break

    if searchDID == 0xF186:
        fr[0] = 0x4
        fr[1] = fr[1] + 0x40
        fr[4] = currentSession
        fr[5] = fr[6] = fr[7] = 0x00
        return "\nPositive Response :-"
    elif flagD:
        if m[flagD - 1].session_requirement == currentSession:
            fr[0] = 0x4
            fr[1] = fr[1] + 0x40
            fr[4] = m[flagD - 1].data
            fr[5] = fr[6] = fr[7] = 0x00
            return "\nPositive Response :-"
        else:
            return session_check_fail()
    else:
        negative_response_frame(fr, 0x31)
        return "\nNegative Response :- NRC : Request Out of Range"


def service_present_WDBI():
    flagD = 0
    searchDID = (fr[2] << 8) | fr[3]
    for i in range(0, 5):
        if m[i].stored_DID == searchDID:
            flagD = i+1
            break
    if flagD:
        if m[flagD - 1].session_requirement == currentSession:
            m[flagD - 1].data = fr[4]
            fr[0] = 0x4
            fr[1] = fr[1] + 0x40
            fr[4] = m[flagD - 1].data
            fr[5] = fr[6] = fr[7] = 0x00
            return "\nPositive Response :-"
        else:
            return session_check_fail()
    else:
        negative_response_frame(fr, 0x31)
        return "\nNegative Response :- NRC : Request Out of Range"


def service_not_supported():
    negative_response_frame(fr, 0x11)
    return "\nNegative Response :- NRC : Service Not Supported"


def session_check_fail():
    negative_response_frame(fr, 0x7F)
    return "\nNegative Response :- NRC : Request Unavailable in Active Session"


def session_change_fail():
    negative_response_frame(fr, 0x22)
    return "\nNegative Response :- NRC : Conditions Not Correct"


def session_change_pass():
    fr[0] = 0x04
    fr[1] = fr[1] + 0x40
    fr[7] = 0x00
    if fr[2] == 0x01:
        fr[3] = 0xFF
        fr[4] = 0xFF
        fr[5] = 0xFF
        fr[6] = 0xFF
    else:
        fr[3] = 0x02
        fr[4] = 0xAA
        fr[5] = 0x02
        fr[6] = 0xAA

    return "\nPositive Response :-"

# ----------------------------------------------------

# File operations


def readMessage():
    with open('message.txt', 'r') as filehandle:
        lines = filehandle.read().splitlines()
    for i in range(0, 8):
        fr[i] = int(lines[i])


def writeMessage():
    with open('message.txt', 'w+') as filehandle:
        for item in fr:
            filehandle.write(f'{item}\n')


def readSession():
    with open('session.txt', 'r') as filehandle:
        lines = filehandle.read()
    global currentSession
    currentSession = int(lines)


def writeSession():
    with open('session.txt', 'w+') as filehandle:
        filehandle.write(f'{fr[2]}\n')

# ----------------------------------------------------


# if __name__ == "__main__":
#     main()
