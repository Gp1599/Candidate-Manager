#Represents a candidate application that will be processed by the candidate managment host
class Candidate:
    #Initializes the candidate with the specified name
    def __init__(self, name):
        self.name = ''
        self.attributes = {}
    
    #Returns the candidate's name
    def getName(self):
        return self.name
    
    #Returns the candidate's characteristic with the specified name
    def getAttribute(self, name):
        return self.attributes[name]
    
    #Changes the candidate's characteristic with the specified name to the specified value
    def setAttribute(self, name, value):
        self.attributes[name] = value

    #Returns the names of each of the candidate's attributes
    def getAttributeNames(self):
        return self.attributes.getKeys()