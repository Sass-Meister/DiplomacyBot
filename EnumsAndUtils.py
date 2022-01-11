# TODO:__/\\\\\\\\\\\\\\\_______/\\\\\_______/\\\\\\\\\\\\__________/\\\\\____________
# TODO: _\///////\\\/////______/\\\///\\\____\/\\\////////\\\______/\\\///\\\__________
# TODO:  _______\/\\\_________/\\\/__\///\\\__\/\\\______\//\\\___/\\\/__\///\\\________
# TODO:   _______\/\\\________/\\\______\//\\\_\/\\\_______\/\\\__/\\\______\//\\\_______
# TODO:    _______\/\\\_______\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\_______\/\\\__/\\\_
# TODO:     _______\/\\\_______\//\\\______/\\\__\/\\\_______\/\\\_\//\\\______/\\\__\///__
# TODO:      _______\/\\\________\///\\\__/\\\____\/\\\_______/\\\___\///\\\__/\\\__________
# TODO:       _______\/\\\__________\///\\\\\/_____\/\\\\\\\\\\\\/______\///\\\\\/______/\\\_
# TODO:        _______\///_____________\/////_______\////////////__________\/////_______\///__

# This should probably be separate files
# More setters and getters for ADTs
# More __eq__'s

# Double dictionaries are used a lot in this program and maybe an ADT could be created to better use them. The two common
# uses are relatively awkward. Firstly accessing: the ability to access the inner dict w/o a key to the outer dict would
# make access more convenient. Either returning the only item if one can be found on the 2nd layer or an array if more
# than one could be found. Secondly, iteration: the for loops look awkward, if something better (returning a tuple? like
# iterating though a truth table?) could be created, iteration might be clearer. I don't particularly find construction
# to be too bad but if something better could be thought up.

# Add a field for command to serve as a retreat location. This wouldn't be required to be filled out until a retreat is detected

# TODO:____/\\\________/\\\__/\\\__________________/\\\________/\\\__/\\\__________________/\\\________/\\\_
# TODO: ___/\\/\\_____/\\\/__\///\\\_______________/\\/\\_____/\\\/__\///\\\_______________/\\/\\_____/\\\/__
# TODO:  __\//\\\____/\\\/______\///\\\____________\//\\\____/\\\/______\///\\\____________\//\\\____/\\\/____
# TODO:   ___\///___/\\\/__________\///\\\___________\///___/\\\/__________\///\\\___________\///___/\\\/______
# TODO:    ________/\\\/______________\///\\\______________/\\\/______________\///\\\______________/\\\/________
# TODO:     ______/\\\/___/\\\___________\///\\\__________/\\\/___/\\\___________\///\\\__________/\\\/___/\\\___
# TODO:      ____/\\\/____/\\/\\____________\///\\\______/\\\/____/\\/\\____________\///\\\______/\\\/____/\\/\\__
# TODO:       __/\\\/_____\//\\\_______________\///\\\__/\\\/_____\//\\\_______________\///\\\__/\\\/_____\//\\\___
# TODO:        _\///________\///__________________\///__\///________\///__________________\///__\///________\///___

from enum import Enum


# __/\\\\\\\\\\\\\\\____/\\\\\\\\\________/\\\\\\\\\___________/\\\\\_________/\\\\\\\\\_________/\\\\\\\\\\\_________
#  _\/\\\///////////___/\\\///////\\\____/\\\///////\\\_______/\\\///\\\_____/\\\///////\\\_____/\\\/////////\\\_______
#   _\/\\\_____________\/\\\_____\/\\\___\/\\\_____\/\\\_____/\\\/__\///\\\__\/\\\_____\/\\\____\//\\\______\///________
#    _\/\\\\\\\\\\\_____\/\\\\\\\\\\\/____\/\\\\\\\\\\\/_____/\\\______\//\\\_\/\\\\\\\\\\\/______\////\\\_______________
#     _\/\\\///////______\/\\\//////\\\____\/\\\//////\\\____\/\\\_______\/\\\_\/\\\//////\\\_________\////\\\_______/\\\_
#      _\/\\\_____________\/\\\____\//\\\___\/\\\____\//\\\___\//\\\______/\\\__\/\\\____\//\\\___________\////\\\___\///__
#       _\/\\\_____________\/\\\_____\//\\\__\/\\\_____\//\\\___\///\\\__/\\\____\/\\\_____\//\\\___/\\\______\//\\\________
#        _\/\\\\\\\\\\\\\\\_\/\\\______\//\\\_\/\\\______\//\\\____\///\\\\\/_____\/\\\______\//\\\_\///\\\\\\\\\\\/____/\\\_
#         _\///////////////__\///________\///__\///________\///_______\/////_______\///________\///____\///////////_____\///__


class InvariantError(Exception):
    pass


class CommandConflict(Exception):
    pass


class RuleCheckException(Exception):
    pass


class RetreatDetected(Exception):
    def __init__(self, command):
        self.command = command

    def getCommand(self):
        return self.command


# __/\\\\\\\\\\\\\\\__/\\\\\_____/\\\__/\\\________/\\\__/\\\\____________/\\\\_____/\\\\\\\\\\\_________
#  _\/\\\///////////__\/\\\\\\___\/\\\_\/\\\_______\/\\\_\/\\\\\\________/\\\\\\___/\\\/////////\\\_______
#   _\/\\\_____________\/\\\/\\\__\/\\\_\/\\\_______\/\\\_\/\\\//\\\____/\\\//\\\__\//\\\______\///________
#    _\/\\\\\\\\\\\_____\/\\\//\\\_\/\\\_\/\\\_______\/\\\_\/\\\\///\\\/\\\/_\/\\\___\////\\\_______________
#     _\/\\\///////______\/\\\\//\\\\/\\\_\/\\\_______\/\\\_\/\\\__\///\\\/___\/\\\______\////\\\_______/\\\_
#      _\/\\\_____________\/\\\_\//\\\/\\\_\/\\\_______\/\\\_\/\\\____\///_____\/\\\_________\////\\\___\///__
#       _\/\\\_____________\/\\\__\//\\\\\\_\//\\\______/\\\__\/\\\_____________\/\\\__/\\\______\//\\\________
#        _\/\\\\\\\\\\\\\\\_\/\\\___\//\\\\\__\///\\\\\\\\\/___\/\\\_____________\/\\\_\///\\\\\\\\\\\/____/\\\_
#         _\///////////////__\///_____\/////_____\/////////_____\///______________\///____\///////////_____\///__


class LocEnum(Enum):
    BOH = 0
    BUD = 1
    GAL = 2
    TRI = 3
    TYR = 4
    VIE = 5
    CLY = 6
    EDI = 7
    LVP = 8
    LON = 9
    WAL = 10
    YOR = 11
    BRE = 12
    BUR = 13
    GAS = 14
    MAR = 15
    PAR = 16
    PIC = 17
    BER = 18
    KIE = 19
    MUN = 20
    PRU = 21
    RUH = 22
    SIL = 23
    APU = 24
    NAP = 25
    PIE = 26
    ROM = 27
    TUS = 28
    VEN = 29
    FIN = 30
    LVN = 31
    MOS = 32
    SEV = 33
    STP = 34
    UKR = 35
    WAR = 36
    ANK = 37
    ARM = 38
    CON = 39
    SMY = 40
    SYR = 41
    ALB = 42
    BEL = 43
    BUL = 44
    DEN = 45
    GRE = 46
    HOL = 47
    NWY = 48
    NAF = 49
    POR = 50
    RUM = 51
    SER = 52
    SPA = 53
    SWE = 54
    TUN = 55
    ADR = 56
    AEG = 57
    BAL = 58
    BAR = 59
    BLA = 60
    EAS = 61
    ENG = 62
    BOT = 63
    GOL = 64
    HEL = 65
    ION = 66
    IRI = 67
    MID = 68
    NAT = 69
    NTH = 70
    NRG = 71
    SKA = 72
    TYN = 73
    WES = 74
    SPA_NC = 75
    SPA_SC = 76
    STP_NC = 77
    STP_SC = 78
    BUL_EC = 79
    BUL_SC = 80

    # If a class that overrides __eq__() needs to retain the implementation of __hash__() from a parent class, the
    # interpreter must be told this explicitly by setting __hash__ = <ParentClass>.__hash__.
    # https://docs.python.org/3/reference/datamodel.html
    __hash__ = Enum.__hash__

    def __str__(self):
        return str(self.name).upper().replace('_', '-')

    # How are the Specific Movement Clarifications (see the rules) implemented? Part of the magic is in this function.
    # The issue is that different map locations have different exact locations for different units. STP, BUL, and SPA
    # have separate coasts with different borders for Fleets. Counting sub-locations (XXX_XC) as the same as their parent
    # location allows for more useful comparisons. If you want to test with a little more accuracy, use is to
    # distinguish all locations and sub-locations.
    def __eq__(self, other):
        if not isinstance(other, LocEnum):
            if other is None:
                return False

            raise Exception(f"Fail Fast: {other} ({type(other)}) was compared against a {type(self)}")

        if self is other:
            return True

        for locgroup in ({LocEnum.STP, LocEnum.STP_SC, LocEnum.STP_NC},
                         {LocEnum.BUL, LocEnum.BUL_EC, LocEnum.BUL_SC},
                         {LocEnum.SPA, LocEnum.SPA_SC, LocEnum.SPA_NC}):
            if {self, other}.issubset(locgroup):
                return True

        return False


class UnitEnum(Enum):
    ARMY = 0
    FLEET = 1

    def __str__(self):
        return str(self.name).capitalize()


class CountryEnum(Enum):
    AUSTRIA = 0
    ENGLAND = 1
    FRANCE = 2
    GERMANY = 3
    ITALY = 4
    RUSSIA = 5
    TURKEY = 6

    def __str__(self):
        return str(self.name).capitalize()


class LocTypeEnum(Enum):
    INLAND = 0
    COASTAL = 1
    WATER = 2

    def __str__(self):
        return str(self.name).capitalize()


class ActionEnum(Enum):
    HOLD = 0
    MOVE = 1
    SUPPORT = 2
    CONVOY = 3

    def __str__(self):
        return str(self.name).capitalize()


class SeasonEnum(Enum):
    SPRING = 0
    FALL = 1

    def __str__(self):
        return str(self.name).capitalize()


class GainLoseEnum(Enum):
    GAIN = 0
    LOSE = 1


# _____/\\\\\\\\\_____/\\\\\\\\\\\\_____/\\\\\\\\\\\\\\\_____/\\\\\\\\\\\_________
#  ___/\\\\\\\\\\\\\__\/\\\////////\\\__\///////\\\/////____/\\\/////////\\\_______
#   __/\\\/////////\\\_\/\\\______\//\\\_______\/\\\________\//\\\______\///________
#    _\/\\\_______\/\\\_\/\\\_______\/\\\_______\/\\\_________\////\\\_______________
#     _\/\\\\\\\\\\\\\\\_\/\\\_______\/\\\_______\/\\\____________\////\\\_______/\\\_
#      _\/\\\/////////\\\_\/\\\_______\/\\\_______\/\\\_______________\////\\\___\///__
#       _\/\\\_______\/\\\_\/\\\_______/\\\________\/\\\________/\\\______\//\\\________
#        _\/\\\_______\/\\\_\/\\\\\\\\\\\\/_________\/\\\_______\///\\\\\\\\\\\/____/\\\_
#         _\///________\///__\////////////___________\///__________\///////////_____\///__


class Country:
    def __init__(self, country: CountryEnum, name: str = None, units: dict[LocEnum: UnitEnum] = None, capitals: list[LocEnum] = None,
                 bot: bool = False):
        self.country = country
        self.name = name if name is not None else str(country)
        self.units = units if units is not None else dict()
        self.capitals = capitals if capitals is not None else list()
        self.bot = bot

    def __eq__(self, other):
        if not isinstance(other, Country):
            if other is None:
                return False

            raise Exception(f"Fail Fast: {other} ({type(other)}) was compared against a {type(self)}")

        if self is other:
            return True

        for attr in ["country", "name", "bot"]:
            if hasattr(other, attr) and not getattr(self, attr) == getattr(other, attr):
                return False

        for attr in ["units", "capitals"]:
            if not hasattr(other, attr):
                return False

        if len(self.units) != len(other.units):
            return False

        for province in self.units:
            if province in other.units and self.units[province] != other.units[province]:
                return False

        if len(self.capitals) != len(other.capitals):
            return False

        for capital in self.capitals:
            if capital not in other.capitals:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class Location:
    def __init__(self, name: str, location: LocEnum, loctype: LocTypeEnum, iscapital: bool = False):
        self.name = name
        self.location = location
        self.loctype = loctype
        self.iscapital = iscapital
        self.border = list()

    def __str__(self):
        return "%s (%s)" % (self.name, self.location)

    def addBorder(self, loc: LocEnum):
        if loc not in self.border:
            self.border.append(loc)

    def getBorders(self):
        return self.border


class Command:
    def __init__(self, author: CountryEnum, unit: LocEnum, action: ActionEnum,
                 location: LocEnum = None, dropoff: LocEnum = None, retreat: LocEnum = None):
        self.unit = unit  # Used in every command
        self.action = action  # Used in every command
        self.author = author  # Who wrote the command?
        self.location = location  # Used for move, convoy, and support
        self.dropoff = dropoff  # Used for just convoy
        self.retreat = retreat  # Where to go when retreating

        self.validate()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Command):
            return False

        for attr in ["unit", "action", "author", "location", "dropoff", "retreat"]:
            if hasattr(other, attr) and not getattr(self, attr) == getattr(other, attr):
                return False

        return True

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def getCurrentLocation(self) -> LocEnum:
        return self.unit

    def getAction(self) -> ActionEnum:
        return self.action

    def getAuthor(self) -> CountryEnum:
        return self.author

    def getTargetLocation(self) -> LocEnum:
        return self.location

    def getConvoyDropoff(self) -> LocEnum:
        return self.dropoff

    def getRetreatLocation(self):
        return self.retreat

    def __str__(self):
        rtr = "%s %s %s" % (self.author, self.unit, self.action)

        if self.location is not None:
            rtr = "%s %s" % (rtr, self.location)

            if self.dropoff is not None:
                rtr = "%s to %s" % (rtr, self.dropoff)

        return rtr

    def __hash__(self):
        return hash(str(self))

    def copy(self):
        return Command(self.author, self.unit, self.action, self.location, self.dropoff, self.retreat)

    # Takes in a string and fills out self with the data inside
    def load(self, s: str):
        pass

    def validate(self):
        if self.unit is None:
            raise InvariantError("Unit cannot be None")

        if type(self.unit) != LocEnum:
            raise InvariantError("Bad unit type")

        if self.action is None:
            raise InvariantError("Action cannot be None")

        if type(self.action) != ActionEnum:
            raise InvariantError("Bad action type")

        if self.action != ActionEnum.HOLD:
            if self.location is None:
                raise InvariantError("Location cannot be None")

            if type(self.location) != LocEnum:
                raise InvariantError("Bad Location type")

            if self.action == ActionEnum.CONVOY:
                if self.dropoff is None:
                    raise InvariantError("Unit2 cannot be None")

                if type(self.dropoff) != LocEnum:
                    raise InvariantError("Bad Unit2 type")

        if self.retreat is not None and type(self.retreat) != LocEnum:
            raise InvariantError("Retreat is of the wrong type")


# __/\\\________/\\\__/\\\\\\\\\\\\\\\__/\\\\\\\\\\\__/\\\_________________/\\\\\\\\\\\_________
#  _\/\\\_______\/\\\_\///////\\\/////__\/////\\\///__\/\\\_______________/\\\/////////\\\_______
#   _\/\\\_______\/\\\_______\/\\\___________\/\\\_____\/\\\______________\//\\\______\///________
#    _\/\\\_______\/\\\_______\/\\\___________\/\\\_____\/\\\_______________\////\\\_______________
#     _\/\\\_______\/\\\_______\/\\\___________\/\\\_____\/\\\__________________\////\\\_______/\\\_
#      _\/\\\_______\/\\\_______\/\\\___________\/\\\_____\/\\\_____________________\////\\\___\///__
#       _\//\\\______/\\\________\/\\\___________\/\\\_____\/\\\______________/\\\______\//\\\________
#        __\///\\\\\\\\\/_________\/\\\________/\\\\\\\\\\\_\/\\\\\\\\\\\\\\\_\///\\\\\\\\\\\/____/\\\_
#         ____\/////////___________\///________\///////////__\///////////////____\///////////_____\///__


def cleanse(s: str) -> str:
    for c in [' ', '\t', '\n']:
        s = s.replace(c, '')

    return s


def identical_lists(l1: list, l2: list) -> bool:
    if len(l1) != len(l2):
        return False

    for item in l1:
        if item not in l2:
            return False

    return True


def count_support(audit, commandlist: list[Command]) -> int:
    rtr = 0

    for command in commandlist:
        if audit is not command and command.getAction() == ActionEnum.SUPPORT and command.getTargetLocation() == audit.getCurrentLocation():
            rtr = rtr + 1

    return rtr


# Sorts a list of commands by the given attribute. Useful for traversing all the commands like a map. All commands with
# the same value for the given attribute are put into the same list. Returned is a dictionary with LocEnums for keys and
# for values lists of Commands with that given value for that attribute. Most popular is "unit" and "location" to sort
# commands into what unit they instruct and what unit that is being targeted respectively.
def sort_commands(sort: str, commands: list[Command]) -> dict[LocEnum: list[Command]]:
    if len(commands) == 0:
        return dict()

    rtr = dict()

    for command in commands:
        if not hasattr(command, sort):
            raise Exception("Invalid Sort")

        key = getattr(command, sort)

        if key not in rtr:
            rtr[key] = list()

        rtr[key].append(command)

    return rtr


def turn_to_hold(command: Command) -> Command:
    return Command(command.getAuthor(), command.getCurrentLocation(), ActionEnum.HOLD, retreat=command.retreat)


def copy_commands(commands: list[Command]) -> list[Command]:
    return [command.copy() for command in commands]


# __/\\\\\\\\\\\__/\\\\\_____/\\\__/\\\\\\\\\\\\\\\__/\\\\\\\\\\\\\\\____/\\\\\\\\\______/\\\\\\\\\\\\\\\_____/\\\\\\\\\___________/\\\\\\\\\__/\\\\\\\\\\\\\\\_____/\\\\\\\\\\\_________
#  _\/////\\\///__\/\\\\\\___\/\\\_\///////\\\/////__\/\\\///////////___/\\\///////\\\___\/\\\///////////____/\\\\\\\\\\\\\______/\\\////////__\/\\\///////////____/\\\/////////\\\_______
#   _____\/\\\_____\/\\\/\\\__\/\\\_______\/\\\_______\/\\\_____________\/\\\_____\/\\\___\/\\\______________/\\\/////////\\\___/\\\/___________\/\\\______________\//\\\______\///________
#    _____\/\\\_____\/\\\//\\\_\/\\\_______\/\\\_______\/\\\\\\\\\\\_____\/\\\\\\\\\\\/____\/\\\\\\\\\\\_____\/\\\_______\/\\\__/\\\_____________\/\\\\\\\\\\\_______\////\\\_______________
#     _____\/\\\_____\/\\\\//\\\\/\\\_______\/\\\_______\/\\\///////______\/\\\//////\\\____\/\\\///////______\/\\\\\\\\\\\\\\\_\/\\\_____________\/\\\///////___________\////\\\_______/\\\_
#      _____\/\\\_____\/\\\_\//\\\/\\\_______\/\\\_______\/\\\_____________\/\\\____\//\\\___\/\\\_____________\/\\\/////////\\\_\//\\\____________\/\\\_____________________\////\\\___\///__
#       _____\/\\\_____\/\\\__\//\\\\\\_______\/\\\_______\/\\\_____________\/\\\_____\//\\\__\/\\\_____________\/\\\_______\/\\\__\///\\\__________\/\\\______________/\\\______\//\\\________
#        __/\\\\\\\\\\\_\/\\\___\//\\\\\_______\/\\\_______\/\\\\\\\\\\\\\\\_\/\\\______\//\\\_\/\\\_____________\/\\\_______\/\\\____\////\\\\\\\\\_\/\\\\\\\\\\\\\\\_\///\\\\\\\\\\\/____/\\\_
#         _\///////////__\///_____\/////________\///________\///////////////__\///________\///__\///______________\///________\///________\/////////__\///////////////____\///////////_____\///__

# What does a RuleBase look like under the hood? All RuleBases are iterators who iterate through tuples with
# (the old Command, what to replace it with). All you must do to implement a RuleBase is write the attempt_resolve
# function. This function takes a list of commands to which you will attempt to resolve situations and reduce from the
# command list Commands that, if passed, would create an illegal game state. This is most often turning MOVEs to assume
# what hase been resolved before it AKA RuleBases are resolved in a set order.
class RuleBase:
    def __init__(self, commands: list[Command]):
        self.commands = commands
        self.fixed = dict()
        self.fix_it = None  # fixed_iterator

    def attempt_resolve(self, commands: list[Command]) -> dict[Command: Command]:
        pass

    def __iter__(self):
        self.fixed = self.attempt_resolve(self.commands)
        self.fix_it = iter(self.fixed)

        return self

    def __next__(self) -> (Command, Command):
        next = self.fix_it.__next__()

        return next, self.fixed[next]

    def __str__(self):
        return str(type(self))
