# -------------------------------------------------
# A collection of usable map weights that can be
# used by the bot
#
# @author Joe Coleman
# -------------------------------------------------

# There are 42 regions divided between 6 super regions (see map file for names)

from priority_weights import PriorityWeights


class UniformWeights(object):
    def __init__(self):
        self.super_region_weight = dict()
        self.region_weight = dict()

        # North America
        self.super_region_weight['1'] = 5
        self.region_weight['1'] = 1
        self.region_weight['2'] = 1
        self.region_weight['3'] = 1
        self.region_weight['4'] = 1
        self.region_weight['5'] = 1
        self.region_weight['6'] = 1
        self.region_weight['7'] = 1
        self.region_weight['8'] = 1
        self.region_weight['9'] = 1

        # South America
        self.super_region_weight['2'] = 2
        self.region_weight['10'] = 1
        self.region_weight['11'] = 1
        self.region_weight['12'] = 1
        self.region_weight['13'] = 1

        # Europe
        self.super_region_weight['3'] = 5
        self.region_weight['14'] = 1
        self.region_weight['15'] = 1
        self.region_weight['16'] = 1
        self.region_weight['17'] = 1
        self.region_weight['18'] = 1
        self.region_weight['19'] = 1
        self.region_weight['20'] = 1

        # Africa
        self.super_region_weight['4'] = 3
        self.region_weight['21'] = 1
        self.region_weight['22'] = 1
        self.region_weight['23'] = 1
        self.region_weight['24'] = 1
        self.region_weight['25'] = 1
        self.region_weight['26'] = 1

        # Asia
        self.super_region_weight['5'] = 7
        self.region_weight['27'] = 1
        self.region_weight['28'] = 1
        self.region_weight['29'] = 1
        self.region_weight['30'] = 1
        self.region_weight['31'] = 1
        self.region_weight['32'] = 1
        self.region_weight['33'] = 1
        self.region_weight['34'] = 1
        self.region_weight['35'] = 1
        self.region_weight['36'] = 1
        self.region_weight['37'] = 1
        self.region_weight['38'] = 1

        # Australia
        self.super_region_weight['6'] = 2
        self.region_weight['39'] = 1
        self.region_weight['40'] = 1
        self.region_weight['41'] = 1
        self.region_weight['42'] = 1


# All available map weights in a convenient dictionary for use in bot_tests
class MapWeightList(object):
    def __init__(self):
        self.map_weights = dict()
        self.map_weights['uniform'] = UniformWeights
        self.map_weights['priority'] = PriorityWeights

    # Returns all available map weights by name (key)
    def get_map_weights(self):
        return self.map_weights.keys()

    # Returns an instance of a specific map weight
    def create_map_weight(self, name):
        weight = self.map_weights[name]()
        return weight
