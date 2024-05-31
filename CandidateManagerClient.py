import sys
import socket

import Candidate
import CandidateManagerPort
import CandidateStatus
import CandidateManagerMessages

candidate = None;

# 
def getMainMenuOption():
    print('Main Menu: ')
    print('0 - \tEnter new attrbiute')
    print('1 - \tRequest candidate invariant')
    print('2 - \tSubmit candidate')
    print('q - \tQuit')
    option = input('Enter option: ')
    return option

# Enter new attrbute or change existing attribute
def setNewAttribute():
    attributeName = input('Enter attribute name: ')
    attributeValue = input('Enter the value of the attrbute: ')
    candidate.setAttribute(attributeName, attributeValue)

# Send the candidate invariant request to the host and recieve and print the requested invariant
def requestCandidateInvariant(clientSocket):
    requestMessage = CandidateManagerMessages.createCandidateInvariantRequestMessage()
    clientSocket.send(requestMessage)

    response, responseIPAddress = clientSocket.recv(1024)
    invariant = CandidateManagerMessages.createCandidateInvariantFromMessage(response)
    
    for attributeName in invariant.getAttributeNames():
        print(attributeName + ": " + invariant[attributeName])

# Send candidate information to the host and wait for your determined status
def sendCandidate(clientSocket):
    message = CandidateManagerMessages.createCandidateMessage(candidate)
    clientSocket.send(message)
    
    print('Candidate info sent, wait for the status response...')
    statusResponse, responseIP = clientSocket.recv(1024)
    
    status, index = CandidateManagerMessages.extractNumberFromMessage(statusResponse, 0)
    match status:
        case CandidateStatus.accepted:
            print('Congradulations, ' + candidate.getName() + '! You have been accepted!')
        case CandidateStatus.rejected:
            print('Sorry + ' + candidate.getName() + '! You have been rejected!')



#Main program for the candidate manager client
def main():
    global candidate
    #Prompt the user to enter his/her name
    print('Welcome to the Candidate Manager Client!')
    name = input('Enter your name: ')
    
    #Initialize Candidate
    candidate = Candidate.Candidate(name)

    #Run a client loop
    ipAddress = input('Enter the host\'s IP Address: ')
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect(ipAddress, CandidateManagerPort.port)
    except ConnectionError:
        print('Error: Cannot find a host with the ip address of ' + ipAddress + '! try again next time.')
        return

    while True:
        option = getMainMenuOption()

        match option:
            case '0':
                setNewAttribute();
            case '1':
                requestCandidateInvariant(clientSocket)
            case '2':
                sendCandidate()
                break
            case 'q':
                print('Thank you for using the Candidate Manager Client, bye!')
                break
        
    clientSocket.close()
        