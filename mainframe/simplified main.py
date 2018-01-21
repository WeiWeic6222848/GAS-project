from Queue_rij import Queue
import sys
from Bestelling import *
from adttabel import *
from stock import *
from functools import reduce
from gebruiker import *
from werknemer_modified import *


#This code. is purely created based on the goal of:
#reading the input file(input bestand)
#trying to get the correct output format as asked.
#despite the fact that there's still some incomplete and overcomplicated statements.
#such as the string to class function. and the incomplete price of bestllingen.
#this is the first version of the system which gives the correct output.
#and kind of, correctly works with the giving input file and handling the times.


class Chocolademelk: #this is the class of Chocolademelk.
    #a Chocolademelk has various attributes.
    #In this version of the system, ID is not implemented, Chocolademelk just got added into the bestelling.
    #I personally didn't make the part of bestelling so there was a bit of confusion between this class and the class of bestelling.
    #I will explain it further on the Code when there is one.

    prijs=0 #this is the price of Chocomelk
    id=0 #the ID, which we haven't figured out a simple and unique way to give every chocolademelk.
    credit=0 # credit aka workload of a chocolademelk.
    bruin=0 # how much bruin shot is needed
    wit=0 # how much wit shot is needed
    zwart=0 #...
    melk=0 #...
    chilipeper=0 #...
    honing=0 #...
    marshmallow=0 #...

    def __init__(self,zwart=0,wit=0,bruin=0,melk=0,chilipeper=0,honing=0,marshmallow=0):
        #on the init of the chocomelk, there is default no ingredients.
        self.zwart=zwart
        self.wit=wit
        self.melk=melk
        self.bruin=bruin
        self.chilipeper=chilipeper
        self.honing=honing
        self.marshmallow=marshmallow
        self.prijs=2+zwart*ChocoladeShot.price+wit*ChocoladeShot.price+bruin*ChocoladeShot.price+melk*ChocoladeShot.price+marshmallow*Marshmallow.price+chilipeper*Chilipeper.price+honing*Honing.price
        self.credit=5+zwart+wit+bruin+melk+chilipeper+honing+marshmallow
        #the base price is 2, adding the prices of the ingredients

    def addingredient(self,ingredient):
        #if we wants to add an ingredient, just simply get the string infomation of what we wants to add and determine the price and credit(which i seems to forgot. adding it right now)
        if ingredient=="chilipeper":
            self.chilipeper+=1
            self.prijs+=Chilipeper.price
        elif ingredient=="marshmallow":
            self.marshmallow+=1
            self.prijs+=Marshmallow.price
        elif ingredient=="honing":
            self.honing+=1
            self.prijs+=Honing.price
        elif ingredient=="wit":
            self.wit+=1
            self.prijs+=ChocoladeShot.price
        elif ingredient=="bruin":
            self.bruin+=1
            self.prijs+=ChocoladeShot.price
        elif ingredient=="melk":
            self.melk+=1
            self.prijs+=ChocoladeShot.price
        elif ingredient=="zwart":
            self.zwart+=1
            self.prijs+=ChocoladeShot.price
        self.credit+=1#added, though it will give some buggy result when the input is wrong. but i do think that i have done a check on the code already.

    def berekenworkload(self):
        #seems like that i do have a code which calculates the credit.. well..
        #every ingredient has a base credit (workload) of 1, so just add them up with the base credit which is 5.
        return 5+self.bruin+self.wit+self.melk+self.marshmallow+self.honing+self.zwart+self.chilipeper


def str_to_class(str):#code from https://stackoverflow.com/questions/1176136/convert-string-to-python-class-object, credit to sixthgear and more people.
    #basiclly, what this code does. is take a string argument and return the right class that has the same name.
    #for example: I input"ChocoladeShot", then this will return the real class of ChocoladeShot.
    #Then i can use it to do something like str_to_class["input"](arg to make the class)
    return reduce(getattr, str.split("."), sys.modules[__name__])

class Winkel:
    #this is the class of Winkel
    #a Winkel should contain:
    stock=Stock()# A Stock which contains the .. Stocks.
    allewerknemers=Tabel() # A tabel which contains all the werknemers. needed for logging
    werknemerbeschikbaar=Stack() # A stack which contains the werknemers that are available. they will take the order one by one.
    werknemersaantwerken=Tabel() # A tabel which contains the werknemers that are working. on the begin of every timetip. they're going to work. haha..
    bestellingenwaiting=Queue() # a queue which containts the bestellingen that are waiting. needed for logging and general working of the Winkel.
    bestellingenfinished=Tabel() # finished bestellingen. it was asked.
    nieuwbestellingen=Queue() # it's needed for logging.
    gebruikers=Tabel() # a table which contains all the user of the Winkel.
    #We currently aren't validating the users.
    #just simply add it to the list if it doesn't exist yet.


    def __init__(self):
        #on init, a class of stock must be provided.
        #There is a place of improvement here.
        #the reading input function can be directly transferred into the Winkel class.
        #which makes the external stock no more needed.
        #gonna change it.. very soon
        self.werknemerbeschikbaar=Stack()
        self.bestellingen=Queue()
        self.stock=Stock()

        ##reading the init text##

        open("winkellog.txt","w").close()#deleting the previous winkel logging.
        #we can also make every unique winkel write their own unique winkellog. which makes the project works not only for one but for multiple winkels at the same time.

    def update(self):
        #the core function of the Winkel.
        #this function will be called every time when the timetip increases.
        #this function does everything from take bestelling to work to move the bestelling to finished..
        #and logging.
        templist = self.werknemersaantwerken.traverse()#since that we're using wrapper. call the traverse function of the wrapper.
        #traverse returns the list of all working people.
        for i in templist:
        #and of course. all of them have to work.
            i.werken()
            if i.bestelling.afgehaald==True:
                #and if after working. the bestelling is finished(here. afgehaald, since that we can't mesure when the user is coming to take the order, I just assume that they're taken once it's finished)
                self.werknemerbeschikbaar.push(i)#if they are finished with the order then they are available once more.
                self.werknemersaantwerken.remove(i.id)#and remove then from the working list.
                self.bestellingenfinished.insert(i.bestelling.timestamp,i.bestelling)#push the bestelling into the finished table.
                i.bestellingdone()#veranderen de bestelling van de werknemer terug naar None #this was written before haha..


        #this is the place where we check wether or not there is a bestelling to take. and if there is a bestelling which we have to do.
        #and there is a werknemer available.
        #then let that werknemer take it.
        if self.bestellingenwaiting.isempty()==False and self.werknemerbeschikbaar.isEmpty()==False:

            self.werknemerbeschikbaar.getTop().bestellingenaannemen(self.bestellingenwaiting.gettop())#the top werknemer on the available list takes the top bestelling on the waitinglist.
            self.werknemersaantwerken.insert(self.werknemerbeschikbaar.getTop().id,self.werknemerbeschikbaar.getTop())#move him to the working list.
            self.werknemerbeschikbaar.pop()#he is no more available.
            for i in self.bestellingenwaiting.gettop().extraIngredient:#this was the confusion part. I was thinking that a bestelling can be more chocoladeshot. but appearently it's not the case.
                #so i just used the property in the bestelling class. everything is an extra ingredient(including chocoshots. chili. honing. marshmallow...)
                self.stock.deleteStock(i)#give whatever is in the list to the stock and tell the stock to delete one of that kind.
            self.bestellingenwaiting.delete()#the bestelling is nomore waiting


        ######################################log############################################
        #for the logging function, i write a external file.. which contains the information of every iteration.
        input=open("winkellog.txt","a")#open the file in append mode.
        templijstofstring=[]#this is some complicated thing..
        #i wanted to use the '{:<24}'.format thing to write the whole list of string into the file.
        #but i ended up not knowing how i should print it into the file.
        #although i now figured it out but it's already to late to change things.
        #I'll leave it like that and change it in the next version

        tempstring=""#this is a tempopary string which containts one string elements that we have to print(vb. for Stack we need to get the worklaod of multiple werknemers. and temporary store it into a string)

        templist=self.werknemerbeschikbaar.traverse()#get available werknemers.
        for i in templist:
            tempstring+=str(i.workload)+" "#add the workload into the tempstring. with a space between everyone of them(as seen on output file)
        templijstofstring.append("|"+tempstring)#adding the | before the value, trying to approach as close possible as the output file
        tempstring=""#reset temp string
        templist=self.allewerknemers.traverse()# get all available werknemers.
        for i in templist:
            #everyone of the werknemers gets a seperate column, so directly add it into the string list.
            if i.resterendetijd!=0 and i.resterendetijd!=None:
                templijstofstring.append("|"+str(i.resterendetijd))  #if they are working. show the rest of the time.
            elif i.resterendetijd==0 or i.resterendetijd==None:
                templijstofstring.append("|") #else just left it blank

        #as seen on output, next is neworders.
        templist= self.nieuwbestellingen.traverse()
        if templist!=None:#if there is any bestellingen
            for i in templist:
                tempstring+=str(i.credits)+","#get's the workload of every single order.
            tempstring=tempstring[:-1]#removing the "," on the end
        templijstofstring.append("|"+tempstring) # adding it into list
        tempstring=""#resetting tempstring

        #next is waiting one.
        templist=self.bestellingenwaiting.traverse()
        if templist!=None:
            for i in templist:
                tempstring+=str(i.credits)+"," #basiclly the same as newbestelling.
            tempstring=tempstring[:-1]
        templijstofstring.append("|"+tempstring)


        #adding the corresponding length of the stock. euhm..
        #might broke the wall right here. feedback needed.
        templijstofstring.append("|"+str(self.stock.content["wit"].size))
        templijstofstring.append("|"+str(self.stock.content["melk"].size))
        templijstofstring.append("|"+str(self.stock.content["bruin"].size))
        templijstofstring.append("|"+str(self.stock.content["zwart"].size))
        templijstofstring.append("|"+str(self.stock.content["honing"].size))
        templijstofstring.append("|"+str(self.stock.content["marshmallow"].size))
        templijstofstring.append("|"+str(self.stock.content["chilipeper"].size))

        #write every single info into the output file winkellog
        for i in range(len(templijstofstring)):
            input.write(templijstofstring[i])
            if i!=len(templijstofstring)-1:
                input.write("------")
        input.write("\n")#start a newline after that.
        input.close()
        ########################################log###################################################

        self.nieuwbestellingen=Queue() #reset de nieuwe bestelling na elke tijdstip


    def addbestelling(self,bestelling):
        self.bestellingenwaiting.insert(bestelling)#yeah.
        self.nieuwbestellingen.insert(bestelling)#dit is nodig bij log

    def addgebruiker(self,gebruiker):
        self.gebruikers.insert(gebruiker.email,gebruiker)

    def addwerknemers(self,werknemer):
        werknemer.id=self.allewerknemers.size()#the id starts at 0, and goes up to infinite, i guess it's how the most company works.
        self.allewerknemers.insert(werknemer.id,werknemer)
        self.werknemerbeschikbaar.push(werknemer)#I assume that they just start work rightaway?



def initfunction(line,winkel):
    #this function could be implemented in the Winkel class.

    #available starting line choises
    availablechoises={"shot","honing","chilipeper","gebruiker","marshmallow","werknemer"}
    #available sub choises of the shot.
    availableshots = {"wit","zwart","bruin","melk"}
    #info must be splitst with one space
    seperatedline = line.split(" ")
    #some sanity check
    if seperatedline[0] not in availablechoises:
        print("check typfout in de lijn: ",line)
        return False
    else:
        #check which command should be exec 'ed
        if seperatedline[0]=="shot" and len(seperatedline)==6:#if it's a init chocoshot, then it needs to have 6 parameters.
            if seperatedline[1] not in availableshots:
                print("check parameter in de lijn: ", line)
                return False
            else:
                counter=int(seperatedline[2])#the third one indicates how much should be added
                for i in range(counter):
                    soort=seperatedline[1]#de second one indicates which kinda shot it is.
                    temp=str_to_class("ChocoladeShot")(soort,seperatedline[3],seperatedline[4],seperatedline[5])#4,5,6 is jaar maand dag, this part i've changed a little bit, the original maker tends to make it a big Expiry date.
                    #and I think that it will make the code too complicated and much longer than what it should be, so i just decided it kinda on my own.
                    #my bad.
                    #so the Expiry date also doesn't work properly...
                    winkel.stock.addStock(temp)#the stock of the winkel will add this item to it's collection on the correct place.
        elif len(seperatedline)==5 and seperatedline[0] not in {"shot","gebruiker","werknemer"}:#if it's not shot or user/werknermer, then it's ingredient. add into stock x times.
            counter=int(seperatedline[1])
            for i in range(counter):
                temp=str_to_class(seperatedline[0].capitalize())(seperatedline[2],seperatedline[3],seperatedline[4])
                winkel.stock.addStock(temp)
        elif seperatedline[0] in{"gebruiker","werknemer" }and len(seperatedline)==4:#else check the info and add the user/werknemer into right tabel.
            voornaam=seperatedline[1]
            achternaam=seperatedline[2]
            workloadofemailadress=seperatedline[3]
            if seperatedline[0]=="gebruiker":
                temp = str_to_class(seperatedline[0].capitalize())(voornaam, achternaam, workloadofemailadress)
                winkel.addgebruiker(temp)
            else:
                temp = str_to_class(seperatedline[0].capitalize())(voornaam, achternaam, int(workloadofemailadress))
                winkel.addwerknemers(temp)
            #voor gebruiker is 3 de emailadress en voor werknemer is 3 de workload
        else:
            print("check parameter in de lijn: ", line)#the command are probably right but the giving parameter doesn't seems enough or there's too much parameters.
            return False#the returning False Halts the whole process.



def startingfunction(line,winkel,time):

    #this function is called if a new line of starting command has been read.
    #this controls the timetip changes and exec the correct command.

    seperatedline = line.split(" ")#...
    availablechoises={"bestel","stock","log"}#as seen on input, there's 3 available input command.
    #sanity check
    if seperatedline[1] not in availablechoises:
        print("check line:",line)
        return False
    if seperatedline[0].isdigit()==False:
        print("check timestamp, it's wrong on line:", line)
        return False
    else:
        while int(seperatedline[0]) > time:#if the current time is smaller then the readed time, do nothing and update the winkel status.
            winkel.update()
            time += 1

        #and when the time is correct, do the command.
        if seperatedline[1]=="bestel":#at the start of the bestelling.
            chocolademelk=Chocolademelk()#make a chocomelk, which now appears can be done by just making a bestelling and see it as a chocomelk entity. since that a bestelling can only take one chocomelk.
            emailadress=seperatedline[2]#on the third param, there should be the email of the user.
            bestelling=Bestelling(emailadress,time)#bestelling is inited with emailadress and timestamp, again, we don't know how to give them an id.


            if winkel.gebruikers.retrieve(emailadress)==None:
                #if the user doesn't exist yet, add it.
                tempgebruiker=Gebruiker("idk","idk",emailadress)
                winkel.addgebruiker(tempgebruiker)
            for i in range(3,len(seperatedline)):#this needs to change, possibly.
                #no giving instruction of how the input should work, just take the easy way around.
                # two extra melk shot = melk melk.
                # two extra chilipeper= chili chili...
                chocolademelk.addingredient(seperatedline[i])
                bestelling.VoegIngredientToe(seperatedline[i])#Here you can see the conflict between the class chocomelk and bestelling.
                #quite frustrating.
            winkel.addbestelling(bestelling)#calling the winkel function to add the bestelling
            winkel.update()#and they have to update after all these works.


        #stock command just add a certain amout of the product to the stock, which is initfunction's job. we prepare a stringline for initfunction and send it to init.
        elif seperatedline[1]=="stock":
            linepreparedforinit=line[len(seperatedline[0])+len(seperatedline[1])+2:]+" unknown"+" unknown"+" unknown"
            #this line starts after the timestip and the string stock, plus 2 whitespace. then adding the unknown Expiry yy/mm/dd.
            initfunction(linepreparedforinit,winkel)
            winkel.update()#update at the end of the cycle.

        #logging is just reading the log file. and print the header.
        elif seperatedline[1]=="log":
            winkel.update()#let it update first, like in the output

            templistofstring=[]#list of things that needs to be outputted in a formatted form
            templistofstring.append("Tijdstip")
            templistofstring.append("|Stack")
            templijst=winkel.allewerknemers.traverse()
            for i in templijst:
                templistofstring.append("|"+i.voornaam+" "+i.achternaam)
            templistofstring.append("|Nieuwe bestelling")
            templistofstring.append("|Wachtende bestelling")
            templistofstring.append("|wit")
            templistofstring.append("|melk")
            templistofstring.append("|bruin")
            templistofstring.append("|zwart")
            templistofstring.append("|honing")
            templistofstring.append("|marshmallow")
            templistofstring.append("|chili")
            #everything here is just the header


            for i in templistofstring:#print every item formatted on the left 22 space.
                print('\033[4m', '{:<22}'.format(i), '\033[0m', end="")
            print()#print a white line
            input = open("winkellog.txt", "r")#reading the log file.
            counter=0#counter is for the timestip, it starts at one and goes to the end of the log.
            for logline in input:
                logline=logline.strip("\n")#we don't need it. maybe we do.. ill reconsider that.
                splitline=logline.split("------")#this is a kinda unique splitsymbol, so i think that no one is going to mess it up.
                splitline.insert(0,str(counter))#the firstthing should be the timetip, so just add it into the splitted line
                for i in splitline:
                    print('\033[4m','{:<22}'.format(i),'\033[0m',end="")
                print()#manually print a return
                counter+=1#timetip is increased.


if __name__ =="__main__":
    #finally worked my way here.
    #this whole thing.
    #can be converted into a function in the winkel class..
    #i think.
    #this generally only reads the input file and give it to the right function.

    input=open("input.txt","r")#open input.txt, obvious.

    initing=False#we need to know wether it's initing or working.
    starting=False

    stock=Stock()
    winkel=Winkel()#redundant.

    counter=0#timestip.

    for line in input:
        #read every line in input
        line=line.strip('\n')#remove the newline symbol
        if line[:5]=="chili":#this.... i just don't want to change everything in the code so just changed the input simply.
            line="chilipeper"+line[5:]


        #print(line)
        #test purpose

        if line=="init":#triviaal
            initing=True
            starting=False
            continue
        elif line=="start":#obvious.
            starting=True
            initing=False
            continue
        if initing:
            if initfunction(line,winkel)==False:#if we're initing, call the init function, if it returns false, stop the whole thing.
                break
        if starting:
            if startingfunction(line,winkel,counter)==False:#same here, but we need to check if the first char is the timestip and it must be bigger than the current time.
                break
            if line[0].isdigit():
                if int(line[0])+1>counter:#this is some last moment change, check if the time is bigger than the previous one.
                    counter=int(line[0])+1#we have run the command of that timetip so the current time is the readed time plus 1
                else:
                    break
            else:
                break
        #print(line)
    input.close()
    pass