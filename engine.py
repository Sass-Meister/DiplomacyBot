# TODO:__/\\\\\\\\\\\\\\\_______/\\\\\_______/\\\\\\\\\\\\__________/\\\\\____________
# TODO: _\///////\\\/////______/\\\///\\\____\/\\\////////\\\______/\\\///\\\__________
# TODO:  _______\/\\\_________/\\\/__\///\\\__\/\\\______\//\\\___/\\\/__\///\\\________
# TODO:   _______\/\\\________/\\\______\//\\\_\/\\\_______\/\\\__/\\\______\//\\\_______
# TODO:    _______\/\\\_______\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\_______\/\\\__/\\\_
# TODO:     _______\/\\\_______\//\\\______/\\\__\/\\\_______\/\\\_\//\\\______/\\\__\///__
# TODO:      _______\/\\\________\///\\\__/\\\____\/\\\_______/\\\___\///\\\__/\\\__________
# TODO:       _______\/\\\__________\///\\\\\/_____\/\\\\\\\\\\\\/______\///\\\\\/______/\\\_
# TODO:        _______\///_____________\/////_______\////////////__________\/////_______\///__


# TODO:______/\\\_____/\\\\\\\_________/\\\_____/\\\\\\\_________/\\\_____/\\\\\\\_________/\\\_
# TODO: __/\\\\\\\___/\\\/////\\\___/\\\\\\\___/\\\/////\\\___/\\\\\\\___/\\\/////\\\___/\\\\\\\_
# TODO:  _\/////\\\__/\\\____\//\\\_\/////\\\__/\\\____\//\\\_\/////\\\__/\\\____\//\\\_\/////\\\_
# TODO:   _____\/\\\_\/\\\_____\/\\\_____\/\\\_\/\\\_____\/\\\_____\/\\\_\/\\\_____\/\\\_____\/\\\_
# TODO:    _____\/\\\_\/\\\_____\/\\\_____\/\\\_\/\\\_____\/\\\_____\/\\\_\/\\\_____\/\\\_____\/\\\_
# TODO:     _____\/\\\_\/\\\_____\/\\\_____\/\\\_\/\\\_____\/\\\_____\/\\\_\/\\\_____\/\\\_____\/\\\_
# TODO:      _____\/\\\_\//\\\____/\\\______\/\\\_\//\\\____/\\\______\/\\\_\//\\\____/\\\______\/\\\_
# TODO:       _____\/\\\__\///\\\\\\\/_______\/\\\__\///\\\\\\\/_______\/\\\__\///\\\\\\\/_______\/\\\_
# TODO:        _____\///_____\///////_________\///_____\///////_________\///_____\///////_________\///_
from EnumsAndUtils import *
from map import Map
from state import State

HOLD = ActionEnum.HOLD
MOVE = ActionEnum.MOVE
SUPPORT = ActionEnum.SUPPORT
CONVOY = ActionEnum.CONVOY


# class SimpleMove(RuleBase):  # literally untested
#     def attempt_resolve(self, audit: Command, commands: list[Command]) -> dict[Command: Command]:
#         if audit.getAction() == MOVE:
#             for command in commands:
#                 if audit is not command and \
#                         (audit.getTargetLocation() == command.getCurrentLocation() or
#                          (audit.getTargetLocation() == command.getTargetLocation() and command.getAction() == MOVE)):
#                     return dict()
#             return {audit: audit}
#         return dict()

# Assumes all commands have been checked and audit is in commands

def turn_to_hold(command: Command) -> Command:
    return Command(command.getAuthor(), command.getCurrentLocation(), HOLD)


class ResolveDislodge(RuleBase):  # Am I dislodged?
    def attempt_resolve(self, audit: Command, commands: list[Command]) -> dict[Command: Command]:
        if audit.getAction() == MOVE:
            return dict()

        TargetSort = sort_commands("location", commands)

        if audit.getCurrentLocation() in TargetSort:
            for command in TargetSort[audit.getCurrentLocation()]:
                if command.getAction() == MOVE:
                    return {audit: turn_to_hold(audit)}

        return dict()


class DetectRetreats(RuleBase):
    def attempt_resolve(self, audit: Command, commands: list[Command]) -> dict[Command: Command]:
        if audit.getAction() == MOVE:
            return dict()

        TargetSort = sort_commands("location", commands)

        if audit.getCurrentLocation() in TargetSort:
            for command in TargetSort[audit.getCurrentLocation()]:
                if command.getAction() == MOVE and count_support(command, commands) > count_support(audit, commands):
                    raise RetreatDetected

        return dict()


class ResolveMove(RuleBase):
    def resolvable_move(self, audit: Command, commands: list[Command]) -> bool:
        if audit not in commands:
            raise Exception("audit must be in commands")

        if audit.getAction() != MOVE:
            print("Not a move......")
            return False

        LocSort = sort_commands("unit", commands)
        TargetSort = sort_commands("location", commands)

        if audit.getCurrentLocation() in TargetSort:
            for command in TargetSort[audit.getCurrentLocation()]:
                if command.getAction() == MOVE and count_support(command, commands) > count_support(audit, commands):
                    raise RetreatDetected(audit)

        if audit.getTargetLocation() in LocSort and count_support(audit, commands) > count_support(
                LocSort[audit.getTargetLocation()][0], commands):
            return True

        current = audit

        while True:
            for loc in TargetSort[current.getTargetLocation()]:
                if loc is current:
                    continue

                if loc.getAction() == MOVE:
                    if loc.getTargetLocation() == current.getCurrentLocation() and \
                       count_support(loc,commands) > count_support(current, commands):
                        raise RetreatDetected(current)

                    if count_support(loc, commands) >= count_support(current, commands):  # If someone else is trying to move there
                        print("Someone else is trying to move there")
                        return False

            # If no one is where you're trying to move
            if current.getTargetLocation() not in LocSort:
                print("No one is trying to move there")
                return True  # Everyone else is doing something other than moving there

            next = LocSort[current.getTargetLocation()][0]

            if next.getAction() != MOVE:  # The unit on the next locaiton is not moving
                print("The unit is blocked by something non moving")
                return False

            if next is audit:
                return audit.getTargetLocation() != current.getCurrentLocation()

            current = next

    def attempt_resolve(self, audit: Command, commands: list[Command]) -> dict[Command: Command]:
        rtr = dict()

        if not self.resolvable_move(audit, commands):
            rtr[audit] = turn_to_hold(audit)

        return rtr


rules = [ResolveDislodge,
         DetectRetreats,
         ResolveMove]


class Engine:
    def __init__(self, players: int):
        startpos = {CountryEnum.AUSTRIA: {LocEnum.VIE: UnitEnum.ARMY,
                                          LocEnum.BUD: UnitEnum.ARMY,
                                          LocEnum.TRI: UnitEnum.FLEET},
                    CountryEnum.ENGLAND: {LocEnum.LON: UnitEnum.FLEET,
                                          LocEnum.EDI: UnitEnum.FLEET,
                                          LocEnum.LVP: UnitEnum.ARMY},
                    CountryEnum.FRANCE: {LocEnum.PAR: UnitEnum.ARMY,
                                         LocEnum.MAR: UnitEnum.ARMY,
                                         LocEnum.BRE: UnitEnum.FLEET},
                    CountryEnum.GERMANY: {LocEnum.BER: UnitEnum.ARMY,
                                          LocEnum.MUN: UnitEnum.ARMY,
                                          LocEnum.KIE: UnitEnum.FLEET},
                    CountryEnum.ITALY: {LocEnum.ROM: UnitEnum.ARMY,
                                        LocEnum.VEN: UnitEnum.ARMY,
                                        LocEnum.NAP: UnitEnum.FLEET},
                    CountryEnum.RUSSIA: {LocEnum.MOS: UnitEnum.ARMY,
                                         LocEnum.SEV: UnitEnum.FLEET,
                                         LocEnum.WAR: UnitEnum.ARMY,
                                         LocEnum.STP_SC: UnitEnum.FLEET},
                    CountryEnum.TURKEY: {LocEnum.ANK: UnitEnum.FLEET,
                                         LocEnum.CON: UnitEnum.ARMY,
                                         LocEnum.SMY: UnitEnum.ARMY}}

        self.state = State(startpos)
        self.players = players
        self.map = Map()

    ####################################################################################################################
    ## Checking each command against the map and the state to see if the list of commands could be rendered           ##
    ####################################################################################################################
    def check_commands(self, commands: list):
        checkedlocations = []

        if len(commands) != len(self.state.getAllUnits()):
            raise CommandConflict("Mismatch: %i commands and %i units" % (len(commands), len(self.state.getAllUnits())))

        for command in commands:
            command.validate()

            country = self.state.getCountry(command.getAuthor())  # What I really want is the country object
            province = self.map.getLocation(command.getCurrentLocation())

            if command.getCurrentLocation() in checkedlocations:
                raise CommandConflict("More than one command for the unit at %s" % command.getCurrentLocation())

            if command.getCurrentLocation() not in country.units:
                raise CommandConflict("No unit at that location")

            if command.getAction() == HOLD:
                continue

            if command.getTargetLocation() not in province.border:
                raise CommandConflict("Invalid Location")

            if command.action == MOVE:
                if country.units[command.unit] == UnitEnum.ARMY and province.loctype == LocTypeEnum.WATER:
                    raise CommandConflict("Your little men can't swim silly")

                if country.units[command.unit] == UnitEnum.FLEET and province.loctype == LocTypeEnum.INLAND:
                    raise CommandConflict("The fleet is unable to progress inland")

    # Working Commands
    # Hold: In
    # Move: Under Construction
    # Support: TBD
    # Convoy: TBD
    def update_state(self, commands: list[Command]):
        if len(commands) == 0:
            return

        self.check_commands(commands)

        for rule in rules:
            oldlist = []
            fixedlist = []

            for command in commands.copy():
                for old, fixed in rule(command, commands):
                    oldlist.append(old)
                    fixedlist.append(fixed)

            for old in oldlist:
                commands.remove(old)

            commands = commands + fixedlist

        # At this point all commands are now in fixed and are ready to construct a new state

        startpos = dict()  # First construct the new startpos

        for command in commands:
            if command.getAuthor() not in startpos:
                startpos[command.getAuthor()] = dict()

            if command.getAction() == MOVE:
                startpos[command.getAuthor()][command.getTargetLocation()] = self.state.getUnit(
                    command.getCurrentLocation())

            else:
                startpos[command.getAuthor()][command.getCurrentLocation()] = self.state.getUnit(
                    command.getCurrentLocation())

        self.state = State(startpos)  # Construct the new state and set it to self
