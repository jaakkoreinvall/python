# Empirical tests for Crawford-Knoer type matching algorithm. Link to their paper: 
# http://econweb.ucsd.edu/~vcrawfor/CrawfordKnoer81EMT.pdf
# Created by Jaakko Reinvall

def cal_S(A):
    S = []
    dummy_list = []
    for i in range(len(A)):
        for j in range(len(A[i])):
            Sij = -A[i][j]
            dummy_list.append(Sij)
        S.append(dummy_list)
        dummy_list = []
    return S

def cal_sum(A,B):
    C = []
    for i in range(len(A)):
        dummy_list = []
        for j in range(len(A[0])):
            dummy_list.append((A[i][j]+B[i][j]))
        C.append(dummy_list)
    return C

def copy(a):
    b = []
    for i in range(len(a)):
        dummy_list = []
        for j in range(len(a[0])):
            dummy_list.append(a[i][j])
        b.append(dummy_list)
    return b

def list_of_offers(A,B):
    C = cal_sum(A,B)
    S = cal_S(A)
    F = []
    for j in range(len(A[0])):
        list = len(A)*[0]
        dummy_list = []
        maximum = C[0][j]
        dummy_list.append([0, S[0][j]])
        for i in range(1,len(A)):
            if C[i][j] > maximum:
                dummy_list = []
                dummy_list.append([i, S[i][j]])
                maximum = C[i][j]
            elif C[i][j] == maximum:
                dummy_list.append([i, S[i][j]])
        from random import shuffle
        shuffle(dummy_list)
        a = copy(dummy_list)
        F.append(a)
        for k in range(len(dummy_list)):
            m = dummy_list[k][0]
            S[m][j] += 1
            dummy_list[k][1] = S[m][j]
            C[m][j] -= 1
            list[m] = 1
        maximum -= 1
        while maximum >= 0:
            for i in range(len(A)):
                if list[i] == 0:
                    if C[i][j] == maximum:
                        dummy_list.append([i, S[i][j]])
                        list[i] = 1
            from random import shuffle
            shuffle(dummy_list)
            for n in range(len(dummy_list)):
                F[j].append(dummy_list[n])
            b = copy(dummy_list)
            for p in range(len(b)):
                m = b[p][0]
                S[m][j] += 1
                b[p][1] = S[m][j]
                C[m][j] -= 1
            dummy_list = []
            dummy_list = copy(b)
            maximum -= 1
    return F

def favorite_sellers(B,S):
    maximums = len(B[0])*[-10]
    Q = len(B[0])*[-1]
    q = len(B[0])*[-1000]
    for j in range(len(B[0])):
        dummy_list = []
        net_productivity = B[0][j] - S[0][j]
        maximums[j]=net_productivity
        dummy_list.append(0)
        for i in range(1,len(B)):
            net_productivity = B[i][j] - S[i][j]
            if net_productivity == maximums[j]:
                dummy_list.append(i)
            elif net_productivity > maximums[j]:
                maximums[j] = net_productivity
                dummy_list = []
                dummy_list.append(i)
            else:
                pass
        from random import choice
        a = choice(dummy_list)
        print a, j
        if Q[a] == -1:
            Q[a] = [j]
        else:
            Q[a].append(j)
        q[j] = S[a][j]
    return Q, q

def I_turn(lenght, lenght2, pi, pj, si, fj, Q, q, A):
    for i in range(lenght):
        if Q[i] != -1:
            if pi[i] != -1:
                x = pi[i]
                R = Q[i][:]
                R.append(pi[i])
                y = si[i]
                q[x] = y
            else:
                R = Q[i][:]
            maximum = A[i][R[0]]+q[R[0]]
            j = R[0]
            for a in range(1, len(R)):
                b = R[a]
                if A[i][b]+q[b] > maximum:     
                    maximum = A[i][b]+q[b]
                    j = b
                elif A[i][b]+q[b] == maximum:
                    coin_toss = ["Heads","Tails"]
                    from random import choice
                    if choice(coin_toss) == "Heads":
                        j = b
            if j != pi[i]:
                if pi[i] != -1:
                    pj[pi[i]] = ["break", i]
                fj[j] = ["accept",[i,q[j]]]
                pi[i] = j
                si[i] = q[j]
            for c in range(len(Q[i])):
                if Q[i][c] != pi[i]:
                    k = Q[i][c]
                    fj[k] = ["reject",[i,q[k]]]
    return pj, fj, pi, si

def J_turn(lenght2, pj, sj, fj, F):
    dummy = 0
    for j in range(lenght2):
        if pj[j] != -1:
            if type(pj[j]) != int:
                if type(pj[j][0]) == str:
                    m = pj[j][0]
                    if m == "break":
                        F[j].remove([pj[j][1],sj[j]])
                        pj[j] = -1
                        sj[j] = -1000
        if fj[j] != -1:
            m = fj[j][0] 
            if m == "accept":
                pj[j] = fj[j][1][0]
                sj[j] = fj[j][1][1]
            elif m == "reject":
                F[j].remove(fj[j][1])
            fj[j] = -1
        if pj[j]==-1 and F[j]:
            fj[j] = ["j offers q" ,F[j][0]]
#            prices[F[j][0][0]] += 1
            dummy = 1
    return fj, F, pj, sj, dummy
            
            
            
            
def subsets(F, B):
    Q = len(B)*[-1]
    q = len(B[0])*[-1000]
    for j in range(len(F)):
        i = F[j][0][0]
        b = F[j][0][1]
        if Q[i] == -1:
            Q[i] = [j]
        else:
            Q[i].append(j)
        q[j] = b
    return Q, q
        
def subsets2(fj, B):
    Q = len(B)*[-1]
    q = len(B[0])*[-1000]
    for j in range(len(fj)):
        if fj[j] != -1:
            if type(fj[j][0]) == str:
                if fj[j][0] == "j offers q":
                    i = fj[j][1][0]
                    q[j] = fj[j][1][1]
                    if Q[i] == -1:
                        Q[i] = [j]
                    else:
                        Q[i].append(j)
    return Q, q

def matching(pj):
    count = 0
    for j in range(len(pj)):
        if pj[j] != -1:
            count += 1
    return count
    
def unstable_edges(pi,pj,si,sj,A,B):
    count = 0
    for j in range(len(pj)):
        if pj[j] == -1:
            for i in range(len(pi)):
                if pi[i] == -1 and B[i][j] > -A[i][j]:
                    count += 1
                elif pi[i] != -1 and B[i][j] > A[i][pi[i]]+si[i]-A[i][j]:
                    count += 1
        else:
            for i in range(len(pi)):
                if pi[i] == -1 and B[i][j]-B[pj[j]][j]+sj[j] > -A[i][j]:
                    count += 1
                elif pi[i] != -1 and i != pj[j] and B[i][j]-B[pj[j]][j]+sj[j] > A[i][pi[i]]+si[i]-A[i][j]:
                    count += 1
    return count
            
    
def mechanism(A,B):
#    prices = [0,0,0,0,0]
    ROUNDS = 0
    lenght = len(A)
    lenght2 = len(A[0])
    pi = lenght*[-1]
    pj = lenght2*[-1]
    sj = lenght2*[-1000]
    fj = lenght2*[-1]
    si = lenght*[-1000]
    F = list_of_offers(A,B)
    Q, q = subsets(F, B)
    carryon = 1
    while carryon == 1:
        pj, fj, pi, si = I_turn(lenght, lenght2, pi, pj, si, fj, Q, q, A)
        fj, F, pj, sj, carryon2 = J_turn(lenght2, pj, sj, fj, F)
        carryon = carryon2
        u = float(unstable_edges(pi,pj,si,sj,A,B))
        m = float(matching(pj))
        ROUNDS += 1
        print (u/m), "in round number", ROUNDS
        Q, q = subsets2(fj, B)
    return ROUNDS

    
def main():
    list1 = ["input.txt"]
    list2 = ["output.txt"]
    for w in range(len(list1)):
        f = 0
        while f < 1:
            inputfile = open(list1[w], "r")
            outputfile = open(list2[w], "a")
            i = 0
            for row in inputfile:
                row = eval(row.rstrip())
                if i == 0:
                    A = row
                elif i == 1:
                    B = row
                i += 1
            outputfile.write(str(mechanism(A, B))+"\n")
            inputfile.close()
            outputfile.close()
            f += 1
main()
