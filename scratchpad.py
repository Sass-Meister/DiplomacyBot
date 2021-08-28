from EnumsAndUtils import *
from engine import *
from sys import version

print(version)

FRANCE = CountryEnum.FRANCE
GERMANY = CountryEnum.GERMANY
ITALY = CountryEnum.ITALY

BEL = LocEnum.BEL
NTH = LocEnum.NTH
HOL = LocEnum.HOL
NRG = LocEnum.NRG
BUL = LocEnum.BUL
BUL_EC = LocEnum.BUL_EC
BUL_SC = LocEnum.BUL_SC
SPA = LocEnum.SPA
SPA_NC = LocEnum.SPA_NC
SPA_SC = LocEnum.SPA_SC
STP = LocEnum.STP
STP_NC = LocEnum.STP_NC
STP_SC = LocEnum.STP_SC
WES = LocEnum.WES
MID = LocEnum.MID
AEG = LocEnum.AEG
BLA = LocEnum.BLA
BOT = LocEnum.BOT
BAR = LocEnum.BAR
RUH = LocEnum.RUH
SWE = LocEnum.SWE
DEN = LocEnum.DEN

ARMY = UnitEnum.ARMY
FLEET = UnitEnum.FLEET

HOLD = ActionEnum.HOLD
MOVE = ActionEnum.MOVE

commands = [Command(FRANCE, BEL, MOVE, HOL),
            Command(FRANCE, WES, HOLD),
            Command(FRANCE, RUH, HOLD)]

rules = [SimpleMove]

for rule in rules:
    for command in commands:
        print("Rule: %s, Command: %s" % (rule, command))

        for old, fixed in rule(command, commands):
            print("Old: %s\nFixed: %s\n\n" % (old, fixed))


