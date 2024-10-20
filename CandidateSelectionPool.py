#Represents a collection of folders that contain candidate that are currently accepted or selected from the waitlist
class CandidateSelectionPool:

    #Initializes the Candidate Selection Pool
    def __init__(self):
        self.folders = {"first folder": {} }
        self.folders.pop("first folder")

    #Adds a new selection folder with the specified name
    def addFolder(self, folderName):
        self.folders[folderName] = {}

    #Moves all the candidates from the folder with the specified name to the waitlist and removes that folder completely
    def removeFolder(self, folderName, waitlist):
        candidateIDs = self.folders[folderName].keys()
        for id in candidateIDs:
            waitlist[id] = self.folders[folderName][id]
        self.folders.remove(folderName)

    #Adds the candidate from the waitlist to the destination folder
    def addCandidate(self, destFolder, waitlist, candidateID):
        candidate = waitlist[candidateID]
        self.folders[destFolder][candidateID] = candidate
        waitlist.pop(candidateID)

    #Moves the candidate from one folder to another
    def swap(self, srcFolder, destFolder, candidateID):
        candidate = self.folders[srcFolder][candidateID]
        self.folders[srcFolder].pop(candidateID)
        self.folders[destFolder][candidateID] = candidate

    #Put the candidate back to the waitlist
    def removeCandidate(self, srcFolder, waitlist, candidateID):
        candidate = self.folders[srcFolder][candidateID]
        self.folders[srcFolder].pop(candidateID)
        waitlist[candidateID] = candidate
    
    #Displays all of the contents of the selection pool that will be printed in the selection document
    def display(self):
        for folderName in self.folders.keys():
            self.displayFolder(folderName)

    #Displays the folders name and all its listed candidates
    def displayFolder(self, folderName):
        if len(self.folders[folderName]) <= 0:
            print(folderName + ': None')
        else:
            print(folderName + ':')
            for candidateID in self.folders[folderName].keys():
                print(str(candidateID) + "-\t" + self.folders[folderName][candidateID].getName())