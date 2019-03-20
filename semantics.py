# Interpreter version
import symtable

class Node: 
    def __init__(self, nodetype, char, lhn = None, rhn = None):
        self.nodetype = nodetype
        self.char = char 
        self.lhn = lhn
        self.rhn = rhn

    def eval(node):
        switcher = {
            "equal": node.equal,
            "addition": node.add,
            "subtraction": node.sub,
            "multiply": node.mult,
            "divide": node.div,
            "variable": node.var,
            "constant": node.const
            }
        function = switcher[node.nodetype]
        return function()

    def equal(node):
        r = node.rhn.eval()
        l = symtable.lookup(node.lhn.char)
        symtable.set_attribute(l, r)
        return

    def add(node):
        l = node.lhn.eval()
        r = node.rhn.eval()
        return l + r

    def sub(node):
        l = node.lhn.eval()
        r = node.rhn.eval()
        return l - r

    def mult(node):
        l = node.lhn.eval()
        r = node.rhn.eval()
        return l * r

    def div(node):
        l = node.lhn.eval()
        r = node.rhn.eval()
        return l / r

    def var(node):
        var = symtable.lookup(node.char)
        return var.value

    def const(node):
        return node.char

    #by peter :) prints all node information not pretty but its enough for testing.

    def PrintTree(self):
        print(self.nodetype , " - \'", self.char, "\'\n left Node- ")
        if self.lhn == None : print(self.lhn)
        else : self.lhn.PrintTree()

        print("right node- ")

        if self.rhn == None : print(self.rhn)
        else : self.rhn.PrintTree()

        print("\n")
    

