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

# ----------------------------------------------------

# MAIN


def main():
    # imitate reading bus data
    readMessage()

    # configure active session as last used session
    readSession()

    flagS = 0
    for i in range(0, 5):
        if stored_SID[i] == fr[1]:
            flagS = 1
            break

    if(flagS):
        if fr[1] == 0x10:
            if fr[2] == 0x02 and currentSession == 0x01:
                session_change_fail()  # defaultSession to programmingSession is unallowed
            else:
                session_change_pass()
                writeSession()
        else:
            service_present()
    else:
        service_not_supported()

    displayFrame(fr)
    writeSession()

# ----------------------------------------------------

# Test cases


def service_present():
    flagD = 0
    searchDID = (fr[2] << 8) | fr[3]
    for i in range(0, 5):
        if m[i].stored_DID == searchDID:
            flagD = i+1
            break

    if searchDID == 0xF186:
        print("\nPositive Response :-")
        fr[0] = 0x4
        fr[1] = fr[1] + 0x40
        fr[4] = currentSession
        fr[5] = fr[6] = fr[7] = 0x00
    elif flagD:
        if m[flagD - 1].session_requirement == currentSession:
            print("\nPositive Response :-")
            fr[0] = 0x4
            fr[1] = fr[1] + 0x40
            fr[4] = m[flagD - 1].data
            fr[5] = fr[6] = fr[7] = 0x00
        else:
            session_check_fail()
    else:
        print("\nNegative Response :- NRC : Request Out of Range")
        negative_response_frame(fr, 0x31)


def service_not_supported():
    print("\nNegative Response :- NRC : Service Not Supported")
    negative_response_frame(fr, 0x11)


def session_check_fail():
    print("\nNegative Response :- NRC : Request Unavailable in Active Session")
    negative_response_frame(fr, 0x7F)


def session_change_fail():
    print("\nNegative Response :- NRC : Conditions Not Correct")
    negative_response_frame(fr, 0x22)


def session_change_pass():
    print("\nPositive Response :-")
    fr[0] = 0x04
    fr[1] = fr[1] + 0x40
    fr[3] = fr[4] = fr[5] = fr[7] = fr[7] = 0x00

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


if __name__ == "__main__":
    main()
