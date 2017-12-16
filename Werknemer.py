class Werknemer:
    def __init__(self,voornaam,achternaam,workload):
        self.id = None
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.workload = workload


    def VeranderWorkload(self,Newworkload):
        self.workload = Newworkload
