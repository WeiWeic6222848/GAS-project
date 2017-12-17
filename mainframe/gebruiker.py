class Gebruiker:
    def __init__(self,voornaam,achternaam,email):
        self.id = None
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.email = email
        self.zoeksleutel = None

    def createGebruiker(self,id,voornaam,achternaam,email):
        self.id = id
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.email = email

    #def destroyGebruiker(self):

    #def retrieve