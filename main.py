from adttabel import *
#from gebruiker import *
from multiprocessing import Process,SimpleQueue
import threading
import time

class gebruiker:
    pass

class bestelling:
    timestamp=0
    product=tabel()

    def __init__(self,timestamp):
        pass
    def insert(self,item):
        pass
    pass

class chocolademelk:
    prijs=0
    id=0
    credit=0
    bruin=0
    wit=0
    zwart=0
    melk=0
    chilipeper=0
    honing=0
    marshmallow=0

    def __init__(self,zwart=0,wit=0,bruin=0,melk=0,chilipeper=0,honing=0,marshmallow=0):
        self.zwart=zwart
        self.wit=wit
        self.melk=melk
        self.bruin=bruin
        self.chilipeper=chilipeper
        self.honing=honing
        self.marshmallow=marshmallow
        self.prijs=2+zwart*1+wit*1+bruin*1+melk*1+marshmallow*0.75+chilipeper*0.25+honing*0.5

    def addingredient(self,chiliperper=0,honing=0,marshmallow=0):
        self.chilipeper+=chiliperper
        self.honing+=honing
        self.marshmallow+=marshmallow
        self.prijs+=chiliperper*0.25+marshmallow*0.75+honing*0.5



class stack:
    content=[]

    def __init__(self):
        self.content=[]

    def insert(self,val):
        self.content.append(val)

    def remove(self):
        self.content.pop(len(self.content)-1)

    def retrieve(self):
        if len(self.content)!=0:
            return self.content[len(self.content)-1]
        return None

class queue:

    def enqueue(self,item):
        pass

    def dequeue(self,item):
        pass

def ordermenu(account,time):
    chocos=tabel()
    chocoavailable=["1) zwartchoco","2) witchoco","3) melkchoco","4) bruinchoco"]
    dezebestelling=bestelling(time)
    print("Welkom ",account.firstname," ", account.lastname,", wat wilt u bestellen?")
    while True:
        print("U heeft keuzes tussen 4 verschillende soorten chocolade")
        choco=input("1) zwartchoco 2)witchoco 3)melkchoco 4)bruinchoco")
        while choco not in {"1","2","3","4"}:
            choco = input("1) zwartchoco 2)witchoco 3)melkchoco 4)bruinchoco")
        chocos.insert(int(choco),1)
        while 4-chocos.size()>0:
            print("u kunt nog een mix maken met de andere ", 4-chocos.size(), "chocolade(s)")
            for i in range (4):
                if i not in chocos.content:
                    print(chocoavailable[i])
            print("5) nee bedankt")
            choco = input()
            if choco=="5":
                break
            while choco not in {"1", "2", "3", "4"}:
                continue
            chocos.insert(int(choco),1)
        thismelk=chocolademelk(chocos.retrieve(1),chocos.retrieve(2),chocos.retrieve(3),chocos.retrieve(4))

        print("alright, wilt u nog extra toppings op de chocomelk?")
        while True:
            topping=input("1) extra chiliperper 2)extra honing 3)extra marshmallow 4)nee bedankt")
            if topping=="4":
                break
            while topping not in {"1","2","3"}:
                continue
            thismelk.addingredient(topping=="1",topping=="2",topping=="3")

        dezebestelling.insert(thismelk)
        doonemore=input("wilt u nog eentje bestellen? 1)ja 2)nee")
        while choco not in {"1", "2"}:
            doonemore = input("wilt u nog eentje bestellen? 1)ja 2)nee")
        if doonemore=="1":
            continue
        elif doonemore=="2":
            break
    return dezebestelling



class Winkel:
    werknemersbeschikbaar=stack()
    bestellingen=queue()
    werknemers=tabel()
    


def userside(Queuetoinput,winkelsideinput):
    winkel=Winkel()
    user=tabel()
    time.sleep(0.2)#assure that the winkelside begins first
    print("Welkom to Quetzal")
    while True:
        print(winkelsideinput.get())
        command=input("1)login with existing user id, 2)register")
        while command != "1" and command != "2":
            print("please input a correct command")
            command = input(" 1)login with existing user id, 2)register")
        if command=="1":
            username=input("please give me your emailadress")
            useraccount=user.retrieve(username)
            if useraccount!=None:
                print("login succesful, going to the order menu now...")
                dezebestelling=ordermenu(useraccount,winkelsideinput.get())
                Queuetoinput.put(dezebestelling)
            else:
                print("this username doesn't exist, please check the capital letters and typos and try again, or register as a new user")
                continue
        elif command=="2":
            print("registering new user")
            firstname=input("what's your first name?")
            lastname=input("what's your last name?")
            email=input("what's your email adress?")
            print("completing registration")
            #user.insert(username,gebruiker(firstname,lastname,email))#need to be implemented
            print("you can now login with your username")
            continue

def winkelside(winkelsideinput,userinput):
    timestamp=0
    counter=0
    winkelsideinput.put(timestamp)
    while True:
        while counter<60:
            print(counter)
            winkelsideinput.empty()
            winkelsideinput.put(timestamp)
            time.sleep(1)
            counter+=1
        timestamp+=1



if __name__=="__main__":
    userinput=SimpleQueue()
    winkelsideinput=SimpleQueue()
    winkelsidefunction = threading.Thread(target=winkelside, args=(winkelsideinput,userinput))
    usersidefunction= threading.Thread(target=userside, args=(userinput,winkelsideinput))#appearently process cannot handle the getting input part, just call thread on this one and process on the other one
    winkelsidefunction.start()
    usersidefunction.start()
