# bridge.py
# Author: Tom Zajac
# Description: Provides an interface between the compiler's frontend and backend.

# Represents a piece of data to be stored in memory (e.g. constants, variables)
# In assembly generation, this will be declared in `section .data`
class Data:
    # Datatype (e.g. String, Integer, Bool)
    # typename = ""

    # The identifier for this piece of data - normally this will be the constant/variable name.
    # identifier = ""

    # The value of this data - in Python, keep this a string, even if it's numerical data.
    # value = ""

    def __init__(self, dataType: str, dataIdentifier: str, dataValue: str):
        self.typename = dataType
        self.identifier = dataIdentifier
        self.value = dataValue

# A piece of data passed into a command call.
# This can either be a reference to a variable/constant,
# or the value of a literal.
class CallData:
    # Value of this data.
    # Important: for a variable/constant reference, this should be the Data identifier.
    # For a literal, this should of course store the value of the literal.
    # value = ""

    # True if value points to a variable/constant name,
    # False if value stores a literal.
    # isName = False

    # Datatype of this data.
    # This can stay empty if isName is True.
    # Otherwise, it should be the datatype of the literal.
    # typename = ""

    def __init__(self, typename = "", value = "", isName = False):
        self.value = value
        self.isName = isName
        self.typename = typename

# Represents command calls (e.g. function calls) in the source code.
# In assembly generation, each Call will be placed in `section .text`
class Call:
    # Name of the command
    # This will usually be a function name (e.g. "print"),
    # but can also be a macro or built-in expression.
    # command = ""

    # Data to be passed into the command. Each element is a CallData object.
    # This will usually be the parameter list for a function call.
    # Parameter order is critical for this.
    # Remember to pass Python's "None" constant to represent skipped parameters
    # data = []

    def __init__(self, commandName = "", dataList = []):
        self.command = commandName
        self.data = dataList
    def addData(self, dataObj):
        self.data.append(dataObj)
    def dataCount(self):
        return len(self.data)

class Program:
    # List of data
    # Each element should contain a Data object
    # data = []

    # List of command calls
    # Each element should contain a Call object
    # calls = []
    
    def __init__(self, programData = [], programCalls = []):
        self.data = programData
        self.calls = programCalls
    def callCount(self):
    	return len(self.calls)
    def dataCount(self):
        return len(self.data)
