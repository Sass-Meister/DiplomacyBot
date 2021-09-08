# TODO:__/\\\\\\\\\\\\\\\_______/\\\\\_______/\\\\\\\\\\\\__________/\\\\\____________
# TODO: _\///////\\\/////______/\\\///\\\____\/\\\////////\\\______/\\\///\\\__________
# TODO:  _______\/\\\_________/\\\/__\///\\\__\/\\\______\//\\\___/\\\/__\///\\\________
# TODO:   _______\/\\\________/\\\______\//\\\_\/\\\_______\/\\\__/\\\______\//\\\_______
# TODO:    _______\/\\\_______\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\_______\/\\\__/\\\_
# TODO:     _______\/\\\_______\//\\\______/\\\__\/\\\_______\/\\\_\//\\\______/\\\__\///__
# TODO:      _______\/\\\________\///\\\__/\\\____\/\\\_______/\\\___\///\\\__/\\\__________
# TODO:       _______\/\\\__________\///\\\\\/_____\/\\\\\\\\\\\\/______\///\\\\\/______/\\\_
# TODO:        _______\///_____________\/////_______\////////////__________\/////_______\///__

# Implement the separate coastlines of BUL, SPA, and StP
# One idea to implement this would go like this, using SPA as an example. Create two LocEnums for the north coast (NC)
# and the south coast (SC). Create the corresponding Locations in the map except SPA becomes INLAND and the NC and SC
# Locations become WATER. These locations would have these classifications to prevent units from being in the wrong spots.
# Ships can only go on the coasts (and never on the land) and armies can never go on the coasts and only on the land.
# This would also require an implementation of __eq__ for LocEnums that would handle comparisons between SPA and its
# coasts (being equal locations). I'm just not sure if this could cause problems somewhere else.

# TODO: _______/\\\\\__/\\\\\___________/\\\\\_______/\\\\\__/\\\\\______/\\\\\___________/\\\\\__/\\\\\_____
# TODO:  _____/\\\///__\////\\\________/\\\///______/\\\///__\////\\\____\////\\\________/\\\///__\////\\\____
# TODO:   ____\//\\\_______/\\\________\//\\\_______\//\\\_______/\\\________/\\\________\//\\\_______/\\\_____
# TODO:    __/\\\\\\_______\//\\\\\\__/\\\\\\______/\\\\\\_______\//\\\\\\___\//\\\\\\__/\\\\\\_______\//\\\\\\_
# TODO:     _\/////\\\_______/\\\///__\/////\\\____\/////\\\_______/\\\///_____/\\\///__\/////\\\_______/\\\///__
# TODO:      _____/\\\_______\//\\\________/\\\_________/\\\_______\//\\\______\//\\\________/\\\_______\//\\\____
# TODO:       ____\///\\\\\__/\\\\\________\///\\\\\____\///\\\\\__/\\\\\______/\\\\\________\///\\\\\__/\\\\\_____
# TODO:        ______\/////__\/////___________\/////_______\/////__\/////______\/////___________\/////__\/////______
from EnumsAndUtils import LocEnum, Location, LocTypeEnum, InvariantError


map = {LocEnum.BOH: Location("Bohemia", LocEnum.BOH, LocTypeEnum.INLAND),
       LocEnum.BUD: Location("Budapest", LocEnum.BUD, LocTypeEnum.INLAND, True),
       LocEnum.GAL: Location("Galicia", LocEnum.GAL, LocTypeEnum.INLAND),
       LocEnum.TRI: Location("Trieste", LocEnum.TRI, LocTypeEnum.COASTAL, True),
       LocEnum.TYR: Location("Tyrolia", LocEnum.TYR, LocTypeEnum.INLAND),
       LocEnum.VIE: Location("Vienna", LocEnum.VIE, LocTypeEnum.INLAND, True),
       LocEnum.CLY: Location("Clyde", LocEnum.CLY, LocTypeEnum.COASTAL),
       LocEnum.EDI: Location("Edinburgh", LocEnum.EDI, LocTypeEnum.COASTAL, True),
       LocEnum.LVP: Location("Liverpool", LocEnum.LVP, LocTypeEnum.COASTAL, True),
       LocEnum.LON: Location("London", LocEnum.LON, LocTypeEnum.COASTAL, True),
       LocEnum.WAL: Location("Wales", LocEnum.WAL, LocTypeEnum.COASTAL),
       LocEnum.YOR: Location("Yorkshire", LocEnum.YOR, LocTypeEnum.COASTAL),
       LocEnum.BRE: Location("Brest", LocEnum.BRE, LocTypeEnum.COASTAL, True),
       LocEnum.BUR: Location("Burgundy", LocEnum.BUR, LocTypeEnum.INLAND),
       LocEnum.GAS: Location("Gascony", LocEnum.GAS, LocTypeEnum.COASTAL),
       LocEnum.MAR: Location("Marseilles", LocEnum.MAR, LocTypeEnum.COASTAL, True),
       LocEnum.PAR: Location("Paris", LocEnum.PAR, LocTypeEnum.INLAND, True),
       LocEnum.PIC: Location("Picardy", LocEnum.PIC, LocTypeEnum.COASTAL),
       LocEnum.BER: Location("Berlin", LocEnum.BER, LocTypeEnum.COASTAL, True),
       LocEnum.KIE: Location("Kiel", LocEnum.KIE, LocTypeEnum.COASTAL, True),
       LocEnum.MUN: Location("Munich", LocEnum.MUN, LocTypeEnum.INLAND, True),
       LocEnum.PRU: Location("Prussia", LocEnum.PRU, LocTypeEnum.COASTAL),
       LocEnum.RUH: Location("Ruhr", LocEnum.RUH, LocTypeEnum.INLAND),
       LocEnum.SIL: Location("Silesia", LocEnum.SIL, LocTypeEnum.INLAND),
       LocEnum.APU: Location("Apulia", LocEnum.APU, LocTypeEnum.COASTAL),
       LocEnum.NAP: Location("Naples", LocEnum.NAP, LocTypeEnum.COASTAL, True),
       LocEnum.PIE: Location("Piedmont", LocEnum.PIE, LocTypeEnum.COASTAL),
       LocEnum.ROM: Location("Rome", LocEnum.ROM, LocTypeEnum.COASTAL, True),
       LocEnum.TUS: Location("Tuscany", LocEnum.TUS, LocTypeEnum.COASTAL),
       LocEnum.VEN: Location("Venice", LocEnum.VEN, LocTypeEnum.COASTAL, True),
       LocEnum.FIN: Location("Finland", LocEnum.FIN, LocTypeEnum.COASTAL),
       LocEnum.LVN: Location("Livonia", LocEnum.LVN, LocTypeEnum.COASTAL),
       LocEnum.MOS: Location("Moscow", LocEnum.MOS, LocTypeEnum.INLAND, True),
       LocEnum.SEV: Location("Sevastopol", LocEnum.SEV, LocTypeEnum.COASTAL, True),
       LocEnum.STP: Location("St. Petersburg", LocEnum.STP, LocTypeEnum.INLAND, True),
       LocEnum.UKR: Location("Ukraine", LocEnum.UKR, LocTypeEnum.INLAND),
       LocEnum.WAR: Location("Warsaw", LocEnum.WAR, LocTypeEnum.INLAND, True),
       LocEnum.ANK: Location("Ankara", LocEnum.ANK, LocTypeEnum.COASTAL, True),
       LocEnum.ARM: Location("Armenia", LocEnum.ARM, LocTypeEnum.COASTAL),
       LocEnum.CON: Location("Constantinople", LocEnum.CON, LocTypeEnum.COASTAL, True),
       LocEnum.SMY: Location("Smyrna", LocEnum.SMY, LocTypeEnum.COASTAL, True),
       LocEnum.SYR: Location("Syria", LocEnum.SYR, LocTypeEnum.COASTAL),
       LocEnum.ALB: Location("Albania", LocEnum.ALB, LocTypeEnum.COASTAL),
       LocEnum.BEL: Location("Belgium", LocEnum.BEL, LocTypeEnum.COASTAL, True),
       LocEnum.BUL: Location("Bulgaria", LocEnum.BUL, LocTypeEnum.COASTAL, True),
       LocEnum.DEN: Location("Denmark", LocEnum.DEN, LocTypeEnum.COASTAL, True),
       LocEnum.GRE: Location("Greece", LocEnum.GRE, LocTypeEnum.COASTAL, True),
       LocEnum.HOL: Location("Holland", LocEnum.HOL, LocTypeEnum.COASTAL, True),
       LocEnum.NWY: Location("Norway", LocEnum.NWY, LocTypeEnum.COASTAL, True),
       LocEnum.NAF: Location("North Africa", LocEnum.NAF, LocTypeEnum.COASTAL),
       LocEnum.POR: Location("Portugal", LocEnum.POR, LocTypeEnum.COASTAL, True),
       LocEnum.RUM: Location("Rumania", LocEnum.RUM, LocTypeEnum.COASTAL, True),
       LocEnum.SER: Location("Serbia", LocEnum.SER, LocTypeEnum.INLAND, True),
       LocEnum.SPA: Location("Spain", LocEnum.SPA, LocTypeEnum.INLAND, True),
       LocEnum.SWE: Location("Sweden", LocEnum.SWE, LocTypeEnum.COASTAL, True),
       LocEnum.TUN: Location("Tunis", LocEnum.TUN, LocTypeEnum.COASTAL, True),
       LocEnum.ADR: Location("Adriatic Sea", LocEnum.ADR, LocTypeEnum.WATER),
       LocEnum.AEG: Location("Aegean Sea", LocEnum.AEG, LocTypeEnum.WATER),
       LocEnum.BAL: Location("Baltic Sea", LocEnum.BAL, LocTypeEnum.WATER),
       LocEnum.BAR: Location("Barents Sea", LocEnum.BAR, LocTypeEnum.WATER),
       LocEnum.BLA: Location("Black Sea", LocEnum.BLA, LocTypeEnum.WATER),
       LocEnum.EAS: Location("Eastern Mediterranean", LocEnum.EAS, LocTypeEnum.WATER),
       LocEnum.ENG: Location("English Channel", LocEnum.ENG, LocTypeEnum.WATER),
       LocEnum.BOT: Location("Gulf of Bothnia", LocEnum.BOT, LocTypeEnum.WATER),
       LocEnum.GOL: Location("Gulf of Lyon", LocEnum.GOL, LocTypeEnum.WATER),
       LocEnum.HEL: Location("Helgoland Bight", LocEnum.HEL, LocTypeEnum.WATER),
       LocEnum.ION: Location("Ionian Sea", LocEnum.ION, LocTypeEnum.WATER),
       LocEnum.IRI: Location("Irish Sea", LocEnum.IRI, LocTypeEnum.WATER),
       LocEnum.MID: Location("Mid-Atlantic Ocean", LocEnum.MID, LocTypeEnum.WATER),
       LocEnum.NAT: Location("North Atlantic Ocean", LocEnum.NAT, LocTypeEnum.WATER),
       LocEnum.NTH: Location("North Sea", LocEnum.NTH, LocTypeEnum.WATER),
       LocEnum.NRG: Location("Norwegian Sea", LocEnum.NRG, LocTypeEnum.WATER),
       LocEnum.SKA: Location("Skagerrak", LocEnum.SKA, LocTypeEnum.WATER),
       LocEnum.TYN: Location("Tyrrhenian Sea", LocEnum.TYN, LocTypeEnum.WATER),
       LocEnum.WES: Location("Western Mediterranean", LocEnum.WES, LocTypeEnum.WATER),
       LocEnum.SPA_NC: Location("Northern Coast of Spain", LocEnum.SPA_NC, LocTypeEnum.WATER),
       LocEnum.SPA_SC: Location("Southern Coast of Spain", LocEnum.SPA_SC, LocTypeEnum.WATER),
       LocEnum.STP_NC: Location("Northern Coast of St. Petersburg", LocEnum.STP_NC, LocTypeEnum.WATER),
       LocEnum.STP_SC: Location("Southern Coast of St. Petersburg", LocEnum.STP_SC, LocTypeEnum.WATER),
       LocEnum.BUL_EC: Location("Eastern Coast of Bulgaria", LocEnum.BUL_EC, LocTypeEnum.WATER),
       LocEnum.BUL_SC: Location("Southern Coast of Bulgaria", LocEnum.BUL_SC, LocTypeEnum.WATER)}

edgelist = [[LocEnum.NAT, LocEnum.CLY], [LocEnum.NAT, LocEnum.LVP], [LocEnum.NAT, LocEnum.IRI],
            [LocEnum.NAT, LocEnum.MID],
            [LocEnum.NAT, LocEnum.NRG], [LocEnum.CLY, LocEnum.NRG], [LocEnum.CLY, LocEnum.EDI],
            [LocEnum.CLY, LocEnum.LVP],
            [LocEnum.IRI, LocEnum.LVP], [LocEnum.IRI, LocEnum.WAL], [LocEnum.IRI, LocEnum.ENG],
            [LocEnum.IRI, LocEnum.MID],
            [LocEnum.MID, LocEnum.ENG], [LocEnum.MID, LocEnum.BRE], [LocEnum.MID, LocEnum.GAS],
            [LocEnum.MID, LocEnum.SPA_NC],
            [LocEnum.MID, LocEnum.POR], [LocEnum.MID, LocEnum.WES], [LocEnum.MID, LocEnum.NAF],
            [LocEnum.NRG, LocEnum.EDI],
            [LocEnum.NRG, LocEnum.NTH], [LocEnum.NRG, LocEnum.NWY], [LocEnum.NRG, LocEnum.BAR],
            [LocEnum.NTH, LocEnum.EDI],
            [LocEnum.NTH, LocEnum.YOR], [LocEnum.NTH, LocEnum.LON], [LocEnum.NTH, LocEnum.ENG],
            [LocEnum.NTH, LocEnum.BEL],
            [LocEnum.NTH, LocEnum.HOL], [LocEnum.NTH, LocEnum.HEL], [LocEnum.NTH, LocEnum.DEN],
            [LocEnum.NTH, LocEnum.SKA],
            [LocEnum.NTH, LocEnum.NWY], [LocEnum.SKA, LocEnum.NWY], [LocEnum.SKA, LocEnum.SWE],
            [LocEnum.SKA, LocEnum.DEN],
            [LocEnum.HEL, LocEnum.DEN], [LocEnum.HEL, LocEnum.KIE], [LocEnum.HEL, LocEnum.HOL],
            [LocEnum.ENG, LocEnum.WAL],
            [LocEnum.ENG, LocEnum.LON], [LocEnum.ENG, LocEnum.BEL], [LocEnum.ENG, LocEnum.PIC],
            [LocEnum.ENG, LocEnum.BRE],
            [LocEnum.BAR, LocEnum.NWY], [LocEnum.BAR, LocEnum.STP_NC], [LocEnum.BAL, LocEnum.SWE],
            [LocEnum.BAL, LocEnum.DEN],
            [LocEnum.BAL, LocEnum.KIE], [LocEnum.BAL, LocEnum.BER], [LocEnum.BAL, LocEnum.PRU],
            [LocEnum.BAL, LocEnum.LVN],
            [LocEnum.BAL, LocEnum.BOT], [LocEnum.BOT, LocEnum.SWE], [LocEnum.BOT, LocEnum.FIN],
            [LocEnum.BOT, LocEnum.STP_SC],
            [LocEnum.BOT, LocEnum.LVN], [LocEnum.WES, LocEnum.SPA_SC], [LocEnum.WES, LocEnum.GOL],
            [LocEnum.WES, LocEnum.TYN],
            [LocEnum.WES, LocEnum.TUN], [LocEnum.WES, LocEnum.NAF], [LocEnum.TUN, LocEnum.NAF],
            [LocEnum.GOL, LocEnum.SPA_SC],
            [LocEnum.GOL, LocEnum.MAR], [LocEnum.GOL, LocEnum.PIE], [LocEnum.GOL, LocEnum.TUS],
            [LocEnum.GOL, LocEnum.TYN],
            [LocEnum.TYN, LocEnum.TUS], [LocEnum.TYN, LocEnum.ROM], [LocEnum.TYN, LocEnum.NAP],
            [LocEnum.TYN, LocEnum.ION],
            [LocEnum.TYN, LocEnum.TUN], [LocEnum.ION, LocEnum.TUN], [LocEnum.ION, LocEnum.NAP],
            [LocEnum.ION, LocEnum.APU],
            [LocEnum.ION, LocEnum.ADR], [LocEnum.ION, LocEnum.ALB], [LocEnum.ION, LocEnum.GRE],
            [LocEnum.ION, LocEnum.AEG],
            [LocEnum.ION, LocEnum.EAS], [LocEnum.ADR, LocEnum.APU], [LocEnum.ADR, LocEnum.VEN],
            [LocEnum.ADR, LocEnum.TRI],
            [LocEnum.ADR, LocEnum.ALB], [LocEnum.AEG, LocEnum.GRE], [LocEnum.AEG, LocEnum.BUL_SC],
            [LocEnum.AEG, LocEnum.CON],
            [LocEnum.AEG, LocEnum.SMY], [LocEnum.AEG, LocEnum.EAS], [LocEnum.EAS, LocEnum.SMY],
            [LocEnum.EAS, LocEnum.SYR],
            [LocEnum.BLA, LocEnum.SEV], [LocEnum.BLA, LocEnum.ARM], [LocEnum.BLA, LocEnum.ANK],
            [LocEnum.BLA, LocEnum.CON],
            [LocEnum.BLA, LocEnum.BUL_EC], [LocEnum.BLA, LocEnum.RUM], [LocEnum.SYR, LocEnum.SMY],
            [LocEnum.SYR, LocEnum.ARM],
            [LocEnum.ARM, LocEnum.ANK], [LocEnum.ARM, LocEnum.SMY], [LocEnum.SMY, LocEnum.ANK],
            [LocEnum.SMY, LocEnum.CON],
            [LocEnum.CON, LocEnum.ANK], [LocEnum.CON, LocEnum.BUL], [LocEnum.ARM, LocEnum.SEV],
            [LocEnum.GRE, LocEnum.ALB],
            [LocEnum.GRE, LocEnum.SER], [LocEnum.GRE, LocEnum.BUL], [LocEnum.SER, LocEnum.BUL],
            [LocEnum.SER, LocEnum.RUM],
            [LocEnum.SER, LocEnum.BUD], [LocEnum.SER, LocEnum.TRI], [LocEnum.SER, LocEnum.ALB],
            [LocEnum.BUL, LocEnum.RUM],
            [LocEnum.RUM, LocEnum.BUD], [LocEnum.RUM, LocEnum.GAL], [LocEnum.RUM, LocEnum.UKR],
            [LocEnum.RUM, LocEnum.SEV],
            [LocEnum.MOS, LocEnum.SEV], [LocEnum.MOS, LocEnum.UKR], [LocEnum.MOS, LocEnum.WAR],
            [LocEnum.MOS, LocEnum.LVN],
            [LocEnum.MOS, LocEnum.STP], [LocEnum.UKR, LocEnum.SEV], [LocEnum.UKR, LocEnum.WAR],
            [LocEnum.UKR, LocEnum.GAL],
            [LocEnum.WAR, LocEnum.GAL], [LocEnum.WAR, LocEnum.SIL], [LocEnum.WAR, LocEnum.PRU],
            [LocEnum.WAR, LocEnum.LVN],
            [LocEnum.STP, LocEnum.LVN], [LocEnum.STP, LocEnum.FIN], [LocEnum.STP, LocEnum.NWY],
            [LocEnum.NWY, LocEnum.SWE],
            [LocEnum.NWY, LocEnum.FIN], [LocEnum.SWE, LocEnum.FIN], [LocEnum.MUN, LocEnum.BUR],
            [LocEnum.MUN, LocEnum.RUH],
            [LocEnum.MUN, LocEnum.KIE], [LocEnum.MUN, LocEnum.BER], [LocEnum.MUN, LocEnum.SIL],
            [LocEnum.MUN, LocEnum.BOH],
            [LocEnum.MUN, LocEnum.TYR], [LocEnum.SIL, LocEnum.BOH], [LocEnum.SIL, LocEnum.GAL],
            [LocEnum.SIL, LocEnum.PRU],
            [LocEnum.SIL, LocEnum.BER], [LocEnum.PRU, LocEnum.BER], [LocEnum.PRU, LocEnum.LVN],
            [LocEnum.KIE, LocEnum.DEN],
            [LocEnum.KIE, LocEnum.BER], [LocEnum.KIE, LocEnum.RUH], [LocEnum.KIE, LocEnum.HOL],
            [LocEnum.RUH, LocEnum.BUR],
            [LocEnum.RUH, LocEnum.BEL], [LocEnum.RUH, LocEnum.HOL], [LocEnum.VIE, LocEnum.BOH],
            [LocEnum.VIE, LocEnum.GAL],
            [LocEnum.VIE, LocEnum.BUD], [LocEnum.VIE, LocEnum.TRI], [LocEnum.VIE, LocEnum.TYR],
            [LocEnum.TYR, LocEnum.BOH],
            [LocEnum.TYR, LocEnum.TRI], [LocEnum.TYR, LocEnum.VEN], [LocEnum.TYR, LocEnum.PIE],
            [LocEnum.BUD, LocEnum.GAL],
            [LocEnum.BUD, LocEnum.TRI], [LocEnum.VEN, LocEnum.PIE], [LocEnum.VEN, LocEnum.TRI],
            [LocEnum.VEN, LocEnum.APU],
            [LocEnum.VEN, LocEnum.ROM], [LocEnum.VEN, LocEnum.TUS], [LocEnum.APU, LocEnum.NAP],
            [LocEnum.APU, LocEnum.ROM],
            [LocEnum.NAP, LocEnum.ROM], [LocEnum.TUS, LocEnum.ROM], [LocEnum.TUS, LocEnum.PIE],
            [LocEnum.BUR, LocEnum.BEL],
            [LocEnum.BUR, LocEnum.PIC], [LocEnum.BUR, LocEnum.PAR], [LocEnum.BUR, LocEnum.GAS],
            [LocEnum.BUR, LocEnum.MAR],
            [LocEnum.MAR, LocEnum.PIE], [LocEnum.MAR, LocEnum.SPA], [LocEnum.MAR, LocEnum.GAS],
            [LocEnum.PAR, LocEnum.PIC],
            [LocEnum.PAR, LocEnum.BRE], [LocEnum.PAR, LocEnum.GAS], [LocEnum.BRE, LocEnum.GAS],
            [LocEnum.BRE, LocEnum.PIC],
            [LocEnum.BEL, LocEnum.HOL], [LocEnum.BEL, LocEnum.PIC], [LocEnum.SPA, LocEnum.POR],
            [LocEnum.SPA, LocEnum.GAS],
            [LocEnum.YOR, LocEnum.EDI], [LocEnum.YOR, LocEnum.LVP], [LocEnum.YOR, LocEnum.WAL],
            [LocEnum.YOR, LocEnum.LON],
            [LocEnum.LVP, LocEnum.EDI], [LocEnum.LVP, LocEnum.WAL], [LocEnum.LON, LocEnum.WAL],
            # All new
            [LocEnum.SWE, LocEnum.DEN], [LocEnum.SPA_SC, LocEnum.SPA_NC], [LocEnum.BUL_EC, LocEnum.BUL_SC],
            [LocEnum.STP_NC, LocEnum.STP_SC]]

for edge in edgelist:
    if edge[0] is edge[1]:
        raise InvariantError("Location cannot have an edge with itself")

    map[edge[0]].addBorder(edge[1])
    map[edge[1]].addBorder(edge[0])

# Map has been created, verify it

capcount = 0

for prov in map:
    if map[prov].iscapital:
        capcount = capcount + 1

    if map[prov].location is not prov:
        raise InvariantError("Mismatched location with key. {%s: %s}" % (prov, map[prov]))

    # if prov in map[prov].border:
    #     raise InvariantError("%s cannot border self" % prov)

    if map[prov].iscapital and map[prov].loctype == LocTypeEnum.WATER:
        raise InvariantError("%s cannot be a capital" % prov)

    for adj in map[prov].border:
        if prov is adj:
            raise InvariantError("%s cannot border self" % prov)

        if prov not in map[adj].border:
            raise InvariantError("%s is missing link back to %s" % (adj, prov))

        if (map[prov].loctype == LocTypeEnum.INLAND and map[adj].loctype == LocTypeEnum.WATER) or \
                (map[prov].loctype == LocTypeEnum.WATER and map[adj].loctype == LocTypeEnum.INLAND):
            raise InvariantError(
                "%s (%s) cannot be adjacent to %s (%s)" % (prov, map[prov].loctype, adj, map[adj].loctype))

if capcount != 34:
    raise InvariantError("Wrong Number of capitals: %i" % capcount)


def getLocation(location: LocEnum) -> Location:
    if location not in map:
        raise InvariantError("Map integrity error: lacking %s" % location)

    return map[location]
