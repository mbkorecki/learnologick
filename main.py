from parser import *
import sys
import itertools
from operator import itemgetter 

def intersections(combinations, predSets, predicates, domains):
    intersectionDict = {}
    for combo in combinations:
        set1 = predSets[combo[0]]
        set2 = predSets[combo[1]]

        intersectionList = []
        
        it1 = 0
        for arg1 in set1:
            it2 = 0
            for arg2 in set2:
                intersection = arg1.intersection(arg2)
                intersectionList.append(((it1, it2), len(intersection) / len(domains[predicates[combo[0]][it1]]), len(domains[predicates[combo[0]][it1]])))
                it2 += 1
            it1 +=1
            
        intersectionDict.update({combo : intersectionList})
        
    return intersectionDict

def support(itemSet, intersects):
    combos = itertools.combinations(itemSet, 2)
    support = 0
    count = 0
    indexDict = {}
    for pair in combos:
        maxSupport = max(intersects[pair], key = itemgetter(1))
        support += maxSupport[1]
        indexDict.update({pair: maxSupport[0]})
        count += 1
    return support / count, indexDict
    


def main(dataFile='data/imdb/imdb.all.db', legendFile='data/imdb/legend.txt'):
# def main(dataFile='data/smoking/smoking-full.db', legendFile='data/smoking/legend.txt'):

    if len(sys.argv) == 3:
        dataFile = sys.argv[1]
        legendFile = sys.argv[2]

    if dataFile is None:
        print("error: data file name is not specified")
        return 0
    if legendFile is None:
        print("error: legend file name is not specified")
        return 0

    parser = Parser()
    domains, predicates = parser.parseLegend(legendFile)

    predSets = parser.parseData(dataFile, predicates)

    print(domains, predicates)
    if not bool(domains):
        domSet = set()
        for key in predicates.keys():
            for dom in predicates[key]:
                domSet.add(dom)
        for dom in domSet:
            domains.update({dom : set()})
        for key in predicates.keys():
            for dom, predSet in zip(predicates[key], predSets[key]):
                updatedDom = domains[dom].union(predSet)
                domains.update({dom : updatedDom})

    combinations = itertools.combinations(predSets.keys(), 2)
    intersects = intersections(combinations, predSets, predicates, domains)

    minSupport = 0.5
    minConf  = 0.5

    intersectionDict = {}
    for pred in predicates:
        if type(predSets[pred]) is list:
            set1 = predSets[pred]
            set2 = predSets[pred]

            intersectionList = []
        
            it1 = 0
            for arg1 in set1:
                it2 = 0
                for arg2 in set2:
                    intersection = arg1.intersection(arg2)
                    intersectionList.append(((it1, it2), len(intersection) / len(domains[predicates[pred][it1]]), len(domains[predicates[pred][it1]])))
                    it2 += 1
                it1 +=1
        intersectionDict.update({(pred, pred) : intersectionList})

    for pred in predicates:
        if type(predSets[pred]) is list:
            supp, interactDict = support([pred,pred], intersectionDict)
            if supp > 0:
                print('suport:', supp)

                print(intersectionDict[(pred, pred)])
                maxSupport = max(intersectionDict[(pred, pred)], key = itemgetter(1))
                confidence = maxSupport[1]
                if confidence >= 0:
                    print(pred, '=>', pred, confidence, maxSupport[0])

    for i in range(2,len(predicates)+1):
        combo = itertools.combinations(predSets.keys(), i)
        for itemSet in combo:
            supp, interactDict = support(itemSet, intersects)
            if supp > minSupport:
                print('suport:', supp)
                for item in itemSet:
                    ancendants = set(itemSet) - set([item])
                    confidence = 0
                    for x in ancendants:
                        if (x, item) in intersects:
                            maxSupport = max(intersects[(x, item)], key = itemgetter(1))
                            confidence += (maxSupport[1] * maxSupport[2]) / len(predSets[x][maxSupport[0][0]])
                            print(x, item, maxSupport[0], len(predSets[x][maxSupport[0][0]]), len(predSets[item][maxSupport[0][1]]))
                        else:
                            maxSupport = max(intersects[(item, x)], key = itemgetter(1))
                            confidence += (maxSupport[1] * maxSupport[2]) / len(predSets[x][maxSupport[0][1]])
                            print(x, item, (maxSupport[0][1], maxSupport[0][0]), len(predSets[x][maxSupport[0][1]]), len(predSets[item][maxSupport[0][0]]))
                    confidence = confidence / len(ancendants)
                    if confidence >= minConf:
                        
                        print(ancendants, '=>', item, confidence)
    # return 0

    # for pred in predicates:
    #     if type(predSets[pred]) is list:
    #         it0 = 0
    #         for subset1 in predSets[pred]:
    #             it1 = 0
    #             for subset2 in predSets[pred]:
    #                 intersection = subset1.intersection(subset2)
    #                 confRule = 0
    #                 if bool(intersection):
    #                     confRule = len(intersection) / len(domains[predicates[pred][it1]])
    #                     print(confRule)
    #                 if  confRule > minConf:
    #                     conf = len(intersection) / len(subset1)
    #                     print(pred, tuple(predicates[pred]), '->', pred, tuple(predicates[pred]), conf, it0, it1)
    #                 it1 += 1
    #             it0 += 1

    # return 0
    # for combo in combinations:
    #     set1 = predSets[combo[0]]
    #     set2 = predSets[combo[1]]
        
    #     if type(set1) is list and type(set2) is list:
    #         it0 = 0
    #         for subset1 in set1:
    #             it1 = 0
    #             for subset2 in set2:
    #                 intersection = subset1.intersection(subset2)
    #                 confRule = 0
    #                 if bool(intersection):
    #                     confRule = len(intersection) / len(domains[predicates[combo[it0]][it1]])
    #                     print('confidence: ', confRule)
    #                 if  confRule > minConf:
    #                     sup1 = len(subset1) / len(domains[predicates[combo[0]][it0]])
    #                     sup2 = len(subset2) / len(domains[predicates[combo[1]][it1]])
    #                     if sup1 > sup2:
    #                         conf = len(intersection) / len(subset1)
    #                         print(combo[0], tuple(predicates[combo[0]]), '=>', combo[1], tuple(predicates[combo[1]]), conf, it0, it1)
    #                     else:
    #                         conf = len(intersection) / len(subset2) 
    #                         print(combo[1], tuple(predicates[combo[1]]), '=>', combo[0],  tuple(predicates[combo[0]]), conf, it0, it1)
    #                 it1 += 1
    #             it0 += 1
    #     elif type(set1) is list:
    #         it = 0
    #         for subset1 in set1:
    #             intersection = subset1.intersection(set2)
    #             confRule = 0
    #             if bool(intersection):
    #                 confRule = len(intersection) / len(domains[predicates[combo[0]][it]])
    #                 print('confidence: ', confRule)                    
    #             if confRule > minConf:
    #                 sup1 = len(subset1) / len(domains[predicates[combo[0]][it]])
    #                 sup2 = len(set2) / len(domains[predicates[combo[1]][0]])
    #                 if sup1 > sup2:
    #                     conf = len(intersection) / len(subset1) 
    #                     print(combo[0], tuple(predicates[combo[0]]), '=>', combo[1], tuple(predicates[combo[1]]), conf, it)
    #                 else:
    #                     conf = len(intersection) / len(set2) 
    #                     print(combo[1], tuple(predicates[combo[1]]), '=>', combo[0],  tuple(predicates[combo[0]]), conf, it)
    #             it += 1
    #     elif type(set2) is list:
    #         it = 0
    #         for subset2 in set2:
    #             intersection = subset2.intersection(set1)
    #             confRule = 0
    #             if bool(intersection):
    #                 confRule = len(intersection) / len(domains[predicates[combo[1]][it]])
    #                 print('confidence: ', confRule)
    #             if confRule > minConf:
    #                 sup1 = len(set1) / len(domains[predicates[combo[0]][0]])
    #                 sup2 = len(subset2) / len(domains[predicates[combo[1]][it]])
    #                 if sup1 > sup2:
    #                     conf = len(intersection) / len(set1) 
    #                     print(combo[0], tuple(predicates[combo[0]]), '=>', combo[1], tuple(predicates[combo[1]]), conf, it)
    #                 else:
    #                     conf = len(intersection) / len(subset2) 
    #                     print(combo[1], tuple(predicates[combo[1]]), '=>', combo[0],  tuple(predicates[combo[0]]), conf, it)
    #             it += 1

    #     else:
    #         intersection = set1.intersection(set2)
    #         confRule = 0
    #         if bool(intersection):
    #             confRule = len(intersection) / len(domains[predicates[combo[0]][0]])
    #             print('confidence: ', confRule)
    #         if confRule > minConf:
    #             sup1 = len(set1) / len(domains[predicates[combo[0]][0]])
    #             sup2 = len(set2) / len(domains[predicates[combo[1]][0]])
    #             if sup1 > sup2:
    #                 conf = len(intersection) / len(set1) 
    #                 print(combo[0], tuple(predicates[combo[0]]), '=>', combo[1], tuple(predicates[combo[1]]), conf, '0')
    #             else:
    #                 conf = len(intersection) / len(set2) 
    #                 print(combo[1], tuple(predicates[combo[1]]), '=>', combo[0],  tuple(predicates[combo[0]]), conf, '0')
    
if __name__ == "__main__":
    main()
