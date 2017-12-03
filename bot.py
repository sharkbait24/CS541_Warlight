# -------------------------------------------------
# Base bot class for building AIs to play the
# Risk like game Warlight on www.theaigames.com.  This bot
# is based on the starter bot supplied on the site
#
# @author Joe Coleman
# -------------------------------------------------

from abc import abstractmethod
from sys import stdin, stdout
from map import Map
import const


# Bot is an abstract base class that contains all of the base support for
# communicating with the server.  The actual ai functionality
# is implemented in derived classes
class Bot(object):
    def __init__(self, map_weights, heuristic):
        self.map = Map()                            # Game map
        self.name = ''                              # Player name
        self.opponents = []                         # List of opponent names( only 1 on theaigames site)
        self.available_armies = 0                   # Number of armies that can be placed during army placement phase
        self.map_weights = map_weights              # Collection of weights for the map regions and super regions
        self.heuristic = heuristic                  # Heuristic to use in evaluation
        self.command = self.build_command_dict()    # A dictionary of commands the server may make
        self.turn_elapsed = 1

    # A dictionary of available commands that could be sent by the game server
    # and the functions that will be executed for the command received
    def build_command_dict(self):
        cmd = dict()
        cmd[const.SETUP_MAP] = self.setup_map
        cmd[const.PICK_STARTING_REGIONS] = self.pick_starting_regions
        cmd[const.SETTINGS] = self.settings
        cmd[const.UPDATE_MAP] = self.update_map
        cmd[const.OPPONENT_MOVES] = self.opponent_moves
        cmd[const.GO] = self.go
        return cmd

    # Runs the game when executed as its own program on theaigames website
    def run(self):
        # Main loop
        #
        # Keeps running while being fed data from stdin.
        # Writes output to stdout, remember to flush!
        while not stdin.closed:
            try:
                rawline = stdin.readline()
                if len(rawline) == 0:  # End of file check
                    break
                line = rawline.strip()
                if len(line) == 0:  # Empty lines can be ignored
                    continue
                # Hacky way to get theaigames version to work with same run_cmd code
                parts = line.split()
                response = self.run_cmd(parts)
                if response != '':
                    stdout.write(response + '\n')
                    stdout.flush()
            except EOFError:
                return

    # Returns a string of the bot's decision or '' if no response needed
    def run_cmd(self, parts):
        if parts[0] in self.command:
            if parts[0] == const.OPPONENT_MOVES and len(parts) == 1:  # Can receive nothing on opponent moves
                return self.opponent_moves()
            return self.command[parts[0]](parts[1:])
        else:
            return 'Unknown command: ' + parts[0]

    # Commands for initial map creation
    def setup_map(self, options):
        sub_command = options[0]
        if sub_command == const.SUPER_REGIONS:
            self.map.setup_super_regions(options[1:])
        elif sub_command == const.REGIONS:
            self.map.setup_regions(options[1:])
        elif sub_command == const.NEIGHBORS:
            self.map.setup_neighbors(options[1:])
        else:
            return 'Unknown sub command: ' + sub_command
        return ''

    # Commands for setting up the player names and for getting the available
    # armies to be placed on the board each turn
    def settings(self, options):
        sub_command = options[0]
        if sub_command == const.STARTING_ARMIES:
            self.available_armies = int(options[1])
        elif sub_command == const.OPPONENT_BOT:
            self.opponents.append(options[1])
        elif sub_command == const.YOUR_BOT:
            self.name = options[1]
        else:
            return 'Unknown sub command: ' + sub_command
        return ''

    # Command to update the board with all visible regions
    def update_map(self, regions):
        self.map.update_map(regions)
        return ''

    # Parses out opponent moves are stores them in a dict in the map
    def opponent_moves(self, options=''):
        self.map.opponent_moves(options)
        return ''

    # Commands for placing armies and move / attacking
    def go(self, options):
        sub_command = options[0]
        if sub_command == const.PLACE_ARMIES:
            return self.place_armies(options[1])
        elif sub_command == const.ATTACK_TRANSFER:
            return self.attack_transfer(options[1])
        else:
            return 'Unknown sub command: ' + sub_command

    # Command to choose 6 starting regions from a list of options (space delimited)
    # First argument is the amount of time you have to choose
    # ex: 1 4 2 3 22 19
    @abstractmethod
    def pick_starting_regions(self, options):
        return ''

    # Command to create a string of regions and qty for troop placement
    # Each placement is of the form: <name> place_armies <region_id> <qty>
    # and each placement should be comma delimited with a space.
    # ex: player1 place_armies 1 2, player1 place_armies 2 5
    @abstractmethod
    def place_armies(self, time):
        return ''

    # Command to create a string of attacks and transfers of armies.
    # Each attack/transfer is of the form: <name> attack/transfer <from region_id> <to region_id> <qty>
    # and each attack/transfer should be comma delimited with a space
    # ex: player1 attack/transfer 1 2 3, player1 attack/transfer 2 3 8
    @abstractmethod
    def attack_transfer(self, time):
        return ''

    # Parses the server input for picking starting regions into a list of regions
    def parse_pick_starting_regions(self, options):
        option_list = options[1:]
        regions = []
        for option in option_list:
            regions.append(self.map.regions[option])
        return regions


# Used for easy building of the output string for placing armies
class PlaceArmyBuilder(object):
    def __init__(self, player):
        self.actions = []
        self.name = player

    # Add a new army tuple to the list (region, qty)
    def add(self, region, qty):
        self.actions.append((region, qty))

    # Convert all queued army placements to a string
    def to_string(self):
        if not self.actions:
            return const.NO_MOVES
        return ', '.join(['%s %s %s %d' % (self.name, const.PLACE_ARMIES, action[0], action[1])
                          for action in self.actions])


# Used for easy building of the output string for attacking and transferring
class AttackTransferBuilder(object):
    def __init__(self, player):
        self.actions = []
        self.name = player

    # Add a new movement tuple to the list (from_region, to_region, qty)
    def add(self, from_region, to_region, qty):
        self.actions.append((from_region, to_region, qty))

    # Convert all queued army movements to a string
    def to_string(self):
        if not self.actions:
            return const.NO_MOVES
        return ', '.join(['%s %s %s %s %d' % (self.name, const.ATTACK_TRANSFER, action[0], action[1],
                                              action[2]) for action in self.actions])


# Used for easy building of the output string for placing starting armies
class PickStartingBuilder(object):
    def __init__(self):
        self.regions = []

    # Add all starting region choices
    def add_all(self, region_list):
        for region in region_list:
            self.regions.append(region.id)

    # Convert all queued army movements to a string
    def to_string(self):
        return ' '.join([region for region in self.regions])
