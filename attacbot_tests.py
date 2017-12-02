# -------------------------------------------------
# Program that gets the bot, map_weights and heuristic
# from user and then runs those tests on the ones
# supplied in testlist
#
# @author Joe Coleman
# -------------------------------------------------

import priority_weights 
import heuristics
import ailist
from map import RegionMap, SuperRegionMap
from testlist import TestList
import const


# This class lets the user choose a bot, map_weight and heuristic to run against
# test maps and prints the response from the bot
class BotTester(object):
    def __init__(self):
        self.bot_list = ailist.AiList()
        self.weight_list = priority_weights.MapWeightList()
        self.heuristic_list = heuristics.HeuristicList()
        self.region_map = RegionMap()                           # mapping of region ids to names
        self.super_region_map = SuperRegionMap()                # mapping of super region ids to names
        self.tests = TestList()

        # Holds the bot, weight and heuristic to be used in tests
        # Assigned defaults so PyCharm will stop giving warnings on calls
        self.weight = priority_weights.UniformWeights()
        self.heuristic = heuristics.HeuristicList()
        self.bot = ailist.RandomBot(self.weight, self.heuristic)

    # Let the player choose bot, weight and heuristic
    def setup(self):
        print('--- Map Weight ---')
        names = self.weight_list.get_map_weights()
        i = 0
        for name in names:
            print('{i}: {name}'.format(i=i, name=name))
            i = i + 1
        resp = int(input('Enter number of map weight to use: '))
        self.weight = self.weight_list.create_map_weight(self.get_key_by_index(names, resp))
        print('--- Heuristic ---')
        names = self.heuristic_list.get_heuristics()
        i = 0
        for name in names:
            print('{i}: {name}'.format(i=i, name=name))
            i = i + 1
        resp = int(input('Enter number of heuristic to use: '))
        self.heuristic = self.heuristic_list.create_heuristic(self.get_key_by_index(names, resp))
        print('--- Bot ---')
        names = self.bot_list.get_bot_names()
        i = 0
        for name in names:
            print('{i}: {name}'.format(i=i, name=name))
            i = i + 1
        resp = int(input('Enter number of bot to test: '))
        self.bot = self.bot_list.create_bot(self.get_key_by_index(names, resp), self.weight, self.heuristic)

    # Sets up the bot's settings and map to the default one used on www.theaigames.com
    def setup_bot(self):
        print([const.SETTINGS, const.YOUR_BOT, const.TAG_PLAYER_NAME])
        self.assert_cmd([const.SETTINGS, const.YOUR_BOT, const.TAG_PLAYER_NAME], '')
        self.assert_cmd([const.SETTINGS, const.OPPONENT_BOT, const.TAG_OPPONENT_NAME], '')
        self.assert_cmd([const.SETUP_MAP, const.SUPER_REGIONS] + const.TAG_SUPER_REGIONS.split(), '')
        self.assert_cmd([const.SETUP_MAP, const.REGIONS] + const.TAG_REGIONS.split(), '')
        self.assert_cmd([const.SETUP_MAP, const.NEIGHBORS] + const.TAG_NEIGHBORS.split(), '')

    # Helper function to perform assert checks that the command issued responded properly
    def assert_cmd(self, args, expected):
        resp = self.bot.run_cmd(args)
        if resp != expected:
# TODO: Assign all the new weights
            print('On command: ', end='')
            print(' '.join(arg for arg in args))
            print('Expected: {exp}'.format(exp=expected))
            print('Received: {rec}'.format(rec=resp))
            raise ValueError('Command returned unexpected response')

    # Returns a key in a collection of keys by index (starting at 0)
    @staticmethod
    def get_key_by_index(keys, index):
        i = 0
        for key in keys:
            if index == i:
                return key
            i = i + 1
        return -1

    # Run tests
    def run(self):
        resp = -1
        tests = self.tests.get_tests()
        while resp != 0:
            print('--- Tests ---\n0: quit\n1: run all')
            i = 2
            for test in tests:
                print('{i}: {name}'.format(i=i, name=test))
                i = i + 1
            resp = int(input('Enter the number of the test to run: '))
            if resp == 1:
                for test in tests:
                    self.tests.run_test(test, self)
                    self.bot.map.reset_map()
            elif resp != 0:
                self.tests.run_test(self.get_key_by_index(tests, resp-2), self)
                self.bot.map.reset_map()


if __name__ == '__main__':
    tester = BotTester()
    tester.setup()
    try:
        tester.setup_bot()
        tester.run()
    except ValueError as error:
        print('Test failed.  Error: ' + repr(error))
