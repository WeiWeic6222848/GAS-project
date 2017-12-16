class Werknemer:
    def __init__(self,voornaam,achternaam,credit):
        self.id = None
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.credit = credit

    def createWerkNemer(self,id,voornaam,achternaam,credit):
        self.id = id
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.credit = credit

    def VeranderCredit(self,NewCredit):
        self.credit = NewCredit

    #def verwijderwerknemer

