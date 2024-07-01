#Represents a collection of folders that contain candidate that are currently accepted or selected from the waitlist
class CandidateSelectionPool:

    #Initializes the Candidate Selection Pool
    def __init__(self):
        self.folders = {"first folder": CandidateSelectionPoolFolder() }
        self.folders.pop("first folder")

    #Adds the candidate from the waitlist to the destination folder
    def addCandidate(self, destFolder, waitlist, candidate):
        self.folders[destFolder].addCandidate(candidate)
        waitlist.remove(candidate)
    
    #Put the candidate back to the waitlist
    def removeCandidate(self, srcFolder, waitlist, candidateIndex):
        candidate = self.folders[srcFolder].removeCandidate(candidateIndex)
        waitlist.append(candidate)                   
    
    #Moves the candidate from one folder to another
    def swap(self, srcFolder, destFolder, candidateIndex):
        candidate = self.folders[srcFolder].removeCandidate(candidateIndex)
        self.folders[destFolder].addCandidate(candidate)
    

#Represents a folder that represents a particular selection spot for the selected candidates
class CandidateSelectionPoolFolder:

    #Initializes the candidate selection folder
    def __init__(self):
        self.candidates = []
        self.responseMessage = ''
    
    #Returns the candidate in the specified index
    def getCandidate(self, index):
        return self.candidates[index]

    #Adds the specified candidate into the folder
    def addCandidate(self, candidate):
        self.candidates.append(candidate)

    #Removes the candidate from the folder and returns it
    def removeCandidate(self, index):
        candidate = self.getCandidate(index)
        self.candidates.remove(candidate);
        return candidate
    
    #Makes the two specified candidates switch places
    def swapCandidates(self, index1, index2):
        temp = self.candidates[index1]
        self.candidates[index1] = self.candidates[index2]
        self.candidates[index2] = temp

    
