class Photon():
    STANDARD_POLARIZATION = 0
    DIAGONAL_POLARIZATION = 1
    def __init__(self,base:int = 0,value: int = 0):
        if value not in [0,1] or base not in [0,1]:
            raise ValueError
        self.base = base
        self.value = value
    def switch_base(self):
        self.base = abs(self.base - 1)
    def change_value(self):
        self.value = abs(self.value - 1)