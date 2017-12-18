class Bestelling:
    def __init__(self,gebruikersid,timestamp):
        self.gebruikersid = gebruikersid
        self.timestamp = timestamp
        self.aantalshots = []    #in credits
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
        print("Shots")
        for i in self.aantalshots:
            print(i,",")
        print("Ingredienten")
        for i in self.extraIngredient:
            print(i,",")
