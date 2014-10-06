# Voronoi game implementation where a player can use heuristic model.
# Created by Jaakko Reinvall

from Tree import TreeNode
import random
import sys

#Function creates a tree. The first input (nodes) represents the number of nodes in a tree.
#The second input (parent_list) is either initial substitution [9, 8, 7, 6, 5] or created by 
#next_parent_list function. create_Tree function returns all the nodes in a list (nodelist). When trying
#out all the different parent_list:s, it should create all the non-isomorphic trees with given n, but 
#there might be some repeats.
def create_Tree(nodes, parent_list):
    #parent_list encodes the added neighbour structure
    #node j has parent parent_list[nodes-j] (which is < j)
    #parent_list[...] should be a nonincreasing sequence for maximum effectiveness

    nodelist=[]
    for j in range(1,nodes+1):
        nodelist.append(TreeNode("node"+str(j)))

    #initial 5-node structure
    for pair in [[1,2],[2,3],[1,4],[1,5]]:
        nodelist[pair[0]-1].add_neighbour(nodelist[pair[1]-1])
        nodelist[pair[1]-1].add_neighbour(nodelist[pair[0]-1])
  
    next = nodes  
    while (next > 5):    
        parent = parent_list[nodes-next]
        nodelist[parent-1].add_neighbour(nodelist[next-1])
        nodelist[next-1].add_neighbour(nodelist[parent-1])
        next -= 1
    
    return nodelist 

#This function creates next parent list always from the previous one.
def next_parent_list(p_list):
    n = len(p_list)+5
    for i in range(0, (n-5)-1):
        if p_list[i] > p_list[i+1]:
            p_list[i] -= 1
            for j in range(0,i):
                p_list[j] = (n-1)-j
            return p_list
    return None # last parent list, no successor

#For creating trees, you can also use the one below. Input is prufer sequence in the form of a list.
#If you want to create a tree with n nodes, then the length of prufer sequence should be n-2 and
#the numbers in it from 1 to n. If you run through all the different prufer sequences with a given
#n, the function returns all the n-size trees. For more information, check the wikipedia page below.
#wikipedia: Prufer sequence, section 2 Algorithm to convert a Prufer sequence into a tree (15.6.2011)
#def Convert_Prufer_to_Tree(prufer_sequence):
#    m=len(prufer_sequence)
#    nodeq=m+2
#    nodelist=[]
#    for i in range(1,nodeq+1):
#        nodelist.append(TreeNode("node"+str(i)))
#    for i in prufer_sequence:
#        nodelist[i-1].increase_degree()
#    for i in prufer_sequence:    
#        for j in range(1,nodeq+1):
#            if nodelist[j-1].return_degree()==1:
#                nodelist[j-1].add_neighbour(nodelist[i-1])
#                nodelist[i-1].add_neighbour(nodelist[j-1])
#                nodelist[i-1].decrease_degree()
#                nodelist[j-1].decrease_degree()
#                break
#    u=0
#    v=0
#    for i in range(1,nodeq+1):
#        if nodelist[i-1].return_degree()==1:
#            if u==0:
#                u=i
#            else:
#                v=i
#                break
#    nodelist[u-1].add_neighbour(nodelist[v-1])
#    nodelist[v-1].add_neighbour(nodelist[u-1])
#    nodelist[u-1].decrease_degree()
#    nodelist[v-1].decrease_degree()
#    return nodelist


#BFS_1 updates the minimum distances in the game. It doesn't return anything. For more information
#about minimum distances, check Tree.py.
def BFS_1(nodelist):
    Q=[]
    for v in nodelist:
        if v.return_mindistance()[0]==0:
            Q.append(v)
        else:
            v.change_mindistance([1000,0])
    while Q:
        v=Q[0]
        del Q[0]
        for u in v.return_neighbours():
            if (v.return_mindistance()[0]+1)<u.return_mindistance()[0]:
                u.change_mindistance([v.return_mindistance()[0]+1,v.return_mindistance()[1]])
                Q.append(u)
            elif (v.return_mindistance()[0]+1)==u.return_mindistance()[0] and v.return_mindistance()[1]!=u.return_mindistance()[1]:
                u.change_mindistance([u.return_mindistance()[0],0])
                Q.append(u)
            else: pass


#Function computes maximum ("good luck") and minimum ("bad luck") values for L-max ("maximum locking") 
#heuristic. 
def game_routine(Player, nodelist, nodelist_2, k):
    if Player==True: #Player has two values True=red and False=blue
        positions=[]
        BFS_1(nodelist)
        for i in nodelist:
            positions.append(i.return_mindistance())
        maxlocked=0 
        maxs=[]             
        for child in nodelist_2: # child is red's next move, list includes all possible moves that red can make            
            l=child.BFS_3(nodelist)
            for m in nodelist:
                m.change_marked(False)
            if l>=k:                
                nodelist_3=nodelist_2[:]
                nodelist_3.remove(child)
                for j in nodelist_3:
                    j.BFS_4(nodelist, k)
                    for m in nodelist:
                        m.change_marked(False)
                lockedpts=0
                for p in nodelist:
                    lockedpts+=p.return_lockedpoints()
                if lockedpts>maxlocked:
                    maxlocked=lockedpts
                    maxs=[]
                    maxs.append(child)
                elif lockedpts==maxlocked:       
                    maxs.append(child)
                else: pass
            else:
                pass    
                # In this case, cannot play
            sum=0 
            for i in nodelist:
                i.change_lockedpoints(0)
                i.change_mindistance(positions[sum])
                sum+=1
        else: pass
        if not maxs:
            red=0.0
            for node in nodelist:
                if node.return_mindistance()[1]==1:
                    red+=1.0
                elif node.return_mindistance()[1]==0:
                    red+=0.5
                else: pass
            return red, red
        else:
            mintemp=10000
            maxtemp=-10000
            for node in maxs:
#                print "red plays", node.return_name()
                nodelist_5=nodelist_2[:]
                nodelist_5.remove(node)
                dummy=node.return_mindistance()
                node.change_mindistance([0,1])
                max, min=game_routine(not(Player), nodelist, nodelist_5, k)                
                node.change_mindistance(dummy)
                # trying to find max and min from all the maxs
                if max>maxtemp:
                    maxtemp=max
                else: pass
                if min<mintemp:
                    mintemp=min
                else: pass
#            print "red returns", maxtemp, mintemp
            return maxtemp, mintemp


    
    else:
        mintemp=10000
        maxtemp=10000
        a=0
        listlength=len(nodelist_2)
        for child in nodelist_2:
            BFS_1(nodelist)
            l=child.BFS_5(nodelist)
            if l>=k:
#                print "blue plays", child.return_name()
                for m in nodelist:
                    m.change_marked(False)
                nodelist_4=nodelist_2[:]
                nodelist_4.remove(child)
                dummy=child.return_mindistance()
                child.change_mindistance([0,-1])
                max, min=game_routine(not(Player), nodelist, nodelist_4, k)   
                child.change_mindistance(dummy)  
                if max<maxtemp:
                    maxtemp=max
                else: pass
                if min<mintemp:
                    mintemp=min
                else: pass
            else:
                a+=1
            for m in nodelist:
                m.change_marked(False)
        if a==listlength:
            BFS_1(nodelist)    
            for m in nodelist:
                m.change_marked(False)
            red=0.0
            for node in nodelist:
                if node.return_mindistance()[1]==1:
                    red+=1.0
                elif node.return_mindistance()[1]==0:
                    red+=0.5
                else: pass
            return red, red
        else:
            return maxtemp, mintemp
    
    



def main():
    n=10
    Player=True
    k=2.0
    #depth=n-1
    parent_list = []
    val = n-1
    while (val >= 5):
        parent_list.append(val)
        val -= 1
    print parent_list
    #count=0
    #locklist=[]
    
#    pl1=[13, 11, 10, 9, 9, 8, 7, 6, 5]
#    pl2=[12, 11, 10, 9, 9, 8, 7, 6, 5]
    while (parent_list != None):
        nodelist=create_Tree(n, parent_list)
        nodelist_2=nodelist[:]
        max, min=game_routine(Player, nodelist, nodelist_2, k)
        print max, min
        parent_list=next_parent_list(parent_list)

#    while (parent_list!=None):
#        count+=1
#        print count, parent_list
#        nodelist=create_Tree(n, parent_list)
#        nodelist_2=nodelist[:]
#        max, min, locklist=alphabeta(None, depth, Player, nodelist, nodelist_2, k, count, locklist)
#        print max, min
#        parent_list=next_parent_list(parent_list)
#    print locklist
#    sys.exit()


#-for testing the code   
#    n=15
#    Player=True
#    k=2.0
#    input=3
#    input=float(sys.argv[1][0:])
#    k=float(sys.argv[1][0:])
#    depth=n-1
#    distribution=(2*n+1)*[0]
    # "first" parent list
#    parent_list = []
#    val = n-1
#    while (val >= 5):
#        parent_list.append(val)
#        val -= 1
#    count=1.0
#    while count<input:
#        parent_list=next_parent_list(parent_list)
#        count+=1.0
#    nodelist=create_Tree(n, parent_list)
#    nodelist_2=nodelist[:] 
#    max, min=alphabeta(None, depth, Player, nodelist, nodelist_2, k)
#    print min
    # let's count the number of trees to be created:
#    count = 0
#    ldiff=0
#--------------------------------------------------------
#    while(parent_list != None):
#        count+=1
#        parent_list=next_parent_list(parent_list)
#    print n, count

#--------------------------------------------------------
    
#    while(parent_list != None):
#        count += 1
#        nodelist=create_Tree(n, parent_list)
#        nodelist_2=nodelist[:] 
#        max, min=alphabeta(None, depth, Player, nodelist, nodelist_2, k)
#        print min
        
#        diff=float(max-min)
#        distribution[int(2*diff)]+=1
#        print max, min, float(max-min), parent_list
##        parent_list=next_parent_list(parent_list)
#    print count, distribution

#    sys.exit()

    
    
main()
