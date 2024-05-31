import Candidate
import CandidateInvariant

# Creates a message about the candidate to be sent from the client to the host.
def createCandidateMessage(candidate):
    message = bytearray('', 'ascii')

    insertNumberToMessage(message, 0)

    nameBytes = bytearray(candidate.getName(), 'ascii')
    insertNumberToMessage(message, len(nameBytes))

    for attributeName in candidate.getAttributeNames():
        attributeValue = candidate.getAttribute(attributeName)
        insertStringToMessage(message, attributeValue)
    return message

# Creates a candidate read from the specified message.
def createCandidateFromMessage(message, invariant):
    index = 4
    
    name, index = extractStringFromMessage(message, index)
    candidate = Candidate.Candidate(name)

    for attributeName in invariant.getAttributeNames():
        stringValue, index = extractStringFromMessage(message, index)
        candidate.setAttribute(attributeName, stringValue)

    return candidate

# Creates a candidate invariant request for the host.
def createCandidateInvariantRequestMessage():
    message = bytearray('', 'ascii')
    insertNumberToMessage(message, 1)
    return message

# Creates a message that contains the data for the specified invariant.
def createCandidateInvariantMessage(invariant):
    message = bytearray('', 'ascii')

    for attributeName in invariant.getAttributeNames():
        insertStringToMessage(message, attributeName)
        insertStringToMessage(message, invariant.getRule(attributeName))
    
    return message

# Extracts the candidate invariant from the specified message.
def createCandidateInvariantFromMessage(message):
    invariant = CandidateInvariant.CandidateInvariant()

    index = 0
    while(index < len(message)):
        attributeName, index = extractStringFromMessage(message, index)
        attributeRule, index = extractStringFromMessage(message, index)
        invariant.addRule(attributeName, attributeRule)
        
    return invariant

# A utility function that inserts the specified int or float value into the specified message.
def insertNumberToMessage(message, value):
    message += (value >> 24) & 0xFF
    message += (value >> 16) & 0xFF
    message += (value >> 08) & 0xFF
    message += (value >> 00) & 0xFF      

# A utility function that inserts the specified string value into the specified message.
def insertStringToMessage(message, value):
    stringBytes = bytearray(value, 'ascii')
    insertNumberToMessage(message, stringBytes)
    message += stringBytes

# A utility function that extracts an integer from the specified message.
def extractNumberFromMessage(message, index):
    value = 0
    value += (message[index + 0]) << 24
    value += (message[index + 1]) << 16
    value += (message[index + 2]) << 8
    value += (message[index + 3]) << 0
    return value, index + 4

# A utility function that extracts a string from the specified message.
def extractStringFromMessage(message, index):
    length, index = extractNumberFromMessage(message, index)

    value = bytearray('', 'ascii')
    for i in range(0, length):
        value += message[i + index]
    
    return value, index + length
