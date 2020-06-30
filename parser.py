

class Parser(object):
    def parseLegend(self, name):
        print("parsing file:", name)

        with open(name) as f:
            content = f.readlines()

        parsingDomains = False
        parsingPredicates = False

        domains = {}
        predicates = {}
        
        for line in content:
            if line[0:line.find(':')] == 'Domains':
                parsingDomains = True
                parsingPredicates = False
            elif line[0:line.find(':')] == 'Predicates':
                parsingDomains = False
                parsingPredicates = True
            elif parsingDomains:
                domName = line[0:line.find('{')]
                elems = line[line.find('{')+1:line.find('}')].split(',')
                domains.update({domName : elems})
            elif parsingPredicates:
                predName = line[0:line.find('(')]
                args = line[line.find('(')+1:line.find(')')].split(',')
                predicates.update({predName : args})

        return domains, predicates


    def parseData(self, name, predicates):
        print("parsing file:", name)


        predSets = {}
        for key in predicates.keys():
            if len(predicates[key]) == 1:
                predSets.update({key :[set()]})
            elif len(predicates[key]) == 2:
                predSets.update({key : [set(), set()]})

        with open(name) as f:
            content = f.readlines()
            content = (line.rstrip() for line in content) # All lines including the blank ones
            content = (line for line in content if line)

        for line in content:
            predName = line[0:line.find('(')]
            if len(predicates[predName]) == 1:
                const = line[line.find('(')+1:line.find(')')]
                predSets[predName][0].add(const)
            elif len(predicates[predName]) == 2:
                consts = line[line.find('(')+1:line.find(')')].replace(" ", "").split(",")
                predSets[predName][0].add(consts[0])
                predSets[predName][1].add(consts[1])

        return predSets
