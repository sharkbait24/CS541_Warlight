# -------------------------------------------------
# A collection of names used as part of commands and
# sub commands in the game
#
# @author Joe Coleman
# -------------------------------------------------

NO_MOVES = 'No moves'                           # can be returned during attack/transfer if bot does nothing
PLACE_ARMIES = 'place_armies'                   # placement command name
ATTACK_TRANSFER = 'attack/transfer'             # attack/transfer command name
SETUP_MAP = 'setup_map'                         # initialize map
SUPER_REGIONS = 'super_regions'                 # collection of regions (country)
REGIONS = 'regions'                             # a single map space
NEIGHBORS = 'neighbors'                         # regions that share a border
PICK_STARTING_REGIONS = 'pick_starting_regions'  # command to choose starting regions
SETTINGS = 'settings'                           # command for setting player names and starting armies
YOUR_BOT = 'your_bot'                           # receiving your bot's name
OPPONENT_BOT = 'opponent_bot'                   # receiving an opponent's name
STARTING_ARMIES = 'starting_armies'             # number of armies that can be placed
UPDATE_MAP = 'update_map'                       # receive all visible regions
OPPONENT_MOVES = 'opponent_moves'               # list of opponent moves
GO = 'go'                                       # command to place / move armies
NEUTRAL = 'neutral'                             # default name for regions with no player
STARTING_TROOPS_PER_REGION = 2                  # number of troops each region starts with

# www.theaigames.com default values
TAG_PLAYER_NAME = 'player1'
TAG_OPPONENT_NAME = 'player2'
TAG_SUPER_REGIONS = '1 5 2 2 3 5 4 3 5 7 6 2'
TAG_REGIONS = '1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 ' \
              '1 9 1 10 2 11 2 12 2 13 2 14 3 ' \
              '15 3 16 3 17 3 18 3 19 3 20 3 ' \
              '21 4 22 4 23 4 24 4 25 4 26 4 ' \
              '27 5 28 5 29 5 30 5 31 5 32 5 ' \
              '33 5 34 5 35 5 36 5 37 5 38 5 ' \
              '39 6 40 6 41 6 42 6'
TAG_NEIGHBORS = '1 2,4,30 2 4,3,5 3 5,6,14 4 5,7 ' \
                '5 6,7,8 6 8 7 8,9 8 9 9 10 10 ' \
                '11,12 11 12,13 12 13,21 14 15,16 ' \
                '15 16,18,19 16 17 17 19,20,27,32,36 ' \
                '18 19,20,21 19 20 20 21,22,36 21 ' \
                '22,23,24 22 23,36 23 24,25,26,36 ' \
                '24 25 25 26 27 28,32,33 28 ' \
                '29,31,33,34 29 30,31 30 31,34,35 ' \
                '31 34 32 33,36,37 33 34,37,38 34 ' \
                '35 36 37 37 38 38 39 39 40,41 40 ' \
                '41,42 41 42'
TAG_PICK_STARTING_TIME = 10000
TAG_GO_TIME = 2000
