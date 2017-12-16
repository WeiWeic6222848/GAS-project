class Bestelling:
    def __init__(self):
        self.gebruikersid = None
        self.timestamp = None
        self.chocolademelkid = None
        self.afgehaald = False
        self.zoeksleutel = None
        self.bestellingen = []

    def createBestelling(self,gebruikersid,timestamp,chocolademelkid):
        self.gebruikersid = gebruikersid
        self.timestamp = timestamp
        self.chocolademelkid = chocolademelkid

    def setAfgehaaldTrue(self):
        self.afgehaald = True

    #def berekenWorkload
    # 5 credits voor chocolademelk
    # 1 credti voor chocolademelk,honing...
