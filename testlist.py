# -------------------------------------------------
# A collection of simple bot tests to run on a specific
# bot, map_weight and heuristic combination.
# Includes basic and a basic text output of results
#
# @author Joe Coleman
# -------------------------------------------------
from abc import abstractmethod
import const
import time


# Generic printing functionality
class Print(object):
    # Print the generic header with the command to be called
    @staticmethod
    def cmd_header(args):
        print('------\nCommand: ', end='')
        print(' '.join(str(arg) for arg in args))
        print('------')

    # Print elapsed time
    @staticmethod
    def runtime(elapsed):
        print('RUNTIME: {elapsed} s'.format(elapsed=elapsed))

    # Print the visible map for a bot
    @staticmethod
    def update_map(bot, region_map):
        print('** UPDATE MAP **')
        print('{0:3}  {1:25}  {2:6}  {3:10}'.format('ID', 'NAME', 'ARMIES', 'OWNER'))
        for region in bot.map.last_update:
            print('{0:3}  {1:25}  {2:6}  {3:10}'.format(region.id, region_map.map[region.id],
                                                        region.troop_count, region.owner))

    # Print bot response to go place_armies
    @staticmethod
    def place_armies(resp, region_map):
        resp_parts = resp.split(', ')
        print('** PLACE ARMIES **')
        print('{0:3}  {1:25}  {2:6}'.format('ID', 'NAME', 'ARMIES'))
        for placement in resp_parts:
            parts = placement.split()
            print('{0:3}  {1:25}  {2:6}'.format(parts[2], region_map.map[parts[2]], parts[3]))

    # Print bot response to attack/transfer
    @staticmethod
    def attack_transfer(resp, region_map, player_map):
        print('** ATTACK/TRANSFER **')
        if resp == const.NO_MOVES:
            print('No Moves')
            return
        resp_parts = resp.split(', ')
        print('{0:8}  {1:3}  {2:25}  ->  {3:3}  {4:25}  {5:6}'.format('TYPE', 'ID', 'NAME', 'ID', 'NAME', 'ARMIES'))
        for placement in resp_parts:
            parts = placement.split()
            player = parts[0]
            move_type = 'transfer'
            if player != player_map.regions[parts[3]].owner:
                move_type = 'attack'
            print('{0:8}  {1:3}  {2:25}  ->  {3:3}  {4:25}  {5:6}'.format(move_type, parts[2], region_map.map[parts[2]],
                                                                          parts[3], region_map.map[parts[3]],
                                                                          parts[4]))


# abstract base class for tests
class Test(object):
    # Function that is called by BotTester which passes itself as the argument
    @staticmethod
    @abstractmethod
    def test(tester):
        return

    # Function to simplify testing commands by calculating running time
    @staticmethod
    def run_cmd(tester, cmd):
        Print.cmd_header(cmd)
        starting_time = time.process_time()
        resp = tester.bot.run_cmd(cmd)
        elapsed_time = time.process_time() - starting_time
        return resp, elapsed_time


# Check if bot picks 6 starter regions
class PickStartingTest(Test):
    @staticmethod
    def test(tester):
        print('\n#######################################################')
        print('\nPICK STARTING TEST\n')
        regions = '3 2 10 12 20 17 24 25 31 36 42 39'
        parts = regions.split()
        cmd = [const.PICK_STARTING_REGIONS, const.TAG_PICK_STARTING_TIME] + parts
        resp, elapsed = Test.run_cmd(tester, cmd)
        resp_parts = resp.split()
        if len(resp_parts) != 6:
            print('Failed to return 6 regions\nReceived: ', end='')
            print(' '.join(str(part) for part in parts))
            raise ValueError('Invalid number of regions returned in pick_starting')
        for part in resp_parts:
            if part not in parts:
                print('Choose a region that was not in the supplied list: ' + str(part))
                raise ValueError('Invalid region choice')
        print('Choices:')
        print(', '.join(tester.region_map.map[region] for region in parts))
        print('Returned:')
        print(', '.join(tester.region_map.map[region] for region in resp_parts))
        Print.runtime(elapsed)
        print('#######################################################')


# Set starting_armies, update map, opponent_moves then get placement and movement
class StandardTurnTest(Test):
    @staticmethod
    def test(tester):
        print('\n#######################################################')
        print('\nSTANDARD TURN TEST\n')
        StandardTurnTest.setup_generic_map(tester)
        Print.update_map(tester.bot, tester.region_map)
        cmd = [const.GO, const.PLACE_ARMIES, const.TAG_GO_TIME]
        resp, elapsed = Test.run_cmd(tester, cmd)
        print('AVAILABLE ARMIES = 5')
        Print.place_armies(resp, tester.region_map)
        Print.runtime(elapsed)
        cmd = [const.GO, const.ATTACK_TRANSFER, const.TAG_GO_TIME]
        resp, elapsed = Test.run_cmd(tester, cmd)
        Print.attack_transfer(resp, tester.region_map, tester.bot.map)
        Print.runtime(elapsed)
        print('#######################################################')

    # Set the bot's map to a general one based on a game on www.theaigames.com
    @staticmethod
    def setup_generic_map(tester):
        tester.assert_cmd([const.SETTINGS, const.STARTING_ARMIES, '5'], '')
        update_string = 'update_map 3 player1 1 14 player1 3 16 player1 4 17 player1 4 36 player1 4 37 player1 4 ' \
                        '38 player1 4 ' \
                        '39 player1 4 41 player1 29 42 player1 35 2 neutral 2 5 neutral 2 6 neutral 2 15 neutral 2 ' \
                        '19 neutral 2 20 neutral 2 27 neutral 2 32 neutral 2 22 neutral 2 23 player2 4 33 player2 6 ' \
                        '40 neutral 2'
        tester.assert_cmd(update_string.split(), '')
        opponent_string = 'opponent_moves player2 place_armies 23 2 player2 attack/transfer 23 21 5 ' \
                          'player2 attack/transfer 25 23 2 player2 attack/transfer 33 28 3 ' \
                          'player2 attack/transfer 34 33 5'
        tester.assert_cmd(opponent_string.split(), '')


# Run the heuristic on the generic map and print its result
class HeuristicTest(Test):
    @staticmethod
    def test(tester):
        print('\n#######################################################')
        print('\nHEURISTIC TEST\n')
        StandardTurnTest.setup_generic_map(tester)
        Print.update_map(tester.bot, tester.region_map)
        val = tester.bot.heuristic.evaluate(tester.bot)
        print('VALUE: ' + str(val))
        print('#######################################################')


# All available tests
class TestList(object):
    def __init__(self):
        self.tests = dict()
        self.tests['Pick Starting Test'] = PickStartingTest.test
        self.tests['Standard Turn Test'] = StandardTurnTest.test
        self.tests['Heuristic Test'] = HeuristicTest.test

    # Returns all available map weights by name (key)
    def get_tests(self):
        return self.tests.keys()

    # Runs selected test
    def run_test(self, test, tester):
        self.tests[test](tester)
        return
