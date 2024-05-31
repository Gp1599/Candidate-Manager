import Candidate

#Represents a set of rules that determine which attribute types each candidate needs from the host 
class CandidateInvariant:
    #Initializes the invariant
    def __init__(self):
        self.attributeRules = {}

    #Returns the attribute names in the candidate invariant
    def getAttributeNames(self):
        return self.attributeRules.getKeys()
    
    #Returns the int that indicates the required datatype of the attribute with the specified name 
    def getRule(self, attributeName):
        return self.attributeRules[attributeName]
    
    #Adds the specified rule into the candidate invariant
    def addRule(self, attributeName, attributeRule):
        self.attributeRules[attributeName] = attributeRule