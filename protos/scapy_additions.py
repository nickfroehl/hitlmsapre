from scapy.all import *

class RandNumChoice(RandNum):
    choices: list[int] = []
    
    def __init__(self, choices: list[int]):
        self.choices = choices
    
    def _fix(self) -> int:
        return random.choice(self.choices)
    
    def _command_args(self) -> str:
        if self.__class__.__name__ == "RandNumChoice":
            return f"choices = {self.choices}"
        else:
            return super(RandNum, self)._command_args()

class RandMACChoice(RandMAC):
    choices: list[str] = []
    
    def __init__(self, choices: list[str]):
        self.choices = choices
    
    def _fix(self) -> str:
        return random.choice(self.choices)
    
    def _command_args(self) -> str:
        if self.__class__.__name__ == "RandMACChoice":
            return f"choices = {self.choices}"
        else:
            return super(RandMAC, self)._command_args()

class RandIPChoice(RandIP):
    choices: list[str] = []
    
    def __init__(self, choices: list[str]):
        self.choices = choices
    
    def _fix(self) -> str:
        return random.choice(self.choices)
    
    def _command_args(self) -> str:
        if self.__class__.__name__ == "RandIPChoice":
            return f"choices = {self.choices}"
        else:
            return super(RandIP, self)._command_args()