# -------------------------------------------------
# A collection of usable map weights that can be
# used by the bot.
#
# The degree is how many regions surround a given
# region.
#
# Weights are equal to the degree.
#
# Lower weights are prioritized.
#
# @author Joe Coleman, Selmon Afzal
# -------------------------------------------------

# There are 42 regions divided between 6 super regions (see map file for names)


class PriorityWeights(object):
    def __init__(self):
        self.super_region_weight = dict()
        self.region_weight = dict()

        # North America
        self.super_region_weight['1'] = 1
        self.region_weight['1'] = 3 # Alaska
        self.region_weight['2'] = 4 # Northwest Territory
        self.region_weight['3'] = 4 # Greenland
        self.region_weight['4'] = 4 # Alberta
        self.region_weight['5'] = 6 # Ontario
        self.region_weight['6'] = 3 # Quebec
        self.region_weight['7'] = 4 # Western United States
        self.region_weight['8'] = 4 # Eastern United States
        self.region_weight['9'] = 3 # Central America

        # South America
        self.super_region_weight['2'] = 1
        self.region_weight['10'] = 3 # Venezuela
        self.region_weight['11'] = 3 # Peru
        self.region_weight['12'] = 4 # Brazil
        self.region_weight['13'] = 2 # Argentina

        # Europe
        self.super_region_weight['3'] = 1
        self.region_weight['14'] = 3 # Iceland
        self.region_weight['15'] = 4 # Great Britain
        self.region_weight['16'] = 4 # Scandinavia
        self.region_weight['17'] = 6 # Ukraine
        self.region_weight['18'] = 4 # Western Europe
        self.region_weight['19'] = 5 # Northern Europe
        self.region_weight['20'] = 6 # Southern Europe


        # Africa
        self.super_region_weight['4'] = 1
        self.region_weight['21'] = 6 # North Africa
        self.region_weight['22'] = 4 # Egypt
        self.region_weight['23'] = 6 # East Africa
        self.region_weight['24'] = 4 # Congo
        self.region_weight['25'] = 3 # South Africa
        self.region_weight['26'] = 2 # Madagascar

        # Asia
        self.super_region_weight['5'] = 1
        self.region_weight['27'] = 4 # Ural
        self.region_weight['28'] = 5 # Siberia
        self.region_weight['29'] = 3 # Yakutsk
        self.region_weight['30'] = 4 # Kamchatka
        self.region_weight['31'] = 4 # Irkutsk
        self.region_weight['32'] = 5 # Kazakhstan
        self.region_weight['33'] = 6 # China
        self.region_weight['34'] = 5 # Mongolia
        self.region_weight['35'] = 2 # Japan
        self.region_weight['36'] = 6 # Middle East
        self.region_weight['37'] = 4 # India
        self.region_weight['38'] = 3 # Siam

        # Australia
        self.super_region_weight['6'] = 1
        self.region_weight['39'] = 2 # Indonesia
        self.region_weight['40'] = 3 # New Guinea
        self.region_weight['41'] = 2 # Western Australia
        self.region_weight['42'] = 2 # Eastern Australia

# All available map weights in a convenient dictionary for use in bot_tests
class MapWeightList(object):
    def __init__(self):
        self.map_weights = dict()
        self.map_weights['uniform'] = UniformWeights

    # Returns all available map weights by name (key)
    def get_map_weights(self):
        return self.map_weights.keys()

    # Returns an instance of a specific map weight
    def create_map_weight(self, name):
        weight = self.map_weights[name]()
        return weight
