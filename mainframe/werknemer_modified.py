class Werknemer:
    def __init__(self,voornaam,achternaam,workload):#class of werknemer
        self.id = None#contains id
        self.voornaam = voornaam#name
        self.achternaam = achternaam#name
        self.workload = workload#worload
        self.bestelling=None#bestellingen working
        self.resterendetijd=None#how much work left

    def VeranderWorkload(self,Newworkload):
        self.workload = Newworkload#setworkload function

    def bestellingenaannemen(self,bestellingen):#take order function
        self.bestelling=bestellingen
        self.resterendetijd=bestellingen.credits

    def werken(self):#works. if work is done set bestelling to afgehaald.
        self.resterendetijd-=self.workload
        if self.resterendetijd<=0:
            if self.bestelling!=None:
                self.bestelling.Afgehaald()
            self.resterendetijd=0

    def bestellingdone(self):#remove bestelling
        self.bestelling=None