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
    while running:
        accepted_socket, socketAddress = host_socket.accept()
        packet, clientAddr = accepted_socket.recv(1024)

        processMessage(accepted_socket, packet)
        accepted_socket.close()        
    
    host_socket.close()

#Processes the received message
def processMessage(socket, message):
    messagetype = CandidateManagerMessages.extractIntFromMessage(message, 0)
    match messagetype:
        case 0:
            #Check to see if the received candidate obeys the host's candidate invariant. If it does, accept it. Otherwise, reject it.
            candidate = CandidateManagerMessages.createCandidateFromMessage(message) 
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

#Represents the set of folders that will be used by the host to contain and process accepted candidates
class CandidateSelection:
    def __init__(self, folderNames):
        self.folders = {}
        for folderName in folderNames:
            self.folders[folderName] = []
    
    #Returns the candidate selection's folders
    def getFolders(self):
        pass

    #Moves the candidate at the source folder's index to the destination folder
    def moveCandidate(self, candidateName, srcFolder, destFolder):
        pass

def promptInvariant():
    global candidate_invariant
    global candidate_invariant_done

    print()
    print('Create a candidate invariant:')
    while True:
        variableName = input('Enter variable name(enter _quit to finish the invariant): ')
        if(variableName == '_quit'):
            candidate_invariant_done = True
            break

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
                    candidate_invariant.addRule(variableName, CandidateInvariant.CandidateInvariantStringRule())
                case 1:
                    try:
                        min = int(input('Enter minimum value: '))
                        max = int(input('Enter maximum value: '))
                        candidate_invariant.addRule(variableName, CandidateInvariant.CandidateInvariantIntRangeRule(min, max))
                    except TypeError:
                        print('Error: invalid value; must be an integer')
        

#The main menu loop to manage candidates
def mainMenu():
    #Use global variables
    global running

    #Display Main Menu
    print('Main Menu:')
    print('0 - View Candidates')
    print('1 - View Candidate Information')
    print('q - Quit')

    #Prompt the user with the option
    option = input('Please Select valid option: ')

    #Process the specified option
    if(option == 'q'):
        running = False


main() #Run the host main program
