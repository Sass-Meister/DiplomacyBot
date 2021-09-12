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

# Create a command to just do retreats

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
import random

from EnumsAndUtils import *
from engine import Engine, ResolveMove
from state import State
from map import getLocation

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
NWY = LocEnum.NWY
TUN = LocEnum.TUN
ION = LocEnum.ION

ARMY = UnitEnum.ARMY
FLEET = UnitEnum.FLEET

HOLD = ActionEnum.HOLD
MOVE = ActionEnum.MOVE
SUPPORT = ActionEnum.SUPPORT
CONVOY = ActionEnum.CONVOY


class MapTests(unittest.TestCase):
    def setUp(self):
        self.e = Engine(1)

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
    # Given a list of commands, a state will be returned which will allow the commands to be run against it. Fleets are
    # only placed on water, armies for coastal and inland.
    #
    # commands: A list of commands to generate the state from
    def state_from_commands(self, commands: list[Command]) -> State:
        startpos = dict()

        for command in commands:
            author = command.getAuthor()

            if author not in startpos:
                startpos[author] = dict()

            loctypeset = {getLocation(command.getCurrentLocation()).loctype,
                          None if command.getTargetLocation() is None else getLocation(
                              command.getTargetLocation()).loctype}

            startpos[author][command.getCurrentLocation()] = FLEET if LocTypeEnum.WATER in loctypeset else ARMY

        return State(startpos)

    # Runs a list of commands along with a base state and test if the expected final state is reached.
    #
    # commands: the commands to run
    # final_state: The final stat expected after the commands have been run. If None, state_from_commands is used.
    # base_state: The base state for the commands to be tested against. If None, state_from_commands is used.
    def isStateUpdated(self, commands: list[Command], final_state: State = None, base_state: State = None):
        if base_state is None:
            base_state = self.state_from_commands(commands)

        if final_state is None:
            final_state = self.state_from_commands(commands)

        self.e.state = base_state

        self.e.update_state(commands)

        self.assertTrue(self.e.state == final_state)

    # Runs a list of commands along with a base state to test if the provided exception is raised.
    #
    # test_exception: The exception expected to be raised when update_state is ran with these commands
    # commands: The commands as an array of Command objects
    # base_state: The base state for the commands to be tested against. If None, state_from_commands is used
    def isErrorRaised(self, test_exception: Exception, commands: list[Command], base_state: State = None):
        if base_state is None:
            base_state = self.state_from_commands(commands)

        self.e.state = base_state

        with self.assertRaises(test_exception):
            self.e.update_state(commands.copy())

    def setUp(self) -> None:
        self.e = Engine(7)

    def testDiagram01(self):
        for loc in [PIC, BUR, GAS, BRE]:
            self.isStateUpdated([Command(FRANCE, PAR, MOVE, loc)], State({FRANCE: {loc: ARMY}}))

    def testDiagram02(self):
        for loc in [IRI, WAL, LON, NTH, BEL, PIC, BRE, MID]:
            self.isStateUpdated([Command(FRANCE, ENG, MOVE, loc)], State({FRANCE: {loc: FLEET}}))

    def testDiagram03(self):
        basestate = State({FRANCE: {ROM: FLEET}})

        for loc in [TUS, NAP]:
            self.isStateUpdated([Command(FRANCE, ROM, MOVE, loc)], State({FRANCE: {loc: FLEET}}), basestate)

        for loc in [VEN, APU]:
            self.isErrorRaised(CommandConflict, [Command(FRANCE, ROM, MOVE, loc)], basestate)

    def testDiagram04(self):
        self.isStateUpdated([Command(GERMANY, BER, MOVE, SIL),
                             Command(FRANCE, WAR, MOVE, SIL)])

    def testDiagram05(self):
        self.isStateUpdated([Command(GERMANY, KIE, MOVE, BER),
                             Command(GERMANY, BER, MOVE, PRU),
                             Command(FRANCE, PRU, HOLD)])

    def testDiagram06(self):
        self.isStateUpdated([Command(GERMANY, BER, MOVE, PRU),
                             Command(GERMANY, PRU, MOVE, BER)])

    def testDiagram07(self):
        commands = [Command(GERMANY, HOL, MOVE, BEL),
                    Command(GERMANY, BEL, MOVE, NTH),
                    Command(FRANCE, NTH, MOVE, HOL)]

        state = State({GERMANY: {NTH: FLEET,
                                 BEL: ARMY},
                       FRANCE: {HOL: FLEET}})

        self.isStateUpdated(commands, state)

    def testDiagram08(self):
        commands = [Command(FRANCE, MAR, MOVE, BUR),
                    Command(FRANCE, GAS, SUPPORT, MAR),
                    Command(GERMANY, BUR, HOLD)]

        self.isErrorRaised(RetreatDetected, commands)

        commands[2].retreat = MUN

        final_state = State({FRANCE: {BUR: ARMY, GAS: ARMY}, GERMANY: {MUN: ARMY}})

        self.isStateUpdated(commands, final_state)

    def testDiagram09(self):
        commands = [Command(GERMANY, SIL, MOVE, PRU),
                    Command(GERMANY, BAL, SUPPORT, SIL),
                    Command(FRANCE, PRU, HOLD)]

        self.isErrorRaised(RetreatDetected, commands)

        commands[2].retreat = WAR

        self.isStateUpdated(commands, State({GERMANY: {PRU: ARMY, BAL: FLEET}, FRANCE: {WAR: ARMY}}))

    def testDiagram10(self):
        self.isStateUpdated([Command(FRANCE, GOL, MOVE, TYN),
                             Command(FRANCE, WES, SUPPORT, GOL),
                             Command(GERMANY, NAP, MOVE, TYN),
                             Command(GERMANY, ROM, SUPPORT, NAP)])

    def testDiagram11(self):
        self.isStateUpdated([Command(FRANCE, GOL, MOVE, TYN),
                             Command(FRANCE, WES, SUPPORT, GOL),
                             Command(GERMANY, TYN, HOLD),
                             Command(GERMANY, ROM, SUPPORT, TYN)])

    def testDiagram12(self):
        commands = [Command(FRANCE, BOH, MOVE, MUN),
                    Command(FRANCE, TYR, SUPPORT, BOH),
                    Command(GERMANY, MUN, MOVE, SIL),
                    Command(GERMANY, BER, SUPPORT, MUN),
                    Command(ITALY, WAR, MOVE, SIL),
                    Command(ITALY, PRU, SUPPORT, WAR)]

        self.isErrorRaised(RetreatDetected, commands)

        commands[2].retreat = RUH

        self.isStateUpdated(commands, State({FRANCE: {MUN: ARMY,
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

        self.isErrorRaised(RetreatDetected, commands)

        commands[3].retreat = CON

        self.isStateUpdated(commands, State({FRANCE: {SER: ARMY,
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

        self.isErrorRaised(RetreatDetected, commands)

        commands[0].retreat = CON

        self.isStateUpdated(commands, State({FRANCE: {BLA: FLEET,
                                                      CON: ARMY},
                                             GERMANY: {RUM: ARMY,
                                                       BUL: ARMY,
                                                       SER: ARMY,
                                                       GRE: ARMY}}))

    def testDiagram15(self):
        self.isStateUpdated([Command(FRANCE, PRU, MOVE, WAR),
                             Command(FRANCE, SIL, SUPPORT, PRU),
                             Command(GERMANY, WAR, HOLD),
                             Command(GERMANY, BOH, MOVE, SIL)])

    def testDiagram16(self):
        commands = [Command(FRANCE, PRU, MOVE, WAR),
                    Command(FRANCE, SIL, SUPPORT, PRU),
                    Command(GERMANY, WAR, MOVE, SIL)]

        self.isErrorRaised(RetreatDetected, commands)

        commands[2].retreat = GAL

        self.isStateUpdated(commands, State({FRANCE: {SIL: ARMY,
                                                      WAR: ARMY},
                                             GERMANY: {GAL: ARMY}}))

    def testDiagram17(self):
        commands = [Command(FRANCE, BER, MOVE, PRU),
                    Command(FRANCE, SIL, SUPPORT, BER),
                    Command(GERMANY, PRU, MOVE, SIL),
                    Command(GERMANY, WAR, SUPPORT, PRU),
                    Command(GERMANY, BAL, MOVE, PRU)]

        self.isErrorRaised(RetreatDetected, commands)

        commands[1].retreat = BOH

        self.isStateUpdated(commands, State({FRANCE: {BER: ARMY,
                                                      BOH: ARMY},
                                             GERMANY: {SIL: ARMY,
                                                       WAR: ARMY,
                                                       BAL: FLEET}}))

    def testDiagram18(self):
        commands = [Command(FRANCE, BER, HOLD),
                    Command(FRANCE, MUN, MOVE, SIL),
                    Command(GERMANY, PRU, MOVE, BER),
                    Command(GERMANY, SIL, SUPPORT, PRU),
                    Command(GERMANY, BOH, MOVE, MUN),
                    Command(GERMANY, TYR, SUPPORT, BOH)]

        self.isErrorRaised(RetreatDetected, commands)

        commands[1].retreat = RUH

        self.isStateUpdated(commands, State({FRANCE: {BER: ARMY,
                                                      RUH: ARMY},
                                             GERMANY: {PRU: ARMY,
                                                       SIL: ARMY,
                                                       MUN: ARMY,
                                                       TYR: ARMY}}))

    def testDiagram19(self):
        commands = [Command(FRANCE, LON, MOVE, NWY),
                    Command(FRANCE, NTH, CONVOY, LON, NWY)]

        self.isStateUpdated(commands, State({FRANCE: {NWY: ARMY,
                                                      NTH: FLEET}}))

    def testDiagram20(self):
        commands = [Command(FRANCE, LON, MOVE, TUN),
                    Command(FRANCE, ENG, CONVOY, LON, MID),
                    Command(FRANCE, MID, CONVOY, ENG, WES),
                    Command(GERMANY, WES, CONVOY, MID, TUN)]

        self.isStateUpdated(commands, State({FRANCE: {TUN: ARMY,
                                                      ENG: FLEET,
                                                      MID: FLEET},
                                             GERMANY: {WES: FLEET}}))

    def testDiagram21(self):
        commands = [Command(FRANCE, SPA, MOVE, NAP),
                    Command(FRANCE, GOL, CONVOY, SPA, TYN),
                    Command(FRANCE, TYN, CONVOY, GOL, NAP),
                    Command(GERMANY, ION, MOVE, TYN),
                    Command(GERMANY, TUN, SUPPORT, ION)]

        self.isErrorRaised(RetreatDetected, commands)

        commands[2].retreat = WES

        self.isStateUpdated(commands, State({FRANCE: {SPA: ARMY,
                                                      GOL: FLEET,
                                                      WES: FLEET},
                                             GERMANY: {TYN: FLEET,
                                                       TUN: FLEET}}))  # A base state will need to be constructed to make sure a fleet is on TUN

    def testDiagram22(self):
        self.isStateUpdated([Command(FRANCE, PAR, MOVE, BUR),
                             Command(FRANCE, MAR, SUPPORT, PAR),
                             Command(FRANCE, BUR, HOLD)])

    def testDiagram23(self):
        self.isStateUpdated([Command(FRANCE, PAR, MOVE, BUR),
                             Command(FRANCE, BUR, MOVE, MAR),
                             Command(GERMANY, RUH, SUPPORT, PAR),
                             Command(ITALY, MAR, MOVE, BUR)])

    def testDiagram24(self):
        self.isStateUpdated([Command(GERMANY, RUH, MOVE, BUR),
                             Command(GERMANY, MUN, HOLD),
                             Command(FRANCE, PAR, SUPPORT, RUH),
                             Command(FRANCE, BUR, HOLD)])

    def testDiagram25(self):
        self.isStateUpdated([Command(GERMANY, MUN, MOVE, TYR),
                             Command(GERMANY, RUH, MOVE, MUN),
                             Command(GERMANY, SIL, MOVE, MUN),
                             Command(FRANCE, TYR, MOVE, MUN),
                             Command(FRANCE, BOH, SUPPORT, SIL)])

class WanderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.MAX_MOVES = 1000
        self.e = Engine(1)

    def testSingleArmy(self):
        current = BOH  # Starting Location

        self.e.state = State({FRANCE: {current: ARMY}})

        moves = 0

        while moves < self.MAX_MOVES:
            loc = getLocation(current)
            move_to = random.choice(loc.border)

            try:
                self.e.update_state([Command(FRANCE, current, MOVE, move_to)])
                # print("Moved to %s" % move_to)
            except CommandConflict:
                self.assertTrue(getLocation(move_to).loctype == LocTypeEnum.WATER)
                # print("Correctly detected an attempt to move into the water")
                continue

            current = move_to

            self.assertTrue(self.e.state == State({FRANCE: {current: ARMY}}))

            moves = moves + 1

    def testSingleFleet(self):
        current = TYN  # Starting Location

        self.e.state = State({FRANCE: {current: FLEET}})

        moves = 0

        while moves < self.MAX_MOVES:
            loc = getLocation(current)
            move_to = random.choice(loc.border)

            try:
                self.e.update_state([Command(FRANCE, current, MOVE, move_to)])
                # print("Moved to %s" % move_to)
            except CommandConflict:
                # self.assertTrue(getLocation(move_to).loctype == LocTypeEnum.INLAND)
                # print("Correctly detected an attempt to move into the water")
                continue

            current = move_to

            self.assertTrue(self.e.state == State({FRANCE: {current: FLEET}}))

            moves = moves + 1


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
