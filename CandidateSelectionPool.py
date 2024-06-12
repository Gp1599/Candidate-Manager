
class CandidateSelectionPool:

    def __init__(self):
        self.folders = {"first folder", CandidateSelectionPoolFolder() }
        self.folders.pop("first folder")


class CandidateSelectionPoolFolder:

    def __init__(self, link):
        self.candidates = []
        self.responseMessage = ''


    def swapCandidates(self, index1, index2):
        temp = self.candidates[index1]
        self.candidates[index1] = self.candidates[index2]
        self.candidates[index2] = temp

    
