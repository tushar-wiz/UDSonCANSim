# UDSonCAN Simulator

This project was aimed at creating a set of python scripts that are able to mimic the working of an Electronic Control Unit (ECU) as well as a client script that acts as the tester tool and will be able to generate a predefined set of UDS messages or any custom message desired by the user.

Every frame is required to follow the UDS message format specified within ISO 14229-1. The basic message format is as follows :

Request frame :

![](/media/message%20format%20request.png)

Response frame generated by the server :

![](/media/positive%20response.png)

Negative response generated by the server :

![](/media/negative%20response.png)

## Running the GUI

By running the `main.py` script, the GUI should appear. The project is now ready to use and all interactions can be done on the GUI using buttons and text boxes.

Please note that the projects requires the CustomTkinter library for proper functioning of the GUI.

## Flowchart

# Implementation

There are four seperate python scripts out of which three constitute the backend (`headerfile.py, client.py, server.py`) and the fourth script links them all together and is in charge of the front end GUI (`main.py`).

## headerfile.py

Includes definitions for SIDs.

Includes functions to generate single frames and flow control frames.

Implementations of major ISO-TP frames aswell as a general method for Negative Response frames are available for use.

`fr` is a global array that is supposed to act as the frame throughout every script. This is feasible since the CAN protocol allows only the transmission of a single frame at a time through the BUS and this project is trying to imitate UDSonCAN.

`SID` dictionary can be used to reference any valid UDS service identifiers.
Similarly, `SUBFUNC` tuple is available for subfunctions.

### Methods

```python
def displayFrame(frame)
```

Display any 8 byte frame in the terminal or return an 8 byte frame

```python
def single_frame_did(frame, pci_length, SID, DID, data)
```

Generate a single frame (request frame) that contains a DID

```python
def single_frame_subf(frame, pci_length, SID, subfunc, data)
```

Generate a single frame (request frame) that contains a subfunction

```python
def flow_control_frame(frame, mode, blockSize, separation_time)
```

Generate a flow control frame (CAN-TP/ISO-TP)

```python
def negative_response_frame(frame, NRC)
```

Generate a negative response frame (usage only within server scripts)

## The Client

The client.py script acts as the Tester tool.

General definitions for each type of frame are present.
Manipulate this data and call required functions within headerfile.py to produce a required 8 byte frame.

The text file message.txt is generated which tries to imitate the BUS and is being used here as a medium of frame transfer between the client and server source files. Frames can be transmitted on the bus through the `writeMessage()`method.

The global variable `DATA` is for payload to the any frame generating method within headfile.py.

`suppressPosRspMsgIndicationBit` if made 1, will suppress the response from the server script, i.e, there is no response from the mimicked ECU.

### Methods

```python
def example_sessionControl()
```

Generates a predefined request frame that performs session control.

```python
def example_singleFrame1()
```

Generates a predefined request frame that performs RDBI function.

```python
def writeMessage():
```

Writes the 8 byte frame into message.txt

> NOTE : Only one message can be sent onto the 'BUS' upon the execution of this script. writeMessage() has been programmed to write onto the bus only once and anything previousy present is overwritten.

## The Server

The server.py script acts as the ECU.

The script is able to track active sessions using the `readSession()` function.
Most global variables are just pretend registers to store basic ECU information. Use them as required, names are self-explanatory.

The whole purpose of the server script is to generate and display a response frame in feedback to the most recent frame present within the message.txt file, i.e, the BUS using the `readMessage()` method.

In accordance with this, very primitive implementations of certain positive and negative responses have been implemented.

`currentSession` is a variable that keeps track of the active session.
`stored_SID` array is a list of all SIDs that this server will support.
`registerBank` is a structure that imitates a register bank that stores all valid DIDs aswell as associated data.

### Methods

```python
def ecu_reset_sequence()
def service_present_RDBI()
def service_present_WDBI()
def service_not_supported()
def session_check_fail()
def session_change_fail()
def session_change_pass()
```

Are all different response types to a given request frame.

```python
def readMessage()
```

Reads from the message.txt file, i.e, the _'BUS'_ and stores it in the global frame `fr`.

```python
def writeMessage()
```

Writes the 8 byte frame into message.txt

```python
def readSession()
```

Writes the active session present in the `currentSession` variable into session.txt. This is done mainly to retain the active session everytime the script is compiled.

```python
def writeSession()
```

Reads the active session from session.txt into `currentSession`.

## The GUI

The main.py script makes use of a modified version of the `tkinter` library (CustomTkinter) to generate the GUI.

Both `client.py` and `server.py` are invoked within the main.py script allowing for integration of the two scripts.

The GUI allows for user defined UDS frames to be sent over the BUS or can invoke the example presets present within the client.py file. All activity is displayed on the dialogue box on the left.

![](/media/GUI.png "GUI Window")
