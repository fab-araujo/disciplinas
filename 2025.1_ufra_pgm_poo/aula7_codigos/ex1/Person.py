# Person class

class Person():

    def __init__(self, name, salary):
        self.__name = name
        self.__salary = salary

    def getName(self):
        return self.__name

    def setName(self, newName):
        self.__name = newName
 
    # Allow the caller to retrieve the salary
    def getSalary(self): 
        return self.salary

    # Allow the caller to set a new salary
    def setSalary(self, salary):
        self.salary = salary
