from ketting import node
#from previous taak, modified
class Queue:
    def __init__(self):
        self.backptr=None
        self.size=0

    def insert(self,naam):
        """
        :param naam: naam van een object, bv naam van klanten
        :return: succes of niet
        """
        if self.size==0:
            self.backptr=node(naam)
            self.backptr.next=self.backptr
            self.size+=1
            return True
        else:
            old=self.backptr
            self.backptr=node(naam,self.backptr.next)
            old.next=self.backptr
            self.size+=1
            return True

    def isempty(self):
        if self.size==0:
            return True
        else:
            return False

    def getlength(self):
        """
        :return: lengte van queue
        """
        return self.size

    def delete(self):
        """
        verwijderd de eerste klant
        :return:succes of niet
        """
        if self.isempty()==False:
            self.backptr.next=self.backptr.next.next
            if self.size==1:
                self.backptr=None
            self.size-=1
            return True
        else:
            return False

    def gettop(self):
        """
        :return:de eerste klantse naam
        """
        if self.isempty()==False:
            return self.backptr.next.item
        else:
            return False

    def traverse(self):
        """
        :return: niks, print de rij van begin tot einde
        """
        templist=[]
        if self.isempty()==False:
            counter=0
            a=self.backptr.next
            while counter<self.size:
                templist.append(a.item)
                a=a.next
                counter+=1
        return templist

    def insertonfront(self,item):

        if self.size==0:
            self.backptr=node(item)
            self.backptr.next=self.backptr
            self.size+=1
            return True
        else:
            self.backptr.next=node(item,self.backptr.next)
            self.size+=1
            return True

if __name__=="__main__":
    a=Queue()
    a.insert("hey")
    a.insert("hello")
    a.insert("howareyou")
    a.delete()
    a.delete()
    print(a.gettop())
    print(a.getlength())
    a.traverse()
