import sys
import socket
import threading

import CandidateManagerPort
import CandidateManagerMessages

import Candidate
import CandidateInvariant
import CandidateSelectionPool

#Represent the organization of received candidates
accepted_candidates = CandidateSelectionPool.CandidateSelectionPool()
waitlisted_candidates = []

#Represents the candidate invariant that the host needs all candidates to satisfy
candidate_invariant = CandidateInvariant.CandidateInvariant()
candidate_invariant_done = False

#Global variable for keeping the program running
running = True 

#The thread function to process received candidates
def recieve_candidates():
    #Initalize the host socket
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_socket.bind(('', CandidateManagerPort.port))
    
    while running:
        host_socket.listen()
        accepted_socket, socketAddress = host_socket.accept()
        packet = accepted_socket.recv(1024)
        #print(packet)

        processMessage(accepted_socket, packet)
        accepted_socket.close()       
    
    host_socket.close()

#Processes the received message
def processMessage(socket, message):
    index = 0
    messagetype, index = CandidateManagerMessages.extractIntFromMessage(message, index)
    match messagetype:
        case 0:
            #Check to see if the received candidate obeys the host's candidate invariant. If it does, accept it. Otherwise, reject it.
            candidate = CandidateManagerMessages.createCandidateFromMessage(message, '', index) #FIXME: Remove the IP Address Parameter Later .
            if candidate_invariant.isObeyedBy(candidate):
                waitlisted_candidates.append(candidate)
        case 1:
            invariantMessage = CandidateManagerMessages.createCandidateInvariantMessage(candidate_invariant)
            socket.send(invariantMessage)

#The main program to run the candidate manager host
def main():
    #Use global variables
    global accepted_candidates
    global candidate_invariant
    global running

    #Welcome the user to the Candidate Manager Host program
    print('Welcome Candidate Manager Host: ')
    #Prompt the user to create the candidate invariant
    promptInvariant()

    #Run the candidate manager host loop
    hostThread = threading.Thread(None, recieve_candidates, 'Candidate Host Thread')
    hostThread.start()

    while running:
        mainMenu()
    
    #Print the closing  message
    print('Thank you. Goodbye!')

def promptInvariant():
    global candidate_invariant
    global candidate_invariant_done

    print()
    print('Create a candidate invariant:')
    while not candidate_invariant_done:
        print('0 - Add invariant attribute')
        print('q - Finish invariant')
        option = input('Please select option: ')

        match option:
            case '0':
                variableName = input('Enter attribute name: ')
                print('Specify the variable type: ')
                print('0 - String (e.g. name)')
                print('1 - Integer Range (e.g. 1-12, 3-5, 11-20)')

                try:
                    variableType = int(input('Enter number: '))
                except TypeError:
                    print('Error: invalid value (must be an integer)!')
                    return
        
                if variableType < 0 or variableType > 1:
                    print('Error: Invalid Value (must be between 0-2)!')
                else:
                    match variableType:
                        case 0:
                            candidate_invariant.addRule(variableName, CandidateInvariant.CandidateInvariantRule())
                        case 1:
                            try:
                                min = int(input('Enter minimum value: '))
                                max = int(input('Enter maximum value: '))
                                candidate_invariant.addRule(variableName, CandidateInvariant.CandidateInvariantIntRangeRule(min, max))
                            except TypeError:
                                print('Error: invalid value; must be an integer')
            case 'q':
                candidate_invariant_done = True
        

#The main menu loop to manage candidates
def mainMenu():
    #Use global variables
    global running

    #Display Main Menu
    print('Main Menu:')
    print('0 - View Waitlisted Candidates')
    print('1 - View Waitlisted Candidate Information')
    print('q - Quit')

    #Prompt the user with the option
    option = input('Please Select valid option: ')

    #Process the specified option
    match option:
        case '0':
            viewWaitlistedCandidates()
        case '1':
            viewWaitlistedCandidateInformation()
        case 'q':
            running = False

def viewWaitlistedCandidates():
    if len(waitlisted_candidates) > 0:
        i = 0
        print('Waitlisted Candidate #\tName')
        for candidate in waitlisted_candidates:
            print(str(i) + '-\t' + candidate.getName())
            i = i + 1
    else:
        print('You currently don\'t have any waitlisted candidates')

def viewWaitlistedCandidateInformation():
    try:
        waitlistedCandidateNumber = int(input('Enter waitlisted candidate number:'))
        candidate = waitlisted_candidates[waitlistedCandidateNumber];
    
        print(candidate.getName())
        for attributeName in candidate.getAttributeNames():
            print(attributeName + ':\t' + candidate.getAttribute(attributeName))

    except TypeError:
        print('Error: The waitlisted candidate number must be an integer')
    except IndexError:
        print('Error: Cannot find waitlisted candidate with an out of bounds number')
    

main() #Run the host main program
