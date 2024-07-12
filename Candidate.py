#Represents a candidate application that will be processed by the candidate managment host
class Candidate:
    #Initializes the candidate with the specified name
    def __init__(self, name, ipAddress):
        self.name = ''
        self.ipAddress = ipAddress
        self.attributes = { "attributeName": "attributeValue" }
        self.attributes.pop("attributeName");
    
    #Returns the candidate's name
    def getName(self):
        return self.name
    
    #Returns the ip address that the candidate came from
    def getIPAddress(self):
        return self.ipAdress
    
    #Returns the candidate's characteristic with the specified name
    def getAttribute(self, name):
        return self.attributes[name]
    
    #Changes the candidate's characteristic with the specified name to the specified value
    def setAttribute(self, name, value):
        self.attributes[name] = value

    #Returns the names of each of the candidate's attributes
    def getAttributeNames(self):
        return self.attributes.keys()