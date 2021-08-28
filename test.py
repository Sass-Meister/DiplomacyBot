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
from engine import Engine
from state import State
from map import Map

# https://media.wizards.com/2015/downloads/ah/diplomacy_rules.pdf

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
        self.e.state = State({FRANCE: {BEL: ARMY},
                              GERMANY: {HOL: ARMY}})

        commands = [Command(FRANCE, BEL, MOVE, HOL),
                    Command(GERMANY, HOL, MOVE, BEL)]

        self.e.update_state(commands)

        self.assertTrue(self.e.state == State({FRANCE: {NTH: FLEET}}))

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
                                               ITALY: {BEL, ARMY}}))


if __name__ == '__main__':
    unittest.main()
