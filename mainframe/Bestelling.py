class Bestelling:
    def __init__(self,gebruikersid,timestamp): #bestelling.
        self.gebruikersid = gebruikersid #contains id
        self.timestamp = timestamp #timestamp
        self.aantalshots = []
        #i didn't really use the aantal shot, it will be a lot more harder if i user it.
        self.extraIngredient = []
        self.afgehaald = False
        self.credits = 5 # in credits
    def Afgehaald(self):
        self.afgehaald = True


    def VoegShotToe(self,Shot):#
        self.aantalshots.append(Shot)   #1 credit per cholade shot dus +1
        self.credits += 1
    def VoegIngredientToe(self,Ingredient):
        self.extraIngredient.append(Ingredient)
        self.credits += 1

    def printBestelling(self):
        #beacause it's all string form, this is way easier to print.
        print("Shots:")
        for i in self.aantalshots:#well this is not going to work
            print(i,",",end="")
            print()
        print("Ingredienten")
        for i in self.extraIngredient:
            print(i,",",end="")
            print()