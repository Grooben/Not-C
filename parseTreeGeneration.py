#Author: PeterMaltby
#Created: 18/03/2019

from semantics import Node

class Buffer:  ##Buffer class contains all manipulation code.
    data=[]
    i =0

    def __init__(self):
        data = []

    def find(self, criteria, d = [], i = 0):
        for Node in d:
            if Node.catagory == criteria: return i
            i +=1
        return None

    def find(self, criteria, d = [], i = 0,max= 1000) :##todo remove hardcoded max
        for Node in d:
            if Node.catagory == criteria: return i
            if i<max: return None
            i +=1  
        return None
    
    def StartEval(self):##sets root node and sends program to recursivly gen tree.

        root = None
        splice = None # temp vlaue for storing spice postion for recurision.
        
        print((self.find ("Assignment",self.data)))
        if (self.find ("Assignment",self.data)):
            print("assignement ma boi");
            if self.find("Assignment",self.data,self.find("Assignment",self.data)):##ensures only one assign per line.
                Print("Error Multiple assign") #add error handeling
            root= self.data[self.find ("Assignment",self.data)]
            splice =  self.data[self.find ("Assignment",self.data)]
        elif (self.find("Function",self.data)):
            root= self.data[self.find ("Function",self.data)]
            root= self.data[self.find ("Function",self.data)]
            splice =  self.data[self.find ("Function",self.data)]
        if splice != None:
            if splice>1: self.Eval(root,True,0,splice-1)
            if splice<len(data)-1: Eval(root,False,splice+1)



        return root

    def Eval(self, parent, lhn, min=0, max=len(data)): ##recursive eval function
        print(parent, lhn, min,max)
        if (self.find("Function",self.data,min,max)):
            if lhn: parent.lhn= self.data[self.find ("Function",self.data,min,max)]
            else: parent.rhn= self.data[self.find ("Function",self.data,min,max)]
            splice =  self.data[self.find ("Function",self.data,min,max)]
        elif (self.find("Operator",self.data,min,max)):
            if lhn: parent.lhn= self.data[self.find ("Operator",self.data,min,max)]
            else: parent.rhn= self.data[self.find ("Operator",self.data,min,max)]
            splice =  self.data[self.find ("Operator",self.data,min,max)]
        elif (self.find("Variable",self.data,min,max)):
            if lhn: parent.lhn= self.data[self.find ("Variable",self.data,min,max)]
            else: parent.rhn= self.data[self.find ("Variable",self.data,min,max)]
            return
        else : return

        if lhn: parent = parent.lhn##rebases parent in correct node for send 
        else: parent = parent.rhn

        Eval(parent,True,min,splice-1)
        Eval(parent,False,splice+1,max)

    def add(self, catagory, tokenType, val = None):
        print(catagory)
        self.data.append(Node(catagory, tokenType, val))
        if catagory == "StatementTerminator": 
            GeneratedTrees.append(self.StartEval())
            self.data[self.i].PrintTree()
            self.i =+ 1
            print("tree complete")

GeneratedTrees = []

nodeBuffer = Buffer();
def addNode(catagory, tokenType, val = None):
    nodeBuffer.add(catagory, tokenType, val)


#-------------------------------------------------------------