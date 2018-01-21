class Tabel:#tabel wrapper. naive version
    content=dict()

    def __init__(self):
        self.content=dict()

    def insert(self,key,val):
        self.content[key]=val

    def remove(self,key):
        self.content.pop(key)

    def retrieve(self,key):
        return self.content.get(key,None)

    def size(self):
        return len(self.content)

    def isempty(self):
        return len(self.content)==0

    def traverse(self):
        temp=[]
        for i in self.content:
            temp.append(self.content[i])
        return temp

class Node:#this is just modifield adt code from previous opdracht
    def __init__(self, item, next = None):
        self.item = item
        self.next = next

class Stack:
    def __init__(self):
        self.top = None

    def __del__(self):
        self.top = None

    def isEmpty(self):
        return self.top is None

    def push(self, newItem):
        node = Node(newItem, self.top)
        self.top = node
        return True

    def pop(self):
        if self.isEmpty():
            return None, False
        oldtop = self.top
        self.top = self.top.next
        return oldtop, True

    def getTop(self):
        if self.isEmpty():
            return None
        return self.top.item

    def traverse(self):
        templist=[]
        temp=self.top
        while temp!=None:
            templist.insert(0,temp.item)
            temp=temp.next
        templist.reverse()
        return templist

