#Represents a collection of folders that contain candidate that are currently accepted or selected from the waitlist
class CandidateSelectionPool:

    #Initializes the Candidate Selection Pool
    def __init__(self):
        self.folders = {"first folder": [] }
        self.folders.pop("first folder")

    #Adds a new selection folder with the specified name
    def addFolder(self, name):
        self.folders[name] = []

    #Adds the candidate from the waitlist to the destination folder
    def addCandidate(self, destFolder, waitlist, candidate):
        self.folders[destFolder].append(candidate)
        waitlist.remove(candidate)
    
    #Put the candidate back to the waitlist
    def removeCandidate(self, srcFolder, waitlist, candidateIndex):
        candidate = self.folders[srcFolder].remove(candidateIndex)
        waitlist.append(candidate)                   
    
    #Moves the candidate from one folder to another
    def swap(self, srcFolder, destFolder, candidateIndex):
        candidate = self.folders[srcFolder].remove(candidateIndex)
        self.folders[destFolder].addCandidate(candidate)

