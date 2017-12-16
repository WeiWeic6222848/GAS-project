class Gebruiker:
    def __init__(self):
        self.id = None
        self.voornaam = None
        self.achternaam = None
        self.email = None
        self.zoeksleutel = None

    def createGebruiker(self,id,voornaam,achternaam,email):
        self.id = id
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.email = email

    #def destroyGebruiker(self):

    #def retrieve

