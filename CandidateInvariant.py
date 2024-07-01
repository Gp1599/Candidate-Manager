import Candidate

#Represents a set of rules that determine which attribute types each candidate needs from the host 
class CandidateInvariant:
    #Initializes the invariant
    def __init__(self):
        self.attributeRules = {"attributeName": None }
        self.attributeRules.pop("attributeName")

    #Returns the attribute names in the candidate invariant
    def getAttributeNames(self):
        return self.attributeRules.keys()
    
    #Returns the int that indicates the required datatype of the attribute with the specified name 
    def getRule(self, attributeName):
        return self.attributeRules[attributeName]
    
    #Adds the specified rule into the candidate invariant
    def addRule(self, attributeName, attributeRule):
        self.attributeRules[attributeName] = attributeRule
        #print(self.attributeRules[attributeName])
    
    #Checks whether or not the specified candidate obeys the invariant
    def isObeyedBy(self, candidate):
        correctCount = 0
        for attributeName in candidate.getAttributeNames():
            try:
                attributeValue = candidate.getAttribute(attributeName)
                rule = self.getRule(attributeName)
                if not rule == None:
                    if rule.isObeyedBy(attributeValue):
                        #print('True')
                        correctCount = correctCount + 1
                else:
                    correctCount = correctCount + 1
            except KeyError:
                #print('A Key Error has Ocurred!')
                return False
        return correctCount >= len(self.attributeRules)
    
#Represents a rule that represents which type of attribute is required from the attribute with the specified name
class CandidateInvariantRule:
    def isObeyedBy(self, attributeValue):
        pass

#Represents a rule that requires an attribute to be an integer and be in the specified range
class CandidateInvariantIntRangeRule(CandidateInvariantRule):
    #Initializes the int range rule with the specified range
    def __init__(self, min, max):
        self.min = min
        self.max = max

    #Checks to see if the attribute is an int and is in the range specified in the rule's initialization
    def isObeyedBy(self, attributeValue):
        try:
            intAttributeValue = int(attributeValue)
            return intAttributeValue >= self.min and intAttributeValue <= self.max
        except ValueError:
            return False
    

def test(candidateAttributes, invariantAttributes, expectedResult):
    candidate = Candidate.Candidate('Gabriel')
    invariant = CandidateInvariant()

    for candidateAttribute in candidateAttributes:
        name, value = candidateAttribute
        candidate.setAttribute(name, value)

    for invariantAttribute in invariantAttributes:
        name, rule = invariantAttribute
        invariant.addRule(name, rule)
    
    return invariant.isObeyedBy(candidate) == expectedResult

def main():
    testCases = [ ([], [], True), 
                          ([('Age', '23') ,('Description', 'I am Gabriel!')], [('Age', CandidateInvariantIntRangeRule(0, 100)), ('Description', None)], True),
                          ([('Race', 'Martial'), ('Member ID', '415b')], [('Race', None), ('Member ID', CandidateInvariantIntRangeRule(100, 999))], False),
                          ([('Grade', 100), ('Alternate Name', 'Ga')], [('Grade', CandidateInvariantIntRangeRule(0, 10)), ('Alternate Name', None)], False),
                          ([('Phone Number', '100-100-1000'), ('Employer Name', 'Wizard inc.')], [('Phone Number', None)], False)
    ]

    i = 1
    for testCase in testCases:
        candidateAttributes, invariantAttributes, expectedResult = testCase
        #print(candidateAttributes)
        #print(invariantAttributes)
        #print(expectedResult)
        print('Test Case ' + str(i) + ': ' + str(test(candidateAttributes, invariantAttributes, expectedResult)))
        i = i + 1

main()
