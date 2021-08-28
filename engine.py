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


class SimpleMove(RuleBase):  # literally untested
    def __iter__(self):
        audit = self.audit
        commands = self.commands

        if audit.getAction() != ActionEnum.MOVE:
            return self

        conflict = False

        for command in commands:
            if audit is not command and (audit.getTargetLocation() == command.getCurrentLocation() or (audit.getTargetLocation() == command.getTargetLocation() and command.getAction() == ActionEnum.MOVE)):
                conflict = True
                break

        if not conflict:
            self.fixed = {audit: audit}

        return self


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

            if command.getAction() == ActionEnum.HOLD:
                continue

            if command.getTargetLocation() not in province.border:
                raise CommandConflict("Invalid Location")

            if command.action == ActionEnum.MOVE:
                if country.units[command.unit] == UnitEnum.ARMY and province.loctype == LocTypeEnum.WATER:
                    raise CommandConflict("Your little men can't swim silly")

                if country.units[command.unit] == UnitEnum.FLEET and province.loctype == LocTypeEnum.INLAND:
                    raise CommandConflict("The fleet is unable to progress inland")

    # Working Commands
    # Hold: In
    # Move: Under Construction
    # Support: TBD
    # Convoy: TBD
    def update_state(self, commands: list):
        self.check_commands(commands)

        if len(commands) == 0:
            return

        movers = []
        holders = []

        for command in commands:
            if command.getAction() == ActionEnum.HOLD:
                holders.append(command)

            elif command.getAction() == ActionEnum.MOVE:
                movers.append(command)

        fixed = []

        while len(movers) > 0:
            underreview = movers[0]
            conflict = None

            # Find the unit and its command that conflict with the current one under review
            for command in commands:
                if underreview.getTargetLocation() == command.getCurrentLocation() and command is not underreview:
                    conflict = command
                    break

            if conflict is None:
                fixed.append(movers.pop(0))
                continue

            # Settle conflicts here
            raise Exception("Too stupid to handle conflicts")

        fixed = fixed + holders

        # At this point all commands are now in fixed and are ready to construct a new state

        startpos = dict()  # First construct the new startpos

        for command in fixed:
            if command.getAuthor() not in startpos:
                startpos[command.getAuthor()] = dict()

            if command.getAction() == ActionEnum.MOVE:
                startpos[command.getAuthor()][command.getTargetLocation()] = self.state.getUnit(
                    command.getCurrentLocation())

            else:
                startpos[command.getAuthor()][command.getCurrentLocation()] = self.state.getUnit(
                    command.getCurrentLocation())

        self.state = State(startpos)  # Construct the new state and set it to self
