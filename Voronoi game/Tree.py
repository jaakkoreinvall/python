# Class TreeNode and a few subroutines which are used in Heuristic model.py program.
# Created by Jaakko Reinvall

# Class TreeNode models a node of a tree. 

class TreeNode:
    def __init__(self, name):
        self.__name=name
        
        self.__marked=False         # The attribute is used in breadth-first searches
        
        self.__neighbours=[]             
        
        self.__mindistance=[1000,0] # The first number indicates the minimum distance from this node
                                    # to the closest node occupied some player. By default it's 
                                    # 1000 for convenience. The second number indicates the closest
                                    # player in the following way: 1=red, 0=both and -1=blue. 
        
        self.__reddistance=None     # 
        
        self.__bluedistance=None    
        
        self.__locked=0             
        
#        self.__degree=1 # delete #-symbol
        
    def return_name(self):
        return self.__name
        
    def return_marked(self):
        return self.__marked
    
    def change_marked(self, tf):
        self.__marked=tf
        
    def return_neighbours(self):
        return self.__neighbours
    
    def add_neighbour(self, neighbour):
        self.__neighbours.append(neighbour)
    
    def return_mindistance(self):
        return self.__mindistance
    
    def change_mindistance(self, new_distance):
        self.__mindistance=new_distance    
        
    def return_reddistance(self):
        return self.__reddistance    
    
    def change_reddistance(self, new_distance):
        self.__reddistance=new_distance
    
    def return_bluedistance(self):
        return self.__bluedistance
    
    def change_bluedistance(self, new_distance):
        self.__bluedistance=new_distance            
        
    def return_lockedpoints(self):
        return self.__locked
    
    def change_lockedpoints(self, locked):
        self.__locked=locked    
        
#    def return_degree(self):
#        return self.__degree
    
#    def increase_degree(self):
#        self.__degree+=1
        
#    def decrease_degree(self):
#        self.__degree-=1
        
    
        
    def BFS_3(self, nodelist):
        reserved=0
        self.change_lockedpoints(1)
        Q=[]
        Q.append(self)
        self.change_reddistance(0)
        self.change_mindistance([0,1])
        reserved+=1
        self.change_marked(True)
        while Q:
            v=Q[0]
            del Q[0]
            for w in v.return_neighbours():
                if w.return_marked()==False:
                    w.change_marked(True)
                    reddistance=v.return_reddistance()+1
                    mindistance=w.return_mindistance()[0]
                    w.change_reddistance(reddistance)
                    if reddistance<mindistance:
                        reserved+=1
                        Q.append(w)
                        w.change_lockedpoints(1)
                        w.change_mindistance([reddistance,1])
                    elif reddistance==mindistance:
                        reserved+=0.5
                        Q.append(w)
                        w.change_lockedpoints(0.5)
                        old=w.return_mindistance()[1]
                        if old==-1:
                            w.change_mindistance([reddistance,0])
                        else: pass
                    else: pass
        return reserved      

         

    def BFS_4(self, nodelist, k):
        change_list=[]
        selfpoints=self.return_lockedpoints()
        if selfpoints>0:
            change_list.append([self, selfpoints])
            self.change_lockedpoints(0)
        else: pass
        reserved=0
        Q=[]
        Q.append(self)
        self.change_bluedistance(0)
        reserved+=1
        self.change_marked(True)
        while len(Q)!=0:
            v=Q.pop(0)
            for w in v.return_neighbours():
                if w.return_marked()==False:
                    w.change_marked(True)
                    bluedistance=v.return_bluedistance()+1
                    mindistance=w.return_mindistance()[0]
                    w.change_bluedistance(bluedistance)
                    if bluedistance<mindistance:
                        reserved+=1
                        Q.append(w)
                        change_list.append([w, w.return_lockedpoints()])
                        w.change_lockedpoints(0)
                    elif bluedistance==mindistance:
                        reserved+=0.5
                        Q.append(w)
                        if w.return_mindistance()[1]==1 and w.return_lockedpoints()==1:
                            change_list.append([w, w.return_lockedpoints()])    
                            w.change_lockedpoints(0.5)
                        else:    
                            pass
                    else: pass
        if reserved>=k:
            pass
        else:
            for i in change_list:
                node=i[0]
                node.change_lockedpoints(i[1])
         
                    


    def BFS_5(self, nodelist):
        reserved=0
        Q=[]
        Q.append(self)
        self.change_bluedistance(0)
        reserved+=1
        self.change_marked(True)
        while len(Q)!=0:
            v=Q.pop(0)
            for w in v.return_neighbours():
                if w.return_marked()==False:
                    w.change_marked(True)
                    bluedistance=v.return_bluedistance()+1
                    mindistance=w.return_mindistance()[0]
                    w.change_bluedistance(bluedistance)
                    if bluedistance<mindistance:
                        reserved+=1
                        Q.append(w)
                    elif bluedistance==mindistance:
                        reserved+=0.5
                        Q.append(w)
                    else: pass
        return reserved



