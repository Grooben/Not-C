#Author: PeterMaltby
#Created: 18/03/2019

from semantics import Node

class TreeGen:  ##Buffer class contains all manipulation code.
    data=[]
    GeneratedTrees = []
    count = 0

    def __init__(self):
        data = []

    def find(self, criteria, i = 0):
        for Node in self.data:
            if Node.catagory == criteria: return i
            i +=1
        return None

    def find(self, criteria, i = 0,max = 1000) :##todo remove hardcoded max
        if max>len(self.data)-1:max = (len(self.data)-1)
        while True:
            if self.data[i].catagory == criteria: return i
            if i>=max: return "Null"
            i = i+1
    
    def StartEval(self):##sets root node and sends program to recursivly gen tree.

        root = None
        splice = None # temp vlaue for storing spice postion for recurision.
        
        if (self.find ("Assignment")!= "Null"):
            #if self.find("Assignment",self.find("Assignment")+1):##ensures only one assign per line.
                #print("Error Multiple assign") #add error handeling
            root= self.data[self.find ("Assignment")]
            splice =  self.find ("Assignment")
        elif (self.find("Function")!= "Null"):
            root= self.data[self.find ("Function")]
            splice =  self.find ("Function")
        if splice != "Null":
            if splice>1: self.Eval(root,True,0,splice-1)
            if splice<len(self.data)-1: self.Eval(root,False,splice+1)

        return root

    def Eval(self, parent, ln, min=0, max= None): ##recursive eval function
        if max == None : max=len(self.data)-1
        print(parent, ln, min,max)

        if (self.find("Function",min,max)!= "Null"):
            if ln: parent.lhn= self.data[self.find ("Function",min,max)]
            else: parent.rhn= self.data[self.find ("Function",min,max)]
            splice =  self.find ("Function",min,max)
        elif (self.find("Comma",min,max)!= "Null"):
            if ln: parent.lhn= self.data[self.find ("Comma",min,max)]
            else: parent.rhn= self.data[self.find ("Comma",min,max)]
            splice =  self.find ("Comma",min,max)
        elif (self.find("Operator",min,max)!= "Null"):
            if ln: parent.lhn= self.data[self.find ("Operator",min,max)]
            else: parent.rhn= self.data[self.find ("Operator",min,max)]
            splice =  self.find ("Operator",min,max)
        elif (self.find("Variable",min,max)!= "Null"):
            if ln: parent.lhn= self.data[self.find ("Variable",min,max)]
            else: parent.rhn= self.data[self.find ("Variable",min,max)]
            return
        else : return

        if ln: parent = parent.lhn##rebases parent in correct node for send 
        else: parent = parent.rhn

        if splice-1>=min:self.Eval(parent,True,min,splice-1)
        if splice+1<=max:self.Eval(parent,False,splice+1,max)
        

    def add(self, catagory, tokenType, val = None):
        #print(catagory, " ", tokenType)
        self.data.append(Node(catagory, tokenType, val))
        if catagory == "EOL": 
            self.GeneratedTrees.append(self.StartEval())
            
            self.GeneratedTrees[self.count].PrintTree()
            self.data.clear()
            self.count = self.count + 1
            print("tree complete")

    def retrieve(self, n):
        return GeneratedTrees[n]

##redundant class used for test adding now done withen class.
def addNode(catagory, tokenType, val = None):
    nodeBuffer.add(catagory, tokenType, val)


#-------------------------------------------------------------