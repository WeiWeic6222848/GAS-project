class node:
    def __init__(self,item=None,next=None,previous=None):
        self.item=item
        self.next=next
        self.previous=previous
class doubleketting:
    def __init__(self):
        """
        init ketting zonder element, + dummy head.
        """
        self.head=node(None)
        self.head.next=self.head
        self.head.previous=self.head
        self.size=0

    def insert(self,item,position):
        """
        :param item: item to insert
        :param position: position to insert
        :return: boolean succes gelukt of niet
        """
        counter=0
        a=self.head
        while counter<position and counter<=self.size:
            if counter==position-1 or counter==self.size:
                previous=a
            a=a.next
            counter+=1
        previous.next=node(item,a,previous)#de volgende van de voorgangde zal nu verwijzen naar een nieuwe node die verwijst naar de element die origineel op dat plaats staat, en terugwijzing.
        previous.next.next.previous=previous.next#analoog
        self.size+=1
        return True

    def isempty(self):
        if self.size==0:
            return 1
        else:
            return 0

    def getlength(self):
        return self.size

    def traverse(self):
        counter=1
        lijst=[]
        if self.isempty()!=1:
            a=self.head.next
            while counter<=self.size:#loop de ketting door.
                lijst.append(a.item)
                a=a.next
                counter+=1
            return lijst
        else:
            print("this ketting is empty")
            return False

    def delete(self,position):
        counter=1
        if position>self.size or position<1:
            print("position out of range")
            return False
        else:
            a=self.head.next
            while counter<position:
                a=a.next
                counter += 1
            a.previous.next=a.next#laten de voriger wijzen naar de volgende element.en dan a verwijderen
            del a
            self.size-=1
            return True

    def retrieve(self,position):
        if position>self.size or position<1:
            print("position out of range")
            return False
        else:
            counter = 1
            a=self.head.next
            while counter<position:
                a=a.next
                counter+=1
            return a.item

if __name__=="__main__":
    ketting=doubleketting()
    ketting.insert(5,1)
    ketting.insert(2,1)
    ketting.insert(1,9)
    ketting.insert(52,2)
    print(ketting.traverse())
    ketting.delete(1)
    print(ketting.traverse())
    ketting.delete(2)
    print(ketting.traverse())
    print(ketting.retrieve(1))
    print(ketting.getlength())
    print(ketting.isempty())
