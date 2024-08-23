#Represents a collection of folders that contain candidate that are currently accepted or selected from the waitlist
class CandidateSelectionPool:

    #Initializes the Candidate Selection Pool
    def __init__(self):
        self.folders = {"first folder": [] }
        self.folders.pop("first folder")

    #Adds a new selection folder with the specified name
    def addFolder(self, folderName):
        self.folders[folderName] = []

    #Moves all the candidates from the folder with the specified name to the waitlist and removes that folder completely
    def removeFolder(self, folderName, waitlist):
        folder = self.folders[folderName]
        for candidate in folder:
            waitlist.append(candidate)
        self.folders.pop(folderName)

    #Adds the candidate from the waitlist to the destination folder
    def addCandidate(self, destFolder, waitlist, candidateIndex):
        candidate = waitlist[candidateIndex]
        self.folders[destFolder].append(candidate)
        waitlist.remove(candidate)

    #Moves the candidate from one folder to another
    def swap(self, srcFolder, destFolder, candidateIndex):
        candidate = self.folders[srcFolder][candidateIndex]
        self.folders[srcFolder].remove(candidate)
        self.folders[destFolder].append(candidate)

    #Put the candidate back to the waitlist
    def removeCandidate(self, srcFolder, waitlist, candidateIndex):
        candidate = self.folders[srcFolder][candidateIndex]
        self.folders[srcFolder].remove(candidate)
        waitlist.append(candidate)
    
    #Displays all of the contents of the selection pool that will be printed in the selection document
    def display(self):
        for folderName in self.folders.keys():
            self.displayFolder(folderName)

    #Displays the folders name and all its listed candidates
    def displayFolder(self, folderName):
        if len(self.folders[folderName]) <= 0:
            print(folderName + ': None')
        elif len(self.folders[folderName]) == 1:
            print(folderName + ': ' + self.folders[folderName][0].getName())
        else:
            print(folderName + ':')
            for candidate in self.folders[folderName]:
                print('\t' + candidate.getName())