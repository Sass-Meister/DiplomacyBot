# TODO:__/\\\\\\\\\\\\\\\_______/\\\\\_______/\\\\\\\\\\\\__________/\\\\\____________
# TODO: _\///////\\\/////______/\\\///\\\____\/\\\////////\\\______/\\\///\\\__________
# TODO:  _______\/\\\_________/\\\/__\///\\\__\/\\\______\//\\\___/\\\/__\///\\\________
# TODO:   _______\/\\\________/\\\______\//\\\_\/\\\_______\/\\\__/\\\______\//\\\_______
# TODO:    _______\/\\\_______\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\_______\/\\\__/\\\_
# TODO:     _______\/\\\_______\//\\\______/\\\__\/\\\_______\/\\\_\//\\\______/\\\__\///__
# TODO:      _______\/\\\________\///\\\__/\\\____\/\\\_______/\\\___\///\\\__/\\\__________
# TODO:       _______\/\\\__________\///\\\\\/_____\/\\\\\\\\\\\\/______\///\\\\\/______/\\\_
# TODO:        _______\///_____________\/////_______\////////////__________\/////_______\///__

# update_state

# Update capitals needs to be rewritten to not give claim to the same capital to multiple countries. This could also be
# solved differently by using the old state to know what capitals counties claim beyond where their current units lie.

# TODO:_____/\\\______________________________________________________________________________/\\\____
# TODO: ___/\\\\\\\__________________________________________________________________________/\\\\\\\__
# TODO:  __/\\\\\\\\\________________________________________________________________________/\\\\\\\\\_
# TODO:   _\//\\\\\\\_________/\\\\\\\\\\\________________________________/\\\\\\\\\\\_______\//\\\\\\\__
# TODO:    __\//\\\\\_________\///////////________________________________\///////////_________\//\\\\\___
# TODO:     ___\//\\\____________________________________________________________________________\//\\\____
# TODO:      ____\///______________________________________________________________________________\///_____
# TODO:       _____/\\\_____/\\\____________________________________________________________/\\\_____/\\\____
# TODO:        ____\///_____\///____________________________________________________________\///_____\///_____

from EnumsAndUtils import *
from map import Map


# Keeps the state of the game in order
class State:

    # startpos of a dict of dicts where provided with a CountryEnum and LocEnum (in that order) a UnitEnum will be stored
    # there.
    def __init__(self, startpos: dict[CountryEnum, dict[LocEnum, UnitEnum]]):
        map = Map()
        state = dict()

        for country in startpos:
            state[country] = Country(country)

            for province in startpos[country]:
                state[country].units[province] = startpos[country][province]

                if map.getLocation(province).iscapital:
                    state[country].capitals.append(province)

        self.map = map
        self.state = state

        self.verify_state()

    # Takes capitals from an old state and adds them to the current state. Used to persist capitals after each spring.
    def update_capitals(self, oldstate):
        oldstate = oldstate.state

        for country in oldstate:
            if country not in self.state:
                self.state[country] = Country(country)

            for province in oldstate[country].capitals:
                if province not in self.state[country].capitals:
                    self.state[country].capitals.append(province)

    def verify_state(self):
        unitcnt = 0
        claimedcapitals = []
        claimedunitlocations = []

        for country in self.state.values():
            for capital in country.capitals:
                if capital in claimedcapitals:
                    raise InvariantError("Conflicting capital claims: %s" % capital)

                claimedcapitals.append(capital)

            for location, unit in country.units.items():
                if location in claimedunitlocations:
                    raise InvariantError("Conflicting unit location claims: %s" % location)

                claimedunitlocations.append(location)

                if self.map.getLocation(location).loctype == LocTypeEnum.INLAND and unit == UnitEnum.FLEET:
                    raise InvariantError("Found a Fleet in %s" % location)

                if self.map.getLocation(location).loctype == LocTypeEnum.WATER and unit == UnitEnum.ARMY:
                    raise InvariantError("Found an Army in %s" % location)

                unitcnt = unitcnt + 1

        if unitcnt > 34:
            raise Exception("Too many units")

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False

        if self is other:
            return True

        if len(self.state) != len(other.state):
            return False

        for country in self.state:
            if country not in other.state or self.state[country] != other.state[country]:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    # Returns the country object for a given country enum
    def getCountry(self, country: CountryEnum) -> Country:
        return self.state[country] if country in self.state else None

    # Returns a dictionary with k/v pairs of the province and unit type respectivly
    # Who belongs to which state is not included
    def getAllUnits(self):
        rtr = dict()

        for country in self.state:
            rtr.update(self.state[country].units)

        return rtr

    def getUnit(self, loc: LocEnum) -> UnitEnum:
        for country in self.state:
            if loc in self.state[country].units:
                return self.state[country].units[loc]

        return None
