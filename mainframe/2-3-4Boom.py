class ItemValue:
    def __init__(self, data):
        self.data = data

class Node:
    def __init__(self):
        self.numOfItems = 0
        self.parent = None
        self.arrayChild = [] #array van knopen
        self.arrayItem = [] #array van data items in een knoop
        #Array initialiseren
        for i in range(4):
            self.arrayChild.append(None)
        for j in range(3):
            self.arrayItem.append(None)

    # vind data item in een knoop
    def retrieveItem(self, key):
        for i in range(3):
            if not self.arrayItem[i]:
                break
            elif self.arrayItem[i].data == key:
                return self.arrayItem[i].data
        return -1

    #de gezochte item verwijderen uit een knoop
    def removeItem(self, delItem):
        delKey = delItem.data
        for i in range(3):
            thisKey = self.arrayItem[i].data
            if delKey == thisKey:
                self.arrayItem[i] = None
                self.numOfItems -= 1
                return True
        return False

    # toevoegen van item in op de juiste plaats binnen een knoop
    def insertItem(self, newItem):
        self.numOfItems += 1 #add new item
        newKey = newItem.data #zoekssleutel van de nieuwe item
        for i in reversed(range(3)): #begin van rechts
            #als item leeg is, ga eentje naar links
            if self.arrayItem[i] == None:
                pass
            #als item niet leeg is
            else:
                thisKey = self.arrayItem[i].data   #zoeksleutel van item op pos i
                if newKey < thisKey:
                    self.arrayItem[i+1] = self.arrayItem[i]  #schuif item op pos i eentje naar rechts
                else:
                    self.arrayItem[i+1] = newItem   #insert new item
                    return i+1      #return pos index

        #nadat alle items zijn verschoven
        self.arrayItem[0] = newItem  # insert new item
        return 0    #return pos index

    #knoop is een blad
    def isLeaf(self):
        return not self.arrayChild[0] #als eerste item van array van knopen leeg is(false is)

    #get number of items
    def getnumOfItems(self):
        return self.numOfItems

    #get item at pos
    def getItem(self, pos):
        return self.arrayItem[pos]

    #get child at pos
    def getChild(self, pos):
        return self.arrayChild[pos]

    #bepalen of een knoop vol is
    def isVol(self):
        return self.numOfItems == 3

    #geef de ouder van een knoop
    def getParent(self):
        return self.parent

    #verwijder een kind
    def removeChild(self, pos):
        tempNode = self.arrayChild[pos]
        self.arrayChild[pos] = None
        return tempNode

    #voeg een kind toe
    def insertChild(self, pos, child):
        self.arrayChild[pos] = child
        if child != None:
            child.parent = self

    #verwijder item met grootste zoeksleutel
    def deleteItem(self):
        temp = self.arrayItem[self.numOfItems - 1] #store grootste item in temp
        self.arrayItem[self.numOfItems - 1] = None
        self.numOfItems -= 1    #verminder aantal items met 1
        return temp

    #inorder traversal
    def inorderitem(self):
        inorder_lijst = []
        if self.isLeaf():
            for i in range(self.numOfItems):
                inorder_lijst.append(self.getItem(i).data)
            return inorder_lijst
        if not self.isLeaf():
            for i in range(4):
                if self.getChild(i) != None:
                    inorder_lijst += self.getChild(i).inorderitem()
                if i<=2 and self.arrayItem[i]!=None:
                    inorder_lijst.append(self.arrayItem[i].data)
        return inorder_lijst

class Twee34Boom:
    def __init__(self):
        self.root = Node()

    def insert(self, value):
        """
        Voeg een data item toe op de juiste plaats
        :param value: Value die we gaan toevoegen
        """
        currentNode = self.root     #begin van wortel
        tempItem = ItemValue(value)
        while True:
            #knoop is vol
            if currentNode.isVol():
                self.split(currentNode)     #split de knoop
                currentNode = currentNode.getParent()
                currentNode = self.get_next_child(currentNode, value)
            #knoop is een blad
            elif currentNode.isLeaf():
                break
            #knoop is geen blad en niet vol
            else:
                currentNode = self.get_next_child(currentNode, value)

        currentNode.insertItem(tempItem)  #insert item

    def get_next_child(self, node, value):
        """
        Geef de kind van een node die uiteindelijk zal leiden tot de gezochte kind
        :param node: node waarvan we de juiste kind gaan vinden
        :param value: value om te vergelijken met data van de items
        :return: node
        """
        numOfItems = node.getnumOfItems()
        for i in range(numOfItems):
            if value < node.getItem(i).data:
                return node.getChild(i)     #return linker kind
        else:
            return node.getChild(i + 1) #return rechter kind

    def inorder_successor(self, node, pos):
        """
        Vind de inordersuccesoor node van in een interne knoop
        :param node: knoop waar de item zit waarvan we de successor node gaan vinden
        :param pos: pos van de item waarvan we de successor node gaan vinden
        :return: successor node
        """
        rightChild = node.getChild(pos+1)
        while True:
            if rightChild.isLeaf():
                break
            else:
                rightChild = rightChild.getChild(0)
        return rightChild

    def remove(self, value):
        """
        Verwijder de item van de input value
        :param value: Value van item die gaan verwijderen
        :return: True als remove gelukt is, anders False
        """
        currentNode = self.root
        toRemove = ItemValue(value)
        if currentNode == None: #root is empty
            return False
        while True:
            if currentNode.retrieveItem(value) == value:
                break
            else:
                currentNode = self.get_next_child(currentNode, value)
        # currentnode is nu de juiste nood waar de delete element zit
        for i in range(currentNode.getnumOfItems()):
            if (currentNode.arrayItem[i].data == value):
                delPOs = i      #hier weet je de index van de element to delete
        if currentNode.isLeaf():    #knoop is blad, ga verder
            pass
        #eerst swappen met inorder successor
        elif not currentNode.isLeaf():
            #IO de inorder successor node, IO is altijd een leaf
            #returnt een node, de IO node
            IO = Node()
            IO = self.inorder_successor(currentNode, delPOs)
            #data van to delete item overschrijven door de inorder successor
            currentNode.arrayItem[delPOs] = IO.arrayItem[0].data
            IO.arrayItem[0] = value #want IO is altijd het meest linkse in de nood
            #current node is nu de IO node, zou dit werken?
            currentNode = IO

        #current node is een blad
        #curretnoode is 3 of 4 knoop, delete de item
        if currentNode.getnumOfItems() >=2:
            currentNode.removeItem(toRemove)
            return True
        #current node is 2 knoop, dan heb je 3 gevallen
        elif currentNode.getnumOfItems() == 1:
            parent = currentNode.getParent()
            sibling = parent.getChild(1)    #hier nog een functie maken, get sibling (left en right)
            #herverdelen
            if sibling.getnumOfItems >=2:
                closestChild = parent.removeChild(0)    #kan 0 of 2 zijn, moet nog verbeteren
                parent.insertItem(closestChild)
                this = parent.deleteItem()  #dit gaat de grootste verwijderen, moet nog verbeteren, aparte functie om de juiste item te verwijderen?
                currentNode.insertItem(this)
                mChild = sibling.removeChild(3)  #kan index 2 of 3 zijn, moet nog verbeteren
                currentNode.insertChild(0, mChild)
            #merge and shorten the tree, dit geval wordt enkel bereikt als parent de root is
            elif parent.getnumOfItems == 1 and sibling.getnumOfItems == 1:
                this = self.merge(parent, sibling)
                currentNode = self.merge(this, currentNode)
            #merge
            elif parent.getnumOfItems >= 2 and sibling.getnumOfItems == 1:
                this = parent.deleteItem() #dit gaat de grootste verwijderen, moet nog verbeteren
                currentNode.insertItem(this)
                currentNode = self.merge(currentNode, sibling)
        currentNode.removeItem(toRemove)
        return True

    #voegt knopen samen, neemt aan dat sibling een 2 knoop is en ene nood heeft 1 item van zijn parent gestolen
    #moet nog verbeteren, werkt niet tussen parent en een sibling
    def merge(self, node1, node2):
        item2 = node2.deleteItem()
        kind2a = node2.removeChild(0)
        kind2b = node2.removeChild(1)
        node1.insertItem(item2)
        node1.insertChild(2,kind2a)
        node1.insertChild(3,kind2b)
        return node1

    def split(self, sNode):
        """
        Splits een knoop dat vol zit
        :param sNode:Knoop die we gaaan splitsen
        """
        # telkens grootste item verwijderen uit de volle knoop en store in item3 en item2 respectively
        grootste_item = sNode.deleteItem()
        middelste_item = sNode.deleteItem()
        #verwijder de twee kinderen op pos 2 en 3 van de volle knoop en store in kind2 en kind3
        kind2 = sNode.removeChild(2)
        kind3 = sNode.removeChild(3)

        #maak een nieuwe node
        newNode = Node()

        if sNode == self.root:  #als de voormalige volle knoop een root is, maak nieuwe root
            self.root = Node()
            parent = self.root  #root wordt de ouder
            self.root.insertChild(0,sNode) #voeg de overige item van de volle knoop als een kind toe aan de root
        else:
            parent = sNode.getParent()  #geef de ouder

        itemPos = parent.insertItem(middelste_item) #itemPos bevat de pos index van de toegevoegde item
        i = parent.getnumOfItems() - 1
        while i > itemPos:
            temp = parent.removeChild(i)
            parent.insertChild(i+1, temp)   #schuif de kind met eentje naar rechts
            i -= 1

        #voeg nieuwe kind toe aan de ouder
        parent.insertChild(itemPos+1, newNode)
        #ken een waarde toe aan de knoop
        newNode.insertItem(grootste_item)
        #voeg kinderen toe aan de knoop
        newNode.insertChild(0,kind2)
        newNode.insertChild(1,kind3)


    def retrieve(self, key):
        """
        Geef het item van een 2-3-4 boom, momenteel print ook found of not found om gemakkelijk te testen of het werkt
        :param key: Waarde dat we zoeken
        :return: Return type boolean, true als het gevonden is, anders false
        """
        currentNode = self.root     #begin van wortel
        while True:
            child = currentNode.retrieveItem(key)
            if child != -1:     #gevonden
                print(key, "Found")
                return True
            elif currentNode.isLeaf():  #niet gevonden
                print(key,"not found")
                return False
            else:
                currentNode = self.get_next_child(currentNode, key)   #zoek een niveau dieper

    def inorder(self):
        """
        Inorder traversal
        :return: lijst van data items
        """
        return self.root.inorderitem()

    def isEmpty(self):
        """
        Check of boom leeg is
        :return:True als boom leeg is, anders false
        """
        if self.root.getItem(0) == None:
            print("true")
            return True
        else:
            print("false")
            return False

    def destroy_tree(self):
        """
        Verwijder de boom
        """
        self.__init__()

if __name__ == "__main__":
    a = Twee34Boom()    #maak een boom
    #return true
    a.isEmpty()
    #voeg deze waarden toe
    a.insert(15)
    a.insert(25)
    a.insert(45)
    a.insert(10)
    a.insert(40)
    a.insert(8)
    a.insert(20)
    a.insert(1)
    a.insert(5)
    a.insert(50)
    a.insert(30)
    a.insert(21)
    a.insert(31)
    # return false
    a.isEmpty()
    print(a.inorder())      #geeft alle data items van de boom weer
    #return true en print ook found
    a.retrieve(50)
    a.retrieve(45)
    #return false en print not found
    a.retrieve(780)
    a.retrieve(945)
    #verwijdert 40
    a.remove(40)
    #geeft alle data items in de boom weer
    print(a.inorder())
    # return false en print not found
    a.retrieve(40)
    #verwijder de boom
    a.destroy_tree()
    #return true
    a.isEmpty()


