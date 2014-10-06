# Implementation of Demange-Gale-Sotomayor (1986) auction algorithm.
# Link to their paper: http://www.jstor.org/discover/10.2307/1833206?uid=3737976&uid=2&uid=4&sid=21104755979467
# Created by Jaakko Reinvall

def add_zeros(list1, list2):
    l1 = len(list1)
    for i in range(l1):
        list1[i].append(0)
    list2.append(0)
    return list1, list2
        
def remove_zeros(list1, list2):
    for i in range(len(list1)):
        a = list1[i].pop()
    b = list2.pop()
    return list1, list2

def compute_utilities(demands, prices):
    utilities = []
    dummy = []
    for i in range(len(demands)):
        for j in range(len(demands[i])):
            utility = demands[i][j] - prices[j] 
            dummy.append(utility)
        utilities.append(dummy)
        dummy = []
    return utilities

def return_max_arcs(utilities):
    dummy = []
    maxarcs = []
    for i in range(len(utilities)):
        max1 = max(utilities[i])
        for j in range(len(utilities[i])):
            if max1 == utilities[i][j]:
                dummy.append([i,j])
            else:
                pass
        maxarcs.append(dummy)
        dummy = []
    return maxarcs
    
    
def alphazero(list, given_length):
    dummy = []
    for i in range(len(list)):
        a = 0
        for j in range(len(list[i])):
            if list[i][j][1] == (given_length):
                a = -1
            else:
                pass
        if a == 0:
            dummy.append(list[i])
        else:
            pass
    return dummy

def list_difference(list1, list2):
    new_list = []
    for i in range(len(list1)):
        for element in list1[i]:
            if element not in list2:
                new_list.append(element)
            else:
                pass
    return new_list

def symmetric_difference(list1, list2):
    new_list = []
    for element in list1:
        if element not in list2:
            new_list.append(element)
        else:
            list2.remove(element)
    for element2 in list2:
        new_list.append(element2)
    return new_list

def find_matching(maxarcs, orig_quantity):
    list = orig_quantity*[0]
    M = []
    for i in range(len(maxarcs)):
        j = 0
        while j < len(maxarcs[i]):
            if list[maxarcs[i][j][1]] == 0:
                M.append(maxarcs[i][j])
                list[maxarcs[i][j][1]] = 1
                j = 10*orig_quantity
            else:
                pass
            j += 1
    return M

def bipartite_augment_minimal(maxarcs, M, orig_quantity):
    b = orig_quantity # The number of buyers
    dummy = b*[-1] # Gather saturated buyers to this list. If a buyer is saturated, the respective index will be
    #marked with value 0. If a buyer is unsaturated, the respective index will be marked with value -1.
    for arc in M:
        dummy[arc[0]] = 0
    S = b*[0] # Unsaturated nodes in the set of sellers are marked by value 0.
    for element in M:
        S[element[1]] = 2 # Saturated nodes in the set of sellers are marked by value 2.
    if len(maxarcs) < orig_quantity: # This part is for finding minimal overdemanded set.
        S_quantity = 0
        for element in S:
            if element == 2:
                S_quantity += 1
            else:
                pass
        if S_quantity == len(maxarcs):
            return M, 3, True
        else:
            pass
    else:
        pass
    T = b*[-1] # If y does not belong to T, it will be marked as -1. If y belongs to T, it will be marked as 0.
    p = 2*b*[-1] # Augmenting path (if such exist) will be added to this list. Value of -1 means that augmenting
    # path does not exist.
    P = []
    k = 0
    while k in S:
        for i in range(len(S)):
            if S[i] == 0:
                for element in list_difference(maxarcs, M):
                    x = element[1]
                    if x == i:
                        y = element[0]
                        if dummy[y] == -1:
                            P.append([y, x])
                            while p[x] != -1:
                                if p[x] >= b:
                                    y = p[x] - b
                                    P.append([y, x])
                                    x = p[x]
                                else:
                                    x = p[x]
                                    P.append([y,x])
                            return P, 2, False
                        else:
                            pass
                        for j in M:
                            if j[0] == y:
                                w = j[1]
                        if T[y] == -1 :
                            T[y] = 0
                            p[(y+b)] = x
                        else:
                            pass
                        if S[w] == 2:
                            S[w] = 0
                            p[w] = y+b
                    else:
                        pass
                S[i] = 1
            else:
                pass
    for element in S:
        if element != 2:
            return S, 3, False # Returns overdemanded set.
        else:
            pass
    return M, 3, True # Returns perfect matching.

def remove_element(arcs, overdemanded):
    dummy = []
    dummy2 = []
    dummy3 = []
    for i in range(len(overdemanded)):
        if overdemanded[i] == 2:
            dummy.append(i)
        else:
            pass
    for i in range(len(arcs)):
        if arcs[i][0][1] in dummy:
            dummy2.append(arcs[i])
        else:
            pass
    k = dummy2[:]
    for i in range(len(dummy2)):
        b = dummy2[i]
        dummy2.remove(b)
        dummy3.append(dummy2)
        dummy2 = k[:]
    return dummy3

def minimal(list, length):    
    for i in range(len(list)):
        copy = list[i][:]
        M = find_matching(copy, length)
        R = []
        l = 2
        while l != 3:
            M = symmetric_difference(R, M)
            R, l, TF2 = bipartite_augment_minimal(copy, M, length)
        if TF2 == False:
            return copy
        else:
            pass

def algorithm(initial_values, prices):
    demands, prices = add_zeros(initial_values, prices)
    ROUNDS = 0
    a = 2
    length = len(prices) - 1
    while a == 2:
        ROUNDS += 1
        utilities = compute_utilities(demands, prices)
        maxarcs = return_max_arcs(utilities)
        maxarcs2 = alphazero(maxarcs, length)
        if len(maxarcs2) <= 1:
            demands2, prices2 = remove_zeros(demands, prices)
            return maxarcs, prices2, ROUNDS
        else:
            pass
        M = find_matching(maxarcs2, length)
        P = []
        k = 2
        while k != 3:
            M = symmetric_difference(P, M)
            P, k, TF1 = bipartite_augment_minimal(maxarcs2, M, length)
        if TF1 == True:
            demands2, prices2 = remove_zeros(demands, prices)
            return P, prices2, ROUNDS
            a = 3
        else:
            list = remove_element(maxarcs2, P)
            list2 = minimal(list, length)
            if list2 != None:
                while list2 != None:
                    new_list = []
                    exceeding = [1]*len(prices)
                    for i in range(len(list2)):
                        for j in range(len(list2[i])):
                            number = list2[i][j][1]
                            if number not in new_list:
                                new_list.append(number)
                                exceeding[number] = 2
                            else:
                                pass            
                    list3 = remove_element(list2, exceeding)
                    list2 = minimal(list3, length)
                P = exceeding
            else:
                pass

            for i in range(len(P)):
                if P[i] == 2:
                    prices[i] += 1
                    a = 2
                else:
                    pass
        print prices, ROUNDS
    
def main():
    a = [0,0,0] # Initial prices
    b = [[4,2,12],[5,2,7],[7,6,8]] # Valuations of buyers for the items on sale.
    print algorithm(b, a) # Shows updated prices and the current round number. Finally, shows the arcs for a perfect
    # matching (if such can be found), corresponding prices and round number.
main()

    
#    lahto = open("testfile2.txt", "r")
#    lahto2 = open("satanollaa.txt", "r")
#    tulo = open("dataa23.txt", "w")
#    for rivi in lahto2:
#        rivi1 = eval(rivi.rstrip())
#    for rivi in lahto:
#        rivi2 = eval(rivi.rstrip())
#    tulo.write(str(algorithm(rivi2, rivi1)))
#    lahto.close()
#    lahto2.close()
#    tulo.close()    

    
