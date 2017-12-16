class Werknemer:
    def __init__(self):
        self.id = None
        self.voornaam = None
        self.achternaam = None
        self.credit = None

    def createWerkNemer(self,id,voornaam,achternaam,credit):
        self.id = id
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.credit = credit

    def VeranderCredit(self,NewCredit):
        self.credit = NewCredit

    #def verwijderwerknemer

