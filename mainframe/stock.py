from doubleketting import *
import sys
from functools import reduce

def str_to_class(str):#code from https://stackoverflow.com/questions/1176136/convert-string-to-python-class-object, credit to sixthgear and more.
    return reduce(getattr, str.split("."), sys.modules[__name__])


class tabel:
    content=dict()

    def __init__(self):
        self.content=dict()

    def add(self,key,val):
        self.content[key]=val

    def remove(self,key):
        self.content.pop(key)

    def retrieve(self,key):
        return self.content.get(key,None)

    def size(self):
        return len(self.content)

    def isempty(self):
        return len(self.content)==0

class Stock(tabel):
    def __init__(self,stocklist):
        tabel.__init__(self)
        for i in stocklist:
            self.content[i.capitalize()]=doubleketting()

    def addStock(self, item):
        #this gets a class object, and we need to call str to class to get the class.. i guess? and once we know what kind of item it is, just insert it into the right chain.
        if type(item) == str_to_class("ChocoladeShot"):
            if item.soort=="wit":
                self.content["Wit"].insert(item)
            elif item.soort=="melk":
                self.content["Melk"].insert(item)
            elif item.soort=="zwart":
                self.content["Zwart"].insert(item)
            elif item.soort=="bruin":
                self.content["Bruin"].insert(item)
        else:
            if self.content.get(type(item).__name__,None)!=None:
                self.content[type(item).__name__].insert(item)
            else:
                print("type ",type(item).__name__," is niet teruggevonden in de stock, misschien is dat niet toegevoeg in de ingredient lijst?")
        return True

    def deleteStock(self, item):
        #same thing, but now we're getting a string, and it's lot more easier.
        if self.content.get(item,None)!=None:
            self.content[item].delete()
            return True
        else:
            print(item, " is niet teruggevonden in de stock, typfout?")
            return False

    def checkingredient(self,lijstvaningredient):
        countertable=dict()
        for i in lijstvaningredient:
            countertable[i]=countertable.get(i,0)+1
        for j in countertable:
            amout=countertable[j]
            if self.content[j].size<amout:
                return False
        return True

    #sort methode : producten met vroegst vervaldatum komt eerst
    def sort(self):#oh.. well.. i guess it's in the final version then.
        tempitem=None;
        tempposition=0;
        for i in self.content:
            time=self.content[i].size
            tempdoubleketting=doubleketting()
            for k in range(time):
                expdate = 99999999
                templijst=self.content[i].traverse()
                for j in range (len(templijst)):
                   if templijst[j].expiryDate<expdate:
                        expdate=templijst[j].expiryDate
                        tempitem=templijst[j]
                        tempposition=j+1
                self.content[i].delete(tempposition)
                tempdoubleketting.insert(tempitem)
            self.content[i]=tempdoubleketting


#from here on it's just the class of all the ingredients, with a fixed price and init function which inits the expiry date.
class Chilipeper():
    price = 0.25
    def __init__(self, yyyy,mm,dd):
        self.expiryDate = yyyy*10000+mm*100+dd

class Honing():
    price = 0.5
    def __init__(self, yyyy,mm,dd):
        self.expiryDate = yyyy*10000+mm*100+dd

class Marshmallow():
    price = 0.75
    def __init__(self, yyyy,mm,dd):
        self.expiryDate =yyyy*10000+mm*100+dd

class ChocoladeShot():
    price = 1.0
    def __init__(self,soort, yyyy,mm,dd):
        self.expiryDate = yyyy*10000+mm*100+dd
        self.soort = soort