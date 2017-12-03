# -------------------------------------------------
# The map class holds all information related to the
# regions and super regions in the Warlight game map.
# This code is a heavily modified version of the
# starter bot code supplied on the www.theaigames.com
# site for this game.
#
# @author Joe Coleman
# -------------------------------------------------

import const


# The map holds all information for the playable area of the game
class Map(object):
    def __init__(self):
        self.regions = {}           # All regions in the map (all places that can be owned)
        self.num_regions = 0        # Number of regions
        self.super_regions = {}     # All super regions in the map
        self.num_super_regions = 0  # Number of super regions
        self.last_update = []       # All regions that the player can see (or were lost last turn)
        self.temp_updates = []      # Holds all temporary updates to perform do-undo map changes for evaluation

        # Hold tuples of moves and army placement seen by the player but made by an opponent player
        # The dictionary is keyed by opponent name and the value is a list of tuples
        self.opponent_place_armies = {}     # (region_id, qty(int))
        self.opponent_attack_move = {}      # (from_region_id, to_region_id, qty(int))

    # Returns a region instance by id
    def get_region_by_id(self, region_id):
        return self.regions[region_id]

    # Returns a super region instance by id
    def get_super_region_by_id(self, super_region_id):
        return self.super_regions[super_region_id]

    # Returns a list of of references to region instances owned by `owner`.
    def get_owned_regions(self, owner):
        return [region for region in self.last_update if region.owner == owner]

    # Performs an update on the map with the new temporary values
    # and records the change in the temp_updates list to be undone later
    def do_temp_update(self, from_region, from_qty, to_region, to_qty, to_region_owner):
        from_region.troop_count = from_region.troop_count - from_qty
        to_region.troop_count = to_region.troop_count + to_qty
        previous_owner = to_region.owner
        to_region.owner = to_region_owner
        self.temp_updates.append((from_region, from_qty, to_region, to_qty, previous_owner))

    # Undoes the last temp update
    def undo_last_temp_update(self):
        from_region, from_qty, to_region, to_qty, previous_owner = self.temp_updates.pop()
        from_region.troop_count = from_region.troop_count + from_qty
        to_region.troop_count = to_region.troop_count - to_qty
        to_region.owner = previous_owner

    # Undo all temp updates to restore map to current state
    def undo_all_temp_updates(self):
        while self.temp_updates:
            self.undo_last_temp_update()

    # Returns a tuple of lists (player_owned, neighbors, outlier) which split the
    # visible list of regions into player owned, neighbors of those, the rest (typically from multiple lost regions)
    def split_last_update(self, player):
        player_owned = []
        neighbors = []
        outlier = []
        for region in self.last_update:
            if region.owner == player:
                player_owned.append(region)
            elif player in region.neighbors:
                neighbors.append(region)
            else:
                outlier.append(region)
        return player_owned, neighbors, outlier

    # Returns a list of all regions in a list of regions that are owned by the named player
    @staticmethod
    def get_owned_in_list(region_list, name):
        owned = []
        for region in region_list:
            if name == region.owner:
                owned.append(region)
        return owned

    # Initializes super regions from server string input
    def setup_super_regions(self, regions):
        for i in range(0, len(regions), 2):
            super_region = SuperRegion(regions[i], int(regions[i + 1]))
            self.super_regions[regions[i]] = super_region
            self.num_super_regions = self.num_super_regions + 1

    # Initializes regions from server string input
    def setup_regions(self, regions):
        for i in range(0, len(regions), 2):
            super_region = self.get_super_region_by_id(regions[i + 1])
            region = Region(regions[i], super_region)
            self.regions[regions[i]] = region
            super_region.regions.append(region)
            self.num_regions = self.num_regions + 1

    # Initializes neighbors and determines which regions have a border
    # that crosses super regions
    def setup_neighbors(self, regions):
        for i in range(0, len(regions), 2):
            region = self.get_region_by_id(regions[i])
            neighbors = [self.get_region_by_id(region_id) for region_id in regions[i + 1].split(',')]
            for neighbor in neighbors:
                region.neighbors.append(neighbor)
                neighbor.neighbors.append(region)
        for key in self.regions.keys():
            region = self.regions[key]
            if region.is_on_super_region_border:
                continue
            for neighbor in region.neighbors:
                if neighbor.super_region.id != region.super_region.id:
                    region.is_on_super_region_border = True
                    neighbor.is_on_super_region_border = True

    # Called to update map every round
    def update_map(self, regions):
        self.last_update = []
        self.temp_updates = []
        for i in range(0, len(regions), 3):
            region = self.get_region_by_id(regions[i])
            region.owner = regions[i + 1]
            region.troop_count = int(regions[i + 2])
            self.last_update.append(region)

    # Parse the opponent moves into place_armies and attack/transfer commands and
    # store each in a list keyed on the opponent's name
    def opponent_moves(self, options):
        if options == '':       # no moves seen
            self.opponent_place_armies = {}
            self.opponent_attack_move = {}
            return
        place_armies = dict()
        attack_transfer = dict()
        i = 0
        while i < len(options):
            if options[i+1] == const.PLACE_ARMIES:
                if options[i] not in place_armies:
                    place_armies[options[i]] = list()
                place_armies[options[i]].append((options[i+2], int(options[i+3])))
                i = i + 4
            elif options[i+1] == const.ATTACK_TRANSFER:
                if options[i] not in attack_transfer:
                    attack_transfer[options[i]] = list()
                attack_transfer[options[i]].append((options[i+2], options[i+3], int(options[i+4])))
                i = i + 5
        self.opponent_attack_move = attack_transfer
        self.opponent_place_armies = place_armies

    # Used by bot_test to reset the map to default state for easy updating
    def reset_map(self):
        self.temp_updates = []
        self.last_update = []
        keys = self.regions.keys()
        for key in keys:
            self.regions[key].owner = const.NEUTRAL
            self.regions[key].troop_count = const.STARTING_TROOPS_PER_REGION


# A collection of regions that represent a larger body (typically a country)
class SuperRegion(object):
    # Has an additional troop generation if a player controls all regions
    def __init__(self, super_region_id, bonus_armies):
        self.id = super_region_id
        self.bonus_armies = bonus_armies
        self.regions = []


# A region (smallest area in the map)
class Region(object):
    def __init__(self, region_id, super_region):
        self.id = region_id
        self.owner = const.NEUTRAL
        self.neighbors = []
        self.troop_count = const.STARTING_TROOPS_PER_REGION
        self.super_region = super_region
        self.is_on_super_region_border = False


# The mappings of super_region_id to name as used on www.theaigames.com's site
class SuperRegionMap(object):
    def __init__(self):
        self.map = dict()
        self.map['1'] = 'North America'
        self.map['2'] = 'South America'
        self.map['3'] = 'Europe'
        self.map['4'] = 'Africa'
        self.map['5'] = 'Asia'
        self.map['6'] = 'Australia'


# The mappings of region_id to name as used on www.theaigames.com's site
class RegionMap(object):
    def __init__(self):
        self.map = dict()

        # North America
        self.map['1'] = 'Alaska'
        self.map['2'] = 'Northwest Territory'
        self.map['3'] = 'Greenland'
        self.map['4'] = 'Alberta'
        self.map['5'] = 'Ontario'
        self.map['6'] = 'Quebec'
        self.map['7'] = 'Western United States'
        self.map['8'] = 'Eastern United States'
        self.map['9'] = 'Central America'

        # South America
        self.map['10'] = 'Venezuela'
        self.map['11'] = 'Peru'
        self.map['12'] = 'Brazil'
        self.map['13'] = 'Argentina'

        # Europe
        self.map['14'] = 'Iceland'
        self.map['15'] = 'Great Britain'
        self.map['16'] = 'Scandinavia'
        self.map['17'] = 'Ukraine'
        self.map['18'] = 'Western Europe'
        self.map['19'] = 'Northern Europe'
        self.map['20'] = 'Southern Europe'

        # Africa
        self.map['21'] = 'North Africa'
        self.map['22'] = 'Egypt'
        self.map['23'] = 'East Africa'
        self.map['24'] = 'Congo'
        self.map['25'] = 'South Africa'
        self.map['26'] = 'Madagascar'

        # Asia
        self.map['27'] = 'Ural'
        self.map['28'] = 'Siberia'
        self.map['29'] = 'Yakutsk'
        self.map['30'] = 'Kamchatka'
        self.map['31'] = 'Irkutsk'
        self.map['32'] = 'Kazakhstan'
        self.map['33'] = 'China'
        self.map['34'] = 'Mongolia'
        self.map['35'] = 'Japan'
        self.map['36'] = 'Middle East'
        self.map['37'] = 'India'
        self.map['38'] = 'Siam'

        # Australia
        self.map['39'] = 'Indonesia'
        self.map['40'] = 'New Guinea'
        self.map['41'] = 'Western Australia'
        self.map['42'] = 'Eastern Australia'
