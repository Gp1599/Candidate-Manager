import Candidate

#Constants to represent the types of each attribute that the invariant needs
int_invariant_type = 1
string_invariant_type = 2
float_invariant_type = 3

#Represents a set of rules that determine which attribute types each candidate needs from the host 
class CandidateInvariant:
    #Initializes the invariant
    def __init__(self):
        self.typeDictionary = {}

    #Adds the specified rule into the candidate invariant
    def addRule(self, attributeName, attributeType):
        if not (attributeName is str or attributeType is int):
            raise CandidateInvariantException()
        else:
            self.typeDictionary[attributeName] = attributeType
    
    #Returns whether or not the invariant is satisfied by the specified candidate
    def isObeyedBy(self, candidate):
        if(not candidate is Candidate.Candidate):
            raise CandidateInvariantException()
        
        #Initialize attribute names
        attributeNames = candidate.getAttributeNames()
        attributeCount = len(attributeNames)

        #Check is each attribute satisfies the invariant
        obeyCount = 0
        for attributeName in attributeNames:
            #If the specified attribute does not exist, then return false
            type = self.typeDictionary[attributeName]
            if(type == None):
                return False
            
            #If the attribute value is of the type that is specified in the invariant, then increment the obeyed counter.
            value = candidate.getAttribute(attributeName)
            match type:
                case 1:
                    if(value is int):
                        obeyCount = obeyCount + 1
                case 2:
                    if value is float:
                        obeyCount = obeyCount + 1
            if value is str:
                obeyCount = obeyCount + 1

        #If all the candidate attributes satisfy the invariant, return true. Otherwise, return false.
        return obeyCount >= attributeCount

#Represents the exception that is thrown if the function specifications are not satisfied
class CandidateInvariantException:
    def __init__():
        print()