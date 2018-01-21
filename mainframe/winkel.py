from builtins import int

from stock import *;
from adttabel import *
from Queue_rij import *
from gebruiker import *
from werknemer_modified import *
from Bestelling import *

def str_to_class(str):#code from https://stackoverflow.com/questions/1176136/convert-string-to-python-class-object, credit to sixthgear and more.
    return reduce(getattr, str.split("."), sys.modules[__name__])

class winkel:
    allewerknemers=Tabel()
    werknemerbeschikbaar=Stack()
    werknemersaantwerken=Tabel()
    bestellingenwaiting=Queue()
    bestellingenpending=Stack()
    bestellingenfinished=Tabel()
    nieuwbestellingen=Queue()
    gebruikers=Tabel()
    timestamp=0
    availableshots = {"wit", "zwart", "bruin", "melk"}
    availablechoisesofstock = {"shot", "honing", "chilipeper", "chili", "gebruiker", "marshmallow", "werknemer"}
    availablecommand = {"bestel", "stock", "log"}  # as seen on input, there's 3 available input command.
    availableingredient = ["wit", "melk", "bruin", "zwart", "honing", "marshmallow", "chilipeper"]

    def logging(self):

        ######################################log############################################
        #for the logging function, i write a external file.. which contains the information of every iteration.
        input=open(self.logfilename,"a")#open the file in append mode.
        templijstofstring=[]

        templijstofstring.append(self.timestamp)
        tempstring=""#this is a tempopary string which containts one string elements that we have to print(vb. for Stack we need to get the worklaod of multiple werknemers. and temporary store it into a string)

        templist=self.werknemerbeschikbaar.traverse()#get available werknemers.
        for i in templist[::-1]:
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


        #adding the corresponding length of the stock.
        #it's not breaking the wall since that for the init of stock, we used the availableingredient, so we know what's inside it.
        #stock is after all, a part of the store.
        for i in self.availableingredient:
            templijstofstring.append("|" + str(self.stock.content[i.capitalize()].size))


        #write every single info into the output file winkellog
        for i in range(len(templijstofstring)):
            input.write('{:<22}'.format(templijstofstring[i]))
        input.write("\n")#start a newline after that.
        input.close()
        ########################################log###################################################

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
        while self.bestellingenwaiting.isempty()==False and self.werknemerbeschikbaar.isEmpty()==False:
            if self.stock.checkingredient(self.bestellingenwaiting.gettop().extraIngredient):#check wether there's enough ingredient to prepare this bestelling
                self.werknemerbeschikbaar.getTop().bestellingenaannemen(self.bestellingenwaiting.gettop())#the top werknemer on the available list takes the top bestelling on the waitinglist.
                self.werknemersaantwerken.insert(self.werknemerbeschikbaar.getTop().id,self.werknemerbeschikbaar.getTop())#move him to the working list.
                self.werknemerbeschikbaar.pop()#he is no more available.
                for i in self.bestellingenwaiting.gettop().extraIngredient:#this was the confusion part. I was thinking that a bestelling can be more chocoladeshot. but appearently it's not the case.
                    #so i just used the property in the bestelling class. everything is an extra ingredient(including chocoshots. chili. honing. marshmallow...)
                    self.stock.deleteStock(i)#give whatever is in the list to the stock and tell the stock to delete one of that kind.
                self.bestellingenwaiting.delete()#the bestelling is nomore waiting
            else:#if there's not enough ingredient, put in on the temporary list, to add it back afterwards.
                temp=self.bestellingenwaiting.gettop()
                self.bestellingenwaiting.delete()
                self.bestellingenpending.push(temp)


        templist = self.bestellingenpending.traverse()#since that we're using wrapper. call the traverse function of the wrapper.
        for i in templist:
            self.bestellingenpending.pop()
            self.bestellingenwaiting.insertonfront(i)

        self.logging()
        self.nieuwbestellingen=Queue() #reset de nieuwe bestelling na elke tijdstip

    def addbestelling(self, bestelling):
        self.bestellingenwaiting.insert(bestelling)  # yeah.
        self.nieuwbestellingen.insert(bestelling)  # dit is nodig bij log

    def addgebruiker(self, gebruiker):
        self.gebruikers.insert(gebruiker.email, gebruiker)

    def addwerknemers(self, werknemer):
        werknemer.id = self.allewerknemers.size()  # the id starts at 0, and goes up to infinite, i guess it's how the most company works.
        self.allewerknemers.insert(werknemer.id, werknemer)
        self.werknemerbeschikbaar.push(werknemer)  # I assume that they just start work rightaway?

    def init(self,line):

        # chocoladeshot is a special one so i kinda pick it out alone.
        # if we just make four seperate class or even four seperate stock space for them, then i can smash them into the same line as all the other ingredient does.


        seperatedline = line.split(" ")

        if seperatedline[0] not in self.availablechoisesofstock:
            print("check typfout in de lijn: ", line)
            print("skipping this line")

        else:
            # check which command should be exec 'ed
            if seperatedline[0] == "shot" and len(seperatedline) == 6:  # if it's a init chocoshot, then it needs to have 6 parameters.

                if seperatedline[1] not in self.availableshots:
                    print("check parameter in de lijn: ", line)
                    print("skipping this line")

                else:
                    counter = int(seperatedline[2])  # the third one indicates how much should be added

                    for i in range(counter):
                        soort = seperatedline[1]  # de second one indicates which kinda shot it is.
                        temp = str_to_class("ChocoladeShot")(soort, int(seperatedline[3]), int(seperatedline[4]), int(seperatedline[5]))  # 4,5,6 is jaar maand dag, this part i've changed a little bit, the original maker tends to make it a big Expiry date.
                        # and I think that it will make the code too complicated and much longer than what it should be, so i just decided it kinda on my own.
                        # my bad.
                        # so the Expiry date also doesn't work properly...
                        self.stock.addStock(temp)  # the stock of the winkel will add this item to it's collection on the correct place.

            elif len(seperatedline) == 5 and seperatedline[0] not in {"shot", "gebruiker","werknemer"}:  # if it's not shot or user/werknermer, then it's ingredient. add into stock x times.
                counter = int(seperatedline[1])
                product = seperatedline[0]
                if product == "chili":
                    product = "chilipeper"
                for i in range(counter):
                    temp = str_to_class(product.capitalize())(int(seperatedline[2]), int(seperatedline[3]), int(seperatedline[4]))
                    self.stock.addStock(temp)


            elif seperatedline[0] in {"gebruiker", "werknemer"} and len(seperatedline) == 4:  # else check the info and add the user/werknemer into right tabel.
                voornaam = seperatedline[1]
                achternaam = seperatedline[2]
                workloadofemailadress = seperatedline[3]
                if seperatedline[0] == "gebruiker":
                    temp = str_to_class(seperatedline[0].capitalize())(voornaam, achternaam, workloadofemailadress)
                    self.addgebruiker(temp)
                else:
                    temp = str_to_class(seperatedline[0].capitalize())(voornaam, achternaam,int(workloadofemailadress))
                    self.addwerknemers(temp)
                # voor gebruiker is 3 de emailadress en voor werknemer is 3 de workload
            else:
                print("check parameter in de lijn: ",line)  # the command are probably right but the giving parameter doesn't seems enough or there's too much parameters.
                print("skipping this line")



    def __init__(self,initfilename):
        self.stock=Stock(self.availableingredient)

        #reading init file#
        input=open(initfilename,"r")
        initing=0#parameter to find initing lines.

        for line in input:
            line=line.strip("\n")
            if line == "start" or line == "":  # this doesn't make the reading file stop, but it stops the initing process, if we want to only init once, then we can also break right here.
                initing = 0
            if initing:
                self.init(line)
            if line == "init":
                initing = 1
        input.close()
        self.stock.sort()

        self.logfilename=initfilename+"_log.txt"
        log=open(self.logfilename,"w")#deleting the previous winkel logging.
        templistofstring = []  # list of things that needs to be outputted in a formatted form
        templistofstring.append("Tijdstip")
        templistofstring.append("|Stack")
        templijst = winkel.allewerknemers.traverse()
        for i in templijst:
            templistofstring.append("|" + i.voornaam + " " + i.achternaam)
        templistofstring.append("|Nieuwe bestelling")
        templistofstring.append("|Wachtende bestelling")
        for i in self.availableingredient:
            templistofstring.append("|"+i.capitalize())

        # everything here is just the header
        for i in templistofstring:  # print every item formatted on the left 22 space.
            log.write('{:<22}'.format(i))
        log.write('\n')
        log.close()




    def work(self,inputfilename):
        input=open(inputfilename,"r")
        working=0

        for line in input:
            line=line.strip('\n')#stripping newline symbol
            seperatedline = line.split(" ")  # ...

            if line == "init":
                working=0

            if working:
                if seperatedline[1] not in self.availablecommand:
                    print("check line:", line)
                    print("ignoring this line")

                if seperatedline[0].isdigit() == False:
                    print("check timestamp, it's wrong on line:", line)
                    print("ignoring this line")
                else:
                    time=int(seperatedline[0])
                    while time>self.timestamp:
                        self.update()#update to the last correct time. ea. if it's reading a line with timestamp 5, the winkel will update itself to time 4 in order to proceed.
                        self.timestamp+=1
                    if seperatedline[1]=="bestel":
                        emailadress=seperatedline[2]

                        if self.gebruikers.retrieve(emailadress)==None:
                            print("gebruiker met emailadress ",emailadress," is niet gevonden")
                            print("ignoring deze bestelling")
                            continue

                        bestelling=Bestelling(emailadress,time)
                        for i in range(3,len(seperatedline)):
                            ingredient=seperatedline[i]
                            if ingredient=="chili":
                                seperatedline[i]="chilipeper"
                                ingredient="chilipeper"
                            if ingredient.isdigit() and seperatedline[i-1].isdigit():
                                print("er is een fout opgetreden bij deze lijn: ",line)
                                print("er is twee hoeveelheid parameter achter elkaar")
                            elif ingredient.isdigit() and seperatedline[i-1] not in self.availableingredient:
                                print("er is een fout opgetreden bij deze lijn: ",line)
                                print("u probeert een ingredienten meerdere malen toevoegen die niet in de winkel stock staat")
                            elif i==3 and ingredient.isdigit():
                                print("er is een fout opgetreden bij deze lijn: ",line)
                                print("u begint een ingredientlijst met een getal")
                            elif ingredient.isdigit():
                                for j in range (int(ingredient)-1):#-1 om de vorig lijn te compenseren
                                    bestelling.VoegIngredientToe(seperatedline[i-1].capitalize())
                            else:
                                bestelling.VoegIngredientToe(ingredient.capitalize())
                        self.addbestelling(bestelling)

                    elif seperatedline[1]=="stock":
                        linepreparedforinit = line[len(seperatedline[0]) + len(seperatedline[1]) + 2:] + " 2099" + " 01" + " 01"
                        self.init(linepreparedforinit)
                        self.stock.sort()

                    elif seperatedline[1] == "log":
                        self.logging()#log feature only logs the current state, so if there's new bestellingen, it won't be taken yet
                        #after some enhancement you can use log multiple times in a timestamp and multiple times on the different timestamp.

                        input=open(self.logfilename,"r")
                        lines=input.readlines()
                        for line in lines:
                            line=line.strip('\n')
                            print('\033[4m',line, '\033[0m')
                        input.close()
                        lines=lines[:-1]#deleting the last line.
                        input=open(self.logfilename,"w")
                        for line in lines:
                            input.write(line)
                        input.close()

                        print()#left some space open


            if line == "start":
                working=1



if __name__=="__main__":
    hello=winkel("input.txt")
    hello.work("input.txt")
    pass