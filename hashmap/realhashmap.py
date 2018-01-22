#to Prof or Assistant:
#Honestly I don't really understand the concept of the class wrapper.. which mr.Tom has said once.
#so i just made some function seperatly, inside of their class, i think this will make the changing of implementation easier
#but i don't know if it's what i should be doing.
#I'm going to ask some question in the next practicum for sure..
#
#Greets
from copy import deepcopy


class dataitem:#dataitem is an class which contains an random content object of any kind and a searchkey object which is going to be an integer
    content=None
    key=None
    def __init__(self,item,key):#setting the item and the searchkey
        self.content=item
        self.key=key

class node:#node is a class with a nodeitem which is a dataitem and a pointer to the next node and maybe to the previous node if any
    nodeitem=None
    next=None
    previous=None

    def __init__(self,item,next=None,previous=None):#triviaal
        self.nodeitem=item
        self.next=next
        self.previous=previous

    def addonemore(self,item):#making some functions right on the node class to make the change afterward easier.
        self.previous=node(item,self)
        return self.previous

    def delsomething(self,val):#go through the node and find the right item then delete it by linking the previous one to the next one.
        #special case is already tested on the hashmap class.
        temp = self
        if temp.nodeitem.key==val:
            temp.next=None

        while temp != None:
            if temp.nodeitem.key == val:
                temp.previous.next = temp.next
                temp.previous = None
                return True
            else:
                temp = temp.next
        print("nothing here on chaining")

    def nodetraverse(self):#defined a function to return a list of all dataitems, it is important for swapping probe
        temp = self
        templist=[]
        while temp != None:
            #print(temp.nodeitem.content,"          Key:",temp.nodeitem.key)
            templist.append(temp.nodeitem)
            temp=temp.next
        return templist

    def retrieve(self,val):#also an retrieve function inside of the node which makes changes easier i guess
        temp = self
        while temp != None:
            if temp.nodeitem.key == val:
                return temp
            else:
                temp = temp.next
        return None


class hashmap:#hashmap is the main class in this code, it has an dictionary which stores the dataitem in to a random place with the hashfunction.
    #I simply used the hashfunction key%size.

    probing=0   #the probing is introduced with the probing integer,
    #if probing is 0 then it's going to be sequential probing, I've set it as default
    # one is quatratic probing, two is double hashing which i appearently doesn't need to make, but i kept it. just beacause it won't harm

    size=0     #size indicates the size of the hashtable, it doesn't have a dafault value so you have to input it.

    #array=dict()   #array, or hashtable is an dictionary, I restricted the length of it on the functions but if someone goes accros the wall then it might be broken.

    def __init__(self,size=100,probing=0):#triviaal
        self.size=size
        self.probing=probing
        self.array = dict().copy()

    def openadressing(self,item,mode=0): #item parameter is used both as key and as an item, since that they all need to probe, i just merged them into some strange thing..
        """
        :param item: this is simply the item to add or if it's not an insert, a key to delete or to retrieve
        :param mode: this parameter indicates the working of this probing, it can be either an insert(if mode==0) a delete(mode==1) or a retrieve(mode==2)
        by doing this i don't have to write a lot of codes.
        although maybe i can also write something that only returns an probing adress.. doesn't really know but i think that there might be a better way...
        :return: diffrent mode returns diffrent things.
        insert and delete returns succes boolean and retrieve returns an item. python is really handy in this point i guess.
        """

        if mode==0:
            originalposition=item.key%self.size #calculate the original starting position first,
        else:
            originalposition=item%self.size #if it's not insert then item is a key value, and must be modded directly, don't call .key property.
        counter=1 #first try of probing
        currentposition=originalposition+counter #either sequential or quatratic, the first step is always +1
        #note that im not checking the original position beacause it's already tested before this function will be called.
        while currentposition >= self.size:#if the position goes out of range just min until it gets under. maybe modulo will also do it now i think about it. ..
            currentposition -= self.size
        while currentposition!=originalposition:#since that we did +1 to the original position, the currentposition is nomore the same as original, we can start probing until it goes back to original
            if mode==0:
                #insert, if currentposition doesn't have any item then insert item
                if self.array.get(currentposition,None)==None:
                    self.array[currentposition]=item
                    return True
            elif mode==1:
                #delete, if the key of current position is the given key, delete(pop) it.
                if self.array.get(currentposition,dataitem(None,None)).key==item:
                    self.array.pop(currentposition,None)
                    return True
            elif mode==2:
                #retrieve, if the key of current position is the given key, return the item.
                if self.array.get(currentposition,dataitem(None,None)).key==item:
                    return self.array[currentposition]
            counter+=1
            #probing counter+1
            if self.probing==0: currentposition=originalposition+counter #if it's an sequential one, just let original position + counter
            elif self.probing==1: currentposition=originalposition+counter.__pow__(2) #else let original position + the power of probe time.
            while currentposition>=self.size:#if position outof range, pull it back in
                currentposition-=self.size

        if mode==0:
            #some informational code
            print("either table is full or  there is a circulair probing this is mixed probe")
            return False
        elif mode==1:
            print("not found on mixed")
            return False
        return dataitem(None,None)#if mode==2 just return an empty dataitem

    """
    def doublehashing(self,val,delete=False):
        originalposition=val%self.size
        hashingstep=23-val%23
        counter=1
        if self.probing==2: #2=double hashing
            currentposition=originalposition+hashingstep*counter
            while currentposition!=originalposition:
                if delete==False:
                    if self.array.get(currentposition,None)==None:
                        self.array[currentposition]=val
                        return True
                else:
                    if self.array.get(currentposition,None)==val:
                        self.array.__delitem__(val)
                        return True
                counter+=1
                currentposition=originalposition+counter*hashingstep
                while currentposition>=self.size:
                    currentposition-=self.size
            if delete==False:
                print("the probing failed on double hasing, maybe.. idk")
            else:
                print("wtf.... aahahha")
            return False
    """

    def seperatechaining(self,item,mode=0):
        if self.probing==3: #3=seperatechaining, only written for test purpose
            if mode == 0:
                #if it's an insert, just calculate the position and call the insert in node class
                position = item.key % self.size
                if self.array.get(position, None) == None:
                    #if there is nothing yet, make a new node.
                    self.array[position]=node(item,None,None)
                else:
                    self.array[position]=self.array[position].addonemore(item)
                return True
            elif mode==1:
                #delete, now if there is anything to delete, then call the delete in node class.
                #maybe i doesn't even have to test wether it's empty, beacause i already done it in the main call of delete.
                #can't remember clearly.
                position = item % self.size
                if self.array.get(position, None) == None:
                    print("nothing here on chaining")
                elif self.array[position].nodeitem.key==item:
                    #some desperate last changes for special case delete first elements
                    self.array[position]=self.array[position].next
                    if  self.array[position]==None:
                        self.array.pop(position)
                    return True
                else:
                    self.array[position].delsomething(item)
                return False
            elif mode==2:
                #else it's retrieve, if anything can be retrieved, call retrieve in node class.
                position = item % self.size
                if self.array.get(position, None) == None:
                    print("nothing here on chaining")
                else:
                    return self.array[position].retrieve(item)



    def getintvalueofstring(self,key):
        tempint=0
        for i in range (len(key)):
            tempint+=ord(key[i])+2**i
        return tempint
    
    def getlength(self):
        return len(self.traverse())
    
    def insert(self,key,value):
        if type(key)!=type(1):
            key=self.getintvalueofstring(key)
        item=dataitem(value,key)
        #insert which accepts an dataitem with proper key and content to insert
        if len(self.array)<self.size and self.array.get(key%self.size,None)==None: #testing if the hashmap is full, and wether the first position is already take
            #if not, just add it into list
            if self.probing!=3:
                self.array[item.key%self.size]=item
            else:
                #if probing is chaining, just let the function handle it.
                return self.seperatechaining(item)
            return True
        else:
            if self.probing!=3:
                #it the first position is already tooked, start probing
                return self.openadressing(item)
            else:
                return self.seperatechaining(item)


    def delete(self,val):
        #delete takes val which is the key of a certain dataitem
        if type(val)!=type(1):
            val=self.getintvalueofstring(val)
        if self.probing!=3:
            if self.array.get(val%self.size,dataitem(None,None)).key==val: #if the first possible place is the correct one, just delete it
                #note. nothing, i went to change some code and forget what i wanted to write here.
                self.array.pop(val%self.size)
                return True
            else:#if not on first place, just start probing mode1
                return self.openadressing(val, 1)
        else:#delete of chainning just call function
                return self.seperatechaining(val,1)

    def traverse(self):
        #this is simple traverse tho. no list outputted
        templist=[]
        if self.probing!=3:
            for i in self.array:
                templist.append(self.array[i].content)
                #print (self.array[i].content)
        else:
            for i in self.array:
                #probe3 calling nodetraverse.
                templist+=self.array[i].nodetraverse()
        return templist

    def switchprobing(self,probe):
        #to swap probing, simply make a temp hashmap and insert all the comtent of the current map into the temp map.
        #if all of the item succeded, then just copy the table of the temp map and then change the probe mode to the new one
        #and it's complete
        temp=hashmap(self.size,probe)
        temp.array={}
        succes=True
        for i in self.array:
            if self.probing!=3:
                if succes == False:
                    break
                succes=temp.insert(self.array[i].key,self.array[i])
            else:
                #if chained, get every item on chain and add then
                templist=self.array[i].nodetraverse()
                for j in templist:
                    if succes == False:
                        break
                    succes = temp.insert(j.key,j)
        if succes==False:#if one fails this will come
            print("er is een circulaire probing na switch of er is geen genoeg plaats na switch, stopping")
            return False
        else:#else it's succesful
            self.array=temp.array
            self.probing=probe
            print("succesfully switched to probe mode ", probe)

    def isempty(self):
        return len(self.array)==0

    def retrieve(self,key):
        if type(key)!=type(1):
            key=self.getintvalueofstring(key)
        if self.probing != 3:
            if self.array.get(key % self.size, dataitem(None, None)).key == key:  # if the first one.. return this else start probe
                return self.array[key % self.size]
            else:
                return self.openadressing(key, 2)
        elif self.probing == 3:
            if self.array.get(key % self.size,node(dataitem(None,None))).nodeitem.key == key:  # if first one return first one else start probe.?
                return self.array[key%self.size].nodeitem
            else:
                return self.seperatechaining(key, 2)

    def destroyhashmap(self):
        self.array=dict()#cleaning table

    def testtraverse(self):
        #testpurpose traverse which shows the table location and the key of item.
        if self.probing!=3:
            for i in self.array:
                print (i,":   ",self.array[i].content, "       Key:",self.array[i].key)
        else:
            for i in self.array:
                #probe3 calling nodetraverse.
                #print (i,": ")
                self.array[i].nodetraverse()
                print ()


if __name__ == "__main__":
    #some test, to lazy to write doctest
    temp=hashmap(61,0) #make a temp hashmap
    temp2=hashmap(61,0) #make a temp hashmap
    temp.insert(5,"i am a interger 5") #insert item with content and key 5
    temp.insert(5,"idk why")#only to illustrate that the sequential probing works, in the real situation this will not happend i think.
    temp.insert(5,88888)
    temp.insert(200,"apeark")
    temp.insert(82205,"kay")
    print("expected 5 elements to be printed got:")
    temp.testtraverse()
    #this should show all 5 contents, in random sequence

    print()
    print("expected False got:")
    print(temp.isempty())
    #this should be False since it's nomore empty
    print()
    print()

    temp.insert(20,"im a replacer")
    temp.delete(200)
    print("expected 5 elements to be printed and apeark replaced with replacer")
    temp.testtraverse()
    print()
    print()

    print("expected an succesful probe switch and:")
    temp.switchprobing(1)
    print()
    print()

    print("expected an extra item 50 to be printed and the place of item with key 5 should be following the quatratic rule and:")
    temp.insert(50,5)
    temp.testtraverse()
    print()
    print()

    print("expected a succesful switch to seperate chaining and:")
    temp.switchprobing(3)
    print()
    print()

    print("expected an printed list with the same element and:")
    #this doesn't work anymore sinds i commented out the print function. for main.
    temp.testtraverse()
    print()
    print()

    print("expected the content with key 82205 and got")
    print(temp.retrieve(82205).content)
    print()
    print()

    print("expected an succesful swap to sequential probe and:")
    print("since that the node traverse is called when swapping from mode 3 to any other mode, the following elements in the node is being printed")
    temp.switchprobing(1)
    print()
    print()

    print("Expected the same elements to be printed on a different way and:")
    temp.testtraverse()
    print()
    print()

    print("Expected the content of key 5(multiple keyying) and:")
    print(temp.retrieve(5).content)
    print()
    print()

    print("Expected the map to be destoryed and nothing will print:")
    temp.destroyhashmap()
    temp.testtraverse()
    print()
    print()

    print("Expected True for empty after destory:")
    print(temp.isempty())




