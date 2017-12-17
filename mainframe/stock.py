import sys
from functools import reduce

def str_to_class(str):
    return reduce(getattr, str.split("."), sys.modules[__name__])


class tabel:
    content = dict()

    def __init__(self):
        self.content = dict()

    def add(self, key, val):
        self.content[key] = val

    def remove(self, key):
        self.content.pop(key)

    def retrieve(self, key):
        return self.content.get(key, None)

    def size(self):
        return len(self.content)

    def isempty(self):
        return len(self.content) == 0


class node:
    def __init__(self, item=None, next=None, previous=None):
        self.item = item
        self.next = next
        self.previous = previous


class doubleketting:
    def __init__(self):
        """
        init ketting zonder element, + dummy head.
        """
        self.head = node(None)
        self.head.next = self.head
        self.size = 0

    # insert altijd op de laatste plaats
    def insert(self, item):
        """
        :param item: item to insert
        :return: boolean succes gelukt of niet
        """
        counter = 0
        a = self.head
        while counter <= self.size:
            if counter == self.size:
                previous = a
            a = a.next
            counter += 1
        previous.next = node(item, a, previous)  # de volgende van de voorgangde zal nu verwijzen naar een nieuwe node
        # die verwijst naar de element die origineel op dat plaats staat, en terugwijzing.
        self.size += 1
        return True

    def isempty(self):
        if self.size == 0:
            return 1
        else:
            return 0

    def traverse(self):
        counter = 1
        lijst = []
        if self.isempty() != 1:
            a = self.head.next
            while counter <= self.size:  # loop de ketting door.
                lijst.append(a.item)
                a = a.next
                counter += 1
            return lijst
        else:
            print("this ketting is empty")
            return False

    def delete(self, item):
        pass


class Stock(tabel):
    def __init__(self):
        tabel.__init__(self)
        self.content["chilipeper"] = doubleketting()
        self.content["honing"] = doubleketting()
        self.content["marshmallow"] = doubleketting()
        self.content["chocoladeshot"] = doubleketting()

    def addStock(self, item):
        if type(item) == str_to_class("Marshmallow"):
            self.content["marshmallow"].insert(item)
        elif type(item) == str_to_class("ChocoladeShot"):
            self.content["chocoladeshot"].insert(item)
        elif type(item) == str_to_class("Chilipeper"):
            self.content["chilipeper"].insert(item)
        elif type(item) == str_to_class("Honing"):
            self.content["honing"].insert(item)
        return True

    def deleteStock(self, item):
        if type(item) == str_to_class("Marshmallow"):
            self.content["marshmallow"].delete(item)
        elif type(item) == str_to_class("ChocoladeShot"):
            self.content["chocoladeshot"].delete(item)
        elif type(item) == str_to_class("Chilipeper"):
            self.content["chilipeper"].delete(item)
        elif type(item) == str_to_class("Honing"):
            self.content["honing"].delete(item)
        return True

    # sort methode : producten met vroegst vervaldatum komt eerst
    def sort(self):
        pass


class Chilipeper(tabel):
    price = 0.25

    def __init__(self, expiryDate,f,hf):
        tabel.__init__(self)
        self.expiryDate = expiryDate


class Honing(tabel):
    price = 0.5

    def __init__(self, yy,mm,dd):
        tabel.__init__(self)
        self.expiryDate = yy


class Marshmallow(tabel):
    price = 0.75

    def __init__(self, expiryDate,f,fgh):
        tabel.__init__(self)
        self.expiryDate = expiryDate


class ChocoladeShot(tabel):
    price = 1.0

    def __init__(self, soort, yy,dd,mm):
        tabel.__init__(self)
        self.expiryDate = yy
        self.soort = soort