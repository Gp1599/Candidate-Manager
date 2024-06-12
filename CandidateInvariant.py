import Candidate

#Represents a set of rules that determine which attribute types each candidate needs from the host 
class CandidateInvariant:
    #Initializes the invariant
    def __init__(self):
        self.attributeRules = {"attributeName": CandidiateInvariantStringRule() }
        self.attributeRules.pop("attributeName")

    #Returns the attribute names in the candidate invariant
    def getAttributeNames(self):
        return self.attributeRules.getKeys()
    
    #Returns the int that indicates the required datatype of the attribute with the specified name 
    def getRule(self, attributeName):
        return self.attributeRules[attributeName]
    
    #Adds the specified rule into the candidate invariant
    def addRule(self, attributeName, attributeRule):
        self.attributeRules[attributeName] = attributeRule
    
    #Checks whether or not the specified candidate obeys the invariant
    def isObeyedBy(self, candidate):
        return False
    
#Represents a rule that represents which type of attribute is required from the attribute with the specified name
class CandidateInvariantRule:
    def isObeyedBy(self, attributeValue):
        pass

#Represents a rule that requires an attribute to be a string 
class CandidiateInvariantStringRule(CandidateInvariantRule):
    #Checks to see if the attribute is a string
    def isObeyedBy(self, attributeValue):
        return attributeValue is str

#Represents a rule that requires an attribute to be an integer and be in the specified range
class CandidateInvariantIntRangeRule(CandidateInvariantRule):
    #Initializes the int range rule with the specified range
    def __init__(self, min, max):
        self.min = min
        self.max = max

    #Checks to see if the attribute is an int and is in the range specified in the rule's initialization
    def isObeyedBy(self, attributeValue):
        if not attributeValue is int:
            return False

        intAttributeValue = int(attributeValue)
        return intAttributeValue >= self.min and intAttributeValue <= self.max
