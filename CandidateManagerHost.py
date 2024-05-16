import sys
import socket
import threading

import Candidate
import CandidateManagerPort

received_candidates = []
running = True #Global variable for keeping the program running

#The thread function to process received candidates
def receive_candidates():
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while running:
        packet, clientAddr = host_socket.recv(1024)
        #Check to see if the received candidate obeys the host's candidate invariant. If it does accept it. Otherwise, reject it.

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

#The main program to run the candidate manager host
def main():
    #Use global variables
    global running

    #Welcome the user to the Candidate Manager Host program
    print('Welcome Candidate Manager Host: ')
    
    #Prompt the user to create the candidate invariant

    #Run the candidate manager host loop
    while running:
        mainMenu()
    
    #Print the closing  message
    print('Thank you. Goodbye!')

main() #Run the host (main programi
