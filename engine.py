# TODO:__/\\\\\\\\\\\\\\\_______/\\\\\_______/\\\\\\\\\\\\__________/\\\\\____________
# TODO: _\///////\\\/////______/\\\///\\\____\/\\\////////\\\______/\\\///\\\__________
# TODO:  _______\/\\\_________/\\\/__\///\\\__\/\\\______\//\\\___/\\\/__\///\\\________
# TODO:   _______\/\\\________/\\\______\//\\\_\/\\\_______\/\\\__/\\\______\//\\\_______
# TODO:    _______\/\\\_______\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\_______\/\\\__/\\\_
# TODO:     _______\/\\\_______\//\\\______/\\\__\/\\\_______\/\\\_\//\\\______/\\\__\///__
# TODO:      _______\/\\\________\///\\\__/\\\____\/\\\_______/\\\___\///\\\__/\\\__________
# TODO:       _______\/\\\__________\///\\\\\/_____\/\\\\\\\\\\\\/______\///\\\\\/______/\\\_
# TODO:        _______\///_____________\/////_______\////////////__________\/////_______\///__

# Add support for moving years

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
from map import getLocation
from state import State

HOLD = ActionEnum.HOLD
MOVE = ActionEnum.MOVE
SUPPORT = ActionEnum.SUPPORT
CONVOY = ActionEnum.CONVOY


def resolvable_move(audit: Command, commands: list[Command]) -> bool:
    if audit not in commands:
        raise Exception("audit must be in commands")

    if audit.getAction() != MOVE:
        # print("Not a move......")
        return False

    LocSort = sort_commands("unit", commands)
    TargetSort = sort_commands("location", commands)

    # If a unit is where we're trying to move, we can assuredly move there if they're not moving and we're got more
    # support or they are moving somewhere other than where we are and we've got at least one supporter. If the
    # move at that location is later deemed to not be resolvable, that location must retreat
    onlymove = True

    for cmd in TargetSort[audit.getTargetLocation()]:
        if cmd is not audit and cmd.getAction() is MOVE:
            onlymove = False
            break

    if audit.getTargetLocation() in LocSort and onlymove:
        target_command = LocSort[audit.getTargetLocation()][0]
        my_support = count_support(audit, commands)
        their_support = count_support(target_command, commands)

        if target_command.getAction() != MOVE and my_support > their_support:
            return True

        if target_command.getAction() == MOVE and target_command.getTargetLocation() != audit.getCurrentLocation() and my_support > 0:
            return True

    # Now we traverse the map at each location (starting with our audit) first checking what happens when someone
    # else is trying to move where we are and if the unit in front is moving. If they are we start over and repeat
    # these checks
    current = audit

    while True:
        my_support = count_support(current, commands)

        # Checking the other units targeting the location where the current command is trying to move
        for loc in TargetSort[current.getTargetLocation()]:
            if loc is current or loc.getAction() is not MOVE:  # We only care about other people moving there
                continue

            # If someone else is trying to move there with at least the same support we have, we cannot move there
            if count_support(loc, commands) >= my_support:
                return False

        # If no one is where you're trying to move
        if current.getTargetLocation() not in LocSort:
            return True

        next = LocSort[current.getTargetLocation()][0]

        if next is audit:
            return audit.getTargetLocation() != current.getCurrentLocation()  # Prevent Diagram 6

        if my_support > count_support(next, commands):
            return True

        if next.getAction() != MOVE:  # The unit on the next location is not moving
            return False

        current = next


class ResolveCutSupport(RuleBase):
    def attempt_resolve(self, commands: list[Command]) -> dict[Command: Command]:
        rtr = dict()
        TargetSort = sort_commands("location", commands)
        LocSort = sort_commands("unit", commands)

        for cmd in commands:
            if cmd.getAction() is not SUPPORT:
                continue

            if cmd.getCurrentLocation() in TargetSort:
                supported_cmd = LocSort[cmd.getTargetLocation()][0]

                for invader in TargetSort[cmd.getCurrentLocation()]:
                    if invader.getAction() == MOVE and invader.getAuthor() != cmd.getAuthor():
                        if supported_cmd.getTargetLocation() != invader.getCurrentLocation() or \
                           (supported_cmd.getTargetLocation() == invader.getCurrentLocation() and count_support(supported_cmd, commands) <= count_support(invader, commands)):
                            rtr[cmd] = turn_to_hold(cmd)
                            break

        return rtr


class DetectRetreats(RuleBase):
    def attempt_resolve(self, commands: list[Command]) -> dict[Command: Command]:
        rtr = dict()
        TargetSort = sort_commands("location", commands)

        for cmd in commands:
            if cmd.getAction() == MOVE or cmd.getCurrentLocation() not in TargetSort:
                continue

            my_support = count_support(cmd, commands)

            for invader in TargetSort[cmd.getCurrentLocation()]:
                if invader.getAction() == MOVE and count_support(invader, commands) > my_support:
                    if cmd.retreat is None:
                        raise RetreatDetected(cmd)

                    rtr[cmd] = Command(cmd.getAuthor(), cmd.getCurrentLocation(), MOVE, cmd.retreat)
                    print("%s is retreating" % cmd)
                    break

        return rtr


class ResolveMoveRetreats(RuleBase):
    def attempt_resolve(self, commands: list[Command]) -> dict[Command: Command]:
        rtr = dict()

        LocSort = sort_commands("unit", commands)
        TargetSort = sort_commands("location", commands)

        for cmd in commands:
            if cmd.getAction() is not MOVE or \
               cmd.getCurrentLocation() not in TargetSort or \
               resolvable_move(cmd, commands):
                continue

            my_support = count_support(cmd, commands)

            for invader in TargetSort[cmd.getCurrentLocation()]:
                if invader.getAction() != MOVE:
                    continue

                their_support = count_support(invader, commands)

                if their_support > my_support or (cmd.getTargetLocation() != invader.getCurrentLocation() and their_support > 1):
                    if cmd.retreat is None:
                        raise RetreatDetected

                    rtr[cmd] = Command(cmd.getAuthor(), cmd.getCurrentLocation(), MOVE, cmd.getRetreatLocation())

        return rtr


class ResolveMove(RuleBase):
    def attempt_resolve(self, commands: list[Command]) -> dict[Command: Command]:
        rtr = dict()
        TargetSort = sort_commands("location", commands)

        for command in commands:
            if command.getAction() != MOVE:
                continue

            if not resolvable_move(command, commands):
                rtr[command] = turn_to_hold(command)

                if command.getCurrentLocation() in TargetSort:
                    for targeter in TargetSort[command.getCurrentLocation()]:
                        if targeter.getAction() == SUPPORT:
                            rtr[targeter] = turn_to_hold(targeter)

        return rtr


rules = [ResolveCutSupport,
         ResolveMoveRetreats,
         ResolveMove,
         DetectRetreats]


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

    ####################################################################################################################
    ## Checking each command against the map and the state to see if the list of commands could be rendered           ##
    ####################################################################################################################
    def check_commands(self, commands: list):
        checkedlocations = []

        LocSort = sort_commands("unit", commands)

        if len(commands) != len(self.state.getAllUnits()):
            raise CommandConflict("Mismatch: %i commands and %i units" % (len(commands), len(self.state.getAllUnits())))

        for command in commands:
            command.validate()

            country = self.state.getCountry(command.getAuthor())  # What I really want is the country object
            province = getLocation(command.getCurrentLocation())

            if command.getCurrentLocation() in checkedlocations:
                raise CommandConflict("More than one command for the unit at %s" % command.getCurrentLocation())

            if command.getCurrentLocation() not in country.units:
                raise CommandConflict("No unit at that location")

            if command.getAction() == HOLD:
                continue

            if command.getAction() == SUPPORT:
                if command.getTargetLocation() not in LocSort:
                    continue

                supportedcommand = LocSort[command.getTargetLocation()][0]

                if supportedcommand.getTargetLocation() not in province.border and supportedcommand.getCurrentLocation() not in province.border:
                    raise CommandConflict(
                        "%s does not border %s" % (province, getLocation(supportedcommand.getTargetLocation())))

            if command.action == MOVE:
                if command.getTargetLocation() not in province.border:
                    raise CommandConflict(
                        "%s does not border %s" % (province, getLocation(command.getTargetLocation())))

                if country.units[command.unit] == UnitEnum.ARMY and getLocation(
                        command.getTargetLocation()).loctype == LocTypeEnum.WATER:
                    raise CommandConflict("Your little men can't swim silly")

                if country.units[command.unit] == UnitEnum.FLEET:
                    if getLocation(command.getTargetLocation()).loctype == LocTypeEnum.INLAND:
                        raise CommandConflict("The fleet is unable to progress inland")

                    target = getLocation(command.getTargetLocation())

                    if province.loctype == LocTypeEnum.COASTAL and target.loctype == LocTypeEnum.COASTAL:
                        found = False

                        for border in province.border:
                            if getLocation(border).loctype == LocTypeEnum.WATER and border in target.border:
                                found = True
                                break

                        if not found:
                            raise CommandConflict("Can only move to coasts that share a water border")

    def update_state(self, commands: list[Command]):
        if len(commands) == 0:
            return

        self.check_commands(commands)

        for rule in rules:
            for old, fixed in rule(commands):
                commands[commands.index(old)] = fixed

        self.check_commands(commands)

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
