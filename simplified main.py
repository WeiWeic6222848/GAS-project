from Queue_rij import Queue
import sys
from chilipeper import *
from Bestelling import *
from adttabel import *

class Stock:
    pass

class Chocolademelk:
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

    def addingredient(self,ingredient):
        if ingredient=="chilipeper":
            self.chilipeper+=1
            self.prijs+=Chilipeper.prijs
        elif ingredient=="marshmallow":
            self.marshmallow+=1
            self.prijs+=marshmallow.prijs
        elif ingredient=="honing":
            self.honing+=1
            self.prijs+=honing.prijs
        elif ingredient=="wit":
            self.wit+=1
            self.prijs+=chocoladeShot.prijs
        elif ingredient=="bruin":
            self.bruin+=1
            self.prijs+=chocoladeShot.prijs
        elif ingredient=="melk":
            self.melk+=1
            self.prijs+=chocoladeShot.prijs
        elif ingredient=="zwart":
            self.zwart+=1
            self.prijs+=chocoladeShot.prijs


def str_to_class(str):#code from https://stackoverflow.com/questions/1176136/convert-string-to-python-class-object, credit to sixthgear
    return getattr(sys.modules[__name__], str)

def addproduct(kind,amount,year,mouth,day,kindofshot=0):
    for i in range(amount):
        temp=str_to_class(kind)()

class Winkel:
    werknemerbeschikbaar=Stack()
    werknemers=Tabel()
    bestellingenwaiting=Queue()
    bestellingenfinished=Tabel()
    bestellingenworking=Tabel()

    def __init__(self):
        self.werknemerbeschikbaar=Stack()
        self.werknemers=Tabel()
        self.bestellingen=Queue()

    def update(self):
        #deze functie wordt elke keer opgeroepen wanneer de timestamp vernieuwd wordt, dit laat de werknemer bestellingen nemen en berekenen hoeveel minuut er nog is om de bestellingen te doen.
        #en de bestellingen
        pass

    def addbestelling(self,bestelling):
        self.bestellingenwaiting.insert(bestelling)



#    def addStock(self,item):
 #       if type(item)==str_to_class("marshmallow"):
  #          self.content["marshmallow"].insert(item)
   #     elif type(item)==str_to_class("chocoladeshot"):
    #        self.content["chocoladeshot"].insert(item)
     #   elif type(item)==str_to_class("chilipeper"):
      #      self.content["chilipeper"].insert(item)
       # elif type(item)==str_to_class("honing"):
        #    self.content["honing"].insert(item)
        #return True



def initfunction(line,stock,winkel):
    availablechoises={"shot","honing","chili","gebruiker","marshmallow","werknemer"}
    availableshots = {"wit","zwart","bruin","melk"}
    seperatedline = line.split(" ")
    if seperatedline[0] not in availablechoises:
        print("check typfout in de lijn: ",line)
        return False
    else:
        if seperatedline[0]=="shot" and len(seperatedline)==6:
            if seperatedline[1] not in availableshots:
                print("check parameter in de lijn: ", line)
                return False
            else:
                counter=seperatedline[2]
                for i in range(counter):
                    soort=seperatedline[1]
                    temp=str_to_class(seperatedline[0])(soort,seperatedline[3],seperatedline[4],seperatedline[5])#345 is jaar maand dag
                    stock.addstock(temp)
        elif len(seperatedline)==5 and seperatedline not in {"shot","gebruiker","werknemer"}:
            counter=seperatedline[1]
            for i in range(counter):
                temp=str_to_class(seperatedline[0])(seperatedline[2],seperatedline[3],seperatedline[4])
                stock.addstock(temp)
        elif seperatedline[0] in{"gebruiker","werknemer" }and len(seperatedline)==4:
            voornaam=seperatedline[1]
            achternaam=seperatedline[2]
            workloadofemailadress=int(seperatedline[3])
            temp=str_to_class(seperatedline[0])(voornaam,achternaam,workloadofemailadress)
            stock.addstock(temp)
            #voor gebruiker is 3 de emailadress en voor werknemer is 3 de workload
        else:
            print("check parameter in de lijn: ", line)
            return False



def startingfunction(line,stock,winkel,time):
    seperatedline = line.split(" ")
    availablechoises={"bestel","stock","log"}
    if seperatedline[1] not in availablechoises:
        print("check line:",line)
        return False
    while seperatedline[0]>str(time):
        winkel.update()
        time+=1
    else:
        if seperatedline[1]=="bestel":
            chocolademelk=Chocolademelk()
            emailadress=seperatedline[2]
            bestelling=Bestelling().createBestelling(emailadress,time,chocolademelk.id)
            for i in range(3,len(seperatedline)):#this needs to change, possibly
                chocolademelk.addingredient(seperatedline[i])
            winkel.addbestelling(bestelling)






if __name__ =="__main__":
    input=open("input.txt","r")
    initing=False
    starting=False
    stock=Stock()
    winkel=Winkel()
    counter=0
    for line in input:
        line=line.strip('\n')
        print(line)
        if line=="init":
            initing=True
            starting=False
            continue
        elif line=="start":
            starting=True
            initing=False
            continue
        if initing:
            if initfunction(line,stock)==False:
                break
        if starting:
            if startingfunction(line,stock,winkel,counter)==False:
                break
            line=line.split(" ")
            counter=line[0]
        #print(line)
