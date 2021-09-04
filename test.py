# TODO:__/\\\\\\\\\\\\\\\_______/\\\\\_______/\\\\\\\\\\\\__________/\\\\\____________
# TODO: _\///////\\\/////______/\\\///\\\____\/\\\////////\\\______/\\\///\\\__________
# TODO:  _______\/\\\_________/\\\/__\///\\\__\/\\\______\//\\\___/\\\/__\///\\\________
# TODO:   _______\/\\\________/\\\______\//\\\_\/\\\_______\/\\\__/\\\______\//\\\_______
# TODO:    _______\/\\\_______\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\_______\/\\\__/\\\_
# TODO:     _______\/\\\_______\//\\\______/\\\__\/\\\_______\/\\\_\//\\\______/\\\__\///__
# TODO:      _______\/\\\________\///\\\__/\\\____\/\\\_______/\\\___\///\\\__/\\\__________
# TODO:       _______\/\\\__________\///\\\\\/_____\/\\\\\\\\\\\\/______\///\\\\\/______/\\\_
# TODO:        _______\///_____________\/////_______\////////////__________\/////_______\///__

# Implement the playbook of the rulebook
# Random tests are cool

# TODO:___________________________________________________________________________________________
# TODO: ___________/\\\___________/\\\___________/\\\__/\\\___________/\\\___________/\\\__________
# TODO:  ________/\\\//_________/\\\//_________/\\\//__\////\\\_______\////\\\_______\////\\\_______
# TODO:   _____/\\\//_________/\\\//_________/\\\//________\////\\\_______\////\\\_______\////\\\____
# TODO:    __/\\\//_________/\\\//_________/\\\//______________\////\\\_______\////\\\_______\////\\\_
# TODO:     _\////\\\_______\////\\\_______\////\\\______________/\\\//_________/\\\//_________/\\\//__
# TODO:      ____\////\\\_______\////\\\_______\////\\\________/\\\//_________/\\\//_________/\\\//_____
# TODO:       _______\////\\\_______\////\\\_______\////\\\__/\\\//_________/\\\//_________/\\\//________
# TODO:        __________\///___________\///___________\///__\///___________\///___________\///___________

import unittest

from EnumsAndUtils import *
from engine import Engine, ResolveMove
from state import State
from map import Map

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
GOL = LocEnum.GOL
TYN = LocEnum.TYN
ROM = LocEnum.ROM
NAP = LocEnum.NAP
BOH = LocEnum.BOH
TYR = LocEnum.TYR
MUN = LocEnum.MUN
SIL = LocEnum.SIL
BER = LocEnum.BER
WAR = LocEnum.WAR
PRU = LocEnum.PRU
PIC = LocEnum.PIC
BUR = LocEnum.BUR
GAS = LocEnum.GAS
BRE = LocEnum.BRE
PAR = LocEnum.PAR
IRI = LocEnum.IRI
WAL = LocEnum.WAL
LON = LocEnum.LON
ENG = LocEnum.ENG
VEN = LocEnum.VEN
APU = LocEnum.APU
TUS = LocEnum.TUS
KIE = LocEnum.KIE
MAR = LocEnum.MAR
BAL = LocEnum.BAL
SEV = LocEnum.SEV
RUM = LocEnum.RUM
SER = LocEnum.SER
CON = LocEnum.CON
GRE = LocEnum.GRE
GAL = LocEnum.GAL

ARMY = UnitEnum.ARMY
FLEET = UnitEnum.FLEET

HOLD = ActionEnum.HOLD
MOVE = ActionEnum.MOVE
SUPPORT = ActionEnum.SUPPORT


# Only uses fleets when a move involves a water tile, otherwise uses an army.
def state_from_commands(commands: list[Command]) -> State:
    m = Map()
    startpos = dict()

    for command in commands:
        author = command.getAuthor()

        if author not in startpos:
            startpos[author] = dict()

        loctypeset = {m.getLocation(command.getCurrentLocation()).loctype,
                      None if command.getTargetLocation() is None else m.getLocation(command.getTargetLocation()).loctype}

        startpos[author][command.getCurrentLocation()] = FLEET if LocTypeEnum.WATER in loctypeset else ARMY

    return State(startpos)


class MapTests(unittest.TestCase):
    def setUp(self):
        self.e = Engine(1)
        self.m = Map()

    def testBulgariaCoast1(self):  # See: Specific Movement Clarifications
        self.e.state = State({FRANCE: {AEG: FLEET}})
        self.e.update_state([Command(FRANCE, AEG, MOVE, BUL_SC)])

        self.assertTrue(self.e.state == State({FRANCE: {BUL_SC: FLEET}}))

        with self.assertRaises(CommandConflict):
            self.e.update_state([Command(FRANCE, BUL_SC, MOVE, BLA)])

    def testBulgariaCoast2(self):  # See: Specific Movement Clarifications
        self.e.state = State({FRANCE: {BLA: FLEET}})
        self.e.update_state([Command(FRANCE, BLA, MOVE, BUL_EC)])

        self.assertTrue(self.e.state == State({FRANCE: {BUL_EC: FLEET}}))

        with self.assertRaises(CommandConflict):
            self.e.update_state([Command(FRANCE, BUL_EC, MOVE, AEG)])

    def testSpainCoast1(self):  # See: Specific Movement Clarifications
        self.e.state = State({FRANCE: {WES: FLEET}})
        self.e.update_state([Command(FRANCE, WES, MOVE, SPA_SC)])

        self.assertTrue(self.e.state == State({FRANCE: {SPA_SC: FLEET}}))

        with self.assertRaises(CommandConflict):
            self.e.update_state([Command(FRANCE, SPA_SC, MOVE, MID)])

    def testSpainCoast2(self):  # See: Specific Movement Clarifications
        self.e.state = State({FRANCE: {MID: FLEET}})
        self.e.update_state([Command(FRANCE, MID, MOVE, SPA_NC)])

        self.assertTrue(self.e.state == State({FRANCE: {SPA_NC: FLEET}}))

        with self.assertRaises(CommandConflict):
            self.e.update_state([Command(FRANCE, SPA_NC, MOVE, WES)])

    def testStPCoast1(self):  # See: Specific Movement Clarifications
        self.e.state = State({FRANCE: {BOT: FLEET}})
        self.e.update_state([Command(FRANCE, BOT, MOVE, STP_SC)])

        self.assertTrue(self.e.state == State({FRANCE: {STP_SC: FLEET}}))

        with self.assertRaises(CommandConflict):
            self.e.update_state([Command(FRANCE, STP_SC, MOVE, BAR)])

    def testStPCoast2(self):  # See: Specific Movement Clarifications
        self.e.state = State({FRANCE: {BAR: FLEET}})
        self.e.update_state([Command(FRANCE, BAR, MOVE, STP_NC)])

        self.assertTrue(self.e.state == State({FRANCE: {STP_NC: FLEET}}))

        with self.assertRaises(CommandConflict):
            self.e.update_state([Command(FRANCE, STP_NC, MOVE, BOT)])

    def testSWEtoDEN(self):
        for start, end in ((SWE, DEN), (DEN, SWE)):
            for unit in (FLEET, ARMY):
                self.e.state = State({FRANCE: {start: unit}})

                self.e.update_state([Command(FRANCE, start, MOVE, end)])

                self.assertTrue(self.e.state == State({FRANCE: {end: unit}}))


class Diagrams(unittest.TestCase):  # https://media.wizards.com/2015/downloads/ah/diplomacy_rules.pdf
    # commands: the commands to run
    # final_state: The final stat expected after the commands have been run. Leave blank if you're not expecting change
    #
    # The state is generated using state_from_commands
    def diagramRunner(self, commands: list[Command], final_state: State = None):
        self.e.state = state_from_commands(commands)

        self.e.update_state(commands)

        self.assertTrue(self.e.state == final_state)

    def setUp(self) -> None:
        self.e = Engine(7)

    def testDiagram1(self):
        for loc in [PIC, BUR, GAS, BRE]:
            command = [Command(FRANCE, PAR, MOVE, loc)]

            self.e.state = State({FRANCE: {PAR: ARMY}})

            self.e.update_state(command)

            self.assertTrue(self.e.state == State({FRANCE: {loc: ARMY}}))

    def testDiagram2(self):
        for loc in [IRI, WAL, LON, NTH, BEL, PIC, BRE, MID]:
            command = [Command(FRANCE, ENG, MOVE, loc)]

            self.e.state = State({FRANCE: {ENG: FLEET}})

            self.e.update_state(command)

            self.assertTrue(self.e.state == State({FRANCE: {loc: FLEET}}))

    def testDiagram3(self):
        basestate = State({FRANCE: {ROM: FLEET}})

        for loc in [TUS, NAP]:
            command = [Command(FRANCE, ROM, MOVE, loc)]
            self.e.state = basestate

            self.e.update_state(command)

            self.assertTrue(self.e.state == State({FRANCE: {loc: FLEET}}))

        for loc in [VEN, APU]:
            command = [Command(FRANCE, ROM, MOVE, loc)]
            self.e.state = basestate

            with self.assertRaises(CommandConflict):
                self.e.update_state(command)

    # def testDiagram4(self):
    #     commands = [Command(GERMANY, BER, MOVE, SIL),
    #                 Command(FRANCE, WAR, MOVE, SIL)]
    #
    #     self.e.state = state_from_commands(commands)
    #     oldstate = state_from_commands(commands)
    #
    #     self.e.update_state(commands)
    #
    #     self.assertTrue(self.e.state == oldstate)

    def testDiagram4(self):
        commands = [Command(GERMANY, BER, MOVE, SIL),
                    Command(FRANCE, WAR, MOVE, SIL)]

        self.e.state = state_from_commands(commands)
        oldstate = state_from_commands(commands)

        self.e.update_state(commands)

        self.assertTrue(self.e.state == oldstate)

        self.diagramRunner(commands, )

    def testDiagram5(self):
        commands = [Command(GERMANY, KIE, MOVE, BER),
                    Command(GERMANY, BER, MOVE, PRU),
                    Command(FRANCE, PRU, HOLD)]

        self.e.state = state_from_commands(commands)
        oldstate = state_from_commands(commands)

        self.e.update_state(commands)

        self.assertTrue(self.e.state == oldstate)

    def testDiagram6(self):
        commands = [Command(GERMANY, BER, MOVE, PRU),
                    Command(GERMANY, PRU, MOVE, BER)]

        self.e.state = state_from_commands(commands)
        oldstate = state_from_commands(commands)

        self.e.update_state(commands)

        self.assertTrue(self.e.state == oldstate)

    def testDiagram7(self):
        commands = [Command(GERMANY, HOL, MOVE, BEL),
                    Command(GERMANY, BEL, MOVE, NTH),
                    Command(FRANCE, NTH, MOVE, HOL)]

        self.e.state = state_from_commands(commands)

        self.e.update_state(commands)

        self.assertTrue(self.e.state == State({GERMANY: {NTH: FLEET, BEL: ARMY},
                                               FRANCE: {HOL: FLEET}}))

    def testDiagram8(self):
        commands = [Command(FRANCE, MAR, MOVE, BUR),
                    Command(FRANCE, GAS, SUPPORT, MAR),
                    Command(GERMANY, BUR, HOLD)]

        self.e.state = state_from_commands(commands)

        with self.assertRaises(RetreatDetected):
            self.e.update_state(commands.copy())

        commands[2].retreat = MUN

        self.e.update_state(commands)

        self.assertTrue(self.e.state == State({FRANCE: {BUR: ARMY, GAS: ARMY},
                                               GERMANY: {MUN: ARMY}}))

    def testDiagram9(self):
        commands = [Command(GERMANY, SIL, MOVE, PRU),
                    Command(GERMANY, BAL, SUPPORT, SIL),
                    Command(FRANCE, PRU, HOLD)]

        self.e.state = state_from_commands(commands)

        with self.assertRaises(RetreatDetected):
            self.e.update_state(commands.copy())

        commands[2].retreat = WAR

        self.e.update_state(commands)

        self.assertTrue(self.e.state == State({GERMANY: {PRU: ARMY, BAL: FLEET},
                                               FRANCE: {WAR: ARMY}}))

    def testDiagram10(self):
        commands = [Command(FRANCE, GOL, MOVE, TYN),
                    Command(FRANCE, WES, SUPPORT, GOL),
                    Command(GERMANY, NAP, MOVE, TYN),
                    Command(GERMANY, ROM, SUPPORT, NAP)]

        self.e.state = state_from_commands(commands)
        oldstate = state_from_commands(commands)

        self.e.update_state(commands)

        self.assertTrue(self.e.state == oldstate)

    def testDiagram11(self):
        commands = [Command(FRANCE, GOL, MOVE, TYN),
                    Command(FRANCE, WES, SUPPORT, GOL),
                    Command(GERMANY, TYN, HOLD),
                    Command(GERMANY, ROM, SUPPORT, TYN)]

        self.e.state = state_from_commands(commands)
        oldstate = state_from_commands(commands)

        self.e.update_state(commands)

        self.assertTrue(self.e.state == oldstate)

    def testDiagram12(self):
        commands = [Command(FRANCE, BOH, MOVE, MUN),
                    Command(FRANCE, TYR, SUPPORT, BOH),
                    Command(GERMANY, MUN, MOVE, SIL),
                    Command(GERMANY, BER, SUPPORT, MUN),
                    Command(ITALY, WAR, MOVE, SIL),
                    Command(ITALY, PRU, SUPPORT, WAR)]

        self.e.state = state_from_commands(commands.copy())

        with self.assertRaises(RetreatDetected):
            self.e.update_state(commands)

        commands[2].retreat = RUH

        self.e.update_state(commands)

        self.assertTrue(self.e.state == State({FRANCE: {MUN: ARMY,
                                                        TYR: ARMY},
                                               GERMANY: {RUH: ARMY,
                                                         BER: ARMY},
                                               ITALY: {PRU: ARMY,
                                                       WAR: ARMY}}))

    def testDiagram13(self):
        commands = [Command(FRANCE, SEV, MOVE, RUM),
                    Command(FRANCE, RUM, MOVE, BUL),
                    Command(FRANCE, SER, SUPPORT, RUM),
                    Command(GERMANY, BUL, MOVE, RUM)]

        self.e.state = state_from_commands(commands)

        with self.assertRaises(RetreatDetected):
            self.e.update_state(commands)

        commands[3].retreat = CON

        self.e.update_state(commands)

        self.assertTrue(self.e.state == State({FRANCE: {SER: ARMY,
                                                        BUL: ARMY,
                                                        RUM: ARMY},
                                               GERMANY: {CON: ARMY}}))

    def testDiagram14(self):
        commands = [Command(FRANCE, BUL, MOVE, RUM),
                    Command(FRANCE, BLA, SUPPORT, BUL),
                    Command(GERMANY, RUM, MOVE, BUL),
                    Command(GERMANY, GRE, SUPPORT, RUM),
                    Command(GERMANY, SER, SUPPORT, RUM),
                    Command(GERMANY, SEV, MOVE, RUM)]

        self.e.state = state_from_commands(commands)

        with self.assertRaises(RetreatDetected):
            self.e.update_state(commands)

        commands[0].retreat = CON

        self.e.update_state(commands)

        self.assertTrue(self.e.state == State({FRANCE: {BLA: ARMY,
                                                        CON: ARMY},
                                               GERMANY: {RUM: ARMY,
                                                         BUL: ARMY,
                                                         SER: ARMY,
                                                         GRE: ARMY}}))

    def testDiagram15(self):
        commands = [Command(FRANCE, PRU, MOVE, WAR),
                    Command(FRANCE, SIL, SUPPORT, PRU),
                    Command(GERMANY, WAR, HOLD),
                    Command(GERMANY, BOH, MOVE, SIL)]

        self.e.state = state_from_commands(commands)
        oldstate = state_from_commands(commands)

        self.e.update_state(commands)

        self.assertTrue(self.e.state == oldstate)

    def testDiagram16(self):
        commands = [Command(FRANCE, PRU, MOVE, WAR),
                    Command(FRANCE, SIL, SUPPORT, PRU),
                    Command(GERMANY, WAR, MOVE, SIL)]

        self.e.state = state_from_commands(commands)

        with self.assertRaises(RetreatDetected):
            self.e.update_state(commands)

        commands[2].retreat = GAL

        self.e.update_state(commands)

        self.assertTrue(self.e.state == State({FRANCE: {SIL: ARMY,
                                                        WAR: ARMY},
                                               GERMANY: {GAL: ARMY}}))

    def testDiagram17(self):
        commands = [Command(FRANCE, BER, MOVE, PRU),
                    Command(FRANCE, SIL, SUPPORT, BER),
                    Command(GERMANY, PRU, MOVE, SIL),
                    Command(GERMANY, WAR, SUPPORT, PRU),
                    Command(GERMANY, BAL, MOVE, PRU)]

        self.e.state = state_from_commands(commands)

        with self.assertRaises(RetreatDetected):
            self.e.update_state(commands.copy())

        commands[1].retreat = BOH

        self.e.update_state(commands)

        self.assertTrue(self.e.state == State({FRANCE: {BER: ARMY,
                                                        SIL: BOH},
                                               }))





class Singles(unittest.TestCase):
    def setUp(self):
        self.e = Engine(1)

    def testDoNothing(self):
        self.e.state = State({FRANCE: {BEL: ARMY}})
        oldstate = self.e.state

        command = [Command(FRANCE, BEL, HOLD)]

        self.e.update_state(command)

        self.assertTrue(self.e.state == oldstate)

    def testLandToLand(self):
        self.e.state = State({FRANCE: {BEL: ARMY}})

        command = [Command(FRANCE, BEL, MOVE, HOL)]

        self.e.update_state(command)

        self.assertTrue(self.e.state == State({FRANCE: {HOL: ARMY}}))

    def testWaterToWater(self):
        self.e.state = State({FRANCE: {NTH: FLEET}})

        command = [Command(FRANCE, NTH, MOVE, NRG)]

        self.e.update_state(command)

        self.assertTrue(self.e.state == State({FRANCE: {NRG: FLEET}}))

    def testWaterToLand(self):
        self.e.state = State({FRANCE: {NTH: FLEET}})

        command = [Command(FRANCE, NTH, MOVE, HOL)]

        self.e.update_state(command)

        self.assertTrue(self.e.state == State({FRANCE: {HOL: FLEET}}))

    def testLandToWater(self):
        self.e.state = State({FRANCE: {HOL: FLEET}})

        command = [Command(FRANCE, HOL, MOVE, NTH)]

        self.e.update_state(command)

        self.assertTrue(self.e.state == State({FRANCE: {NTH: FLEET}}))


class Duos(unittest.TestCase):
    def setUp(self):
        self.e = Engine(2)

    def testBumperCars(self):
        self.e.state = State({FRANCE: {BEL: ARMY}, GERMANY: {HOL: ARMY}})

        commands = [Command(FRANCE, BEL, MOVE, HOL),
                    Command(GERMANY, HOL, MOVE, BEL)]

        self.e.update_state(commands)

        self.assertTrue(self.e.state == State({FRANCE: {BEL: ARMY}, GERMANY: {HOL: ARMY}}))

    def testKOTH(self):
        self.e.state = State({FRANCE: {HOL: ARMY}, GERMANY: {RUH: ARMY}})

        oldstate = State({FRANCE: {HOL: ARMY}, GERMANY: {RUH: ARMY}})

        commands = [Command(FRANCE, HOL, MOVE, BEL),
                    Command(GERMANY, RUH, MOVE, BEL)]

        self.e.update_state(commands)

        self.assertTrue(self.e.state == oldstate)

    def testSnake(self):
        self.e.state = State({FRANCE: {HOL: ARMY},
                              GERMANY: {BEL: ARMY}})

        commands = [Command(FRANCE, HOL, MOVE, BEL),
                    Command(GERMANY, BEL, MOVE, RUH)]

        self.e.update_state(commands)

        self.assertTrue(self.e.state == State({FRANCE: {BEL: ARMY},
                                               GERMANY: {RUH: ARMY}}))


class Trios(unittest.TestCase):
    def setUp(self):
        self.e = Engine(3)

    def testTriangleMove(self):
        self.e.state = State({FRANCE: {BEL: ARMY},
                              GERMANY: {HOL: ARMY},
                              ITALY: {RUH: ARMY}})

        commands = [Command(FRANCE, BEL, MOVE, HOL),
                    Command(GERMANY, HOL, MOVE, RUH),
                    Command(ITALY, RUH, MOVE, BEL)]

        self.e.update_state(commands)

        self.assertTrue(self.e.state == State({FRANCE: {HOL: ARMY},
                                               GERMANY: {RUH: ARMY},
                                               ITALY: {BEL: ARMY}}))


if __name__ == '__main__':
    unittest.main()
