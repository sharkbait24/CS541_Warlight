# -------------------------------------------------
# A collection of usable heuristics for the bot
#
# @author Joe Coleman
# -------------------------------------------------

from abc import abstractmethod


# Abstract base class for a heuristic
class Heuristic(object):
    @staticmethod
    @abstractmethod
    def evaluate(bot):
        return


# Returns the number of regions the player has not captured
# This is NOT an admissible heuristic
class RegionsNotCaptured(Heuristic):
    @staticmethod
    def evaluate(bot):
        num_owned = len(bot.map.get_owned_regions(bot.name))
        return bot.map.num_regions - num_owned


# All available map weights in a convenient dictionary for use in bot_tests
class HeuristicList(object):
    def __init__(self):
        self.heuristics = dict()
        self.heuristics['Regions Not Captured'] = RegionsNotCaptured

    # Returns all available map weights by name (key)
    def get_heuristics(self):
        return self.heuristics.keys()

    # Returns an instance of a specific map weight
    def create_heuristic(self, name):
        heuristic = self.heuristics[name]()
        return heuristic
