# TODO:__/\\\\\\\\\\\\\\\_______/\\\\\_______/\\\\\\\\\\\\__________/\\\\\____________
# TODO: _\///////\\\/////______/\\\///\\\____\/\\\////////\\\______/\\\///\\\__________
# TODO:  _______\/\\\_________/\\\/__\///\\\__\/\\\______\//\\\___/\\\/__\///\\\________
# TODO:   _______\/\\\________/\\\______\//\\\_\/\\\_______\/\\\__/\\\______\//\\\_______
# TODO:    _______\/\\\_______\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\_______\/\\\__/\\\_
# TODO:     _______\/\\\_______\//\\\______/\\\__\/\\\_______\/\\\_\//\\\______/\\\__\///__
# TODO:      _______\/\\\________\///\\\__/\\\____\/\\\_______/\\\___\///\\\__/\\\__________
# TODO:       _______\/\\\__________\///\\\\\/_____\/\\\\\\\\\\\\/______\///\\\\\/______/\\\_
# TODO:        _______\///_____________\/////_______\////////////__________\/////_______\///__

# Write this file

# TODO:__/\\\\\\____________________/\\\\\\__/\\\\\\____________________/\\\\\\__/\\\\\\____________________/\\\\\\
# TODO: _\/\\\//____________________\////\\\_\/\\\//____________________\////\\\_\/\\\//____________________\////\\\
# TODO:  _\/\\\_________________________\/\\\_\/\\\_________________________\/\\\_\/\\\_________________________\/\\\
# TODO:   _\/\\\_________________________\/\\\_\/\\\_________________________\/\\\_\/\\\_________________________\/\\\
# TODO:    _\/\\\_________________________\/\\\_\/\\\_________________________\/\\\_\/\\\_________________________\/\\\
# TODO:     _\/\\\_________________________\/\\\_\/\\\_________________________\/\\\_\/\\\_________________________\/\\\
# TODO:      _\/\\\_________________________\/\\\_\/\\\_________________________\/\\\_\/\\\_________________________\/\\
# TODO:       _\/\\\\\\__/\\\\\\\\\\\\\\\__/\\\\\\_\/\\\\\\__/\\\\\\\\\\\\\\\__/\\\\\\_\/\\\\\\__/\\\\\\\\\\\\\\\__/\\\\
# TODO:        _\//////__\///////////////__\//////__\//////__\///////////////__\//////__\//////__\///////////////__\////

from EnumsAndUtils import *
import discord
from discord.ext import commands
from engine import Engine
from map import getLocation
import random
import os

keyfile = "botkey.txt"
rebuildfile = "rebuild.txt"

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description)

bot.engine = None
bot.players = dict()
bot.tmpcmd = dict()
bot.lockedcmd = dict()
bot.startchannel = 0

if os.path.isfile(rebuildfile):
    print("Rebuilding")

    with open(rebuildfile, 'r') as f:
        bot.startchannel = int(clense(f.readline()))

        print("Rebuilt startchannel: %i" % bot.startchannel)

        for line in f:
            if '$' in line:
                break

            line = clense(line)

            id, country = line.split(",")

            bot.players[id] = CountryEnum[country.upper()]

            print("%s is playing %s" % (id, country))

        bot.engine = Engine(len(bot.players))

        print("Constructed base engine")

        cmdtypes = [CountryEnum, LocEnum, ActionEnum, LocEnum, LocEnum, LocEnum]
        commands = []

        for line in f:
            line = clense(line)

            if '$' in line:
                print("Running Commands")
                bot.engine.update_state(commands)
                commands = []
                continue

            cmddata = line.split(',')

            for i in range(len(cmddata)):
                if "None" == cmddata[i]:
                    cmddata[i] = None

                else:
                    cmddata[i] = cmdtypes[i][cmddata[i].upper().replace("-", "_")]

            cmd = Command(cmddata[0], cmddata[1], cmddata[2], cmddata[3], cmddata[4], cmddata[5])

            commands.append(cmd)

            print("Loaded Command: %s" % str(cmd))


def isPlayerID(s: str) -> bool:
    if s[0:3] != "<@!":
        return False

    if s[-1] != ">":
        return False

    if len(s[4:-1]) != 17:
        return False

    try:
        int(s[4:-1])

    except ValueError:
        return False

    return True


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Sucking and fucking'))
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def test(ctx, player):
    print(player)

    id = int(player[3:-1])

    u = await bot.fetch_user(id)

    print(u)


@bot.command()
async def start(ctx, *players):
    if ctx.channel.type != discord.ChannelType.text:
        return

    if bot.engine is not None:
        await ctx.send("The game has already started!")
        return

    if len(players) > 7:
        await ctx.send("Max number of players is 7")
        return

    if len(players) == 0:
        await ctx.send("Must have at least 1 player")
        return

    for player in players:
        if not isPlayerID(player):
            await ctx.send('Parameters must only be players (invalid: "%s")' % player)
            return

    if len(players) != len(set(players)):
        await ctx.send("Cannot have duplicate players")
        return

    bot.engine = Engine(len(players))
    countries = list(bot.engine.getState().state.keys())
    random.shuffle(countries)

    await ctx.send("Game Started!")

    for id in players:
        bot.players[id[3:-1]] = countries.pop()
        await ctx.send("%s is playing the role of %s" % (id, bot.players[id[3:-1]]))

    bot.startchannel = ctx.channel.id

    with open(rebuildfile, 'w') as f:
        f.write("%i\n" % ctx.channel.id)

        for id in bot.players:
            f.write("%s,%s\n" % (id, bot.players[id]))

        f.write("$\n")

    print("Started the game")


@bot.command()
async def state(ctx, country=None):
    if bot.engine is None:
        await ctx.send("Game hasn't started yet")
        return

    if country is not None:
        try:
            key = CountryEnum[country.upper()]

        except KeyError:  # Enums throw keyerrors but don't support in? where am i?
            await ctx.send("Invalid Country")
            return

        rtr = ".\n%s has:\n" % key
        country = bot.engine.getState().getCountry(key)

        if country is None:
            await ctx.send("Invalid Country")
            return

        for loc in country.units:
            rtr = rtr + "\t%s in %s\n" % (country.units[loc], getLocation(loc))

        await ctx.send(rtr)

    else:
        await ctx.send('.\n' + str(bot.engine.getState()))


@bot.command()
async def command(ctx, *commands):
    if ctx.channel.type != discord.ChannelType.private:
        return

    if bot.engine is None:
        await ctx.send("The game hasn't started")
        return

    author = bot.players[ctx.author.mention[2:-1]]
    commands = list(commands)
    toprocess = []

    cmdtypes = [LocEnum, ActionEnum, LocEnum, LocEnum]

    while len(commands) > 0:
        cmdvalues = []

        for cmdtype in cmdtypes:
            try:
                value = commands.pop(0)
                cmdvalues.append(cmdtype[value.upper().replace('-', '_')])

            except (KeyError, IndexError) as e:
                error = "Error processing "

                if len(cmdvalues) == 0:
                    error = error + "%ith command: " % len(toprocess)

                else:
                    error = error + "command at %s: " % cmdvalues[0]

                if type(e) == IndexError:
                    error = error + "Not enough arguments"

                elif type(e) == KeyError:
                    error = error + 'Unknown %s: "%s"' % (cmdtype, value)

                else:
                    error = error + "fucked up"

                await ctx.send(error)
                return

            if len(cmdvalues) > 1:
                if cmdvalues[1] == ActionEnum.HOLD:
                    break

                elif cmdvalues[1] == ActionEnum.MOVE and len(cmdvalues) > 2:
                    break

                elif cmdvalues[1] == ActionEnum.SUPPORT and len(cmdvalues) > 2:
                    break

                elif cmdvalues[1] == ActionEnum.CONVOY and len(cmdvalues) > 3:
                    break

        if cmdvalues[1] == ActionEnum.HOLD:
            toprocess.append(Command(author, cmdvalues[0], cmdvalues[1]))

        elif cmdvalues[1] in [ActionEnum.MOVE, ActionEnum.SUPPORT]:
            toprocess.append(Command(author, cmdvalues[0], cmdvalues[1], cmdvalues[2]))

        else:
            toprocess.append(Command(author, cmdvalues[0], cmdvalues[1], cmdvalues[2], cmdvalues[3]))

    try:
        bot.engine.check_commands(toprocess, author)

    except CommandConflict as e:
        await ctx.send("Error proceesing commands: {0}".format(e))
        return

    for cmd in toprocess:
        await ctx.send("Received: %s\n" % cmd)

    bot.tmpcmd[author] = toprocess

    await ctx.send("If these commands look right, type !lock to lock them in to be processed when everyone else has also done so")


async def _runcommands():
    print("Running commands")

    ch = await bot.fetch_channel(bot.startchannel)
    await ch.send("Running Commands")

    commands = []

    for cmdlist in bot.lockedcmd.values():
        for cmd in cmdlist:
            commands.append(cmd)

    bot.engine.update_state(commands.copy())

    with open(rebuildfile, 'a') as f:
        for cmd in commands:
            f.write("%s,%s,%s,%s,%s,%s\n" % (cmd.author, cmd.unit, cmd.action, cmd.location, cmd.dropoff, cmd.retreat))

        f.write("$\n")

    await ch.send("State Updated")


@bot.command()
async def lock(ctx):
    if ctx.channel.type != discord.ChannelType.private:
        return

    if bot.engine is None:
        await ctx.send("The game hasn't started")
        return

    country = bot.players[ctx.author.mention[2:-1]]

    if country not in bot.tmpcmd:
        await ctx.send("Nothing to lock in")
        return

    bot.lockedcmd[country] = bot.tmpcmd[country]
    del bot.tmpcmd[country]

    await ctx.send("Locked and loaded")
    print("%s has locked in commands" % ctx.author)

    if identical_lists(list(bot.lockedcmd.keys()), list(bot.players.values())):
        await _runcommands()


with open(keyfile, 'r') as f:
    key = clense(f.read())

print("Starting Server")

bot.run(key, bot=True, reconnect=True)
