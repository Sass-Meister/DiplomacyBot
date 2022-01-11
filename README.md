# DiplomacyBot
Discord bot to simulate games of diplomacy for up to seven players. Currently still under construction.

state.py - The State Object which keeps track of players units, capitals, and the year and season.

engine.py - Holds the state and processes commands.

map.py - Has the data for the map, constructed with a list of its edges.

discordbot.py - Where each command is processed. This is *the* file that is run.

renderer.py - Receives a state and outputs an image representation of that state.

EnumsAndUtils.py - Where all other ADTs, interfaces, enums, and other small utility commands are kept. 