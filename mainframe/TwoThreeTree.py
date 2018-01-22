from copy import *

#klasse Node met een key en een value
class Node():
    def __init__(self,key,value):
        self.key = key
        self.content = value

#klasse van een 23 boom dat van onder naar boven groeit
class TwoThreeTree():
    def __init__(self, Data=[None,None,None], parent=None, Childs=[None,None,None,None]):
        self.Data = Data.copy()  #list met plaats voor drie data items
        self.parent = parent        #  parent van de huidige tree
        self.Childs = Childs.copy() # list met plaats voor deelbomen
        self.counter = 0



    def getwortel(self):    # geeft de wortel terug.(Nodig Want de Boom groeit van onder naar boven)
        root = self
        while (root.parent != None):
            root = root.parent
        return root


    def insert(self,key, NewItem): #insert (nodig want de insert helper heeft de root nodig)
        self.InsertHelper(self.getwortel(),key, NewItem)

    def DataSize(self): # geeft de size van een data list terug
        size = 0
        for i in self.Data:
            if i != None:
                size += 1
        return size


    def InsertHelper(self, root,key, NewItem): #insert een nieuwe item
        item = Node(key, NewItem)

        if (root.Childs[0] == None): #als de root geen kinderen heeft mag het de item toevoegen

            if (root.Data[2] == None): #

                root.InsertToData(item)
                if (root.Data[2] != None):
                    root.split() # als er 3 items zijn in de lijst wordt de split functie aangeroepen

        elif (root.Data[0] != None and root.Data[1] != None): # als er 2 data items zijn in de root

            if (item.key < root.Data[0].key):
                self.InsertHelper(root.Childs[0],key, NewItem)
            elif (item.key < root.Data[1].key):
                self.InsertHelper(root.Childs[2],key, NewItem)
            else:

                self.InsertHelper(root.Childs[3],key, NewItem)

        else: # als er 1 data item is in de root

            if (item.key < root.Data[0].key):
                self.InsertHelper(root.Childs[0],key, NewItem)
            else:
                self.InsertHelper(root.Childs[3],key, NewItem)

    def InsertToData(self, Item): # gebruikt om items in de data item list toe te voegen. De items worden ook gesorteerd

        if self.Data[0] == None:
            self.Data[0] = Item
        elif (self.Data[1] == None):
            if Item.key > self.Data[0].key:
                self.Data[1] = Item
            else:
                self.Data[1] = self.Data[0]
                self.Data[0] = Item
        elif (self.Data[2] == None):
            if (Item.key < self.Data[0].key):
                self.Data[2] = self.Data[1]
                self.Data[1] = self.Data[0]
                self.Data[0] = Item
            elif (Item.key < self.Data[1].key):
                self.Data[2] = self.Data[1]
                self.Data[1] = Item
            else:
                self.Data[2] = Item



    def split(self): # deze functie wordt gebruikt om een root met 3 items op te splitsen
        n1 = self       #linker deelboom
        n2 = TwoThreeTree([self.Data[2], None, None], [None, None, None, None]) #rechter deelboom

        if (self.parent == None): #geval dat de parent van de huidige tree leeg is
            p = TwoThreeTree([self.Data[1], None, None], None, [n1, None, None, n2])
            self.parent = p
            n2.parent = p
            n1.Data = [n1.Data[0], None, None]

        else:
            p = self.parent
            p.InsertToData(self.Data[1])

            if (p.DataSize() == 2): # de parent heeft 2 items
                if (self.Data[0].key > p.Data[0].key):
                    p.Childs[2] = n1
                    p.Childs[3] = n2
                    p.Childs[2].parent = p
                    p.Childs[3].parent = p

                else:
                    p.Childs[2] = n2
                    p.Childs[0] = n1
                    p.Childs[0].parent = p
                    p.Childs[2].parent = p

            else:
                if(self.Data[0].key <p.Data[0].key ): #het eerste data element van de huidige boom is kleiner dan het eerste element van de parent van de huidgie boom
                    if (n2.Data[0].key > p.Childs[2].Data[0].key):  #
                        p.Childs[0] = n1
                        p.Childs[1] = p.Childs[2]
                        p.Childs[2] = n2

                    else:
                        p.Childs[0] = n1
                        p.Childs[1] = 2

                    p.Childs[1].parent = p
                    p.Childs[2].parent = p
                    p.Childs[3].parent = p

                elif (self.Data[0].key < p.Data[1].key):
                    p.Childs[1] = n1
                    p.Childs[2] = n2
                    p.Childs[1].parent = p
                    p.Childs[2].parent = p

                else:

                    if(n1.Data[0].key > p.Childs[2].Data[0].key):
                        p.Childs[1] = p.Childs[2]
                        p.Childs[2] = n1
                        p.Childs[3] = n2
                    else:
                        p.Childs[1] = n1
                        p.Childs[3] = n2
                    p.Childs[1].parent = p
                    p.Childs[2].parent = p
                    p.Childs[3].parent = p

            n1.Data[1] = None
            n1.Data[2] = None

        #Geval dat de 4 items van Childs vol is
        if (n1.Childs[0] != None and n1.Childs[1] != None and n1.Childs[2] != None and n1.Childs[3] != None):
            n2.Childs = [n1.Childs[2], None, None, n1.Childs[3]]
            n1.Childs = [n1.Childs[0], None, None, n1.Childs[1]]
            n2.Childs[3].parent = n2
            n2.Childs[0].parent = n2
            n1.Childs[3].parent = n1
            n1.Childs[0].parent = n1

        #split als er 3 items zijn
        if (p.Data[2] != None):
            p.split()


    def inorder(self):#
        """
        functie dat nodig is omdat de boom van onder naar boven groeit
        :return: geeft een lijst terug met items in inorder
        """
        return self.inorderhelper(self.getwortel())


    def isEmpty(self):
        """

        :return: geeft een bool terug. Als leeg = True
        """
        root = self.getwortel()
        if(root.Childs == [None,None,None,None] and root.Data == [None,None,None]):
            return True
        else:
            return False


    def inorderhelper(self, root): # print de items volgens inorder traverse
        """

        :param root:
        :return: geeft een lijst terug met items in order
        """
        List = []
        if (root.Childs[0] == None):

            for i in root.Data:
                if i != None:
                    List.append(i.content)



        elif (root.Data[1] != None):

            List += self.inorderhelper(root.Childs[0])
            #print(root.Data[0].key)
            if(root.Data[0] != None):
                List.append(root.Data[0].content)
            List += self.inorderhelper(root.Childs[2])
            #print(root.Data[1].key)
            if (root.Data[1] != None):
                List.append(root.Data[1].content)
            List += self.inorderhelper(root.Childs[3])
        else:
            List += self.inorderhelper(root.Childs[0])
            #print(root.Data[0].key)
            if (root.Data[0] != None):

                List.append(root.Data[0].content)
            List += self.inorderhelper(root.Childs[3])

        return List

    def findNode(self, root, searchkey): # zoekt de node op met een bepaalde searchkey. geeft een tuple terug met de node en met de index van het item met de searcjkey


        if(root.Data[0] != None and root.Data[0].key == searchkey):
            return (root,0)

        elif (root.Data[1] != None and root.Data[1].key == searchkey):
            return (root, 1)

        elif (root.Data[2] != None and root.Data[2].key == searchkey):
            return (root, 2)


        elif (root.Childs[0] == None):
            return None

        elif (root.Data[1] != None):
            if (searchkey < root.Data[0].key):
                return self.findNode(root.Childs[0], searchkey)
            elif (searchkey < root.Data[1].key):
                return self.findNode(root.Childs[2], searchkey)
            else:
                return self.findNode(root.Childs[3], searchkey)


        elif(root.Data == [None,None,None]):
            if(root.Childs[0].Data[0].key == searchkey):
                return (root.Childs[0],0)
            else:
                return (root.Childs[0],1)
        else:
            if (searchkey < root.Data[0].key):
                return self.findNode(root.Childs[0], searchkey)
            else:
                return self.findNode(root.Childs[3], searchkey)



    def retrieve(self,searchkey):
        return self.retrieveItem(self.getwortel(),searchkey)

    def retrieveItem(self, root, searchkey): #geeft true terug als het item bestaat
        if (searchkey == root.Data[0].key):

            return root.Data[0].content

        elif (root.Data[1] != None and searchkey == root.Data[1].key ):

            return root.Data[1].content

        elif (root.Data[2] != None and searchkey == root.Data[2].key):

            return root.Data[2].content


        elif (root.Childs[0] == None):

            return False

        elif (root.Data[1] != None):
            if (searchkey < root.Data[0].key):
                return self.retrieveItem(root.Childs[0], searchkey)
            elif (searchkey < root.Data[1].key):
                return self.retrieveItem(root.Childs[2], searchkey)
            else:
                return self.retrieveItem(root.Childs[3], searchkey)

        else:
            if (searchkey < root.Data[0].key):
                return self.retrieveItem(root.Childs[0], searchkey)
            else:
                return self.retrieveItem(root.Childs[3], searchkey)



    def deleteItem(self, searchkey):
        self.deletehelper(self.getwortel(), searchkey)

    def deletehelper(self, root, searchkey): # delete een item met een bepaalde searchkey
        node = self.findNode(root, searchkey)
        leafnode = node[0]
        if(node != None):
            IS = self.InorderSuccessor(node[0])
            if(node[0].Childs[0] != None):


                temp = node[0].Data[node[1]]

                #node[0].InsertToData(IS[0].Data[IS[1]])
                if(IS[0].Data[IS[1]].key >node[0].Data[0].key):
                    node[0].Data[1] = IS[0].Data[IS[1]]
                else:
                    node[0].Data[0] = IS[0].Data[IS[1]]

                IS[0].Data[IS[1]] = temp
                leafnode = IS[0]

            if(leafnode.DataSize() == 1 ):
                leafnode.Data[IS[1]] = None
                if(leafnode.parent == None and leafnode.Data == [None,None,None] and leafnode.Childs == [None,None,None,None]):
                    return True
                self.fix(leafnode)

            else:
                if(node[1] == 0):
                    temp = leafnode.Data[1]
                    leafnode.Data[0] = None
                    leafnode.Data[1] = None
                    leafnode.InsertToData(temp)
                else:
                    temp = leafnode.Data[0]
                    leafnode.Data [1] = None
                    print(self.counter)
                    #if(self.counter == 0):
                        #leafnode.InsertToData(temp)


            return True
        return False






    def fix(self,root): # gebruikt voor het herverdelen en samenvoegen na een delete

        if(root.parent == None):
            if(root.Childs[0].Childs[0] == None and root.Childs[0].Childs[3] == None):
                self.counter += 1
                if(self.counter == 2):


                    self.parent = None


                    self.counter = 0
                elif(self.counter == 3):
                    root.Childs[0].Data[0] = None

            elif(root.Childs[0].Childs[0].Data[0] != None and root.Childs[0].Childs[3].Data[0]!= None):
                root.Childs[0].Childs[2] = root.Childs[0].Childs[3]
                root.Childs[0].Childs[3] = root.Childs[3].Childs[0]
                root.Childs[0].Childs[2].parent = root.Childs[0]
                root.Childs[0].Childs[3].parent = root.Childs[0]
                root.Childs[3].Childs[0] = None
                root.Childs[0].parent = None
            else:
                root.Childs[0].Childs[2] = root.Childs[3].Childs[0]
                root.Childs[0].Childs[3] = root.Childs[3].Childs[3]
                root.Childs[0].Childs[2].parent = root.Childs[0]
                root.Childs[0].Childs[3].parent = root.Childs[0]
                root.Childs[3].Childs[0] = None
                root.Childs[3].Childs[3] = None
                root.Childs[0].parent = None

        else:
            p = root.parent
            counter = 0
            for i in p.Childs:
                if(i != None and i.Data[1] != None and i!= root):

                    counter += 1
                    self.redistirbute(root,i)
                    break
            if(counter == 0):
                self.merge(root)




    def redistirbute(self,root,sibling):#herverdeeld de items
        p = root.parent
        if(p.Data[1] == None):
            if(root == p.Childs[0]):
                root.Data[0] = p.Data[0]
                p.Data[0] = sibling.Data[0]
                sibling.Data[0] = sibling.Data[1]
                sibling.Data[1] = None
                if(sibling.Childs[0] != None ): #geval dat bij lege interne knoop
                    root.Childs[3] = sibling.Childs[0]
                    sibling.Childs[0] = sibling.Childs[2]
                    sibling.Childs[2] = None

            else:
                root.Data[0] = p.Data[0]
                p.Data[0] = sibling.Data[1]
                sibling.Data[1] = None
                if(sibling.Childs[3] != None):
                    root.Childs[3] = root.Childs[0]
                    root.Childs[0] = sibling.Childs[3]
                    sibling.Childs[3] = sibling.Childs[2]
                    sibling.Childs[2] = None


        else:
            if(root == p.Childs[0]):
                if(sibling == p.Childs[2]):
                    root.Data[0] = p.Data[0]
                    p.Data[0] = sibling.Data[0]
                    sibling.Data[0] = sibling.Data[1]
                    sibling.Data[1] = None
                if(sibling == p.Childs[3]):
                    root.Data[0] = p.Data[0]
                    p.Data[0] = p.Childs[2].Data[0]
                    p.Childs[2].Data[0] = p.Data[1]
                    p.Data[1] = p.Childs[3].Data[1]
                    p.Childs[3].Data[1] = p.Childs[3].Data[2]
                    p.Childs[3].Data[1] = None


            elif(root == p.Childs[2]):
                if(sibling == p.Childs[0]):
                    root.Data[0] = p.Data[0]
                    p.Data[0] = sibling.Data[1]
                    sibling.Data[1] = None
                else:
                    root.Data[0] = p.Data[1]
                    p.Data[1] = sibling.Data[0]
                    sibling.Data[0] = sibling.Data[1]
                    sibling.Data[1] = None
            else:
                if(sibling == p.Childs[2]):
                    root.Data[0] = p.Data[1]
                    p.Data[1] = sibling.Data[1]
                    sibling.Data[1] = None
                else:
                    root.Data[0] = p.Data[1]
                    p.Data[1] = p.Childs[2].Data[0]
                    p.Childs[2].Data[0] = p.Data[0]
                    p.Data[0] = p.Childs[0].Data[1]
                    p.Childs[0].Data[1] = None



    def merge(self,root): # voegt de items samen
        p = root.parent
        if(p.Data[1] != None):
            if(root == p.Childs[0]):
                p.Childs[0] = p.Childs[2]
                p.Childs[2] = None
                p.Childs[0].InsertToData(p.Data[0])
                p.Data[0] = p.Data[1]
                p.Data[1] = None
            elif(root == p.Childs[2]):
                p.Childs[3].InsertToData(p.Data[1])
                p.Data[1] = None

            else:
                p.Childs[3] = p.Childs[2]
                p.Childs[2] = None
                p.Childs[3].InsertToData(p.Data[1])
                p.Data[1] = None

        else:
            if(root == p.Childs[0]):
                p.Childs[0].InsertToData(p.Data[0])
                p.Childs[0].InsertToData(p.Childs[3].Data[0])
                p.Childs[3].Data[0] = None
                p.Data[0] = None
                self.fix(p)

            else:
                p.Childs[0].InsertToData(p.Data[0])
                p.Data[0] = None
                self.fix(p)







    def InorderSuccessor(self,root): #zoekt de inorder succesor
        if(root.Childs[0] == None):
            if(root.Data[1] == None):
                return (root,0)
            else:
                if(root.parent == None):
                    return (root,0)
                elif(root == root.parent.Childs[3]):
                    return (root,0)
                else:
                    return (root,3)
        else:
            if(root.Childs[0].Childs[0] == None):
                return (root.Childs[0],0)
            else:
                return self.InorderSuccessor(root.Childs[0].Childs[3])







if __name__ == '__main__':


    tree = TwoThreeTree()
    tree.insert(15,"text15")
    tree.insert(6,"text6")
    tree.insert(20,"text20")
    tree.insert(3,"text3")
    tree.insert(4,"text4")
    tree.insert(19,"text19")
    tree.insert(18,"text18")
    print(tree.retrieveItem(tree.getwortel(), 6))
    print(tree.retrieveItem(tree.getwortel(), 20))
    print(tree.retrieveItem(tree.getwortel(), 27))
    print(tree.getwortel().Data)

    print(tree.inorder())

    tree.deleteItem(3)



    tree.deleteItem(20)
    print("#######")
    print(tree.inorder())


    tree.deleteItem(4)
    print("#######")
    print(tree.inorder())

    tree.deleteItem(19)
    print("#######")
    print(tree.inorder())

    tree.deleteItem(15)
    print("#######")
    print(tree.inorder())

    tree.deleteItem(18)
    print("#######")
    print(tree.inorder())

    tree.deleteItem(6)
    print("#######")
    print(tree.inorder())

    tree.insert(7,"text7")
    print("#######")
    print(tree.inorder())

    tree.insert(1, "text1")
    print("#######")
    print(tree.inorder())

    tree.insert(8, "text8")
    print("#######")
    print(tree.inorder())

    tree.insert(14, "text14")
    print("#######")
    print(tree.inorder())

    tree.insert(2, "text2")
    print("#######")
    print(tree.inorder())

    tree.insert(13, "text13")
    print("#######")
    print(tree.inorder())

    tree.deleteItem(8)
    print("#######")
    print(tree.inorder())

    tree.deleteItem(2)
    print("#######")
    print(tree.inorder())

    tree.deleteItem(14)
    print("#######")
    print(tree.inorder())
