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

#A stage of the host program that prompts the user to create the candidate invariant that will be used throughout the stage of processing received candidates.
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
        

#The main menu loop to manage candidates.
def mainMenu():
    #Use global variables
    global running

    #Display Main Menu
    print('Main Menu:')
    print('0 - View Waitlisted Candidates')
    print('1 - View Waitlisted Candidate Information')
    print('2 - Add Selection Folder')
    print('3 - Remove Selection Folder')
    print('4 - Move Candidate From Waitlist to Selection Folder')
    print('5 - Move Candidate From Selection Folder to Selection Folder')
    print('6 - Move Candidate From Selection Folder to Waitlist')
    print('7 - Display Selection Folder')
    print('8 - Display Selection Pool')
    print('q - Quit')

    #Prompt the user with the option
    option = input('Please Select valid option: ')

    #Process the specified option
    match option:
        case '0':
            viewWaitlistedCandidatesOption()
        case '1':
            viewWaitlistedCandidateInformationOption()
        case '2':
            addFolderOption()
        case '3':
            removeFolderOption()
        case '4':
            moveCandidateFromWaitlistToSelectionOption()
        case '5':
            moveCandidateFromSelectionToSelectionOption()
        case '6':
            moveCandidateFromSelectionToWaitlistOption()
        case '7':
            displaySelectionFolderOption()
        case '8':
            displaySelectionOption()
        case 'q':
            running = False

#Prints a table that has columns containing each candidate's ID number and name.
def viewWaitlistedCandidatesOption():
    if len(waitlisted_candidates) > 0:
        i = 0
        print('Waitlisted Candidate #\tName')
        for candidate in waitlisted_candidates:
            print(str(i) + '-\t\t\t' + candidate.getName())
            i = i + 1
    else:
        print('You currently don\'t have any waitlisted candidates')
    print()

#Prompts the user for the condidate's ID number and prints information about that candidate.
def viewWaitlistedCandidateInformationOption():
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
    print()
    
#Prompts the user for the name of the new folder and adds the new folder with that name.
def addFolderOption():
    folderName = input('Enter folder name: ')
    accepted_candidates.addFolder(folderName)
    print()

#Prompts the user for the name of the folder that he or she wants to delete and deletes that folder if it exists.
def removeFolderOption():
    folderName = input('Enter folder name: ')
    try:
        accepted_candidates.removeFolder(folderName)
    except:
        print('Error: Cannot find selection folder named ' + folderName)
    print()

#Promtps the user for the ID number of a candidate in the waitlist and the name of the destination folder and moves the candidate with that number into that folder.
def moveCandidateFromWaitlistToSelectionOption():
    folderName = ''
    try:
        candidateNumber = int(input('Enter candidate number: '))
        folderName = input('Enter folder name: ')
        accepted_candidates.addCandidate(folderName, waitlisted_candidates, candidateNumber)
    except TypeError:
        print('Error: invalid input for a candidate number (must be an integer greater than or equal to 0)')
    except IndexError:
        print('Error: cannot find a candidate with the number that is out of bounds')
    except KeyError:
        print('Error: cannot find a selection folder named ' + folderName)
    print()

#Prompts the user for the name of the source folder, the ID number of the candidate in the waitlist, and the name of the destination folder and moves the candidate with that ID number from the source folder to the destination folder.
def moveCandidateFromSelectionToSelectionOption():
    try:
        srcFolderName = input('Enter source folder name: ')
        candidateNumber = int(input('Enter candidate number: '))
        destFolderName = input('Enter folder name: ')
        accepted_candidates.swap(srcFolderName, destFolderName, candidateNumber)
    except TypeError:
        print('Error: invalid input for a candidate number (must be an integer greater than or equal to 0)')
    except IndexError:
        print('Error: cannot find a candidate with the number that is out of bounds')
    except KeyError:
        print('Error: cannot find a selection folder')
    print()

#Prompts the user for the name of the source folder and the ID number of the candidate in that folder and moves the candidate with that ID number back into the waitlist
def moveCandidateFromSelectionToWaitlistOption():
    folderName = ''
    try:
        folderName = input('Enter folder name: ')
        candidateNumber = int(input('Enter candidate number: '))
        accepted_candidates.removeCandidate(folderName, waitlisted_candidates, candidateNumber)
    except TypeError:
        print('Error: invalid input for a candidate number (must be an integer greater than or equal to 0)')
    except IndexError:
        print('Error: cannot find a candidate with the number that is out of bounds')
    except KeyError:
        print('Error: cannot find a selection folder named ' + folderName)
    print()

#Prompts the user for the name of the selection folder that he or shet wants the program to display information about and displays the contents of that folder.
def displaySelectionFolderOption():
    folderName = input('Enter folder name: ')
    try:
        accepted_candidates.displayFolder(folderName)
    except KeyError:
        print('Error: cannot find a selection folder named ' + folderName)
    print()

#Displays the contents of the selection pool.
def displaySelectionOption():
    accepted_candidates.display()
    print()

main() #Run the host main program
