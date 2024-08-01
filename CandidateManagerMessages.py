import Candidate
import CandidateInvariant

# Creates a message about the candidate to be sent from the client to the host.
def createCandidateMessage(candidate):
    message = bytearray('', 'ascii')

    insertIntToMessage(message, 0)
    insertStringToMessage(message, candidate.getName())

    for attributeName in candidate.getAttributeNames():
        attributeValue = candidate.getAttribute(attributeName)
        insertStringToMessage(message, attributeName)
        insertStringToMessage(message, attributeValue)

    return message

# Creates a candidate read from the specified message.
def createCandidateFromMessage(message, ipAddress, index):
    name, index = extractStringFromMessage(message, index)
    candidate = Candidate.Candidate(name, ipAddress)

    while index < len(message):
        attributeName, index = extractStringFromMessage(message, index)
        attributeValue, index = extractStringFromMessage(message, index)
        candidate.setAttribute(attributeName, attributeValue)

    return candidate

# Creates a candidate invariant request for the host.
def createCandidateInvariantRequestMessage():
    message = bytearray('', 'ascii')
    insertIntToMessage(message, 1)
    return message

# Creates a message that contains the data for the specified invariant.
def createCandidateInvariantMessage(invariant):
    message = bytearray('', 'ascii')

    for attributeName in invariant.getAttributeNames():
        insertStringToMessage(message, attributeName)
        insertStringToMessage(message, invariant.getRule(attributeName).display())
    
    return message

# Extracts the candidate invariant from the specified message.
def printCandidateInvariantFromMessage(message):
    index = 0
    while(index < len(message)):
        attributeName, index = extractStringFromMessage(message, index)
        attributeRule, index = extractStringFromMessage(message, index)
        print(attributeName + ": " + attributeRule)

# A utility function that inserts the specified int or float value into the specified message.
def insertIntToMessage(message, value):
    byte8 = (value >>24) & 0xFF
    byte4 = (value >> 16) & 0xFF
    byte2 = (value >> 8) & 0xFF
    byte1 = (value >> 0) & 0xFF

    message.append(byte8)
    message.append(byte4)
    message.append(byte2)
    message.append(byte1)      

# A utility function that inserts the specified string value into the specified message.
def insertStringToMessage(message, value):
    stringBytes = value.encode('ascii')
    insertIntToMessage(message, len(stringBytes))
    for byte in stringBytes:
        message.append(byte)

# A utility function that extracts an integer from the specified message.
def extractIntFromMessage(message, index):
    value = 0
    value = value + (message[index + 0]) << 24
    value = value + (message[index + 1]) << 16
    value = value + (message[index + 2]) << 8
    value = value + (message[index + 3]) << 0
    return value, index + 4

# A utility function that extracts a string from the specified message.
def extractStringFromMessage(message, index):
    length, index = extractIntFromMessage(message, index)

    value = bytearray('', 'ascii')
    for i in range(0, length):
        value.append(message[i + index])
    
    return value.decode(), index + length

# Tests the specified test case to see whether it is satisfied
def test(elements):
   message = bytearray('', 'ascii') 
   for element in elements:
        if type(element) == int:
            insertIntToMessage(message, int(element))
        else:
            insertStringToMessage(message, element)
   index = 0
   equalityCount = 0 
   for element in elements:
        if type(element) == int:
           extr, index = extractIntFromMessage(message, index)
           if int(element) == extr:
               equalityCount = equalityCount + 1
        else:
            extr, index = extractStringFromMessage(message, index)
            if element == extr:
                equalityCount = equalityCount + 1 
   return equalityCount >= len(elements)

#Tests the message creation and extraction modules
def runTests():
    testcases = [
        ['Hello World!'], 
        [3, 5, 4], 
        ['String!', 3], 
        ['Rock', 1, 'Paper', 2, 'Scissors', 3]
        ]

    for i in range(0, len(testcases)):
        print('Test Case ' + str(i + 1) + ': ' + str(test(testcases[i])))

runTests()
