#Author: PeterMaltby
#Created: 18/03/2019

from semantics import Node

class Buffer:  ##Buffer class contains all manipulation code.
    data=[]
    count = 0

    def __init__(self):
        data = []

    def find(self, criteria, i = 0):
        for Node in self.data:
            if Node.catagory == criteria: return i
            i +=1
        return None

    def find(self, criteria, i = 0,max = 1000) :##todo remove hardcoded max
        for Node in self.data:
            if Node.catagory == criteria: return i
            if i>max: return None
            i +=1  
        return None
    
    def StartEval(self):##sets root node and sends program to recursivly gen tree.

        root = None
        splice = None # temp vlaue for storing spice postion for recurision.
        
        print((self.find ("Assignment")))
        if (self.find ("Assignment")):
            #if self.find("Assignment",self.find("Assignment")+1):##ensures only one assign per line.
                #print("Error Multiple assign") #add error handeling
            root= self.data[self.find ("Assignment")]
            splice =  self.find ("Assignment")
        elif (self.find("Function")):
            root= self.data[self.find ("Function")]
            splice =  self.find ("Function")
        if splice != None:
            if splice>1: self.Eval(root,True,0,splice-1)
            if splice<len(self.data)-1: self.Eval(root,False,splice+1)



        return root

    def Eval(self, parent, lhn, min=0, max=len(data)): ##recursive eval function
        print(parent, lhn, min,max)
        if (self.find("Function",min,max)):
            if lhn: parent.lhn= self.data[self.find ("Function",min,max)]
            else: parent.rhn= self.data[self.find ("Function",min,max)]
            splice =  self.find ("Function",min,max)
        elif (self.find("Operator",min,max)):
            if lhn: parent.lhn= self.data[self.find ("Operator",min,max)]
            else: parent.rhn= self.data[self.find ("Operator",min,max)]
            splice =  self.find ("Operator",min,max)
        elif (self.find("Variable",min,max)):
            if lhn: parent.lhn= self.data[self.find ("Variable",min,max)]
            else: parent.rhn= self.data[self.find ("Variable",min,max)]
            return
        else : return

        if lhn: parent = parent.lhn##rebases parent in correct node for send 
        else: parent = parent.rhn

        self.Eval(parent,True,min,splice-1)
        self.Eval(parent,False,splice+1,max)

    def add(self, catagory, tokenType, val = None):
        print(catagory)
        self.data.append(Node(catagory, tokenType, val))
        if catagory == "StatementTerminator": 
            GeneratedTrees.append(self.StartEval())
            self.data[self.count].PrintTree()
            self.count =+ 1
            print("tree complete")

GeneratedTrees = []

nodeBuffer = Buffer();
def addNode(catagory, tokenType, val = None):
    nodeBuffer.add(catagory, tokenType, val)


#-------------------------------------------------------------