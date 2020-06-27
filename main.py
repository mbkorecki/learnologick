from parser import *
import sys
import itertools

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

    minConf = 0.6

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

    # for pred in predicates:
    #     if type(predSets[pred]) is list:
    #         it0 = 0
    #         for subset1 in predSets[pred]:
    #             it1 = 0
    #             for subset2 in predSets[pred]:
    #                 intersection = subset1.intersection(subset2)
    #                 confRule = 0
    #                 if bool(intersection):
    #                     union = subset1.union(subset2)
    #                     confRule = len(intersection) / len(domains[predicates[pred][it1]])
    #                     print('union: ', len(union) / len(domains[predicates[pred][it1]]), confRule)
    #                 if  confRule > minConf:
    #                     conf = len(intersection) / len(subset1)
    #                     print(pred, tuple(predicates[pred]), '->', pred, tuple(predicates[pred]), conf, it0, it1)
    #                 it1 += 1
    #             it0 += 1
    # return 0
    for combo in combinations:
        set1 = predSets[combo[0]]
        set2 = predSets[combo[1]]
        
        if type(set1) is list and type(set2) is list:
            it0 = 0
            for subset1 in set1:
                it1 = 0
                for subset2 in set2:
                    intersection = subset1.intersection(subset2)
                    confRule = 0
                    if bool(intersection):
                        union = subset1.union(subset2)
                        confRule = len(intersection) / len(domains[predicates[combo[it0]][it1]])
                        print('union: ', len(union) / len(domains[predicates[combo[it0]][it1]]), 'confidence: ', confRule)
                    if  confRule > minConf:
                        sup1 = len(subset1) / len(domains[predicates[combo[0]][it0]])
                        sup2 = len(subset2) / len(domains[predicates[combo[1]][it1]])
                        if sup1 > sup2:
                            conf = len(intersection) / len(subset1)
                            print(combo[0], tuple(predicates[combo[0]]), '=>', combo[1], tuple(predicates[combo[1]]), conf, it0, it1)
                        else:
                            conf = len(intersection) / len(subset2) 
                            print(combo[1], tuple(predicates[combo[1]]), '=>', combo[0],  tuple(predicates[combo[0]]), conf, it0, it1)
                    it1 += 1
                it0 += 1
        elif type(set1) is list:
            it = 0
            for subset1 in set1:
                intersection = subset1.intersection(set2)
                confRule = 0
                if bool(intersection):
                    union = subset1.union(set2)
                    confRule = len(intersection) / len(domains[predicates[combo[0]][it]])
                    print('union: ', len(union) / len(domains[predicates[combo[0]][it]]), 'confidence: ', confRule)                    
                if confRule > minConf:
                    sup1 = len(subset1) / len(domains[predicates[combo[0]][it]])
                    sup2 = len(set2) / len(domains[predicates[combo[1]][0]])
                    if sup1 > sup2:
                        conf = len(intersection) / len(subset1) 
                        print(combo[0], tuple(predicates[combo[0]]), '=>', combo[1], tuple(predicates[combo[1]]), conf, it)
                    else:
                        conf = len(intersection) / len(set2) 
                        print(combo[1], tuple(predicates[combo[1]]), '=>', combo[0],  tuple(predicates[combo[0]]), conf, it)
                it += 1
        elif type(set2) is list:
            it = 0
            for subset2 in set2:
                intersection = subset2.intersection(set1)
                confRule = 0
                if bool(intersection):
                    union = set1.union(subset2)
                    confRule = len(intersection) / len(domains[predicates[combo[1]][it]])
                    print('union: ', len(union) / len(domains[predicates[combo[1]][it]]), 'confidence: ', confRule)
                if confRule > minConf:
                    sup1 = len(set1) / len(domains[predicates[combo[0]][0]])
                    sup2 = len(subset2) / len(domains[predicates[combo[1]][it]])
                    if sup1 > sup2:
                        conf = len(intersection) / len(set1) 
                        print(combo[0], tuple(predicates[combo[0]]), '=>', combo[1], tuple(predicates[combo[1]]), conf, it)
                    else:
                        conf = len(intersection) / len(subset2) 
                        print(combo[1], tuple(predicates[combo[1]]), '=>', combo[0],  tuple(predicates[combo[0]]), conf, it)
                it += 1

        else:
            intersection = set1.intersection(set2)
            confRule = 0
            if bool(intersection):
                union = set1.union(set2)
                confRule = len(intersection) / len(domains[predicates[combo[0]][0]])
                print('union: ', len(union) / len(domains[predicates[combo[0]][0]]), 'confidence: ', confRule)
            if confRule > minConf:
                sup1 = len(set1) / len(domains[predicates[combo[0]][0]])
                sup2 = len(set2) / len(domains[predicates[combo[1]][0]])
                if sup1 > sup2:
                    conf = len(intersection) / len(set1) 
                    print(combo[0], tuple(predicates[combo[0]]), '=>', combo[1], tuple(predicates[combo[1]]), conf, '0')
                else:
                    conf = len(intersection) / len(set2) 
                    print(combo[1], tuple(predicates[combo[1]]), '=>', combo[0],  tuple(predicates[combo[0]]), conf, '0')
    
if __name__ == "__main__":
    main()
