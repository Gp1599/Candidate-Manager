import sys
import socket

import Candidate
import CandidateManagerPort
import CandidateStatus
import CandidateManagerMessages

candidate = None
#waitMode = False

# Prints the main menu options
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
def requestCandidateInvariant(clientSocket, ipAddress):
    try:
        clientSocket.connect((ipAddress, CandidateManagerPort.port))
    except ConnectionError:
        print('Error: Cannot find a host with the ip address of ' + ipAddress + '! try again next time.')
        return

    requestMessage = CandidateManagerMessages.createCandidateInvariantRequestMessage()
    clientSocket.send(requestMessage)

    response = clientSocket.recv(1024)
    CandidateManagerMessages.printCandidateInvariantFromMessage(response)
    clientSocket.close()

# Send candidate information to the host and wait for your determined status
def sendCandidate(clientSocket, ipAddress):
    try:
        clientSocket.connect((ipAddress, CandidateManagerPort.port))
    except ConnectionError:
        print('Error: Cannot find a host with the ip address of ' + ipAddress + '! try again next time.')
        return
    
    message = CandidateManagerMessages.createCandidateMessage(candidate)
    clientSocket.send(message)
    
    #if(waitMode):
     #   print('Candidate info sent, wait for the status response...')
     #   statusResponse = clientSocket.recv(1024)
    # 
    #     index = 0
    #     status, index = CandidateManagerMessages.extractIntFromMessage(statusResponse, index)
    #     match status:
    #        case CandidateStatus.accepted:
    #            print('Congradulations, ' + candidate.getName() + '! You have been accepted!')
    #        case CandidateStatus.rejected:
    #            print('Sorry + ' + candidate.getName() + '! You have been rejected!')
    #   else:
    print('Candidate info sent, thank you and if selected, you will be placed in the host\'s candidate selection document')
    clientSocket.close()

#Main program for the candidate manager client
def main():
    global candidate
    global waitMode

    #try:
    #    waitMode = bool(sys.argv[1])
    #    print(waitMode)
    #except Exception:
    #    print('Error: Run the program by typing the following: python3 CandidateManagerClient.py <whether the client should wait for the application response (boolean)>')
    #    return

    #Prompt the user to enter his/her name
    print('Welcome to the Candidate Manager Client!')
    name = input('Enter your name: ')
    
    #Initialize Candidate
    candidate = Candidate.Candidate(name, '')

    #Run a client loop
    ipAddress = input('Enter the host\'s IP Address: ')
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        option = getMainMenuOption()

        match option:
            case '0':
                setNewAttribute();
            case '1':
                requestCandidateInvariant(clientSocket, ipAddress)
                break
            case '2':
                sendCandidate(clientSocket, ipAddress)
                break
            case 'q':
                print('Thank you for using the Candidate Manager Client, bye!')
                break
        
    clientSocket.close()

main()
        