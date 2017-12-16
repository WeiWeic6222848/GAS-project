class Werknemer:
    def __init__(self,voornaam,achternaam,workload):
        self.id = None
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.workload = workload
        self.bestelling=None
        self.resterendetijd=None

    def VeranderWorkload(self,Newworkload):
        self.workload = Newworkload

    def bestellingenaannemen(self,bestellingen):
        self.bestelling=bestellingen
        self.resterendetijd=bestellingen.credit

    def werken(self):
        self.resterendetijd-=self.workload
        if self.resterendetijd<0:
            if self.bestelling!=None:
                self.bestelling.Afgehaald()
                self.resterendetijd=0

    def bestellingdone(self):
        self.bestelling=None