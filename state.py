# TODO:__/\\\\\\\\\\\\\\\_______/\\\\\_______/\\\\\\\\\\\\__________/\\\\\____________
# TODO: _\///////\\\/////______/\\\///\\\____\/\\\////////\\\______/\\\///\\\__________
# TODO:  _______\/\\\_________/\\\/__\///\\\__\/\\\______\//\\\___/\\\/__\///\\\________
# TODO:   _______\/\\\________/\\\______\//\\\_\/\\\_______\/\\\__/\\\______\//\\\_______
# TODO:    _______\/\\\_______\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\_______\/\\\__/\\\_
# TODO:     _______\/\\\_______\//\\\______/\\\__\/\\\_______\/\\\_\//\\\______/\\\__\///__
# TODO:      _______\/\\\________\///\\\__/\\\____\/\\\_______/\\\___\///\\\__/\\\__________
# TODO:       _______\/\\\__________\///\\\\\/_____\/\\\\\\\\\\\\/______\///\\\\\/______/\\\_
# TODO:        _______\///_____________\/////_______\////////////__________\/////_______\///__

# run_commands

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
from map import getLocation


# Keeps the state of the game in order
class State:

    # startpos of a dict of dicts where provided with a CountryEnum and LocEnum (in that order) a UnitEnum will be stored
    # there.
    def __init__(self, startpos: dict[CountryEnum, dict[LocEnum, UnitEnum]]):
        state = dict()

        for country in startpos:
            state[country] = Country(country)

            for province in startpos[country]:
                state[country].units[province] = startpos[country][province]

                if getLocation(province).iscapital:
                    state[country].capitals.append(province)

        self.state = state
        self.season = SeasonEnum.SPRING
        self.year = 1901

        self.verify_state()

    def __eq__(self, other) -> bool:
        if not isinstance(other, State):
            if other is not None:
                raise Exception("Fail Fast")

            return False

        if self is other:
            return True

        if len(self.state) != len(other.state):
            return False

        for country in self.state:
            if country not in other.state or self.state[country] != other.state[country]:
                return False

        if self.season != other.season:
            return False

        if self.year != other.year:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        rtr = ""

        for country in self.state:
            rtr = "%s%s has:\n" % (rtr, country)

            for loc in self.state[country].units:
                rtr = "%s\t%s in %s\n" % (rtr, self.state[country].units[loc], getLocation(loc))

        return rtr

    # Returns the country object for a given country enum
    def getCountry(self, country: CountryEnum) -> Country:
        return self.state[country] if country in self.state else None

    # Returns a dictionary with k/v pairs of the province and unit type respectivly
    # Who belongs to which state is not included
    def getAllUnits(self) -> dict[LocEnum: UnitEnum]:
        rtr = dict()

        for country in self.state:
            rtr.update(self.state[country].units)

        return rtr

    def getUnit(self, loc: LocEnum) -> UnitEnum:
        for country in self.state:
            if loc in self.state[country].units:
                return self.state[country].units[loc]

        return None

    # Returns all currently playing countries
    def getCountries(self) -> list[CountryEnum]:
        return list(self.state.keys())

    def getSeason(self):
        return self.season

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

                if getLocation(location).loctype == LocTypeEnum.INLAND and unit == UnitEnum.FLEET:
                    raise InvariantError("Found a Fleet in %s" % location)

                if getLocation(location).loctype == LocTypeEnum.WATER and unit == UnitEnum.ARMY:
                    raise InvariantError("Found an Army in %s" % location)

                unitcnt = unitcnt + 1

        if unitcnt > 34:
            raise InvariantError("Too many units")

    def update_state(self, newpos: dict[CountryEnum, dict[LocEnum, UnitEnum]], increase_year: bool = False):
        newstate = dict()
        claimedcapitals = list()

        # Construct all the new country objects
        for country in newpos:
            newstate[country] = Country(country)

            for province in newpos[country]:
                newstate[country].units[province] = newpos[country][province]

                if getLocation(province).iscapital:
                    newstate[country].capitals.append(province)
                    claimedcapitals.append(province)

        # Preserve the old capitals
        for ckey, country in self.state.items():
            for province in country.capitals:
                if province not in claimedcapitals:
                    newstate[ckey].capitals.append(province)

        if increase_year:
            if self.season == SeasonEnum.FALL:
                self.year = self.year + 1
                self.season = SeasonEnum.SPRING

            else:
                self.season = SeasonEnum.FALL

        self.state = newstate

        self.verify_state()

    # Given a country, returns a tuple of the number of new units that could be placed and where they could go. Used during the gaining and losing units phase.
    def check_gains(self, country: CountryEnum) -> (int, list[LocEnum]):
        country = self.getCountry(country)

        if len(country.units) >= len(country.capitals):
            return 0, []

        capitals = set(country.capitals)
        unit_locations = set(country.units.keys())

        spots = list(capitals.difference(unit_locations))

        gains = len(country.capitals) - len(country.units)

        occupied_capitals = len(capitals.intersection(unit_locations))

        if len(country.capitals) - occupied_capitals < gains:
            gains = len(country.capitals) - occupied_capitals

        return gains, spots

    # Given a country, returns a tuple of the number of the number of units to remove and the locations where they could be removed from. Used during the gaining and losing units phase.--
    def check_losses(self, country: CountryEnum) -> (int, list[LocEnum]):
        country = self.getCountry(country)

        if len(country.units) < len(country.capitals):
            return 0, []

        return len(country.units) - len(country.capitals), country.units.copy()





