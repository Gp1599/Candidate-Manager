import sys
import socket
import threading

import Candidate
import CandidateInvariant
import CandidateManagerPort

#Represent the organization of received candidates
accepted_candidates = None
waitlisted_candidates = []
received_candidates = []

#Represents the candidate invariant that the host needs all candidates to satisfy
candidate_invariant = CandidateInvariant.CandidateInvariant()

#Global variable for keeping the program running
running = True 

#The thread function to process received candidates
def recieve_candidates():
    #Initalize the host socket
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while running:
        packet, clientAddr = host_socket.recv(1024)

        #Check to see if the received candidate obeys the host's candidate invariant. If it does accept it. Otherwise, reject it.
    
    host_socket.close()

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
    hostThread = threading.Thread('Candidate Host Thread', recieve_candidates)
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

    print('Create a candidate invariant:')
    while True:
        variableName = input('Enter variable name: ')
        if(variableName == '_quit'):
            break

        print('Specify the variable type: ')
        print('0 - String (e.g. age, name)')
        print('1 - Integer (e.g. 1 3, 11)')
        print('2 - Decimal (e.g. 1.2)')

        try:
            variableType = int(input('Enter number: '))
            if variableType < 0 or variableType > 2:
                print('Error: Invalid Value (must be between 0-2)!')
            else:
                candidate_invariant.addRule(variableName, variableType)
        except Exception:
            print('Error: invalid value (must be an integer)!')

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


main() #Run the host (main programi
