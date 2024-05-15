import sys

running = True #Global variable for keeping the program running

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
    
    #Run the candidate manager host loop
    while running:
        mainMenu()
    #Print the closing  message
    print('Thank you. Goodbye!')

main() #Run the host (main programi
