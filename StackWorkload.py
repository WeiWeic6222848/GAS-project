class Node:
    def __init__(self, item,next):
        self.item = item
        self.next = next




class StackWorkload:
    def __init__(self):

        self.top = None

    def __del__(self):
        self.top = None

    def isEmpty(self):
        if self.top == None:
            return True
        else:
            return False

    def push(self, newItem):

        node = Node(newItem, self.top)
        self.top = node
        return True

    def pop(self):
        if self.isEmpty():
            return None, False
        denoudentop = self.top.item
        self.top = self.top.next
        return denoudentop, True

    def getTop(self):


        if self.isEmpty():
            return None,False
        return self.top.item, True
